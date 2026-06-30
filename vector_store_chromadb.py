import os
import shutil
from typing import List, Optional
import chromadb
from chromadb.config import Settings

class VectorStoreManager:
    """
    向量数据库管理类：使用原生 chromadb API
    """
    
    def __init__(
        self,
        embedding_model: str = "nomic-embed-text",
        persist_directory: str = "./chroma_db",
        chunk_size: int = 1000,
        chunk_overlap: int = 200
    ):
        self.embedding_model = embedding_model
        self.persist_directory = persist_directory
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
        # 延迟初始化
        self.embeddings = None
        self.text_splitter = None
        self.client = None
        self.collection = None
    
    def _init_components(self):
        """
        延迟初始化组件
        """
        if self.embeddings is None:
            from langchain_ollama import OllamaEmbeddings
            from langchain.text_splitter import RecursiveCharacterTextSplitter
            
            self.embeddings = OllamaEmbeddings(model=self.embedding_model)
            self.text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=self.chunk_size,
                chunk_overlap=self.chunk_overlap,
                length_function=len,
                separators=["\n\n", "\n", "。", "！", "？", "；", "，", " ", ""]
            )
    
    def _init_chromadb(self):
        """
        初始化 chromadb 客户端
        """
        if self.client is None:
            try:
                self.client = chromadb.PersistentClient(
                    path=self.persist_directory,
                    settings=Settings(
                        anonymized_telemetry=False
                    )
                )
                print(f"✅ 成功创建 chromadb 客户端")
            except Exception as e:
                print(f"❌ 创建 chromadb 客户端失败: {str(e)}")
                raise
    
    def create_documents(self, raw_documents: List[dict]) -> List:
        """
        将原始文档转换为简单字典列表
        """
        documents = []
        for doc in raw_documents:
            documents.append({
                "content": doc["content"],
                "metadata": {
                    "source": doc["source"],
                    "filename": doc["filename"]
                }
            })
        return documents
    
    def split_documents(self, documents: List[dict]) -> List[dict]:
        """
        对文档进行分块处理
        """
        self._init_components()
        
        if self.text_splitter is None:
            print("❌ 文本分割器未初始化")
            return []
        
        from langchain.schema import Document
        
        langchain_docs = []
        for doc in documents:
            metadata = doc.get("metadata", {})
            langchain_docs.append(Document(
                page_content=doc["content"],
                metadata={
                    "source": metadata.get("source", doc.get("source", "unknown")),
                    "filename": metadata.get("filename", doc.get("filename", "unknown"))
                }
            ))
        
        split_docs = self.text_splitter.split_documents(langchain_docs)
        
        result = []
        for doc in split_docs:
            result.append({
                "content": doc.page_content,
                "metadata": doc.metadata
            })
        
        print(f"✅ 文档分块完成: {len(documents)} 个文档 -> {len(result)} 个文本块")
        return result
    
    def build_vectorstore(self, documents: List[dict]) -> int:
        """
        构建向量数据库
        """
        self._init_components()
        self._init_chromadb()
        
        split_docs = self.split_documents(documents)
        
        if not split_docs:
            print("❌ 没有文档需要处理")
            return 0
        
        print("正在构建向量数据库...")
        
        # 删除旧集合（如果存在）
        collection_name = "rag_documents"
        try:
            self.client.delete_collection(collection_name)
            print("已删除旧集合")
        except:
            pass
        
        # 创建新集合（不使用默认嵌入函数）
        self.collection = self.client.create_collection(
            name=collection_name
        )
        print(f"✅ 创建集合成功")
        
        # 手动生成嵌入向量
        print("正在生成嵌入向量...")
        texts = [doc["content"] for doc in split_docs]
        metadatas = [doc["metadata"] for doc in split_docs]
        ids = [f"doc_{i}" for i in range(len(split_docs))]
        
        # 生成嵌入
        try:
            embeddings_list = self.embeddings.embed_documents(texts)
            print(f"✅ 成功生成 {len(embeddings_list)} 个嵌入向量")
        except Exception as e:
            print(f"❌ 生成嵌入向量失败: {str(e)}")
            return 0
        
        # 添加到集合
        try:
            self.collection.add(
                documents=texts,
                metadatas=metadatas,
                ids=ids,
                embeddings=embeddings_list
            )
            print(f"✅ 成功添加到向量数据库")
        except Exception as e:
            print(f"❌ 添加到向量数据库失败: {str(e)}")
            return 0
        
        count = len(split_docs)
        print(f"✅ 向量数据库构建完成，共 {count} 个文本块")
        return count
    
    def load_vectorstore(self) -> bool:
        """
        加载已存在的向量数据库
        """
        self._init_chromadb()
        
        collection_name = "rag_documents"
        
        try:
            self.collection = self.client.get_collection(name=collection_name)
            count = self.collection.count()
            print(f"✅ 成功加载向量数据库，共 {count} 个文本块")
            return True
        except Exception as e:
            print(f"❌ 加载向量数据库失败: {str(e)}")
            return False
    
    def get_chunk_count(self) -> int:
        """
        获取向量数据库中的文本块数量
        """
        if self.collection is None:
            return 0
        
        try:
            return self.collection.count()
        except Exception as e:
            print(f"❌ 获取文本块数量失败: {str(e)}")
            return 0
    
    def search(self, query: str, k: int = 3) -> List[dict]:
        """
        搜索与查询最相关的文本块
        """
        if self.collection is None:
            print("❌ 向量数据库未加载")
            return []
        
        try:
            # 生成查询向量
            query_vec = self.embeddings.embed_query(query)
            
            # 查询
            results = self.collection.query(
                query_embeddings=[query_vec],
                n_results=k
            )
            
            sources = []
            docs = results.get('documents', [])
            metadatas = results.get('metadatas', [])
            
            if docs and metadatas:
                for i, doc in enumerate(docs[0]):
                    metadata = metadatas[0][i] if i < len(metadatas[0]) else {}
                    sources.append({
                        "filename": metadata.get("filename", "未知"),
                        "content": doc,
                        "source": metadata.get("source", "未知")
                    })
            
            print(f"✅ 搜索完成，找到 {len(sources)} 个结果")
            return sources
            
        except Exception as e:
            print(f"❌ 搜索失败: {str(e)}")
            return []

# 测试
if __name__ == "__main__":
    print("=== 测试 VectorStoreManager ===")
    
    manager = VectorStoreManager()
    
    # 测试构建
    test_docs = [
        {"content": "这是测试文档1的内容，关于自然语言处理。", "source": "test1.txt", "filename": "test1.txt"},
        {"content": "这是测试文档2的内容，关于机器学习。", "source": "test2.txt", "filename": "test2.txt"}
    ]
    
    count = manager.build_vectorstore(test_docs)
    print(f"添加了 {count} 个文本块")
    
    # 测试搜索
    results = manager.search("自然语言处理")
    print(f"搜索结果: {len(results)} 个")
    for r in results:
        print(f"  - {r['filename']}: {r['content'][:30]}...")
    
    print("=== 测试完成 ===")

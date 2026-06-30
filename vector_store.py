import os
import shutil
from typing import List, Optional

class VectorStoreManager:
    """
    向量数据库管理类：使用 FAISS 作为向量存储
    """
    
    def __init__(
        self,
        embedding_model: str = "nomic-embed-text",
        persist_directory: str = "./faiss_db",
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
        self.vectorstore = None
    
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
    
    def create_documents(self, raw_documents: List[dict]) -> List:
        """
        将原始文档转换为LangChain Document对象
        """
        from langchain.schema import Document
        
        documents = []
        for doc in raw_documents:
            doc_obj = Document(
                page_content=doc["content"],
                metadata={
                    "source": doc.get("source", "unknown"),
                    "filename": doc.get("filename", "unknown")
                }
            )
            documents.append(doc_obj)
        return documents
    
    def split_documents(self, documents: List) -> List:
        """
        对文档进行分块处理
        """
        self._init_components()
        
        if self.text_splitter is None:
            print("[ERROR] 文本分割器未初始化")
            return []
        
        split_docs = self.text_splitter.split_documents(documents)
        print("[INFO] 文档分块完成: {} 个文档 -> {} 个文本块".format(len(documents), len(split_docs)))
        return split_docs
    
    def build_vectorstore(self, documents: List[dict]) -> int:
        """
        构建向量数据库
        返回插入的文本块数量
        """
        self._init_components()
        
        langchain_docs = self.create_documents(documents)
        split_docs = self.split_documents(langchain_docs)
        
        if not split_docs:
            print("[ERROR] 没有文档需要处理")
            return 0
        
        print("[INFO] 正在构建向量数据库...")
        
        from langchain_community.vectorstores import FAISS
        
        # 删除旧目录（如果存在）
        if os.path.exists(self.persist_directory):
            shutil.rmtree(self.persist_directory)
        
        self.vectorstore = FAISS.from_documents(
            documents=split_docs,
            embedding=self.embeddings
        )
        
        # 保存到磁盘
        self.vectorstore.save_local(self.persist_directory)
        
        count = len(split_docs)
        print("[INFO] 向量数据库构建完成，共 {} 个文本块".format(count))
        return count
    
    def load_vectorstore(self) -> bool:
        """
        加载已存在的向量数据库
        """
        self._init_components()
        
        if os.path.exists(self.persist_directory):
            try:
                from langchain_community.vectorstores import FAISS
                
                self.vectorstore = FAISS.load_local(
                    self.persist_directory,
                    self.embeddings,
                    allow_dangerous_deserialization=True
                )
                print("[INFO] 成功加载向量数据库，共 {} 个文本块".format(self.get_chunk_count()))
                return True
            except Exception as e:
                print("[ERROR] 加载向量数据库失败: {}".format(str(e)))
                return False
        else:
            print("[ERROR] 向量数据库目录不存在")
            return False
    
    def get_chunk_count(self) -> int:
        """
        获取向量数据库中的文本块数量
        """
        if self.vectorstore is None:
            return 0
        
        try:
            return len(self.vectorstore.index_to_docstore_id)
        except Exception as e:
            print("[ERROR] 获取文本块数量失败: {}".format(str(e)))
            return 0
    
    def search(self, query: str, k: int = 3) -> List[dict]:
        """
        搜索与查询最相关的文本块
        """
        if self.vectorstore is None:
            print("[ERROR] 向量数据库未加载")
            return []
        
        try:
            results = self.vectorstore.similarity_search(query, k=k)
            
            sources = []
            for doc in results:
                sources.append({
                    "filename": doc.metadata.get("filename", "未知"),
                    "content": doc.page_content,
                    "source": doc.metadata.get("source", "未知")
                })
            
            print("[INFO] 搜索完成，找到 {} 个结果".format(len(sources)))
            return sources
            
        except Exception as e:
            print("[ERROR] 搜索失败: {}".format(str(e)))
            return []

# 测试
if __name__ == "__main__":
    print("=== 测试 VectorStoreManager (FAISS) ===")
    
    manager = VectorStoreManager()
    
    # 测试构建
    test_docs = [
        {"content": "这是测试文档1的内容，关于自然语言处理。", "source": "test1.txt", "filename": "test1.txt"},
        {"content": "这是测试文档2的内容，关于机器学习。", "source": "test2.txt", "filename": "test2.txt"}
    ]
    
    count = manager.build_vectorstore(test_docs)
    print("添加了 {} 个文本块".format(count))
    
    # 测试搜索
    results = manager.search("自然语言处理")
    print("搜索结果: {} 个".format(len(results)))
    for r in results:
        print("  - {}: {}".format(r['filename'], r['content'][:30]))
    
    print("=== 测试完成 ===")

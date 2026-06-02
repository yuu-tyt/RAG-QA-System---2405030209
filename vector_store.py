import os
from typing import List, Optional
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.schema import Document

class VectorStoreManager:
    """
    向量数据库管理类：负责文档分块、向量化和存储检索
    AI生成：使用Trae辅助编写
    """
    
    def __init__(
        self,
        embedding_model: str = "all-MiniLM-L6-v2",
        persist_directory: str = "./chroma_db",
        chunk_size: int = 1000,
        chunk_overlap: int = 200
    ):
        self.embedding_model = embedding_model
        self.persist_directory = persist_directory
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
        self.embeddings = SentenceTransformerEmbeddings(model_name=embedding_model)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", "。", "！", "？", "；", "，", " ", ""]
        )
        self.vectorstore: Optional[Chroma] = None
    
    def create_documents(self, raw_documents: List[dict]) -> List[Document]:
        """
        将原始文档转换为LangChain Document对象
        AI生成：使用Trae辅助编写
        """
        documents = []
        for doc in raw_documents:
            doc_obj = Document(
                page_content=doc["content"],
                metadata={
                    "source": doc["source"],
                    "filename": doc["filename"]
                }
            )
            documents.append(doc_obj)
        return documents
    
    def split_documents(self, documents: List[Document]) -> List[Document]:
        """
        对文档进行分块处理
        AI生成：使用Trae辅助编写
        """
        split_docs = self.text_splitter.split_documents(documents)
        print(f"文档分块完成: {len(documents)} 个文档 -> {len(split_docs)} 个文本块")
        return split_docs
    
    def build_vectorstore(self, documents: List[dict]) -> int:
        """
        构建向量数据库
        返回插入的文本块数量
        AI生成：使用Trae辅助编写
        """
        langchain_docs = self.create_documents(documents)
        split_docs = self.split_documents(langchain_docs)
        
        if not split_docs:
            print("没有文档需要处理")
            return 0
        
        print("正在构建向量数据库...")
        print(f"使用嵌入模型: {self.embedding_model}")
        
        if os.path.exists(self.persist_directory) and self.vectorstore is None:
            print(f"从持久化目录加载向量数据库: {self.persist_directory}")
            self.vectorstore = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings
            )
            existing_count = self.vectorstore._collection.count()
            print(f"现有文本块数量: {existing_count}")
            
            print("添加新文档到向量数据库...")
            self.vectorstore.add_documents(split_docs)
        elif self.vectorstore is None:
            self.vectorstore = Chroma.from_documents(
                documents=split_docs,
                embedding=self.embeddings,
                persist_directory=self.persist_directory
            )
        else:
            self.vectorstore.add_documents(split_docs)
        
        final_count = self.vectorstore._collection.count()
        print(f"向量数据库构建完成，当前共有 {final_count} 个文本块")
        return final_count
    
    def load_vectorstore(self) -> bool:
        """
        加载已有的向量数据库
        AI生成：使用Trae辅助编写
        """
        if not os.path.exists(self.persist_directory):
            print(f"向量数据库目录不存在: {self.persist_directory}")
            return False
        
        try:
            self.vectorstore = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings
            )
            count = self.vectorstore._collection.count()
            print(f"成功加载向量数据库，共 {count} 个文本块")
            return True
        except Exception as e:
            print(f"加载向量数据库失败: {str(e)}")
            return False
    
    def retrieve(self, query: str, k: int = 3) -> List[Document]:
        """
        检索最相关的k个文本块
        AI生成：使用Trae辅助编写
        """
        if self.vectorstore is None:
            print("向量数据库未初始化")
            return []
        
        try:
            results = self.vectorstore.similarity_search(query, k=k)
            return results
        except Exception as e:
            print(f"检索失败: {str(e)}")
            return []
    
    def get_chunk_count(self) -> int:
        """
        获取当前向量数据库中的文本块数量
        AI生成：使用Trae辅助编写
        """
        if self.vectorstore is None:
            return 0
        return self.vectorstore._collection.count()
    
    def clear_vectorstore(self):
        """
        清空向量数据库
        AI生成：使用Trae辅助编写
        """
        if self.vectorstore is not None:
            self.vectorstore.delete_collection()
            self.vectorstore = None
            print("向量数据库已清空")


if __name__ == "__main__":
    from document_processor import DocumentProcessor
    
    processor = DocumentProcessor()
    docs = processor.process_directory("./documents")
    
    if docs:
        vector_manager = VectorStoreManager()
        vector_manager.build_vectorstore(docs)
        
        test_query = "什么是自然语言处理？"
        results = vector_manager.retrieve(test_query)
        
        print(f"\n查询: {test_query}")
        print("=" * 50)
        for i, doc in enumerate(results, 1):
            print(f"\n结果 {i}:")
            print(f"来源: {doc.metadata.get('filename', '未知')}")
            print(f"内容: {doc.page_content[:200]}...")
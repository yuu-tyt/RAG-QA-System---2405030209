from typing import List, Dict, Optional

class RAGQASystem:
    """
    RAG问答系统：整合检索和大模型进行问答
    AI生成：使用Trae辅助编写
    """
    
    def __init__(
        self,
        llm_model: str = "qwen2.5:1.5b",
        embedding_model: str = "nomic-embed-text",
        persist_directory: str = "./faiss_db"
    ):
        self.llm_model = llm_model
        self.embedding_model = embedding_model
        self.persist_directory = persist_directory
        
        # 延迟初始化
        self.vector_manager = None
        self.llm = None
        self.memory = None
        self.qa_chain = None
    
    def initialize(self) -> bool:
        """
        初始化系统，加载向量数据库
        AI生成：使用Trae辅助编写
        """
        try:
            # 延迟导入和初始化
            from langchain_ollama import OllamaLLM
            from langchain.memory import ConversationBufferMemory
            from vector_store import VectorStoreManager
            
            self.vector_manager = VectorStoreManager(
                embedding_model=self.embedding_model,
                persist_directory=self.persist_directory
            )
            
            self.llm = OllamaLLM(
                model=self.llm_model,
                temperature=0.1,
                num_predict=512,
                num_ctx=4096,
                keep_alive="10m"
            )
            
            self.memory = ConversationBufferMemory(
                memory_key="chat_history",
                return_messages=True,
                output_key="answer"
            )
            
            if self.vector_manager.load_vectorstore():
                self._build_qa_chain()
                return True
            return False
        except Exception as e:
            print(f"初始化失败: {str(e)}")
            return False
    
    def _build_qa_chain(self):
        """
        构建问答链
        AI生成：使用Trae辅助编写
        """
        if self.vector_manager is None or self.vector_manager.vectorstore is None:
            print("向量数据库未加载")
            return
        
        system_prompt = """你是一个专业的问答助手。请基于提供的参考文档回答用户问题。

重要规则：
1. 只使用参考文档中的信息回答问题
2. 如果参考文档中没有相关信息，请明确回答："文档中未找到相关答案"
3. 回答要准确、简洁、有条理
4. 如果引用文档内容，请注明来源
5. 不要编造或推测答案

参考文档：
{context}

问题：{question}

请基于以上参考文档回答："""

        self.qa_chain = system_prompt
        
        print("RAG问答链构建完成")
    
    def build_knowledge_base(self, documents: List[dict]) -> int:
        """
        构建知识库
        AI生成：使用Trae辅助编写
        """
        if self.vector_manager is None:
            print("请先初始化系统")
            return 0
        
        count = self.vector_manager.build_vectorstore(documents)
        if count > 0:
            self._build_qa_chain()
        return count
    
    def ask(self, question: str) -> Dict:
        """
        提问并获取答案
        AI生成：使用Trae辅助编写
        """
        if self.qa_chain is None:
            return {
                "answer": "系统未初始化，请先构建知识库",
                "sources": []
            }
        
        try:
            docs = self.vector_manager.vectorstore.similarity_search(question, k=2)
            context = "\n\n".join(
                f"[来源: {doc.metadata.get('filename', '未知')}]\n{doc.page_content}"
                for doc in docs
            )
            
            prompt = self.qa_chain.format(context=context, question=question)
            answer = self.llm.invoke(prompt)
            
            sources = []
            for doc in docs:
                sources.append({
                    "filename": doc.metadata.get("filename", "未知"),
                    "content": doc.page_content[:200] + "..."
                })
            
            if self.memory is not None:
                self.memory.chat_memory.add_user_message(question)
                self.memory.chat_memory.add_ai_message(answer)
            
            return {
                "answer": answer,
                "sources": sources
            }
        except Exception as e:
            return {
                "answer": f"回答时发生错误: {str(e)}",
                "sources": []
            }
    
    def get_chat_history(self) -> List[Dict]:
        """
        获取对话历史
        AI生成：使用Trae辅助编写
        """
        if self.memory is None:
            return []
        
        history = []
        messages = self.memory.chat_memory.messages
        for i in range(0, len(messages), 2):
            if i + 1 < len(messages):
                history.append({
                    "question": messages[i].content,
                    "answer": messages[i + 1].content
                })
        return history
    
    def clear_history(self):
        """
        清空对话历史
        AI生成：使用Trae辅助编写
        """
        if self.memory:
            self.memory.clear()
            print("对话历史已清空")
    
    def get_chunk_count(self) -> int:
        """
        获取知识库文本块数量
        AI生成：使用Trae辅助编写
        """
        if self.vector_manager:
            return self.vector_manager.get_chunk_count()
        return 0


def main():
    """
    命令行版本的RAG问答系统
    AI生成：使用Trae辅助编写
    """
    from document_processor import DocumentProcessor
    
    print("=" * 60)
    print("RAG问答系统 - 命令行版本")
    print("=" * 60)
    
    rag_system = RAGQASystem()
    
    if rag_system.initialize():
        print("成功加载现有知识库")
    else:
        print("未找到现有知识库，请先构建")
        doc_dir = input("请输入文档目录路径（默认 ./documents）: ").strip()
        if not doc_dir:
            doc_dir = "./documents"
        
        processor = DocumentProcessor()
        documents = processor.process_directory(doc_dir)
        
        if documents:
            rag_system.build_knowledge_base(documents)
        else:
            print("未找到任何文档，退出程序")
            return
    
    print("\n" + "=" * 60)
    print("开始问答（输入 'quit' 退出，'clear' 清空历史）")
    print("=" * 60)
    
    while True:
        question = input("\n请输入问题: ").strip()
        
        if question.lower() == 'quit':
            print("感谢使用，再见！")
            break
        elif question.lower() == 'clear':
            rag_system.clear_history()
            print("对话历史已清空")
            continue
        elif not question:
            continue
        
        print("\n正在思考...")
        result = rag_system.ask(question)
        
        print("\n" + "-" * 40)
        print("回答:")
        print(result["answer"])
        
        if result["sources"]:
            print("\n参考来源:")
            for i, source in enumerate(result["sources"], 1):
                print(f"  [{i}] {source['filename']}")


if __name__ == "__main__":
    main()

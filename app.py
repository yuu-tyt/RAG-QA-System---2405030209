import streamlit as st
import os
from typing import List
from document_processor import DocumentProcessor
from vector_store import VectorStoreManager
from rag_chain import RAGQASystem

st.set_page_config(
    page_title="RAG问答系统",
    page_icon="📚",
    layout="wide"
)

def init_session_state():
    """
    初始化会话状态
    AI生成：使用Trae辅助编写
    """
    if "rag_system" not in st.session_state:
        st.session_state.rag_system = RAGQASystem()
        st.session_state.rag_system.initialize()
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    if "knowledge_base_built" not in st.session_state:
        st.session_state.knowledge_base_built = False
    
    if "processed_files" not in st.session_state:
        st.session_state.processed_files = []

def main():
    """
    Streamlit主应用
    AI生成：使用Trae辅助编写
    """
    init_session_state()
    
    st.title("📚 RAG问答系统")
    st.markdown("基于本地知识库的智能问答系统（使用Ollama + LangChain + ChromaDB）")
    
    with st.sidebar:
        st.header("📊 知识库状态")
        
        chunk_count = st.session_state.rag_system.get_chunk_count()
        st.metric("文本块数量", chunk_count)
        
        if st.session_state.processed_files:
            st.subheader("已处理文档")
            for filename in st.session_state.processed_files:
                st.text(f"📄 {filename}")
        
        st.divider()
        
        st.header("⚙️ 设置")
        if st.button("🗑️ 清空对话历史"):
            st.session_state.rag_system.clear_history()
            st.session_state.chat_history = []
            st.success("对话历史已清空！")
        
        if st.button("🔄 重新加载知识库"):
            st.session_state.rag_system = RAGQASystem()
            st.session_state.rag_system.initialize()
            st.success("知识库已重新加载！")
        
        st.divider()
        st.markdown("""
        ### 使用说明
        1. 上传PDF或DOCX文档
        2. 点击"构建知识库"
        3. 在下方输入问题进行问答
        """)
    
    tab1, tab2 = st.tabs(["💬 问答", "📁 文档管理"])
    
    with tab2:
        st.header("文档上传与知识库构建")
        
        uploaded_files = st.file_uploader(
            "上传文档",
            type=["pdf", "docx"],
            accept_multiple_files=True,
            help="支持PDF和DOCX格式"
        )
        
        if uploaded_files:
            st.info(f"已选择 {len(uploaded_files)} 个文件")
            
            for file in uploaded_files:
                st.text(f"📄 {file.name} ({file.size // 1024} KB)")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔨 构建知识库", type="primary", use_container_width=True):
                if uploaded_files:
                    with st.spinner("正在处理文档并构建知识库..."):
                        processor = DocumentProcessor()
                        documents = processor.process_uploaded_files(uploaded_files)
                        
                        if documents:
                            count = st.session_state.rag_system.build_knowledge_base(documents)
                            
                            for doc in documents:
                                if doc["filename"] not in st.session_state.processed_files:
                                    st.session_state.processed_files.append(doc["filename"])
                            
                            st.success(f"知识库构建完成！共 {count} 个文本块")
                            st.rerun()
                        else:
                            st.error("未能从文档中提取文本内容")
                else:
                    st.warning("请先上传文档")
        
        with col2:
            if st.button("📂 从文件夹加载", use_container_width=True):
                doc_dir = st.text_input(
                    "文档目录路径",
                    value="./documents",
                    key="doc_dir_input"
                )
                
                if os.path.exists(doc_dir):
                    with st.spinner("正在处理文档..."):
                        processor = DocumentProcessor()
                        documents = processor.process_directory(doc_dir)
                        
                        if documents:
                            count = st.session_state.rag_system.build_knowledge_base(documents)
                            
                            for doc in documents:
                                if doc["filename"] not in st.session_state.processed_files:
                                    st.session_state.processed_files.append(doc["filename"])
                            
                            st.success(f"知识库构建完成！共 {count} 个文本块")
                            st.rerun()
                        else:
                            st.warning("未找到任何文档")
                else:
                    st.error("目录不存在")
        
        st.divider()
        st.subheader("测试结果记录")
        st.markdown("""
        **相关问题测试（5个）：**
        1. 什么是自然语言处理？
        2. NLP有哪些主要应用领域？
        3. 什么是词向量？
        4. Transformer模型的优势是什么？
        5. 如何评价一个NLP模型的性能？
        
        **无关问题测试（2个）：**
        1. 今天的天气怎么样？
        2. 如何制作红烧肉？
        """)
    
    with tab1:
        st.header("智能问答")
        
        for chat in st.session_state.chat_history:
            with st.chat_message("user"):
                st.write(chat["question"])
            with st.chat_message("assistant"):
                st.write(chat["answer"])
                if chat.get("sources"):
                    with st.expander("查看参考来源"):
                        for i, source in enumerate(chat["sources"], 1):
                            st.markdown(f"**[{i}] {source['filename']}**")
                            st.text(source["content"][:300] + "...")
        
        if prompt := st.chat_input("请输入您的问题..."):
            with st.chat_message("user"):
                st.write(prompt)
            
            with st.chat_message("assistant"):
                with st.spinner("正在思考..."):
                    result = st.session_state.rag_system.ask(prompt)
                
                st.write(result["answer"])
                
                if result["sources"]:
                    with st.expander("查看参考来源"):
                        for i, source in enumerate(result["sources"], 1):
                            st.markdown(f"**[{i}] {source['filename']}**")
                            st.text(source["content"][:300] + "...")
                
                st.session_state.chat_history.append({
                    "question": prompt,
                    "answer": result["answer"],
                    "sources": result["sources"]
                })

if __name__ == "__main__":
    main()
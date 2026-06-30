import streamlit as st
import os
import json

st.set_page_config(
    page_title="RAG问答系统",
    page_icon="📚",
    layout="wide"
)

def check_ollama():
    try:
        import requests
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "deepseek-r1:7b", "prompt": "hi", "stream": False},
            timeout=30
        )
        return response.status_code == 200
    except:
        return False

def load_documents_from_folder(folder_path):
    documents = []
    if os.path.exists(folder_path):
        for filename in os.listdir(folder_path):
            filepath = os.path.join(folder_path, filename)
            try:
                # 支持 txt 文件
                if filename.endswith('.txt'):
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                        documents.append({
                            "filename": filename,
                            "content": content,
                            "source": filepath
                        })
                # 支持 docx 文件
                elif filename.endswith('.docx'):
                    from docx import Document
                    doc = Document(filepath)
                    content = '\n'.join([paragraph.text for paragraph in doc.paragraphs])
                    documents.append({
                        "filename": filename,
                        "content": content,
                        "source": filepath
                    })
            except Exception as e:
                print(f"加载文件 {filename} 失败: {str(e)}")
                pass
    return documents

def main():
    st.title("📚 RAG问答系统")
    st.markdown("基于本地知识库的智能问答系统（使用Ollama + LangChain + FAISS）")
    
    # 系统状态检查
    col1, col2 = st.columns(2)
    with col1:
        if check_ollama():
            st.success("✅ Ollama 服务正常")
        else:
            st.error("❌ Ollama 服务未运行")
    
    with col2:
        doc_dir = "./documents"
        if os.path.exists(doc_dir):
            files = os.listdir(doc_dir)
            st.success(f"✅ 文档目录存在 ({len(files)} 个文件)")
        else:
            st.warning("⚠️ 文档目录不存在")
    
    # 初始化按钮
    st.subheader("🔧 系统初始化")
    if st.button("🔄 初始化RAG系统", type="primary"):
        with st.spinner("正在初始化..."):
            try:
                from rag_chain import RAGQASystem
                st.session_state.rag_system = RAGQASystem()
                st.session_state.rag_system.initialize()
                st.success("✅ RAG系统初始化成功！")
            except Exception as e:
                st.error(f"❌ 初始化失败: {str(e)}")
    
    # 文档管理
    st.subheader("📁 文档管理")
    
    # 上传文档
    uploaded_files = st.file_uploader("上传文档", type=["txt", "pdf", "docx"], accept_multiple_files=True)
    
    if uploaded_files:
        st.info(f"已选择 {len(uploaded_files)} 个文件")
        # 保存上传的文件
        for file in uploaded_files:
            save_path = os.path.join("./documents", file.name)
            with open(save_path, "wb") as f:
                f.write(file.getbuffer())
        st.success("✅ 文件已保存到 documents 目录")
    
    # 从文件夹加载文档
    col3, col4 = st.columns(2)
    with col3:
        if st.button("📂 从文件夹加载文档"):
            docs = load_documents_from_folder("./documents")
            if docs:
                st.session_state.loaded_docs = docs
                st.success(f"✅ 加载成功！共 {len(docs)} 个文档")
                for doc in docs:
                    st.write(f"- {doc['filename']}")
            else:
                st.warning("⚠️ 未找到可加载的文档")
    
    # 构建知识库按钮
    with col4:
        if st.button("🏗️ 构建知识库", type="primary"):
            if 'rag_system' not in st.session_state or not st.session_state.rag_system:
                st.error("❌ 请先初始化RAG系统")
            elif 'loaded_docs' not in st.session_state or not st.session_state.loaded_docs:
                st.warning("⚠️ 请先加载文档")
            else:
                with st.spinner("正在构建知识库..."):
                    count = st.session_state.rag_system.build_knowledge_base(st.session_state.loaded_docs)
                    st.success(f"✅ 知识库构建完成！共 {count} 个文本块")
    
    # 显示知识库状态
    if 'rag_system' in st.session_state and st.session_state.rag_system:
        chunk_count = st.session_state.rag_system.get_chunk_count()
        st.info(f"📊 当前知识库包含 {chunk_count} 个文本块")
    
    # 问答区域
    st.subheader("💬 智能问答")
    
    if 'rag_system' not in st.session_state or not st.session_state.rag_system:
        st.warning("⚠️ 请先初始化RAG系统")
    else:
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        
        for chat in st.session_state.chat_history:
            with st.chat_message("user"):
                st.write(chat["question"])
            with st.chat_message("assistant"):
                st.write(chat["answer"])
        
        if prompt := st.chat_input("请输入问题..."):
            with st.chat_message("user"):
                st.write(prompt)
            
            with st.chat_message("assistant"):
                with st.spinner("正在思考..."):
                    try:
                        result = st.session_state.rag_system.ask(prompt)
                        st.write(result["answer"])
                        
                        st.session_state.chat_history.append({
                            "question": prompt,
                            "answer": result["answer"]
                        })
                    except Exception as e:
                        st.error(f"❌ 问答失败: {str(e)}")

if __name__ == "__main__":
    main()

import streamlit as st
import os

st.set_page_config(
    page_title="RAG问答系统",
    page_icon="📚",
    layout="wide"
)

def main():
    st.title("📚 RAG问答系统")
    st.markdown("基于本地知识库的智能问答系统（使用Ollama + LangChain + ChromaDB）")
    
    st.success("Streamlit 应用启动成功！")
    
    st.subheader("系统状态检查")
    
    # 检查 Ollama
    try:
        import requests
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "deepseek-r1:7b", "prompt": "hello", "stream": False},
            timeout=30
        )
        if response.status_code == 200:
            st.success("✅ Ollama 服务正常")
        else:
            st.error("❌ Ollama 服务异常")
    except Exception as e:
        st.error(f"❌ 无法连接 Ollama: {str(e)}")
    
    # 检查文档目录
    doc_dir = "./documents"
    if os.path.exists(doc_dir):
        files = os.listdir(doc_dir)
        st.success(f"✅ 文档目录存在，共 {len(files)} 个文件")
    else:
        st.warning("⚠️ 文档目录不存在")
    
    st.divider()
    st.subheader("使用说明")
    st.markdown("""
    1. 确保 Ollama 服务正在运行
    2. 确保 deepseek-r1:7b 和 nomic-embed-text 模型已下载
    3. 将文档放入 documents 文件夹
    4. 运行完整版本的应用
    """)

if __name__ == "__main__":
    main()

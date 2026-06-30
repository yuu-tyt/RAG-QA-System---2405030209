import streamlit as st
import os

st.title("🔍 诊断模式")
st.write("逐步测试各个组件")

# 阶段1: 基础测试
st.subheader("阶段1: 基础测试")
st.success("✅ Streamlit基础功能正常")

# 阶段2: 测试requests
st.subheader("阶段2: 网络请求测试")
try:
    import requests
    st.success("✅ requests模块导入成功")
    
    # 测试Ollama连接
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "deepseek-r1:7b", "prompt": "hi", "stream": False},
            timeout=30
        )
        if response.status_code == 200:
            st.success("✅ Ollama连接成功")
        else:
            st.error("❌ Ollama响应异常")
    except Exception as e:
        st.error(f"❌ Ollama连接失败: {str(e)}")
except Exception as e:
    st.error(f"❌ requests模块导入失败: {str(e)}")

# 阶段3: 测试LangChain导入
st.subheader("阶段3: LangChain导入测试")
try:
    from langchain_ollama import OllamaLLM
    st.success("✅ langchain_ollama导入成功")
except Exception as e:
    st.error(f"❌ langchain_ollama导入失败: {str(e)}")

# 阶段4: 测试Chroma导入
st.subheader("阶段4: Chroma导入测试")
try:
    from langchain_community.vectorstores import Chroma
    st.success("✅ Chroma导入成功")
except Exception as e:
    st.error(f"❌ Chroma导入失败: {str(e)}")

# 阶段5: 测试嵌入模型
st.subheader("阶段5: 嵌入模型测试")
try:
    from langchain_ollama import OllamaEmbeddings
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    vec = embeddings.embed_query("test")
    st.success(f"✅ 嵌入模型测试成功，向量长度: {len(vec)}")
except Exception as e:
    st.error(f"❌ 嵌入模型测试失败: {str(e)}")

# 阶段6: 测试文档处理器
st.subheader("阶段6: 文档处理器测试")
try:
    from document_processor import DocumentProcessor
    st.success("✅ DocumentProcessor导入成功")
except Exception as e:
    st.error(f"❌ DocumentProcessor导入失败: {str(e)}")

# 阶段7: 测试RAG系统
st.subheader("阶段7: RAG系统测试")
if st.button("测试RAG系统初始化"):
    with st.spinner("正在初始化..."):
        try:
            from rag_chain import RAGQASystem
            rag_system = RAGQASystem()
            rag_system.initialize()
            st.success("✅ RAG系统初始化成功")
        except Exception as e:
            st.error(f"❌ RAG系统初始化失败: {str(e)}")

st.divider()
st.info("请查看以上测试结果，找出失败的阶段")

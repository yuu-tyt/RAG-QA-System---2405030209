import streamlit as st

st.title("测试页面")
st.write("Hello Streamlit!")

# 测试 Ollama 连接
try:
    from langchain_ollama import OllamaLLM
    llm = OllamaLLM(model="deepseek-r1:7b")
    result = llm.invoke("hello")
    st.success(f"Ollama 连接成功!")
    st.write(f"响应: {result[:50]}...")
except Exception as e:
    st.error(f"Ollama 连接失败: {str(e)}")

# 测试嵌入模型
try:
    from langchain_ollama import OllamaEmbeddings
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    text = "测试文本"
    vec = embeddings.embed_query(text)
    st.success(f"嵌入模型连接成功!")
    st.write(f"向量长度: {len(vec)}")
except Exception as e:
    st.error(f"嵌入模型连接失败: {str(e)}")

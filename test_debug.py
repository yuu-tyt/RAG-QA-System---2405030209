import os
import sys
import traceback

print("=== 调试测试 ===")
print(f"Python版本: {sys.version}")

# 测试1: 导入 langchain_chroma
print("\n1. 测试导入 langchain_chroma")
try:
    from langchain_chroma import Chroma
    print("✅ 成功导入 Chroma")
except Exception as e:
    print(f"❌ 导入失败: {str(e)}")
    traceback.print_exc()
    exit()

# 测试2: 创建简单的向量
print("\n2. 测试创建嵌入向量")
try:
    from langchain_ollama import OllamaEmbeddings
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    
    # 先测试单个嵌入
    vec = embeddings.embed_query("hello")
    print(f"✅ 成功创建嵌入向量，长度: {len(vec)}")
    
    # 测试多个嵌入
    texts = ["hello", "world", "test"]
    vecs = embeddings.embed_documents(texts)
    print(f"✅ 成功创建多个嵌入向量，数量: {len(vecs)}")
    
except Exception as e:
    print(f"❌ 嵌入测试失败: {str(e)}")
    traceback.print_exc()
    exit()

# 测试3: 创建 Chroma 并添加文档（逐个添加）
print("\n3. 测试创建 Chroma 并逐个添加文档")
try:
    persist_dir = "./test_debug_db"
    if os.path.exists(persist_dir):
        import shutil
        shutil.rmtree(persist_dir)
    
    vectorstore = Chroma(
        persist_directory=persist_dir,
        embedding_function=embeddings
    )
    print("✅ 成功创建 Chroma 对象")
    
    from langchain.schema import Document
    
    # 逐个添加文档
    docs = [
        Document(page_content="这是测试文档1的内容", metadata={"source": "test1"}),
        Document(page_content="这是测试文档2的内容", metadata={"source": "test2"})
    ]
    
    for i, doc in enumerate(docs):
        print(f"   添加文档 {i+1}...")
        try:
            vectorstore.add_documents([doc])
            print(f"   ✅ 文档 {i+1} 添加成功")
        except Exception as e:
            print(f"   ❌ 文档 {i+1} 添加失败: {str(e)}")
            traceback.print_exc()
            exit()
            
    print("✅ 所有文档添加成功")
    
except Exception as e:
    print(f"❌ Chroma 测试失败: {str(e)}")
    traceback.print_exc()
    exit()

print("\n=== 测试完成 ===")

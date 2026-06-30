import os
import shutil

print("=== 测试新的 langchain_chroma ===")

# 测试1: 导入
print("\n1. 测试导入")
try:
    from langchain_chroma import Chroma
    print("✅ 成功导入新的 Chroma")
except Exception as e:
    print(f"❌ 导入失败: {str(e)}")
    exit()

# 测试2: 创建 Chroma 对象
print("\n2. 测试创建 Chroma 对象")
try:
    from langchain_ollama import OllamaEmbeddings
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    
    persist_dir = "./test_chroma_db_new"
    if os.path.exists(persist_dir):
        shutil.rmtree(persist_dir)
    
    vectorstore = Chroma(
        persist_directory=persist_dir,
        embedding_function=embeddings
    )
    print("✅ 成功创建 Chroma 对象")
except Exception as e:
    print(f"❌ 创建失败: {str(e)}")
    import traceback
    traceback.print_exc()
    exit()

# 测试3: 添加文档
print("\n3. 测试添加文档")
try:
    from langchain.schema import Document
    docs = [
        Document(page_content="这是测试文档1的内容", metadata={"source": "test1"}),
        Document(page_content="这是测试文档2的内容", metadata={"source": "test2"})
    ]
    vectorstore.add_documents(docs)
    print("✅ 成功添加文档")
except Exception as e:
    print(f"❌ 添加文档失败: {str(e)}")
    import traceback
    traceback.print_exc()
    exit()

# 测试4: 搜索
print("\n4. 测试搜索")
try:
    results = vectorstore.similarity_search("测试", k=2)
    print(f"✅ 搜索成功，找到 {len(results)} 个结果")
    for doc in results:
        print(f"  - {doc.page_content}")
except Exception as e:
    print(f"❌ 搜索失败: {str(e)}")
    import traceback
    traceback.print_exc()
    exit()

print("\n=== 所有测试通过 ===")

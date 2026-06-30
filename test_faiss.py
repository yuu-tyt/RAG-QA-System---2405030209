import os
import sys
import traceback

print("=== 测试 FAISS ===")
print(f"Python版本: {sys.version}")

# 测试1: 导入
print("\n1. 测试导入")
try:
    from langchain_community.vectorstores import FAISS
    from langchain_ollama import OllamaEmbeddings
    print("✅ 成功导入 FAISS 和 OllamaEmbeddings")
except Exception as e:
    print(f"❌ 导入失败: {str(e)}")
    traceback.print_exc()
    exit()

# 测试2: 创建嵌入
print("\n2. 测试创建嵌入")
try:
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    vec = embeddings.embed_query("test")
    print(f"✅ 成功创建嵌入向量，长度: {len(vec)}")
except Exception as e:
    print(f"❌ 创建嵌入失败: {str(e)}")
    traceback.print_exc()
    exit()

# 测试3: 创建 FAISS 并添加文档
print("\n3. 测试创建 FAISS")
try:
    from langchain.schema import Document
    
    docs = [
        Document(page_content="这是测试文档1的内容，关于自然语言处理。", metadata={"source": "test1.txt"}),
        Document(page_content="这是测试文档2的内容，关于机器学习。", metadata={"source": "test2.txt"})
    ]
    
    print("   创建 FAISS 向量库...")
    db = FAISS.from_documents(docs, embeddings)
    print("✅ 成功创建 FAISS 向量库")
    
except Exception as e:
    print(f"❌ 创建 FAISS 失败: {str(e)}")
    traceback.print_exc()
    exit()

# 测试4: 搜索
print("\n4. 测试搜索")
try:
    results = db.similarity_search("自然语言处理", k=2)
    print(f"✅ 搜索成功，找到 {len(results)} 个结果")
    for r in results:
        print(f"  - {r.page_content[:30]}...")
except Exception as e:
    print(f"❌ 搜索失败: {str(e)}")
    traceback.print_exc()
    exit()

# 测试5: 保存和加载
print("\n5. 测试保存和加载")
try:
    persist_dir = "./faiss_db"
    if os.path.exists(persist_dir):
        import shutil
        shutil.rmtree(persist_dir)
    
    db.save_local(persist_dir)
    print("✅ 成功保存 FAISS 向量库")
    
    db2 = FAISS.load_local(persist_dir, embeddings, allow_dangerous_deserialization=True)
    results = db2.similarity_search("机器学习", k=2)
    print(f"✅ 成功加载并搜索，找到 {len(results)} 个结果")
    
except Exception as e:
    print(f"❌ 保存/加载失败: {str(e)}")
    traceback.print_exc()
    exit()

print("\n=== 所有测试通过 ===")

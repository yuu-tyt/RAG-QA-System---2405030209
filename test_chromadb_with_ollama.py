import os
import sys
import traceback

print("=== 测试 chromadb + Ollama 嵌入 ===")
print(f"Python版本: {sys.version}")

# 测试1: 导入 chromadb 和 OllamaEmbeddings
print("\n1. 测试导入")
try:
    import chromadb
    from langchain_ollama import OllamaEmbeddings
    print(f"✅ 成功导入 chromadb，版本: {chromadb.__version__}")
    print("✅ 成功导入 OllamaEmbeddings")
except Exception as e:
    print(f"❌ 导入失败: {str(e)}")
    traceback.print_exc()
    exit()

# 测试2: 创建 OllamaEmbeddings
print("\n2. 测试创建 OllamaEmbeddings")
try:
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    print("✅ 成功创建 OllamaEmbeddings")
    
    # 测试嵌入
    vec = embeddings.embed_query("test")
    print(f"✅ 嵌入向量长度: {len(vec)}")
except Exception as e:
    print(f"❌ 创建嵌入失败: {str(e)}")
    traceback.print_exc()
    exit()

# 测试3: 创建 chromadb 客户端（禁用默认嵌入）
print("\n3. 测试创建 chromadb 客户端")
try:
    # 删除旧目录
    import shutil
    persist_dir = "./test_chromadb_ollama"
    if os.path.exists(persist_dir):
        shutil.rmtree(persist_dir)
    
    client = chromadb.PersistentClient(path=persist_dir)
    print("✅ 成功创建客户端")
except Exception as e:
    print(f"❌ 创建客户端失败: {str(e)}")
    traceback.print_exc()
    exit()

# 测试4: 创建集合（使用 OllamaEmbeddings）
print("\n4. 测试创建集合")
try:
    # 创建自定义嵌入函数
    def custom_embed(texts):
        print(f"   正在嵌入 {len(texts)} 个文本...")
        return embeddings.embed_documents(texts)
    
    collection = client.create_collection(
        name="test_collection",
        embedding_function=custom_embed
    )
    print("✅ 成功创建集合")
except Exception as e:
    print(f"❌ 创建集合失败: {str(e)}")
    traceback.print_exc()
    exit()

# 测试5: 添加文档
print("\n5. 测试添加文档")
try:
    documents = ["这是测试文档1的内容", "这是测试文档2的内容"]
    ids = ["doc1", "doc2"]
    
    print("   添加文档...")
    collection.add(
        documents=documents,
        ids=ids
    )
    print("✅ 成功添加文档")
except Exception as e:
    print(f"❌ 添加文档失败: {str(e)}")
    traceback.print_exc()
    exit()

# 测试6: 查询
print("\n6. 测试查询")
try:
    query_vec = embeddings.embed_query("测试")
    results = collection.query(
        query_embeddings=[query_vec],
        n_results=2
    )
    print(f"✅ 查询成功，结果数量: {len(results['documents'][0])}")
except Exception as e:
    print(f"❌ 查询失败: {str(e)}")
    traceback.print_exc()
    exit()

print("\n=== 所有测试通过 ===")

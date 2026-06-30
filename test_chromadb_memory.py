import os
import sys
import traceback

print("=== 测试 chromadb 内存模式 ===")
print(f"Python版本: {sys.version}")

# 测试1: 导入 chromadb
print("\n1. 测试导入 chromadb")
try:
    import chromadb
    print(f"✅ 成功导入 chromadb，版本: {chromadb.__version__}")
except Exception as e:
    print(f"❌ 导入失败: {str(e)}")
    traceback.print_exc()
    exit()

# 测试2: 创建内存客户端
print("\n2. 测试创建内存客户端")
try:
    client = chromadb.Client()
    print("✅ 成功创建内存客户端")
except Exception as e:
    print(f"❌ 创建客户端失败: {str(e)}")
    traceback.print_exc()
    exit()

# 测试3: 创建集合
print("\n3. 测试创建集合")
try:
    collection = client.create_collection(name="test_collection")
    print("✅ 成功创建集合")
except Exception as e:
    print(f"❌ 创建集合失败: {str(e)}")
    traceback.print_exc()
    exit()

# 测试4: 添加文档（直接提供嵌入向量）
print("\n4. 测试添加文档")
try:
    # 使用随机向量代替真实嵌入
    import random
    documents = ["这是测试文档1的内容", "这是测试文档2的内容"]
    ids = ["doc1", "doc2"]
    embeddings = [[random.random() for _ in range(768)] for _ in range(2)]
    
    print("   添加文档...")
    collection.add(
        documents=documents,
        ids=ids,
        embeddings=embeddings
    )
    print("✅ 成功添加文档")
except Exception as e:
    print(f"❌ 添加文档失败: {str(e)}")
    traceback.print_exc()
    exit()

# 测试5: 查询
print("\n5. 测试查询")
try:
    query_vec = [random.random() for _ in range(768)]
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

import os
import sys
import traceback

print("=== 直接测试 chromadb ===")
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

# 测试2: 创建客户端
print("\n2. 测试创建 chromadb 客户端")
try:
    client = chromadb.PersistentClient(path="./test_chromadb_dir")
    print("✅ 成功创建客户端")
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

# 测试4: 添加文档
print("\n4. 测试添加文档")
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

# 测试5: 查询
print("\n5. 测试查询")
try:
    results = collection.query(
        query_texts=["测试"],
        n_results=2
    )
    print(f"✅ 查询成功，结果数量: {len(results['documents'][0])}")
except Exception as e:
    print(f"❌ 查询失败: {str(e)}")
    traceback.print_exc()
    exit()

print("\n=== 所有测试通过 ===")

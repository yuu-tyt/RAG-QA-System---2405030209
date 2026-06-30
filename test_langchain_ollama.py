print("=== 测试 langchain-ollama ===")

# 测试1: 导入
print("\n1. 测试导入")
try:
    from langchain_ollama import OllamaLLM
    print("✅ 成功导入 OllamaLLM")
except Exception as e:
    print(f"❌ 导入失败: {str(e)}")
    exit()

# 测试2: 创建 LLM 对象
print("\n2. 测试创建 OllamaLLM 对象")
try:
    llm = OllamaLLM(model="deepseek-r1:7b")
    print("✅ 成功创建 OllamaLLM 对象")
except Exception as e:
    print(f"❌ 创建失败: {str(e)}")
    exit()

# 测试3: 调用 LLM
print("\n3. 测试调用 LLM")
try:
    result = llm.invoke("hello")
    print(f"✅ 调用成功")
    print(f"响应: {result[:50]}...")
except Exception as e:
    print(f"❌ 调用失败: {str(e)}")
    exit()

# 测试4: 测试嵌入模型
print("\n4. 测试嵌入模型")
try:
    from langchain_ollama import OllamaEmbeddings
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    vec = embeddings.embed_query("test")
    print(f"✅ 嵌入模型测试成功")
    print(f"向量长度: {len(vec)}")
except Exception as e:
    print(f"❌ 嵌入模型测试失败: {str(e)}")

print("\n=== 所有测试通过 ===")

import subprocess
import time

print("=== 测试 Ollama 连接 ===")

# 测试1: 检查Ollama是否可用
try:
    result = subprocess.run(
        ["ollama", "list"],
        capture_output=True,
        text=True,
        timeout=30
    )
    print("✅ Ollama 命令行可用")
    print(result.stdout)
except Exception as e:
    print(f"❌ Ollama 命令行不可用: {str(e)}")

# 测试2: 测试Ollama API
import requests
print("\n=== 测试 Ollama API ===")
try:
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "deepseek-r1:7b", "prompt": "hello", "stream": False},
        timeout=60
    )
    if response.status_code == 200:
        data = response.json()
        print("✅ Ollama API 连接成功")
        print(f"响应: {data.get('response', '')[:50]}...")
    else:
        print(f"❌ Ollama API 响应异常: {response.status_code}")
except Exception as e:
    print(f"❌ Ollama API 连接失败: {str(e)}")

# 测试3: 测试嵌入模型
print("\n=== 测试嵌入模型 ===")
try:
    response = requests.post(
        "http://localhost:11434/api/embeddings",
        json={"model": "nomic-embed-text", "prompt": "test text"},
        timeout=60
    )
    if response.status_code == 200:
        data = response.json()
        print("✅ 嵌入模型连接成功")
        print(f"向量长度: {len(data.get('embedding', []))}")
    else:
        print(f"❌ 嵌入模型响应异常: {response.status_code}")
except Exception as e:
    print(f"❌ 嵌入模型连接失败: {str(e)}")

print("\n=== 测试完成 ===")

import requests
import json

def test_ollama_api():
    """
    测试Ollama API是否能正常返回结果
    AI生成：使用Trae辅助编写
    """
    ollama_url = "http://localhost:11434/api/generate"
    
    test_payload = {
        "model": "deepseek-r1:7b",
        "prompt": "你好，请用一句话介绍什么是自然语言处理？",
        "stream": False
    }
    
    print("=" * 50)
    print("Ollama API 测试脚本")
    print("=" * 50)
    print(f"\n正在测试模型: {test_payload['model']}")
    print(f"API地址: {ollama_url}")
    print("\n发送测试请求...\n")
    
    try:
        response = requests.post(ollama_url, json=test_payload, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            print("✓ API连接成功！")
            print("\n模型回复:")
            print("-" * 40)
            print(result.get("response", "无响应内容"))
            print("-" * 40)
            return True
        else:
            print(f"✗ API返回错误状态码: {response.status_code}")
            print(f"错误信息: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("✗ 无法连接到Ollama服务！")
        print("\n请确保:")
        print("1. Ollama已正确安装")
        print("2. Ollama服务正在运行 (在终端执行 'ollama serve')")
        print("3. 已下载所需模型 (执行 'ollama pull deepseek-r1:7b')")
        return False
        
    except requests.exceptions.Timeout:
        print("✗ 请求超时！模型响应时间过长。")
        return False
        
    except Exception as e:
        print(f"✗ 发生未知错误: {str(e)}")
        return False

def test_ollama_models():
    """
    列出本地已安装的Ollama模型
    AI生成：使用Trae辅助编写
    """
    ollama_url = "http://localhost:11434/api/tags"
    
    print("\n" + "=" * 50)
    print("检查本地已安装的模型")
    print("=" * 50)
    
    try:
        response = requests.get(ollama_url, timeout=10)
        if response.status_code == 200:
            models = response.json().get("models", [])
            if models:
                print("\n已安装的模型:")
                for model in models:
                    print(f"  - {model['name']}")
            else:
                print("\n暂无已安装的模型")
                print("请执行 'ollama pull deepseek-r1:7b' 下载模型")
        else:
            print("无法获取模型列表")
    except Exception as e:
        print(f"获取模型列表失败: {str(e)}")

if __name__ == "__main__":
    test_ollama_models()
    test_ollama_api()
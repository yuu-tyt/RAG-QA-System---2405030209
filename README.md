# RAG问答系统

基于本地知识库的智能问答系统，使用Ollama大模型、LangChain框架和ChromaDB向量数据库实现检索增强生成(RAG)功能。

## 项目简介

本项目实现了一个完整的RAG问答系统，支持上传PDF/DOCX文档构建本地知识库，并通过大模型实现智能问答。系统采用Streamlit构建Web界面，支持多轮对话和会话记忆。

## 环境要求

- Python 3.9+
- Ollama (已安装并运行)
- 至少8GB内存（运行7B模型）

## 安装步骤

### 1. 安装Ollama

**Windows:**
1. 访问 [Ollama官网](https://ollama.ai) 下载Windows版本
2. 运行安装程序
3. 打开命令行，下载模型：
```bash
ollama pull deepseek-r1:7b
ollama pull nomic-embed-text
```

**验证安装：**
```bash
ollama list
```

### 2. 创建Python虚拟环境

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

## 使用说明

### 1. 启动Ollama服务

确保Ollama服务正在运行：
```bash
ollama serve
```

### 2. 测试Ollama连接

```bash
python test_ollama.py
```

### 3. 准备文档

在项目目录下创建 `documents` 文件夹，放入PDF或DOCX格式的文档：
```bash
mkdir documents
# 将文档复制到documents文件夹
```

### 4. 运行Web应用

```bash
streamlit run app.py
```

### 5. 使用Web界面

1. **上传文档**：在"文档管理"标签页上传PDF或DOCX文件
2. **构建知识库**：点击"构建知识库"按钮处理文档
3. **提问**：在"问答"标签页输入问题，获取基于知识库的回答
4. **查看历史**：对话历史会自动保存，支持多轮对话

### 命令行版本

```bash
python rag_chain.py
```

## 关键技术点

### RAG流程

1. **文档处理**：使用PyPDF2和python-docx提取PDF和DOCX文档中的文本
2. **文本分块**：使用RecursiveCharacterTextSplitter进行分块（chunk_size=1000, chunk_overlap=200）
3. **向量化**：使用Ollama的nomic-embed-text模型生成文本嵌入
4. **存储检索**：使用ChromaDB存储向量，支持相似度检索
5. **问答生成**：使用LangChain的ConversationalRetrievalChain连接检索器和大模型

### 所用模型

- **大语言模型**：deepseek-r1:7b（可替换为qwen2:7b）
- **嵌入模型**：nomic-embed-text（Ollama内置）

### 系统提示词

```
你是一个专业的问答助手。请基于提供的参考文档回答用户问题。

重要规则：
1. 只使用参考文档中的信息回答问题
2. 如果参考文档中没有相关信息，请明确回答："文档中未找到相关答案"
3. 回答要准确、简洁、有条理
4. 如果引用文档内容，请注明来源
5. 不要编造或推测答案
```

## 项目结构

```
RAG-QA-System/
├── app.py                  # Streamlit Web应用
├── rag_chain.py            # RAG问答链（命令行版本）
├── vector_store.py         # 向量数据库管理
├── document_processor.py   # 文档处理模块
├── test_ollama.py          # Ollama API测试脚本
├── requirements.txt        # 依赖列表
├── README.md               # 项目说明
├── .gitignore              # Git忽略配置
├── documents/              # 文档目录（需自行创建）
└── chroma_db/              # 向量数据库（自动生成）
```

## 打包为EXE

使用PyInstaller打包：

```bash
pyinstaller --onefile --add-data "documents;documents" app.py
```

打包后的exe文件位于 `dist/` 目录。

**注意**：目标电脑需要安装Ollama并下载相应模型。

## 测试问答效果

### 相关问题测试（5个）

| 问题 | 回答质量 |
|------|----------|
| 什么是自然语言处理？ | ✓ 准确回答 |
| NLP有哪些主要应用领域？ | ✓ 准确回答 |
| 什么是词向量？ | ✓ 准确回答 |
| Transformer模型的优势是什么？ | ✓ 准确回答 |
| 如何评价一个NLP模型的性能？ | ✓ 准确回答 |

### 无关问题测试（2个）

| 问题 | 回答质量 |
|------|----------|
| 今天的天气怎么样？ | ✓ 正确回复"文档中未找到相关答案" |
| 如何制作红烧肉？ | ✓ 正确回复"文档中未找到相关答案" |

## 已知问题与改进方向

### 已知问题

1. 大模型首次响应可能较慢（需要加载模型到内存）
2. PDF文档中的表格和图片无法提取
3. 长文档处理可能消耗较多内存

### 改进方向

1. 添加更多文档格式支持（如TXT、Markdown）
2. 实现知识库的增量更新和删除
3. 添加回答的置信度评分
4. 支持多用户和权限管理
5. 优化长文档的处理效率

## AI使用声明

本项目使用Trae AI编程辅助工具进行开发，以下部分由AI辅助生成：
- 文档处理模块（document_processor.py）
- 向量数据库管理（vector_store.py）
- RAG问答链（rag_chain.py）
- Streamlit界面（app.py）
- 测试脚本（test_ollama.py）

AI辅助主要用于：
- 代码骨架生成
- API调用方式参考
- 错误调试和优化建议

## 许可证

MIT License
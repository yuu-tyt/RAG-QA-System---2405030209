# GitHub推送指南

## 前提条件
1. 已安装Git（如果未安装，请从 https://git-scm.com/download/win 下载安装）
2. 已在GitHub创建仓库：RAG-QA-System-田雨涛-2405030209

## 操作步骤

### 1. 打开命令行终端
```bash
cd c:\Users\Administrator\Desktop\作业\zuoye
```

### 2. 初始化Git仓库
```bash
git init
```

### 3. 配置Git用户信息
```bash
git config user.name "田雨涛"
git config user.email "你的邮箱地址"
```

### 4. 添加所有文件到暂存区
```bash
git add .
```

### 5. 提交代码
```bash
git commit -m "Initial commit: RAG问答系统完整代码"
```

### 6. 添加远程仓库（使用访问令牌）
```bash
git remote add origin https://<你的访问令牌>@github.com/你的GitHub用户名/RAG-QA-System-田雨涛-2405030209.git
```

### 7. 推送到远程仓库
```bash
git push -u origin main
```

## 注意事项

1. **将"你的GitHub用户名"替换为你的实际GitHub用户名**
2. **访问令牌保密**：请妥善保管你的访问令牌，不要泄露给他人
3. **如果提示分支名称问题**：
   ```bash
   git branch -M main
   git push -u origin main
   ```

## 验证推送结果
1. 打开浏览器访问：https://github.com/你的GitHub用户名/RAG-QA-System-田雨涛-2405030209
2. 确认所有文件已成功上传

## 完成后需要补充的内容
1. 在仓库的README.md中添加项目截图
2. 确保所有文档都已上传到documents文件夹

## 项目文件清单

以下是需要推送的文件：
- app.py                    # Streamlit Web应用
- rag_chain.py              # RAG问答链（命令行版本）
- vector_store.py           # 向量数据库管理
- document_processor.py     # 文档处理模块
- test_ollama.py            # Ollama API测试脚本
- requirements.txt          # 依赖列表
- build.bat                 # 打包脚本
- .gitignore                # Git忽略配置
- README.md                 # 项目说明文档
- ai_usage_log.md           # AI使用日志
- documents/                # 文档目录（包含测试文档）
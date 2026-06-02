@echo off
echo ========================================
echo RAG问答系统 - 打包脚本
echo ========================================
echo.

echo 检查Python环境...
python --version
if errorlevel 1 (
    echo 错误: 未找到Python，请先安装Python
    pause
    exit /b 1
)

echo.
echo 安装依赖...
pip install -r requirements.txt

echo.
echo 安装PyInstaller...
pip install pyinstaller

echo.
echo 开始打包...
pyinstaller --onefile --name "RAG-QA-System" --add-data "documents;documents" app.py

echo.
echo ========================================
echo 打包完成！
echo 可执行文件位于: dist\RAG-QA-System.exe
echo ========================================
echo.
echo 注意: 运行exe前请确保:
echo 1. 已安装Ollama
echo 2. 已下载deepseek-r1:7b模型
echo 3. 已下载nomic-embed-text模型
echo.

pause
@echo off
:: 【关键修复】切换 CMD 窗口编码为 UTF-8 (65001)，解决中文乱码
chcp 65001 >nul
setlocal
title Ledom Layouter 启动器

:: 设置颜色：背景深蓝，文字淡青
color 1F

echo ======================================================
echo           Ledom Layouter v1.3.0 - 启动中心
echo ======================================================
echo.

:: 1. 检查 Python 环境
echo [1/3] 正在检索 Python 环境...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未检测到 Python，请确保已安装并添加至环境变量。
    pause
    exit /b
)

:: 2. 检查关键依赖库
echo [2/3] 正在校验核心库 (Streamlit, Pandoc)...
python -c "import streamlit, pypandoc, pyperclip" >nul 2>&1
if %errorlevel% neq 0 (
    echo [提示] 检测到缺失库，正在尝试自动安装依赖...
    pip install streamlit pypandoc pyperclip
)

:: 3. 检查 Pandoc 引擎
echo [3/3] 正在确认 Pandoc 转换引擎...
pandoc --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [警告] 未检测到 Pandoc 引擎。
    echo 转换功能将不可用，请访问 https://pandoc.org 安装。
    pause
)

:: 启动程序
echo.
echo ------------------------------------------------------
echo    正在启动 Ledom Layouter 界面...
echo ------------------------------------------------------
echo.

:: 运行 Streamlit
streamlit run app.py

:: 如果程序异常退出，保留窗口查看报错
if %errorlevel% neq 0 (
    echo.
    echo [异常] 程序已意外停止运行。
    pause
)

endlocal
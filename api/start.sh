#!/bin/bash

# 紫微斗数API启动脚本

echo "正在启动紫微斗数API服务..."

# 判断是否使用Docker启动
if [ "$1" == "--docker" ] || [ "$1" == "-d" ]; then
    echo "使用Docker方式启动服务..."
    docker-compose up -d
    echo "Docker服务已启动，访问 http://localhost:8000 查看API"
else
    # 检查Python环境
    if ! command -v python &> /dev/null; then
        echo "错误: 未检测到Python，请安装Python 3.8+"
        exit 1
    fi
    
    # 检查依赖
    if [ ! -f "requirements.txt" ]; then
        echo "错误: 未找到requirements.txt文件"
        exit 1
    fi
    
    # 安装依赖
    echo "正在检查依赖..."
    pip install -r requirements.txt
    
    # 启动服务
    echo "正在启动本地服务..."
    python main.py
fi 
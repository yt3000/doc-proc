#!/bin/bash

# 智能文档校对优化系统 - 启动脚本

echo "======================================"
echo "  智能文档校对优化系统"
echo "======================================"

# 检查 Python 版本
echo "检查 Python 环境..."
python3 --version

# 进入后端目录
cd "$(dirname "$0")"

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
echo "激活虚拟环境..."
source venv/bin/activate

# 安装依赖
echo "安装依赖..."
pip install -r requirements.txt -q

# 启动服务
echo ""
echo "启动后端服务..."
echo "后端地址：http://localhost:8000"
echo "API 文档：http://localhost:8000/docs"
echo ""
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

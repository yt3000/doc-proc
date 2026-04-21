#!/bin/bash

# 智能文档校对优化系统 - 前端启动脚本

echo "======================================"
echo "  智能文档校对优化系统 - 前端"
echo "======================================"

# 进入前端目录
cd "$(dirname "$0")"

# 检查 node_modules
if [ ! -d "node_modules" ]; then
    echo "安装依赖..."
    npm install
fi

# 启动服务
echo ""
echo "启动前端开发服务器..."
echo "前端地址：http://localhost:3000"
echo ""
npm run dev

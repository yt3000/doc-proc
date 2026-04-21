#!/bin/bash

# 智能文档校对优化系统 - 全栈启动脚本

echo "======================================"
echo "  智能文档校对优化系统"
echo "======================================"
echo ""

# 检查终端数量
if [ "$(uname)" = "Darwin" ]; then
    # macOS
    open -a Terminal "$(dirname "$0")/backend/start.sh" &
    sleep 2
    open -a Terminal "$(dirname "$0")/frontend/start.sh"
else
    # Linux
    gnome-terminal -- "$(dirname "$0")/backend/start.sh" &
    sleep 2
    gnome-terminal -- "$(dirname "$0")/frontend/start.sh"
fi

echo ""
echo "正在启动服务..."
echo "后端：http://localhost:8000"
echo "前端：http://localhost:3000"
echo ""
echo "请在两个终端中分别查看服务状态"

#!/bin/bash
# start.sh

echo "启动英语长难句解析系统..."

# 检查 data 目录
mkdir -p backend/data

# 启动后端
cd backend
poetry run uvicorn main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!
echo "后端服务已启动 (PID: $BACKEND_PID)"

# 启动前端
if [ -d "../frontend" ]; then
    cd ../frontend
    npm run dev &
    FRONTEND_PID=$!
    echo "前端服务已启动 (PID: $FRONTEND_PID)"
else
    echo "前端尚未创建，仅启动后端。"
    FRONTEND_PID=""
fi

echo ""
echo "系统已就绪："
echo "  后端 API：http://localhost:8000"
echo "  API 文档：http://localhost:8000/docs"
echo ""
echo "按 Ctrl+C 停止所有服务"

# 等待退出信号
if [ -z "$FRONTEND_PID" ]; then
    trap "kill $BACKEND_PID; exit" INT TERM
    wait $BACKEND_PID
else
    trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT TERM
    wait
fi

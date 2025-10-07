#!/bin/bash

# 科研检测平台 - 快速命令脚本

echo "================================"
echo "科研检测服务平台 - 快速命令"
echo "================================"
echo ""

# 显示菜单
show_menu() {
    echo "请选择操作："
    echo ""
    echo "1. 启动后端服务"
    echo "2. 停止后端服务"
    echo "3. 重启后端服务"
    echo "4. 查看后端日志"
    echo "5. 初始化数据库"
    echo "6. 测试API接口"
    echo "7. 查看项目状态"
    echo "8. 启动前端（HBuilderX）"
    echo "9. 清理临时文件"
    echo "0. 退出"
    echo ""
    read -p "输入选项 [0-9]: " choice
    
    case $choice in
        1) start_backend ;;
        2) stop_backend ;;
        3) restart_backend ;;
        4) view_logs ;;
        5) init_database ;;
        6) test_api ;;
        7) check_status ;;
        8) start_frontend ;;
        9) clean_temp ;;
        0) exit 0 ;;
        *) echo "无效选项"; show_menu ;;
    esac
}

# 启动后端
start_backend() {
    echo "🚀 启动后端服务..."
    cd backend
    
    # 检查是否已运行
    if [ -f "server.pid" ]; then
        PID=$(cat server.pid)
        if ps -p $PID > /dev/null; then
            echo "⚠️  后端已在运行 (PID: $PID)"
            return
        fi
    fi
    
    # 启动服务
    nohup uvicorn app.main:app --reload > server.log 2>&1 &
    echo $! > server.pid
    sleep 2
    
    if ps -p $(cat server.pid) > /dev/null; then
        echo "✅ 后端启动成功！"
        echo "   PID: $(cat server.pid)"
        echo "   地址: http://localhost:8000"
        echo "   文档: http://localhost:8000/api/docs"
    else
        echo "❌ 后端启动失败，请查看日志: backend/server.log"
    fi
    
    cd ..
    read -p "按回车继续..."
    show_menu
}

# 停止后端
stop_backend() {
    echo "🛑 停止后端服务..."
    cd backend
    
    if [ -f "server.pid" ]; then
        PID=$(cat server.pid)
        kill $PID 2>/dev/null
        rm server.pid
        echo "✅ 后端已停止"
    else
        echo "⚠️  后端未运行"
    fi
    
    cd ..
    read -p "按回车继续..."
    show_menu
}

# 重启后端
restart_backend() {
    stop_backend
    sleep 1
    start_backend
}

# 查看日志
view_logs() {
    echo "📋 查看后端日志（Ctrl+C 退出）..."
    echo ""
    tail -f backend/server.log
}

# 初始化数据库
init_database() {
    echo "🗄️  初始化数据库..."
    cd backend
    python init_db.py
    echo ""
    read -p "按回车继续..."
    cd ..
    show_menu
}

# 测试API
test_api() {
    echo "🧪 测试API接口..."
    echo ""
    
    echo "1. 测试健康检查..."
    curl -s http://localhost:8000/health | python3 -m json.tool
    echo ""
    
    echo "2. 测试项目分类..."
    curl -s http://localhost:8000/api/v1/projects/categories | python3 -m json.tool | head -20
    echo ""
    
    read -p "按回车继续..."
    show_menu
}

# 查看状态
check_status() {
    echo "📊 项目状态检查..."
    echo ""
    
    echo "后端服务："
    if [ -f "backend/server.pid" ]; then
        PID=$(cat backend/server.pid)
        if ps -p $PID > /dev/null; then
            echo "  ✅ 运行中 (PID: $PID)"
        else
            echo "  ❌ 未运行"
        fi
    else
        echo "  ❌ 未运行"
    fi
    
    echo ""
    echo "MySQL："
    if brew services list | grep mysql | grep started > /dev/null; then
        echo "  ✅ 运行中"
    else
        echo "  ❌ 未运行"
    fi
    
    echo ""
    echo "Redis："
    if brew services list | grep redis | grep started > /dev/null; then
        echo "  ✅ 运行中"
    else
        echo "  ⚠️  未运行（可选）"
    fi
    
    echo ""
    echo "项目文件："
    echo "  后端代码: $(find backend -name '*.py' | wc -l) 个文件"
    echo "  前端代码: $(find frontend -name '*.vue' | wc -l) 个Vue文件"
    echo "  文档: $(find . -maxdepth 1 -name '*.md' | wc -l) 个文档"
    
    echo ""
    read -p "按回车继续..."
    show_menu
}

# 启动前端
start_frontend() {
    echo "🎨 启动前端..."
    echo ""
    echo "请使用 HBuilderX 打开 frontend 目录"
    echo "然后: 运行 → 运行到浏览器 → Chrome"
    echo ""
    echo "或者使用命令行（如果已安装cli）："
    echo "  cd frontend"
    echo "  npm run dev:h5"
    echo ""
    read -p "按回车继续..."
    show_menu
}

# 清理临时文件
clean_temp() {
    echo "🧹 清理临时文件..."
    
    find . -name "*.pyc" -delete
    find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null
    find . -name ".DS_Store" -delete
    
    echo "✅ 清理完成"
    read -p "按回车继续..."
    show_menu
}

# 启动
show_menu

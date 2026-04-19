#!/bin/bash

echo "=========================================="
echo "🧪 项目测试运行脚本"
echo "=========================================="
echo ""

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 优先使用项目虚拟环境，避免误用系统 Python
BACKEND_PYTHON="python3"
if [ -x "backend/venv/bin/python" ]; then
    BACKEND_PYTHON="$(cd backend && pwd)/venv/bin/python"
elif [ -x "backend/venv/bin/python3" ]; then
    BACKEND_PYTHON="$(cd backend && pwd)/venv/bin/python3"
fi

BACKEND_HOST="127.0.0.1"
DEFAULT_BACKEND_PORT="8000"

get_effective_database_url() {
    local env_file="backend/.env"
    if [ -f "$env_file" ]; then
        local url
        url=$(grep '^DATABASE_URL=' "$env_file" | cut -d= -f2-)
        if [ -n "$url" ]; then
            printf '%s' "${url/@localhost:/@127.0.0.1:}"
            return 0
        fi
    fi
    return 1
}

is_backend_healthy() {
    local port=$1
    local health_code
    local root_response
    health_code=$(curl --noproxy '*' -s -o /dev/null -w "%{http_code}" "http://$BACKEND_HOST:$port/health" 2>/dev/null)
    if [ "$health_code" != "200" ]; then
        return 1
    fi
    root_response=$(curl --noproxy '*' -s "http://$BACKEND_HOST:$port/" 2>/dev/null)
    echo "$root_response" | grep -q '"status":"running"'
}

# 检查后端服务是否运行
check_backend() {
    echo "1️⃣ 检查后端服务状态..."
    
    # 检查常见端口
    PORTS=(3000 3001 8000)
    BACKEND_RUNNING=false
    BACKEND_PORT=""
    
    for port in "${PORTS[@]}"; do
        if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1 && is_backend_healthy "$port"; then
            BACKEND_RUNNING=true
            BACKEND_PORT=$port
            echo -e "   ${GREEN}✅ 后端服务正在运行 (端口: $port)${NC}"
            break
        fi
    done
    
    if [ "$BACKEND_RUNNING" = false ]; then
        echo -e "   ${YELLOW}⚠️  后端服务未运行${NC}"
        echo "   尝试启动后端服务..."
        
        cd backend
        
        # 检查是否有PID文件
        if [ -f "server.pid" ]; then
            PID=$(cat server.pid)
            if ! ps -p $PID > /dev/null 2>&1; then
                rm server.pid
            fi
        fi
        
        # 启动服务（后台运行）
        echo "   正在启动后端服务..."
        EFFECTIVE_DATABASE_URL=$(get_effective_database_url || true)
        if [ -n "$EFFECTIVE_DATABASE_URL" ]; then
            nohup env DATABASE_URL="$EFFECTIVE_DATABASE_URL" "$BACKEND_PYTHON" -m uvicorn app.main:app --host "$BACKEND_HOST" --port "$DEFAULT_BACKEND_PORT" > server.log 2>&1 &
        else
            nohup "$BACKEND_PYTHON" -m uvicorn app.main:app --host "$BACKEND_HOST" --port "$DEFAULT_BACKEND_PORT" > server.log 2>&1 &
        fi
        echo $! > server.pid
        
        # 等待服务启动
        sleep 3
        
        # 检查是否启动成功
        if ps -p $(cat server.pid) > /dev/null 2>&1; then
            # 等待服务完全启动
            sleep 2
            if is_backend_healthy "$DEFAULT_BACKEND_PORT"; then
                echo -e "   ${GREEN}✅ 后端服务启动成功${NC}"
                BACKEND_RUNNING=true
                BACKEND_PORT=$DEFAULT_BACKEND_PORT
            else
                echo -e "   ${RED}❌ 后端服务进程已启动，但健康检查未通过${NC}"
                echo "   请查看日志: backend/server.log"
                cd ..
                return 1
            fi
        else
            echo -e "   ${RED}❌ 后端服务启动失败${NC}"
            echo "   请查看日志: backend/server.log"
            cd ..
            return 1
        fi
        
        cd ..
    fi
    
    if [ -z "$BACKEND_PORT" ]; then
        BACKEND_PORT=$DEFAULT_BACKEND_PORT
    fi
    
    BASE_URL="http://$BACKEND_HOST:$BACKEND_PORT"
    echo "   服务地址: $BASE_URL"
    echo ""
    
    return 0
}

# 测试API接口
test_api() {
    local base_url=$1
    echo "2️⃣ 测试API接口..."
    echo ""
    
    # 测试健康检查
    echo "   📍 测试健康检查接口..."
    HEALTH=$(curl --noproxy '*' -s -w "\nHTTP_CODE:%{http_code}" "$base_url/health" 2>/dev/null)
    HTTP_CODE=$(echo "$HEALTH" | grep "HTTP_CODE" | cut -d: -f2)
    RESPONSE=$(echo "$HEALTH" | sed '/HTTP_CODE/d')
    
    if [ "$HTTP_CODE" = "200" ]; then
        echo -e "   ${GREEN}✅ 健康检查通过${NC}"
        echo "   响应: $RESPONSE" | head -3
    else
        echo -e "   ${RED}❌ 健康检查失败 (HTTP $HTTP_CODE)${NC}"
    fi
    echo ""
    
    # 测试根路由
    echo "   📍 测试根路由..."
    ROOT=$(curl --noproxy '*' -s -w "\nHTTP_CODE:%{http_code}" "$base_url/" 2>/dev/null)
    HTTP_CODE=$(echo "$ROOT" | grep "HTTP_CODE" | cut -d: -f2)
    RESPONSE=$(echo "$ROOT" | sed '/HTTP_CODE/d')
    
    if [ "$HTTP_CODE" = "200" ]; then
        echo -e "   ${GREEN}✅ 根路由正常${NC}"
        echo "   响应: $RESPONSE" | head -3
    else
        echo -e "   ${RED}❌ 根路由失败 (HTTP $HTTP_CODE)${NC}"
    fi
    echo ""
    
    # 测试项目分类
    echo "   📍 测试项目分类接口..."
    CATEGORIES=$(curl --noproxy '*' -s -w "\nHTTP_CODE:%{http_code}" "$base_url/api/v1/projects/categories" 2>/dev/null)
    HTTP_CODE=$(echo "$CATEGORIES" | grep "HTTP_CODE" | cut -d: -f2)
    RESPONSE=$(echo "$CATEGORIES" | sed '/HTTP_CODE/d')
    
    if [ "$HTTP_CODE" = "200" ]; then
        echo -e "   ${GREEN}✅ 项目分类接口正常${NC}"
        echo "   响应: $RESPONSE" | head -5
    else
        echo -e "   ${YELLOW}⚠️  项目分类接口返回 HTTP $HTTP_CODE${NC}"
    fi
    echo ""
    
    # 测试项目列表
    echo "   📍 测试项目列表接口..."
    PROJECTS=$(curl --noproxy '*' -s -w "\nHTTP_CODE:%{http_code}" "$base_url/api/v1/projects/list?page=1&page_size=2" 2>/dev/null)
    HTTP_CODE=$(echo "$PROJECTS" | grep "HTTP_CODE" | cut -d: -f2)
    RESPONSE=$(echo "$PROJECTS" | sed '/HTTP_CODE/d')
    
    if [ "$HTTP_CODE" = "200" ]; then
        echo -e "   ${GREEN}✅ 项目列表接口正常${NC}"
        echo "   响应: $RESPONSE" | head -5
    else
        echo -e "   ${YELLOW}⚠️  项目列表接口返回 HTTP $HTTP_CODE${NC}"
    fi
    echo ""
}

# 检查前端
check_frontend() {
    echo "3️⃣ 检查前端项目..."
    echo ""
    
    if [ -d "frontend" ]; then
        echo -e "   ${GREEN}✅ 前端目录存在${NC}"
        
        # 检查package.json
        if [ -f "frontend/package.json" ]; then
            echo -e "   ${GREEN}✅ package.json 存在${NC}"
        else
            echo -e "   ${RED}❌ package.json 不存在${NC}"
        fi
        
        # 检查node_modules
        if [ -d "frontend/node_modules" ]; then
            echo -e "   ${GREEN}✅ 依赖已安装${NC}"
        else
            echo -e "   ${YELLOW}⚠️  依赖未安装，运行: cd frontend && npm install${NC}"
        fi
    else
        echo -e "   ${RED}❌ 前端目录不存在${NC}"
    fi
    echo ""
}

# 显示访问信息
show_info() {
    local base_url=$1
    echo "=========================================="
    echo "📊 测试结果总结"
    echo "=========================================="
    echo ""
    echo "🌐 后端服务:"
    echo "   地址: $base_url"
    echo "   API文档: $base_url/api/docs"
    echo "   健康检查: $base_url/health"
    echo ""
    echo "📱 前端项目:"
    echo "   目录: frontend/"
    echo "   启动命令: cd frontend && npm run dev:h5"
    echo ""
    echo "📝 提示:"
    echo "   - 如果后端未运行，可以使用: ./快速命令.sh"
    echo "   - 查看后端日志: tail -f backend/server.log"
    echo "   - 停止后端服务: kill \$(cat backend/server.pid)"
    echo ""
}

# 主流程
main() {
    # 检查后端
    if check_backend; then
        test_api "$BASE_URL"
    else
        echo -e "${RED}❌ 后端服务检查失败，跳过API测试${NC}"
        echo ""
    fi
    
    # 检查前端
    check_frontend
    
    # 显示信息
    if [ -n "$BASE_URL" ]; then
        show_info "$BASE_URL"
    fi
}

# 运行主流程
main

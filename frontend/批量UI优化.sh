#!/bin/bash

echo "�� 开始批量UI优化..."
echo ""

# 定义颜色替换映射
declare -A COLOR_MAP=(
    ["linear-gradient(135deg, #667eea 0%, #764ba2 100%)"]="#1890ff"
    ["linear-gradient(135deg,#667eea,#764ba2)"]="#1890ff"
    ["linear-gradient(90deg, #667eea 0%, #764ba2 100%)"]="#1890ff"
    ["linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)"]="#1890ff"
    ["linear-gradient(135deg,#4facfe,#00f2fe)"]="#1890ff"
    ["linear-gradient(180deg, #4facfe 0%, #00f2fe 30%, #f5f5f5 30%)"]="#1890ff"
    ["linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%)"]="#faad14"
    ["linear-gradient(135deg,#ff9a9e,#fecfef)"]="#faad14"
    ["linear-gradient(135deg, #f093fb 0%, #f5576c 100%)"]="#ff4d4f"
    ["linear-gradient(135deg,#f093fb,#f5576c)"]="#ff4d4f"
    ["linear-gradient(135deg, #ffb86c 0%, #ff7e5f 100%)"]="#faad14"
    ["linear-gradient(135deg,#ffb86c,#ff7e5f)"]="#faad14"
    ["linear-gradient(135deg, #6ec1ff 0%, #4dabf7 100%)"]="#1890ff"
    ["linear-gradient(135deg,#6ec1ff,#4dabf7)"]="#1890ff"
    ["linear-gradient(135deg, #4dabf7 0%, #1890ff 100%)"]="#1890ff"
    ["linear-gradient(135deg, #1aad19 0%, #2cc562 100%)"]="#52c41a"
)

echo "已定义 ${#COLOR_MAP[@]} 个颜色替换规则"
echo ""

# 统计文件数量
total_files=$(find pages pagesA -name "*.vue" -type f | wc -l | tr -d ' ')
echo "共找到 $total_files 个Vue文件需要处理"
echo ""


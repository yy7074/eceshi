#!/bin/bash

# 数据库设置脚本
# 用于创建数据库和用户，解决连接问题

echo "🔧 开始设置数据库..."

# MySQL 配置
MYSQL_USER="root"
MYSQL_PASSWORD="123456"
DB_NAME="eceshi"

# 检查 MySQL 是否运行
echo "📋 检查 MySQL 服务状态..."
if ! mysql -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" -e "SELECT 1;" &> /dev/null; then
    echo "❌ MySQL 连接失败！"
    echo "请检查："
    echo "1. MySQL 服务是否启动：sudo mysql.server start"
    echo "2. MySQL root 密码是否正确"
    echo "3. MySQL 版本：mysql --version"
    exit 1
fi

echo "✅ MySQL 连接成功！"

# 创建数据库
echo "📦 创建数据库 $DB_NAME..."
mysql -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" << EOF
CREATE DATABASE IF NOT EXISTS $DB_NAME 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;
EOF

if [ $? -eq 0 ]; then
    echo "✅ 数据库 $DB_NAME 创建成功！"
else
    echo "❌ 数据库创建失败！"
    exit 1
fi

# 显示数据库信息
echo ""
echo "📊 数据库信息："
mysql -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" -e "
SHOW DATABASES LIKE '$DB_NAME';
SELECT DEFAULT_CHARACTER_SET_NAME, DEFAULT_COLLATION_NAME 
FROM information_schema.SCHEMATA 
WHERE SCHEMA_NAME = '$DB_NAME';
"

echo ""
echo "🎉 数据库设置完成！"
echo ""
echo "💡 下一步："
echo "1. 确保 backend/.env 文件中的数据库配置正确"
echo "2. 运行测试数据脚本：python3 backend/insert_admin_test_data.py"

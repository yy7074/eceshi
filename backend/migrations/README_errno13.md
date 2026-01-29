# 启动报错 errno 13（Can't create table）处理

## 原因

`(errno: 13)` 表示 **MySQL 数据目录权限不足**：MySQL 进程无法在数据目录下创建新表文件（如 `lab_applications`）。

## 方案一：修复 MySQL 数据目录权限（推荐）

在服务器上执行，将数据目录属主改为 MySQL 运行用户：

**宝塔环境：**
```bash
# 查看数据目录（一般为 /www/server/data）
mysql -e "SELECT @@datadir;"
# 修改属主
chown -R mysql:mysql /www/server/data
# 重启 MySQL（宝塔面板 → 软件商店 → MySQL → 重启）
```

**非宝塔：**
```bash
chown -R mysql:mysql /var/lib/mysql
systemctl restart mysql
```

然后重启后端应用。

## 方案二：用 root 手动创建缺失表

若暂时不能改数据目录权限，可用 root 执行迁移 SQL 创建表，应用启动时不再尝试创建该表（已做容错，表已存在不会报错）：

```bash
cd /www/wwwroot/ceshi/backend
mysql -u root -p123456 eceshi < migrations/create_lab_applications.sql
```

然后重启后端（宝塔 Python 项目管理器里点「重启」）。

## 当前应用行为

- 若创建表时出现 errno 13，应用会**继续启动**并打印上述提示，不会退出。
- 若你已用方案一或方案二创建好表，下次重启时 `create_all` 会跳过已存在的表，或由迁移预先建表，均可正常使用。

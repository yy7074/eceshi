-- 为 users 表添加 is_admin 列（解决后台登录报错 Unknown column 'users.is_admin'）
-- 执行: mysql -u root -p123456 eceshi < migrations/add_users_is_admin.sql
-- 若列已存在会报 Duplicate column，可忽略。

ALTER TABLE users ADD COLUMN is_admin TINYINT(1) DEFAULT 0 COMMENT '是否管理员';

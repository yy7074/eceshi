-- 为 orders 表添加 is_draft 列（解决后台订单列表报错 Unknown column 'orders.is_draft'）
-- 执行: mysql -u root -p123456 eceshi < migrations/add_orders_is_draft.sql

ALTER TABLE orders ADD COLUMN is_draft TINYINT(1) DEFAULT 0 COMMENT '是否为草稿';

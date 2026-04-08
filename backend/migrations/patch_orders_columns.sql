-- 为 orders 表补齐可能缺失的列（与 app/models/order.py 一致）
-- 执行: mysql -u root -p123456 eceshi --force < migrations/patch_orders_columns.sql
-- 使用 --force 时，已存在的列会报 Duplicate column 但会继续执行，未存在的列会被添加

ALTER TABLE orders ADD COLUMN is_draft TINYINT(1) DEFAULT 0 COMMENT '是否为草稿';
ALTER TABLE orders ADD COLUMN invoice_status VARCHAR(20) DEFAULT 'none' COMMENT '开票状态';
ALTER TABLE orders ADD COLUMN invoice_id BIGINT COMMENT '关联发票ID';
ALTER TABLE orders ADD COLUMN payment_status VARCHAR(20) DEFAULT 'unpaid' COMMENT '支付状态';
ALTER TABLE orders ADD COLUMN credit_amount DECIMAL(10,2) DEFAULT 0 COMMENT '信用支付金额';
ALTER TABLE orders ADD COLUMN assigned_lab_id BIGINT COMMENT '指派实验室ID';
ALTER TABLE orders ADD COLUMN assigned_user_id BIGINT COMMENT '指派操作员ID';
ALTER TABLE orders ADD COLUMN assigned_at DATETIME COMMENT '指派时间';
ALTER TABLE orders ADD COLUMN assigned_staff_id BIGINT COMMENT '指派实验人员ID';
ALTER TABLE orders ADD COLUMN assigned_staff_name VARCHAR(50) COMMENT '指派实验人员姓名';
ALTER TABLE orders ADD COLUMN project_fee DECIMAL(10,2) DEFAULT 0 COMMENT '项目费用';
ALTER TABLE orders ADD COLUMN urgent_fee DECIMAL(10,2) DEFAULT 0 COMMENT '加急费用';
ALTER TABLE orders ADD COLUMN shipping_fee DECIMAL(10,2) DEFAULT 0 COMMENT '运费';
ALTER TABLE orders ADD COLUMN discount_amount DECIMAL(10,2) DEFAULT 0 COMMENT '优惠金额';
ALTER TABLE orders ADD COLUMN total_fee DECIMAL(10,2) DEFAULT 0 COMMENT '总金额';
ALTER TABLE orders ADD COLUMN paid_fee DECIMAL(10,2) DEFAULT 0 COMMENT '已支付金额';
ALTER TABLE orders ADD COLUMN sample_count INT DEFAULT 1 COMMENT '样品数量';
ALTER TABLE orders ADD COLUMN shipping_method VARCHAR(20) COMMENT '配送方式';
ALTER TABLE orders ADD COLUMN receiver_name VARCHAR(50) COMMENT '收件人';
ALTER TABLE orders ADD COLUMN receiver_phone VARCHAR(20) COMMENT '收件人电话';
ALTER TABLE orders ADD COLUMN receiver_address VARCHAR(500) COMMENT '收件地址';
ALTER TABLE orders ADD COLUMN payment_method VARCHAR(20) COMMENT '支付方式';
ALTER TABLE orders ADD COLUMN payment_time DATETIME COMMENT '支付时间';
ALTER TABLE orders ADD COLUMN created_at DATETIME COMMENT '创建时间';
ALTER TABLE orders ADD COLUMN paid_at DATETIME COMMENT '支付时间';
ALTER TABLE orders ADD COLUMN confirmed_at DATETIME COMMENT '确认时间';
ALTER TABLE orders ADD COLUMN started_at DATETIME COMMENT '开始实验时间';
ALTER TABLE orders ADD COLUMN completed_at DATETIME COMMENT '完成时间';
ALTER TABLE orders ADD COLUMN cancelled_at DATETIME COMMENT '取消时间';
ALTER TABLE orders ADD COLUMN remark TEXT COMMENT '用户备注';
ALTER TABLE orders ADD COLUMN admin_test_requirements TEXT COMMENT '后台修改后的测试条件/要求';
ALTER TABLE orders ADD COLUMN admin_notes_to_lab TEXT COMMENT '后台给实验室的备注事项';
ALTER TABLE orders ADD COLUMN cancel_reason VARCHAR(200) COMMENT '取消原因';
ALTER TABLE orders ADD COLUMN is_urgent TINYINT(1) DEFAULT 0 COMMENT '是否加急';
ALTER TABLE orders ADD COLUMN estimated_completion_time DATETIME COMMENT '预计完成时间';

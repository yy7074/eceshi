-- 创建充值记录表
CREATE TABLE IF NOT EXISTS recharge_records (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '充值记录ID',
    user_id INT NOT NULL COMMENT '用户ID',
    recharge_no VARCHAR(64) UNIQUE NOT NULL COMMENT '充值单号',
    amount DECIMAL(10, 2) NOT NULL COMMENT '充值金额',
    actual_amount DECIMAL(10, 2) COMMENT '实际到账金额',
    bonus_amount DECIMAL(10, 2) DEFAULT 0 COMMENT '赠送金额',
    payment_method ENUM('wechat', 'alipay') NOT NULL COMMENT '支付方式',
    payment_no VARCHAR(64) COMMENT '支付单号',
    transaction_id VARCHAR(128) COMMENT '第三方交易号',
    status ENUM('pending', 'success', 'failed', 'refunded') DEFAULT 'pending' COMMENT '充值状态',
    remark VARCHAR(255) COMMENT '备注',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    paid_at TIMESTAMP NULL COMMENT '支付时间',
    completed_at TIMESTAMP NULL COMMENT '完成时间',
    INDEX idx_user_id (user_id),
    INDEX idx_recharge_no (recharge_no),
    INDEX idx_status (status),
    INDEX idx_created_at (created_at),
    INDEX idx_user_status (user_id, status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='充值记录表';

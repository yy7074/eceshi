-- 创建优惠券相关表

-- 优惠券模板表
CREATE TABLE IF NOT EXISTS `coupons` (
  `id` INT NOT NULL AUTO_INCREMENT COMMENT '优惠券ID',
  `name` VARCHAR(100) NOT NULL COMMENT '优惠券名称',
  `description` TEXT COMMENT '优惠券描述',
  `type` ENUM('discount', 'cash', 'full_reduction') NOT NULL COMMENT '优惠券类型',
  `discount_rate` DECIMAL(5,2) COMMENT '折扣率（如0.9表示9折）',
  `cash_amount` DECIMAL(10,2) COMMENT '代金券金额',
  `full_amount` DECIMAL(10,2) COMMENT '满减门槛金额',
  `reduction_amount` DECIMAL(10,2) COMMENT '满减优惠金额',
  `min_order_amount` DECIMAL(10,2) DEFAULT 0 COMMENT '最低订单金额',
  `max_discount_amount` DECIMAL(10,2) COMMENT '最大优惠金额',
  `total_quantity` INT DEFAULT 0 COMMENT '发行总量（0表示不限量）',
  `received_quantity` INT DEFAULT 0 COMMENT '已领取数量',
  `valid_days` INT DEFAULT 30 COMMENT '有效天数',
  `applicable_projects` TEXT COMMENT '适用项目ID列表（JSON格式）',
  `applicable_categories` TEXT COMMENT '适用分类ID列表（JSON格式）',
  `status` ENUM('active', 'inactive', 'expired') DEFAULT 'active' COMMENT '优惠券状态',
  `start_time` DATETIME COMMENT '开始时间',
  `end_time` DATETIME COMMENT '结束时间',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_status` (`status`),
  KEY `idx_time` (`start_time`, `end_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='优惠券模板表';

-- 用户优惠券表
CREATE TABLE IF NOT EXISTS `user_coupons` (
  `id` INT NOT NULL AUTO_INCREMENT COMMENT '用户优惠券ID',
  `user_id` INT NOT NULL COMMENT '用户ID',
  `coupon_id` INT NOT NULL COMMENT '优惠券ID',
  `coupon_name` VARCHAR(100) COMMENT '优惠券名称',
  `coupon_type` VARCHAR(20) COMMENT '优惠券类型',
  `discount_value` DECIMAL(10,2) COMMENT '优惠值',
  `status` ENUM('unused', 'used', 'expired') DEFAULT 'unused' COMMENT '使用状态',
  `order_id` INT COMMENT '使用的订单ID',
  `used_at` DATETIME COMMENT '使用时间',
  `received_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '领取时间',
  `expire_at` DATETIME NOT NULL COMMENT '过期时间',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_coupon_id` (`coupon_id`),
  KEY `idx_status` (`status`),
  KEY `idx_expire` (`expire_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户优惠券表';

-- 插入示例优惠券
INSERT INTO `coupons` (`name`, `description`, `type`, `cash_amount`, `min_order_amount`, `total_quantity`, `valid_days`, `status`) 
VALUES 
('新人专享券', '新用户注册即可领取50元代金券', 'cash', 50.00, 100.00, 1000, 30, 'active'),
('满200减30', '订单满200元可使用', 'full_reduction', NULL, 200.00, 500, 15, 'active'),
('9折优惠券', '全场项目9折优惠', 'discount', 0.90, 50.00, 200, 7, 'active');

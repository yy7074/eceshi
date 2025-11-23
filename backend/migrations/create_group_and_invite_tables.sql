-- 创建团队和邀请返利相关表

-- 1. 用户团队表
CREATE TABLE IF NOT EXISTS `user_groups` (
  `id` INT NOT NULL AUTO_INCREMENT COMMENT '团队ID',
  `name` VARCHAR(100) NOT NULL COMMENT '团队名称',
  `avatar` VARCHAR(255) COMMENT '团队头像',
  `description` TEXT COMMENT '团队描述',
  `owner_id` INT NOT NULL COMMENT '负责人用户ID',
  `owner_name` VARCHAR(50) COMMENT '负责人姓名',
  `owner_phone` VARCHAR(20) COMMENT '负责人手机号',
  `university` VARCHAR(100) COMMENT '所属高校',
  `department` VARCHAR(100) COMMENT '所属院系',
  `invite_code` VARCHAR(20) UNIQUE COMMENT '邀请码',
  `member_count` INT DEFAULT 1 COMMENT '成员数量',
  `total_orders` INT DEFAULT 0 COMMENT '累计订单数',
  `total_spent` DECIMAL(10,2) DEFAULT 0 COMMENT '累计消费金额',
  `status` ENUM('active', 'inactive', 'disbanded') DEFAULT 'active' COMMENT '团队状态',
  `is_certified` TINYINT(1) DEFAULT 0 COMMENT '是否认证',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_owner_id` (`owner_id`),
  KEY `idx_invite_code` (`invite_code`),
  KEY `idx_owner_phone` (`owner_phone`),
  KEY `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户团队表';

-- 2. 团队成员表
CREATE TABLE IF NOT EXISTS `group_members` (
  `id` INT NOT NULL AUTO_INCREMENT COMMENT '成员ID',
  `group_id` INT NOT NULL COMMENT '团队ID',
  `user_id` INT NOT NULL COMMENT '用户ID',
  `nickname` VARCHAR(50) COMMENT '昵称',
  `avatar` VARCHAR(255) COMMENT '头像',
  `phone` VARCHAR(20) COMMENT '手机号',
  `role` ENUM('owner', 'admin', 'member') DEFAULT 'member' COMMENT '团队角色',
  `order_count` INT DEFAULT 0 COMMENT '订单数量',
  `total_spent` DECIMAL(10,2) DEFAULT 0 COMMENT '消费金额',
  `joined_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '加入时间',
  PRIMARY KEY (`id`),
  KEY `idx_group_id` (`group_id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_role` (`role`),
  UNIQUE KEY `uk_group_user` (`group_id`, `user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='团队成员表';

-- 3. 邀请记录表
CREATE TABLE IF NOT EXISTS `invite_records` (
  `id` INT NOT NULL AUTO_INCREMENT COMMENT '邀请记录ID',
  `inviter_id` INT NOT NULL COMMENT '邀请人用户ID',
  `invitee_id` INT NOT NULL COMMENT '被邀请人用户ID',
  `inviter_name` VARCHAR(50) COMMENT '邀请人昵称',
  `inviter_phone` VARCHAR(20) COMMENT '邀请人手机号',
  `invitee_name` VARCHAR(50) COMMENT '被邀请人昵称',
  `invitee_phone` VARCHAR(20) COMMENT '被邀请人手机号',
  `reward_amount` DECIMAL(10,2) DEFAULT 0 COMMENT '奖励金额',
  `reward_type` VARCHAR(20) DEFAULT 'balance' COMMENT '奖励类型：balance/points',
  `status` ENUM('pending', 'completed', 'withdrawn') DEFAULT 'pending' COMMENT '邀请状态',
  `first_order_id` INT COMMENT '被邀请人首单ID',
  `first_order_amount` DECIMAL(10,2) COMMENT '首单金额',
  `completed_at` DATETIME COMMENT '完成时间',
  `invited_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '邀请时间',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_inviter_id` (`inviter_id`),
  KEY `idx_invitee_id` (`invitee_id`),
  KEY `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='邀请记录表';

-- 4. 提现记录表
CREATE TABLE IF NOT EXISTS `withdraw_records` (
  `id` INT NOT NULL AUTO_INCREMENT COMMENT '提现记录ID',
  `user_id` INT NOT NULL COMMENT '用户ID',
  `amount` DECIMAL(10,2) NOT NULL COMMENT '提现金额',
  `withdraw_type` VARCHAR(20) DEFAULT 'invite_reward' COMMENT '提现类型',
  `account_type` VARCHAR(20) COMMENT '账户类型：alipay/wechat/bank',
  `account_name` VARCHAR(50) COMMENT '账户名',
  `account_number` VARCHAR(100) COMMENT '账户号码',
  `status` ENUM('pending', 'approved', 'rejected', 'completed') DEFAULT 'pending' COMMENT '提现状态',
  `reject_reason` TEXT COMMENT '拒绝原因',
  `reviewer_id` INT COMMENT '审核人ID',
  `reviewed_at` DATETIME COMMENT '审核时间',
  `transaction_no` VARCHAR(100) COMMENT '交易单号',
  `completed_at` DATETIME COMMENT '完成时间',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='提现记录表';

-- 5. 邀请配置表
CREATE TABLE IF NOT EXISTS `invite_config` (
  `id` INT NOT NULL AUTO_INCREMENT COMMENT '配置ID',
  `inviter_reward` DECIMAL(10,2) DEFAULT 10.00 COMMENT '邀请人奖励金额',
  `invitee_reward` DECIMAL(10,2) DEFAULT 5.00 COMMENT '被邀请人奖励金额',
  `reward_type` VARCHAR(20) DEFAULT 'balance' COMMENT '奖励类型',
  `min_order_amount` DECIMAL(10,2) DEFAULT 0 COMMENT '最低订单金额要求',
  `reward_delay_days` INT DEFAULT 0 COMMENT '奖励延迟天数',
  `min_withdraw_amount` DECIMAL(10,2) DEFAULT 10.00 COMMENT '最低提现金额',
  `withdraw_fee_rate` DECIMAL(5,4) DEFAULT 0 COMMENT '提现手续费率',
  `is_active` TINYINT(1) DEFAULT 1 COMMENT '是否启用',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='邀请配置表';

-- 插入默认配置
INSERT INTO `invite_config` (`inviter_reward`, `invitee_reward`, `reward_type`, `min_order_amount`, `min_withdraw_amount`, `is_active`) 
VALUES (10.00, 5.00, 'balance', 50.00, 10.00, 1);

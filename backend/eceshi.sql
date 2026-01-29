/*
 Navicat Premium Data Transfer
 已适配 MySQL 5.7（COLLATE 使用 utf8mb4_general_ci）

 Source Server         : local
 Source Server Type    : MySQL
 Source Schema         : eceshi

 Target Server Type    : MySQL
 Target Server Version : 50700 (5.7.x)
 File Encoding         : 65001
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for announcements
-- ----------------------------
DROP TABLE IF EXISTS `announcements`;
CREATE TABLE `announcements` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(200) NOT NULL COMMENT '标题',
  `content` text NOT NULL COMMENT '内容',
  `summary` varchar(500) DEFAULT NULL COMMENT '摘要',
  `category` varchar(50) DEFAULT 'system' COMMENT '分类',
  `is_top` tinyint(1) DEFAULT '0' COMMENT '是否置顶',
  `is_active` tinyint(1) DEFAULT '1' COMMENT '是否启用',
  `view_count` int DEFAULT '0' COMMENT '查看次数',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_category_active` (`category`,`is_active`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='公告';

-- ----------------------------
-- Records of announcements
-- ----------------------------
BEGIN;
INSERT INTO `announcements` (`id`, `title`, `content`, `summary`, `category`, `is_top`, `is_active`, `view_count`, `created_at`, `updated_at`) VALUES (1, '系统升级通知', '为了提供更好的服务体验，我们将于本周六凌晨2:00-6:00进行系统升级维护，届时部分功能可能暂时无法使用，请提前做好安排。给您带来的不便，敬请谅解！', '系统将于本周六凌晨进行升级维护', 'system', 1, 1, 0, '2025-12-07 11:55:39', '2025-12-07 11:55:39');
INSERT INTO `announcements` (`id`, `title`, `content`, `summary`, `category`, `is_top`, `is_active`, `view_count`, `created_at`, `updated_at`) VALUES (2, '春节放假通知', '2025年春节放假时间为1月28日至2月4日，期间订单正常接收，检测服务将于2月5日恢复。祝大家新春快乐！', '春节期间服务安排', 'notice', 0, 1, 0, '2025-12-07 11:55:39', '2025-12-07 11:55:39');
INSERT INTO `announcements` (`id`, `title`, `content`, `summary`, `category`, `is_top`, `is_active`, `view_count`, `created_at`, `updated_at`) VALUES (3, '新项目上线', '全新XRD高分辨检测服务已上线，欢迎体验！首周下单享8折优惠。', '新检测项目上线', 'activity', 0, 1, 0, '2025-12-07 11:55:39', '2025-12-07 11:55:39');
COMMIT;

-- ----------------------------
-- Table structure for app_configs
-- ----------------------------
DROP TABLE IF EXISTS `app_configs`;
CREATE TABLE `app_configs` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '配置ID',
  `config_key` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '配置键',
  `config_value` text COLLATE utf8mb4_unicode_ci COMMENT '配置值',
  `config_type` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '配置类型',
  `description` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '配置描述',
  `group_name` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '配置分组',
  `is_active` tinyint(1) DEFAULT NULL COMMENT '是否启用',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `config_key` (`config_key`),
  KEY `ix_app_configs_id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of app_configs
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for banners
-- ----------------------------
DROP TABLE IF EXISTS `banners`;
CREATE TABLE `banners` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(200) NOT NULL COMMENT '标题',
  `subtitle` varchar(500) DEFAULT NULL COMMENT '副标题',
  `image` varchar(500) NOT NULL COMMENT '图片URL',
  `link_type` varchar(50) DEFAULT 'none' COMMENT '链接类型: none/project/url/page',
  `link_value` varchar(500) DEFAULT NULL COMMENT '链接值',
  `button_text` varchar(50) DEFAULT NULL COMMENT '按钮文字',
  `sort_order` int DEFAULT '0' COMMENT '排序',
  `is_active` tinyint(1) DEFAULT '1' COMMENT '是否启用',
  `position` varchar(50) DEFAULT 'home' COMMENT '展示位置',
  `start_time` datetime DEFAULT NULL COMMENT '开始时间',
  `end_time` datetime DEFAULT NULL COMMENT '结束时间',
  `click_count` int DEFAULT '0' COMMENT '点击次数',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_position_active` (`position`,`is_active`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='轮播图';

-- ----------------------------
-- Records of banners
-- ----------------------------
BEGIN;
INSERT INTO `banners` (`id`, `title`, `subtitle`, `image`, `link_type`, `link_value`, `button_text`, `sort_order`, `is_active`, `position`, `start_time`, `end_time`, `click_count`, `created_at`, `updated_at`) VALUES (1, '专业检测服务', '材料检测·分析测试·科研服务', 'https://picsum.photos/1200/400?random=1', 'page', 'projects', '立即预约', 1, 1, 'home', NULL, NULL, 0, '2025-12-07 11:55:39', '2025-12-07 11:55:39');
INSERT INTO `banners` (`id`, `title`, `subtitle`, `image`, `link_type`, `link_value`, `button_text`, `sort_order`, `is_active`, `position`, `start_time`, `end_time`, `click_count`, `created_at`, `updated_at`) VALUES (2, '新用户优惠', '首单立减100元', 'https://picsum.photos/1200/400?random=2', 'page', 'coupons', '领取优惠', 2, 1, 'home', NULL, NULL, 0, '2025-12-07 11:55:39', '2025-12-07 11:55:39');
INSERT INTO `banners` (`id`, `title`, `subtitle`, `image`, `link_type`, `link_value`, `button_text`, `sort_order`, `is_active`, `position`, `start_time`, `end_time`, `click_count`, `created_at`, `updated_at`) VALUES (3, '合作伙伴招募', '区域代理·项目合作·实验室入驻', 'https://picsum.photos/1200/400?random=3', 'page', 'franchise', '了解详情', 3, 1, 'home', NULL, NULL, 0, '2025-12-07 11:55:39', '2025-12-07 11:55:39');
COMMIT;

-- ----------------------------
-- Table structure for chat_messages
-- ----------------------------
DROP TABLE IF EXISTS `chat_messages`;
CREATE TABLE `chat_messages` (
  `id` int NOT NULL AUTO_INCREMENT,
  `session_id` int NOT NULL COMMENT '会话ID',
  `sender_type` varchar(20) NOT NULL COMMENT '发送者类型',
  `sender_id` int DEFAULT NULL COMMENT '发送者ID',
  `content` text NOT NULL COMMENT '消息内容',
  `message_type` varchar(20) DEFAULT 'text' COMMENT '消息类型',
  `is_read` tinyint(1) DEFAULT '0' COMMENT '是否已读',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_session` (`session_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='聊天消息';

-- ----------------------------
-- Records of chat_messages
-- ----------------------------
BEGIN;
INSERT INTO `chat_messages` (`id`, `session_id`, `sender_type`, `sender_id`, `content`, `message_type`, `is_read`, `created_at`) VALUES (1, 1, 'user', 17, '你好', 'text', 0, '2026-01-12 19:35:20');
INSERT INTO `chat_messages` (`id`, `session_id`, `sender_type`, `sender_id`, `content`, `message_type`, `is_read`, `created_at`) VALUES (2, 1, 'system', NULL, '感谢您的咨询，人工客服正在为您接入，请稍候...如有紧急问题，您也可以拨打客服电话：400-123-4567', 'text', 0, '2026-01-12 19:35:20');
COMMIT;

-- ----------------------------
-- Table structure for chat_sessions
-- ----------------------------
DROP TABLE IF EXISTS `chat_sessions`;
CREATE TABLE `chat_sessions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL COMMENT '用户ID',
  `staff_id` int DEFAULT NULL COMMENT '客服ID',
  `status` varchar(20) DEFAULT 'active' COMMENT '状态',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `closed_at` datetime DEFAULT NULL COMMENT '关闭时间',
  PRIMARY KEY (`id`),
  KEY `idx_user_status` (`user_id`,`status`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='聊天会话';

-- ----------------------------
-- Records of chat_sessions
-- ----------------------------
BEGIN;
INSERT INTO `chat_sessions` (`id`, `user_id`, `staff_id`, `status`, `created_at`, `updated_at`, `closed_at`) VALUES (1, 17, NULL, 'active', '2026-01-12 19:35:20', '2026-01-12 19:35:20', NULL);
COMMIT;

-- ----------------------------
-- Table structure for commission_records
-- ----------------------------
DROP TABLE IF EXISTS `commission_records`;
CREATE TABLE `commission_records` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL COMMENT '获得佣金的用户ID',
  `order_id` bigint NOT NULL COMMENT '订单ID',
  `from_user_id` int DEFAULT NULL COMMENT '下单用户ID（被邀请人）',
  `order_amount` decimal(10,2) DEFAULT NULL COMMENT '订单金额',
  `commission_rate` decimal(5,2) DEFAULT NULL COMMENT '佣金比例',
  `commission_amount` decimal(10,2) DEFAULT NULL COMMENT '佣金金额',
  `status` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '状态',
  `settled_at` datetime DEFAULT NULL COMMENT '结算时间',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  KEY `from_user_id` (`from_user_id`),
  KEY `ix_commission_records_order_id` (`order_id`),
  KEY `ix_commission_records_id` (`id`),
  KEY `ix_commission_records_user_id` (`user_id`),
  CONSTRAINT `commission_records_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `commission_records_ibfk_2` FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`),
  CONSTRAINT `commission_records_ibfk_3` FOREIGN KEY (`from_user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of commission_records
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for contracts
-- ----------------------------
DROP TABLE IF EXISTS `contracts`;
CREATE TABLE `contracts` (
  `id` int NOT NULL AUTO_INCREMENT,
  `contract_no` varchar(50) NOT NULL COMMENT '合同编号',
  `user_id` int NOT NULL COMMENT '用户ID',
  `order_id` int DEFAULT NULL COMMENT '关联订单ID',
  `order_no` varchar(50) DEFAULT NULL COMMENT '关联订单号',
  `title` varchar(200) NOT NULL COMMENT '合同标题',
  `content` text COMMENT '合同内容',
  `amount` decimal(10,2) DEFAULT NULL COMMENT '合同金额',
  `status` varchar(20) DEFAULT 'active' COMMENT '状态',
  `signed_at` datetime DEFAULT NULL COMMENT '签订日期',
  `expired_at` datetime DEFAULT NULL COMMENT '到期日期',
  `file_url` varchar(500) DEFAULT NULL COMMENT '合同文件URL',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `contract_no` (`contract_no`),
  KEY `idx_user` (`user_id`),
  KEY `idx_order` (`order_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='合同';

-- ----------------------------
-- Records of contracts
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for coupons
-- ----------------------------
DROP TABLE IF EXISTS `coupons`;
CREATE TABLE `coupons` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '优惠券ID',
  `name` varchar(100) NOT NULL COMMENT '优惠券名称',
  `description` text COMMENT '优惠券描述',
  `type` enum('DISCOUNT','CASH','FULL_REDUCTION') DEFAULT 'CASH',
  `discount_rate` decimal(5,2) DEFAULT NULL COMMENT '折扣率（如0.9表示9折）',
  `cash_amount` decimal(10,2) DEFAULT NULL COMMENT '代金券金额',
  `full_amount` decimal(10,2) DEFAULT NULL COMMENT '满减门槛金额',
  `reduction_amount` decimal(10,2) DEFAULT NULL COMMENT '满减优惠金额',
  `min_order_amount` decimal(10,2) DEFAULT '0.00' COMMENT '最低订单金额',
  `max_discount_amount` decimal(10,2) DEFAULT NULL COMMENT '最大优惠金额',
  `total_quantity` int DEFAULT '0' COMMENT '发行总量（0表示不限量）',
  `received_quantity` int DEFAULT '0' COMMENT '已领取数量',
  `valid_days` int DEFAULT '30' COMMENT '有效天数',
  `applicable_projects` text COMMENT '适用项目ID列表（JSON格式）',
  `applicable_categories` text COMMENT '适用分类ID列表（JSON格式）',
  `status` enum('ACTIVE','INACTIVE','EXPIRED') DEFAULT 'ACTIVE',
  `start_time` datetime DEFAULT NULL COMMENT '开始时间',
  `end_time` datetime DEFAULT NULL COMMENT '结束时间',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_status` (`status`),
  KEY `idx_time` (`start_time`,`end_time`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='优惠券模板表';

-- ----------------------------
-- Records of coupons
-- ----------------------------
BEGIN;
INSERT INTO `coupons` (`id`, `name`, `description`, `type`, `discount_rate`, `cash_amount`, `full_amount`, `reduction_amount`, `min_order_amount`, `max_discount_amount`, `total_quantity`, `received_quantity`, `valid_days`, `applicable_projects`, `applicable_categories`, `status`, `start_time`, `end_time`, `created_at`, `updated_at`) VALUES (1, '新人专享券', '新用户专享，满50减10', 'CASH', NULL, 10.00, NULL, NULL, 50.00, NULL, 1000, 1, 30, NULL, NULL, 'ACTIVE', '2025-11-23 22:35:58', '2025-12-23 22:35:58', '2025-11-23 22:35:58', '2025-11-23 22:36:39');
INSERT INTO `coupons` (`id`, `name`, `description`, `type`, `discount_rate`, `cash_amount`, `full_amount`, `reduction_amount`, `min_order_amount`, `max_discount_amount`, `total_quantity`, `received_quantity`, `valid_days`, `applicable_projects`, `applicable_categories`, `status`, `start_time`, `end_time`, `created_at`, `updated_at`) VALUES (2, '满200减30', '满200元减30元', 'FULL_REDUCTION', NULL, NULL, 200.00, 30.00, 200.00, NULL, 500, 0, 30, NULL, NULL, 'ACTIVE', '2025-11-23 22:35:58', '2026-01-22 22:35:58', '2025-11-23 22:35:58', '2025-11-23 22:35:58');
INSERT INTO `coupons` (`id`, `name`, `description`, `type`, `discount_rate`, `cash_amount`, `full_amount`, `reduction_amount`, `min_order_amount`, `max_discount_amount`, `total_quantity`, `received_quantity`, `valid_days`, `applicable_projects`, `applicable_categories`, `status`, `start_time`, `end_time`, `created_at`, `updated_at`) VALUES (3, '9折优惠券', '全场9折，最高优惠50元', 'DISCOUNT', 0.90, NULL, NULL, NULL, 100.00, 50.00, 300, 0, 30, NULL, NULL, 'ACTIVE', '2025-11-23 22:35:58', '2026-02-21 22:35:58', '2025-11-23 22:35:58', '2025-11-23 22:35:58');
COMMIT;

-- ----------------------------
-- Table structure for credit_debts
-- ----------------------------
DROP TABLE IF EXISTS `credit_debts`;
CREATE TABLE `credit_debts` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL COMMENT '用户ID',
  `order_id` int NOT NULL COMMENT '订单ID',
  `order_no` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '订单编号',
  `original_amount` decimal(10,2) NOT NULL COMMENT '原始欠款金额',
  `paid_amount` decimal(10,2) DEFAULT NULL COMMENT '已还金额',
  `remaining_amount` decimal(10,2) NOT NULL COMMENT '剩余欠款',
  `status` enum('UNPAID','PARTIAL','PAID') COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '还款状态',
  `due_date` datetime DEFAULT NULL COMMENT '应还日期',
  `paid_at` datetime DEFAULT NULL COMMENT '还清时间',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `ix_credit_debts_order_id` (`order_id`),
  KEY `ix_credit_debts_user_id` (`user_id`),
  KEY `ix_credit_debts_id` (`id`),
  CONSTRAINT `credit_debts_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of credit_debts
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for credit_limit_applications
-- ----------------------------
DROP TABLE IF EXISTS `credit_limit_applications`;
CREATE TABLE `credit_limit_applications` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL COMMENT '用户ID',
  `current_limit` decimal(10,2) DEFAULT NULL COMMENT '当前额度',
  `requested_limit` decimal(10,2) DEFAULT NULL COMMENT '申请额度',
  `reason` text COLLATE utf8mb4_unicode_ci COMMENT '申请理由',
  `status` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '状态: pending/approved/rejected',
  `approved_limit` decimal(10,2) DEFAULT NULL COMMENT '批准额度',
  `reviewer_id` int DEFAULT NULL COMMENT '审核人ID',
  `review_remark` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '审核备注',
  `reject_reason` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '拒绝原因',
  `reviewed_at` datetime DEFAULT NULL COMMENT '审核时间',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `ix_credit_limit_applications_user_id` (`user_id`),
  KEY `ix_credit_limit_applications_id` (`id`),
  CONSTRAINT `credit_limit_applications_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of credit_limit_applications
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for credit_records
-- ----------------------------
DROP TABLE IF EXISTS `credit_records`;
CREATE TABLE `credit_records` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL COMMENT '用户ID',
  `transaction_type` enum('CONSUME','REPAY','REFUND','GRANT','ADJUST') COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '交易类型',
  `amount` decimal(10,2) NOT NULL COMMENT '交易金额',
  `balance_before` decimal(10,2) DEFAULT NULL COMMENT '交易前可用额度',
  `balance_after` decimal(10,2) DEFAULT NULL COMMENT '交易后可用额度',
  `order_id` int DEFAULT NULL COMMENT '关联订单ID',
  `order_no` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '订单编号',
  `repayment_id` int DEFAULT NULL COMMENT '关联还款记录ID',
  `reference_type` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '关联类型: certification/limit_application/admin_adjustment',
  `reference_id` int DEFAULT NULL COMMENT '关联ID',
  `operator_id` int DEFAULT NULL COMMENT '操作人ID（管理员）',
  `status` enum('PENDING','SUCCESS','FAILED') COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '交易状态',
  `description` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '交易描述',
  `remark` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '备注',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `ix_credit_records_repayment_id` (`repayment_id`),
  KEY `ix_credit_records_user_id` (`user_id`),
  KEY `ix_credit_records_id` (`id`),
  KEY `ix_credit_records_order_id` (`order_id`),
  CONSTRAINT `credit_records_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of credit_records
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for franchise_applications
-- ----------------------------
DROP TABLE IF EXISTS `franchise_applications`;
CREATE TABLE `franchise_applications` (
  `id` int NOT NULL AUTO_INCREMENT,
  `application_no` varchar(50) NOT NULL COMMENT '申请编号',
  `name` varchar(100) NOT NULL COMMENT '联系人姓名',
  `phone` varchar(20) NOT NULL COMMENT '联系电话',
  `company` varchar(200) DEFAULT NULL COMMENT '公司名称',
  `city` varchar(100) DEFAULT NULL COMMENT '所在城市',
  `mode` varchar(50) DEFAULT 'agent' COMMENT '合作模式',
  `intention` text COMMENT '合作意向',
  `status` varchar(20) DEFAULT 'pending' COMMENT '状态',
  `staff_id` int DEFAULT NULL COMMENT '处理人ID',
  `staff_remark` text COMMENT '处理备注',
  `contacted_at` datetime DEFAULT NULL COMMENT '联系时间',
  `user_id` int DEFAULT NULL COMMENT '关联用户ID',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `application_no` (`application_no`),
  KEY `idx_phone` (`phone`),
  KEY `idx_status` (`status`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='加盟申请';

-- ----------------------------
-- Records of franchise_applications
-- ----------------------------
BEGIN;
INSERT INTO `franchise_applications` (`id`, `application_no`, `name`, `phone`, `company`, `city`, `mode`, `intention`, `status`, `staff_id`, `staff_remark`, `contacted_at`, `user_id`, `created_at`, `updated_at`) VALUES (1, 'FA1768187155000', '联系人1', '13900139000', '测试公司1', '杭州市', 'agent', '测试合作意向1', 'rejected', NULL, NULL, NULL, NULL, '2026-01-12 11:05:55', '2026-01-12 11:05:55');
INSERT INTO `franchise_applications` (`id`, `application_no`, `name`, `phone`, `company`, `city`, `mode`, `intention`, `status`, `staff_id`, `staff_remark`, `contacted_at`, `user_id`, `created_at`, `updated_at`) VALUES (2, 'FA1768187155001', '联系人2', '13900139001', '测试公司2', '广州市', 'partner', '测试合作意向2', 'pending', NULL, NULL, NULL, NULL, '2026-01-12 11:05:55', '2026-01-12 11:05:55');
INSERT INTO `franchise_applications` (`id`, `application_no`, `name`, `phone`, `company`, `city`, `mode`, `intention`, `status`, `staff_id`, `staff_remark`, `contacted_at`, `user_id`, `created_at`, `updated_at`) VALUES (3, 'FA1768187155002', '联系人3', '13900139002', '测试公司3', '北京市', 'agent', '测试合作意向3', 'contacted', NULL, NULL, NULL, NULL, '2026-01-12 11:05:55', '2026-01-12 11:05:55');
INSERT INTO `franchise_applications` (`id`, `application_no`, `name`, `phone`, `company`, `city`, `mode`, `intention`, `status`, `staff_id`, `staff_remark`, `contacted_at`, `user_id`, `created_at`, `updated_at`) VALUES (4, 'FA1768187155003', '联系人4', '13900139003', '测试公司4', '上海市', 'agent', '测试合作意向4', 'pending', NULL, NULL, NULL, NULL, '2026-01-12 11:05:55', '2026-01-12 11:05:55');
INSERT INTO `franchise_applications` (`id`, `application_no`, `name`, `phone`, `company`, `city`, `mode`, `intention`, `status`, `staff_id`, `staff_remark`, `contacted_at`, `user_id`, `created_at`, `updated_at`) VALUES (5, 'FA1768187155004', '联系人5', '13900139004', '测试公司5', '北京市', 'partner', '测试合作意向5', 'contacted', NULL, NULL, NULL, NULL, '2026-01-12 11:05:55', '2026-01-12 11:05:55');
INSERT INTO `franchise_applications` (`id`, `application_no`, `name`, `phone`, `company`, `city`, `mode`, `intention`, `status`, `staff_id`, `staff_remark`, `contacted_at`, `user_id`, `created_at`, `updated_at`) VALUES (6, 'FA1768187155005', '联系人6', '13900139005', '测试公司6', '上海市', 'lab', '测试合作意向6', 'contacted', NULL, NULL, NULL, NULL, '2026-01-12 11:05:55', '2026-01-12 11:05:55');
COMMIT;

-- ----------------------------
-- Table structure for group_members
-- ----------------------------
DROP TABLE IF EXISTS `group_members`;
CREATE TABLE `group_members` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '成员ID',
  `group_id` int NOT NULL COMMENT '团队ID',
  `user_id` int NOT NULL COMMENT '用户ID',
  `nickname` varchar(50) DEFAULT NULL COMMENT '昵称',
  `avatar` varchar(255) DEFAULT NULL COMMENT '头像',
  `phone` varchar(20) DEFAULT NULL COMMENT '手机号',
  `role` enum('OWNER','ADMIN','MEMBER') DEFAULT 'MEMBER',
  `order_count` int DEFAULT '0' COMMENT '订单数量',
  `total_spent` decimal(10,2) DEFAULT '0.00' COMMENT '消费金额',
  `joined_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '加入时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_group_user` (`group_id`,`user_id`),
  KEY `idx_group_id` (`group_id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_role` (`role`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='团队成员表';

-- ----------------------------
-- Records of group_members
-- ----------------------------
BEGIN;
INSERT INTO `group_members` (`id`, `group_id`, `user_id`, `nickname`, `avatar`, `phone`, `role`, `order_count`, `total_spent`, `joined_at`) VALUES (1, 1, 12, '管理员', '/static/uploads/20251018/d099536d2f5b4a4b88c2fbf3cd9b6315.png', 'admin', 'OWNER', 0, 0.00, '2025-11-23 16:16:56');
COMMIT;

-- ----------------------------
-- Table structure for help_articles
-- ----------------------------
DROP TABLE IF EXISTS `help_articles`;
CREATE TABLE `help_articles` (
  `id` int NOT NULL AUTO_INCREMENT,
  `category_id` int NOT NULL COMMENT '分类ID',
  `title` varchar(200) NOT NULL COMMENT '标题',
  `content` text NOT NULL COMMENT '内容',
  `is_hot` tinyint(1) DEFAULT '0' COMMENT '是否热门',
  `view_count` int DEFAULT '0' COMMENT '查看次数',
  `sort_order` int DEFAULT '0' COMMENT '排序',
  `is_active` tinyint(1) DEFAULT '1' COMMENT '是否启用',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_category_active` (`category_id`,`is_active`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='帮助文章';

-- ----------------------------
-- Records of help_articles
-- ----------------------------
BEGIN;
INSERT INTO `help_articles` (`id`, `category_id`, `title`, `content`, `is_hot`, `view_count`, `sort_order`, `is_active`, `created_at`, `updated_at`) VALUES (1, 1, '如何下单预约检测服务？', '1. 登录账户后，在首页或分类页面选择需要的检测项目\n2. 进入项目详情页，查看检测内容、周期和价格\n3. 点击\"立即预约\"按钮，填写样品信息\n4. 选择收货地址和优惠券（如有）\n5. 确认订单信息后提交\n6. 完成支付即可', 1, 0, 1, 1, '2025-12-07 11:55:39', '2025-12-07 11:55:39');
INSERT INTO `help_articles` (`id`, `category_id`, `title`, `content`, `is_hot`, `view_count`, `sort_order`, `is_active`, `created_at`, `updated_at`) VALUES (2, 1, '如何选择适合的检测项目？', '您可以通过以下方式选择检测项目：\n1. 在首页分类中浏览各类检测项目\n2. 使用搜索功能直接搜索项目名称\n3. 联系在线客服获取专业建议\n4. 查看项目详情了解检测内容和应用场景', 0, 0, 2, 1, '2025-12-07 11:55:39', '2025-12-07 11:55:39');
INSERT INTO `help_articles` (`id`, `category_id`, `title`, `content`, `is_hot`, `view_count`, `sort_order`, `is_active`, `created_at`, `updated_at`) VALUES (3, 2, '支持哪些支付方式？', '目前支持以下支付方式：\n1. 微信支付\n2. 支付宝支付\n3. 余额支付（需先充值）\n4. 对公转账（企业用户）', 1, 0, 1, 1, '2025-12-07 11:55:39', '2025-12-07 11:55:39');
INSERT INTO `help_articles` (`id`, `category_id`, `title`, `content`, `is_hot`, `view_count`, `sort_order`, `is_active`, `created_at`, `updated_at`) VALUES (4, 3, '样品如何寄送？', '1. 下单支付后，系统会显示实验室收件地址\n2. 将样品妥善包装，防止运输损坏\n3. 选择顺丰或其他快递寄出\n4. 在订单页面填写快递单号\n5. 实验室收到样品后会及时确认', 1, 0, 1, 1, '2025-12-07 11:55:39', '2025-12-07 11:55:39');
INSERT INTO `help_articles` (`id`, `category_id`, `title`, `content`, `is_hot`, `view_count`, `sort_order`, `is_active`, `created_at`, `updated_at`) VALUES (5, 4, '如何下载检测报告？', '检测完成后，您可以通过以下方式获取报告：\n1. 在\"我的订单\"中找到已完成的订单\n2. 点击\"下载报告\"按钮获取电子版\n3. 纸质报告会邮寄到您预留的地址', 1, 0, 1, 1, '2025-12-07 11:55:39', '2025-12-07 11:55:39');
COMMIT;

-- ----------------------------
-- Table structure for help_categories
-- ----------------------------
DROP TABLE IF EXISTS `help_categories`;
CREATE TABLE `help_categories` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL COMMENT '分类名称',
  `icon` varchar(100) DEFAULT NULL COMMENT '图标',
  `sort_order` int DEFAULT '0' COMMENT '排序',
  `is_active` tinyint(1) DEFAULT '1' COMMENT '是否启用',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='帮助分类';

-- ----------------------------
-- Records of help_categories
-- ----------------------------
BEGIN;
INSERT INTO `help_categories` (`id`, `name`, `icon`, `sort_order`, `is_active`, `created_at`) VALUES (1, '下单指南', '📦', 1, 1, '2025-12-07 11:55:39');
INSERT INTO `help_categories` (`id`, `name`, `icon`, `sort_order`, `is_active`, `created_at`) VALUES (2, '支付问题', '💳', 2, 1, '2025-12-07 11:55:39');
INSERT INTO `help_categories` (`id`, `name`, `icon`, `sort_order`, `is_active`, `created_at`) VALUES (3, '样品寄送', '📮', 3, 1, '2025-12-07 11:55:39');
INSERT INTO `help_categories` (`id`, `name`, `icon`, `sort_order`, `is_active`, `created_at`) VALUES (4, '报告相关', '📄', 4, 1, '2025-12-07 11:55:39');
INSERT INTO `help_categories` (`id`, `name`, `icon`, `sort_order`, `is_active`, `created_at`) VALUES (5, '发票问题', '🧾', 5, 1, '2025-12-07 11:55:39');
INSERT INTO `help_categories` (`id`, `name`, `icon`, `sort_order`, `is_active`, `created_at`) VALUES (6, '账户问题', '👤', 6, 1, '2025-12-07 11:55:39');
COMMIT;

-- ----------------------------
-- Table structure for invite_config
-- ----------------------------
DROP TABLE IF EXISTS `invite_config`;
CREATE TABLE `invite_config` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '配置ID',
  `inviter_reward` decimal(10,2) DEFAULT '10.00' COMMENT '邀请人奖励金额',
  `invitee_reward` decimal(10,2) DEFAULT '5.00' COMMENT '被邀请人奖励金额',
  `reward_type` varchar(20) DEFAULT 'balance' COMMENT '奖励类型',
  `min_order_amount` decimal(10,2) DEFAULT '0.00' COMMENT '最低订单金额要求',
  `reward_delay_days` int DEFAULT '0' COMMENT '奖励延迟天数',
  `min_withdraw_amount` decimal(10,2) DEFAULT '10.00' COMMENT '最低提现金额',
  `withdraw_fee_rate` decimal(5,4) DEFAULT '0.0000' COMMENT '提现手续费率',
  `is_active` tinyint(1) DEFAULT '1' COMMENT '是否启用',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='邀请配置表';

-- ----------------------------
-- Records of invite_config
-- ----------------------------
BEGIN;
INSERT INTO `invite_config` (`id`, `inviter_reward`, `invitee_reward`, `reward_type`, `min_order_amount`, `reward_delay_days`, `min_withdraw_amount`, `withdraw_fee_rate`, `is_active`, `created_at`, `updated_at`) VALUES (1, 10.00, 5.00, 'balance', 50.00, 0, 10.00, 0.0000, 1, '2025-11-23 15:19:25', '2025-11-23 15:19:25');
COMMIT;

-- ----------------------------
-- Table structure for invite_qrcode_records
-- ----------------------------
DROP TABLE IF EXISTS `invite_qrcode_records`;
CREATE TABLE `invite_qrcode_records` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '二维码ID',
  `user_id` int NOT NULL COMMENT '用户ID',
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '二维码名称',
  `scene` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '场景: personal/company/activity',
  `invite_code` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '邀请码',
  `qrcode_url` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '二维码图片URL',
  `scan_count` int DEFAULT NULL COMMENT '扫描次数',
  `register_count` int DEFAULT NULL COMMENT '注册人数',
  `is_active` int DEFAULT NULL COMMENT '是否启用',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_invite_qrcode_records_invite_code` (`invite_code`),
  KEY `ix_invite_qrcode_records_user_id` (`user_id`),
  KEY `ix_invite_qrcode_records_id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of invite_qrcode_records
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for invite_records
-- ----------------------------
DROP TABLE IF EXISTS `invite_records`;
CREATE TABLE `invite_records` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '邀请记录ID',
  `inviter_id` int NOT NULL COMMENT '邀请人用户ID',
  `invitee_id` int NOT NULL COMMENT '被邀请人用户ID',
  `inviter_name` varchar(50) DEFAULT NULL COMMENT '邀请人昵称',
  `inviter_phone` varchar(20) DEFAULT NULL COMMENT '邀请人手机号',
  `invitee_name` varchar(50) DEFAULT NULL COMMENT '被邀请人昵称',
  `invitee_phone` varchar(20) DEFAULT NULL COMMENT '被邀请人手机号',
  `reward_amount` decimal(10,2) DEFAULT '0.00' COMMENT '奖励金额',
  `reward_type` varchar(20) DEFAULT 'balance' COMMENT '奖励类型：balance/points',
  `status` enum('PENDING','COMPLETED','WITHDRAWN') DEFAULT 'PENDING',
  `first_order_id` int DEFAULT NULL COMMENT '被邀请人首单ID',
  `first_order_amount` decimal(10,2) DEFAULT NULL COMMENT '首单金额',
  `completed_at` datetime DEFAULT NULL COMMENT '完成时间',
  `invited_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '邀请时间',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_inviter_id` (`inviter_id`),
  KEY `idx_invitee_id` (`invitee_id`),
  KEY `idx_status` (`status`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='邀请记录表';

-- ----------------------------
-- Records of invite_records
-- ----------------------------
BEGIN;
INSERT INTO `invite_records` (`id`, `inviter_id`, `invitee_id`, `inviter_name`, `inviter_phone`, `invitee_name`, `invitee_phone`, `reward_amount`, `reward_type`, `status`, `first_order_id`, `first_order_amount`, `completed_at`, `invited_at`, `created_at`, `updated_at`) VALUES (1, 30, 24, '周九', '13800138007', '张三', '13800138001', 50.00, 'balance', 'PENDING', NULL, NULL, NULL, '2026-01-12 11:04:55', '2026-01-12 11:04:55', '2026-01-12 11:04:55');
INSERT INTO `invite_records` (`id`, `inviter_id`, `invitee_id`, `inviter_name`, `inviter_phone`, `invitee_name`, `invitee_phone`, `reward_amount`, `reward_type`, `status`, `first_order_id`, `first_order_amount`, `completed_at`, `invited_at`, `created_at`, `updated_at`) VALUES (2, 25, 24, '李四', '13800138002', '张三', '13800138001', 50.00, 'balance', 'PENDING', NULL, NULL, NULL, '2026-01-12 11:04:55', '2026-01-12 11:04:55', '2026-01-12 11:04:55');
INSERT INTO `invite_records` (`id`, `inviter_id`, `invitee_id`, `inviter_name`, `inviter_phone`, `invitee_name`, `invitee_phone`, `reward_amount`, `reward_type`, `status`, `first_order_id`, `first_order_amount`, `completed_at`, `invited_at`, `created_at`, `updated_at`) VALUES (3, 24, 29, '张三', '13800138001', '孙八', '13800138006', 10.00, 'balance', 'PENDING', NULL, NULL, NULL, '2026-01-12 11:04:55', '2026-01-12 11:04:55', '2026-01-12 11:04:55');
INSERT INTO `invite_records` (`id`, `inviter_id`, `invitee_id`, `inviter_name`, `inviter_phone`, `invitee_name`, `invitee_phone`, `reward_amount`, `reward_type`, `status`, `first_order_id`, `first_order_amount`, `completed_at`, `invited_at`, `created_at`, `updated_at`) VALUES (4, 25, 29, '李四', '13800138002', '孙八', '13800138006', 50.00, 'balance', 'PENDING', NULL, NULL, NULL, '2026-01-12 11:04:55', '2026-01-12 11:04:55', '2026-01-12 11:04:55');
INSERT INTO `invite_records` (`id`, `inviter_id`, `invitee_id`, `inviter_name`, `inviter_phone`, `invitee_name`, `invitee_phone`, `reward_amount`, `reward_type`, `status`, `first_order_id`, `first_order_amount`, `completed_at`, `invited_at`, `created_at`, `updated_at`) VALUES (5, 24, 25, '张三', '13800138001', '李四', '13800138002', 20.00, 'balance', 'PENDING', NULL, NULL, '2026-01-10 11:04:55', '2026-01-12 11:04:55', '2026-01-12 11:04:55', '2026-01-12 11:04:55');
INSERT INTO `invite_records` (`id`, `inviter_id`, `invitee_id`, `inviter_name`, `inviter_phone`, `invitee_name`, `invitee_phone`, `reward_amount`, `reward_type`, `status`, `first_order_id`, `first_order_amount`, `completed_at`, `invited_at`, `created_at`, `updated_at`) VALUES (6, 30, 28, '周九', '13800138007', '钱七', '13800138005', 20.00, 'balance', 'PENDING', NULL, NULL, '2025-12-13 11:04:55', '2026-01-12 11:04:55', '2026-01-12 11:04:55', '2026-01-12 11:04:55');
INSERT INTO `invite_records` (`id`, `inviter_id`, `invitee_id`, `inviter_name`, `inviter_phone`, `invitee_name`, `invitee_phone`, `reward_amount`, `reward_type`, `status`, `first_order_id`, `first_order_amount`, `completed_at`, `invited_at`, `created_at`, `updated_at`) VALUES (7, 26, 24, '王五', '13800138003', '张三', '13800138001', 50.00, 'balance', 'PENDING', NULL, NULL, NULL, '2026-01-12 11:04:55', '2026-01-12 11:04:55', '2026-01-12 11:04:55');
INSERT INTO `invite_records` (`id`, `inviter_id`, `invitee_id`, `inviter_name`, `inviter_phone`, `invitee_name`, `invitee_phone`, `reward_amount`, `reward_type`, `status`, `first_order_id`, `first_order_amount`, `completed_at`, `invited_at`, `created_at`, `updated_at`) VALUES (8, 29, 25, '孙八', '13800138006', '李四', '13800138002', 10.00, 'balance', 'PENDING', NULL, NULL, NULL, '2026-01-12 11:04:55', '2026-01-12 11:04:55', '2026-01-12 11:04:55');
INSERT INTO `invite_records` (`id`, `inviter_id`, `invitee_id`, `inviter_name`, `inviter_phone`, `invitee_name`, `invitee_phone`, `reward_amount`, `reward_type`, `status`, `first_order_id`, `first_order_amount`, `completed_at`, `invited_at`, `created_at`, `updated_at`) VALUES (9, 28, 30, '钱七', '13800138005', '周九', '13800138007', 20.00, 'balance', 'PENDING', NULL, NULL, '2025-12-14 11:04:55', '2026-01-12 11:04:55', '2026-01-12 11:04:55', '2026-01-12 11:04:55');
INSERT INTO `invite_records` (`id`, `inviter_id`, `invitee_id`, `inviter_name`, `inviter_phone`, `invitee_name`, `invitee_phone`, `reward_amount`, `reward_type`, `status`, `first_order_id`, `first_order_amount`, `completed_at`, `invited_at`, `created_at`, `updated_at`) VALUES (10, 25, 24, '李四', '13800138002', '张三', '13800138001', 10.00, 'balance', 'PENDING', NULL, NULL, NULL, '2026-01-12 11:04:55', '2026-01-12 11:04:55', '2026-01-12 11:04:55');
INSERT INTO `invite_records` (`id`, `inviter_id`, `invitee_id`, `inviter_name`, `inviter_phone`, `invitee_name`, `invitee_phone`, `reward_amount`, `reward_type`, `status`, `first_order_id`, `first_order_amount`, `completed_at`, `invited_at`, `created_at`, `updated_at`) VALUES (11, 31, 30, '吴十', '13800138008', '周九', '13800138007', 10.00, 'balance', 'PENDING', NULL, NULL, '2026-01-08 11:04:55', '2026-01-12 11:04:55', '2026-01-12 11:04:55', '2026-01-12 11:04:55');
INSERT INTO `invite_records` (`id`, `inviter_id`, `invitee_id`, `inviter_name`, `inviter_phone`, `invitee_name`, `invitee_phone`, `reward_amount`, `reward_type`, `status`, `first_order_id`, `first_order_amount`, `completed_at`, `invited_at`, `created_at`, `updated_at`) VALUES (12, 24, 30, '张三', '13800138001', '周九', '13800138007', 50.00, 'balance', 'PENDING', NULL, NULL, '2025-12-25 11:04:55', '2026-01-12 11:04:55', '2026-01-12 11:04:55', '2026-01-12 11:04:55');
INSERT INTO `invite_records` (`id`, `inviter_id`, `invitee_id`, `inviter_name`, `inviter_phone`, `invitee_name`, `invitee_phone`, `reward_amount`, `reward_type`, `status`, `first_order_id`, `first_order_amount`, `completed_at`, `invited_at`, `created_at`, `updated_at`) VALUES (13, 31, 30, '吴十', '13800138008', '周九', '13800138007', 10.00, 'balance', 'PENDING', NULL, NULL, NULL, '2026-01-12 11:04:55', '2026-01-12 11:04:55', '2026-01-12 11:04:55');
INSERT INTO `invite_records` (`id`, `inviter_id`, `invitee_id`, `inviter_name`, `inviter_phone`, `invitee_name`, `invitee_phone`, `reward_amount`, `reward_type`, `status`, `first_order_id`, `first_order_amount`, `completed_at`, `invited_at`, `created_at`, `updated_at`) VALUES (14, 30, 26, '周九', '13800138007', '王五', '13800138003', 10.00, 'balance', 'PENDING', NULL, NULL, '2026-01-01 11:04:55', '2026-01-12 11:04:55', '2026-01-12 11:04:55', '2026-01-12 11:04:55');
INSERT INTO `invite_records` (`id`, `inviter_id`, `invitee_id`, `inviter_name`, `inviter_phone`, `invitee_name`, `invitee_phone`, `reward_amount`, `reward_type`, `status`, `first_order_id`, `first_order_amount`, `completed_at`, `invited_at`, `created_at`, `updated_at`) VALUES (15, 30, 29, '周九', '13800138007', '孙八', '13800138006', 10.00, 'balance', 'PENDING', NULL, NULL, NULL, '2026-01-12 11:04:55', '2026-01-12 11:04:55', '2026-01-12 11:04:55');
COMMIT;

-- ----------------------------
-- Table structure for invoice_recharge_records
-- ----------------------------
DROP TABLE IF EXISTS `invoice_recharge_records`;
CREATE TABLE `invoice_recharge_records` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL COMMENT '用户ID',
  `amount` decimal(10,2) NOT NULL COMMENT '充值金额',
  `bonus_amount` decimal(10,2) DEFAULT NULL COMMENT '赠送金额',
  `invoice_title` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '发票抬头',
  `invoice_tax_no` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '税号',
  `invoice_type` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '发票类型: normal-普通发票, special-增值税专用发票',
  `invoice_email` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '发票接收邮箱',
  `invoice_remark` text COLLATE utf8mb4_unicode_ci COMMENT '发票备注',
  `bank_name` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '汇款银行',
  `bank_account` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '汇款账号后四位',
  `transfer_date` datetime DEFAULT NULL COMMENT '汇款日期',
  `transfer_voucher` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '汇款凭证图片URL',
  `status` enum('PENDING','CONFIRMED','REJECTED') COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '状态',
  `admin_id` int DEFAULT NULL COMMENT '确认的管理员',
  `confirmed_at` datetime DEFAULT NULL COMMENT '确认时间',
  `reject_reason` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '拒绝原因',
  `remark` text COLLATE utf8mb4_unicode_ci COMMENT '管理员备注',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `admin_id` (`admin_id`),
  KEY `ix_invoice_recharge_records_user_id` (`user_id`),
  KEY `ix_invoice_recharge_records_id` (`id`),
  CONSTRAINT `invoice_recharge_records_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `invoice_recharge_records_ibfk_2` FOREIGN KEY (`admin_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of invoice_recharge_records
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for invoices
-- ----------------------------
DROP TABLE IF EXISTS `invoices`;
CREATE TABLE `invoices` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `invoice_no` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '发票申请编号',
  `user_id` bigint NOT NULL COMMENT '用户ID',
  `invoice_type` enum('NORMAL','SPECIAL') COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '发票类型',
  `title_type` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '抬头类型: personal/company',
  `title` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '发票抬头',
  `tax_number` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '税号',
  `bank_name` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '开户银行',
  `bank_account` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '银行账号',
  `company_address` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '公司地址',
  `company_phone` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '公司电话',
  `content` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '发票内容',
  `amount` decimal(10,2) NOT NULL COMMENT '开票金额',
  `order_ids` text COLLATE utf8mb4_unicode_ci COMMENT '关联订单ID列表（JSON格式）',
  `receiver_email` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '接收邮箱（电子发票）',
  `receiver_phone` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '接收手机号',
  `receiver_address` varchar(300) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '邮寄地址（纸质发票）',
  `invoice_code` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '发票代码',
  `invoice_number` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '发票号码',
  `invoice_url` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '电子发票下载链接',
  `status` enum('PENDING','APPROVED','REJECTED','ISSUED') COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '发票状态',
  `reject_reason` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '拒绝原因',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '申请时间',
  `reviewed_at` datetime DEFAULT NULL COMMENT '审核时间',
  `issued_at` datetime DEFAULT NULL COMMENT '开票时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_invoices_invoice_no` (`invoice_no`),
  KEY `ix_invoices_user_id` (`user_id`),
  KEY `ix_invoices_id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of invoices
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for lab_applications
-- ----------------------------
DROP TABLE IF EXISTS `lab_applications`;
CREATE TABLE `lab_applications` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `applicant_user_id` int NOT NULL COMMENT '申请人用户ID',
  `applicant_name` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '申请人姓名',
  `applicant_phone` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '申请人电话',
  `applicant_email` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '申请人邮箱',
  `applicant_position` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '申请人职位',
  `lab_name` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '实验室名称',
  `lab_type` enum('UNIVERSITY','RESEARCH','ENTERPRISE','THIRD_PARTY','HOSPITAL') COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '实验室类型',
  `institution` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '所属机构',
  `department` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '所属院系/部门',
  `province` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '省份',
  `city` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '城市',
  `address` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '详细地址',
  `qualification` text COLLATE utf8mb4_unicode_ci COMMENT '资质描述',
  `certification_files` json DEFAULT NULL COMMENT '资质证书文件列表',
  `business_license` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '营业执照',
  `description` text COLLATE utf8mb4_unicode_ci COMMENT '实验室介绍',
  `specialties` json DEFAULT NULL COMMENT '专业领域',
  `equipments_desc` text COLLATE utf8mb4_unicode_ci COMMENT '设备情况描述',
  `intended_services` json DEFAULT NULL COMMENT '意向服务类型',
  `expected_monthly_orders` int DEFAULT NULL COMMENT '预期月订单量',
  `status` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '状态: pending/reviewing/approved/rejected',
  `reviewer_id` bigint DEFAULT NULL COMMENT '审核人ID',
  `review_remark` text COLLATE utf8mb4_unicode_ci COMMENT '审核备注',
  `reject_reason` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '拒绝原因',
  `reviewed_at` datetime DEFAULT NULL COMMENT '审核时间',
  `laboratory_id` bigint DEFAULT NULL COMMENT '关联实验室ID',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `ix_lab_applications_applicant_user_id` (`applicant_user_id`),
  KEY `ix_lab_applications_id` (`id`),
  KEY `ix_lab_applications_status` (`status`),
  CONSTRAINT `lab_applications_ibfk_1` FOREIGN KEY (`applicant_user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of lab_applications
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for lab_equipments
-- ----------------------------
DROP TABLE IF EXISTS `lab_equipments`;
CREATE TABLE `lab_equipments` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `laboratory_id` bigint NOT NULL COMMENT '实验室ID',
  `name` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '设备名称',
  `model` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '型号规格',
  `brand` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '品牌',
  `serial_number` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '设备编号',
  `category` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '设备类别',
  `description` text COLLATE utf8mb4_unicode_ci COMMENT '设备描述',
  `specifications` json DEFAULT NULL COMMENT '技术参数',
  `images` json DEFAULT NULL COMMENT '设备图片',
  `status` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '状态: available/in_use/maintenance/retired',
  `unit_price` decimal(10,2) DEFAULT NULL COMMENT '单次使用价格',
  `hourly_rate` decimal(10,2) DEFAULT NULL COMMENT '每小时费率',
  `purchase_date` datetime DEFAULT NULL COMMENT '购入日期',
  `last_maintenance` datetime DEFAULT NULL COMMENT '最近维护时间',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `ix_lab_equipments_id` (`id`),
  KEY `ix_lab_equipments_laboratory_id` (`laboratory_id`),
  CONSTRAINT `lab_equipments_ibfk_1` FOREIGN KEY (`laboratory_id`) REFERENCES `laboratories` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of lab_equipments
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for lab_staff
-- ----------------------------
DROP TABLE IF EXISTS `lab_staff`;
CREATE TABLE `lab_staff` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `laboratory_id` bigint NOT NULL COMMENT '实验室ID',
  `user_id` int DEFAULT NULL COMMENT '关联用户ID',
  `name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '姓名',
  `phone` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '联系电话',
  `email` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '邮箱',
  `avatar` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '头像',
  `position` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '职位',
  `title` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '职称',
  `specialties` json DEFAULT NULL COMMENT '专业领域',
  `role` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '角色: admin/technician/assistant',
  `is_active` tinyint(1) DEFAULT NULL COMMENT '是否在职',
  `joined_at` datetime DEFAULT NULL COMMENT '入职时间',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `ix_lab_staff_laboratory_id` (`laboratory_id`),
  KEY `ix_lab_staff_id` (`id`),
  CONSTRAINT `lab_staff_ibfk_1` FOREIGN KEY (`laboratory_id`) REFERENCES `laboratories` (`id`),
  CONSTRAINT `lab_staff_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of lab_staff
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for laboratories
-- ----------------------------
DROP TABLE IF EXISTS `laboratories`;
CREATE TABLE `laboratories` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `lab_no` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '实验室编号',
  `name` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '实验室名称',
  `short_name` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '简称',
  `type` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '实验室类型',
  `level` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '实验室级别',
  `institution` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '所属机构',
  `province` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '省份',
  `city` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '城市',
  `address` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '详细地址',
  `contact_person` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '联系人',
  `contact_phone` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '联系电话',
  `contact_email` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '联系邮箱',
  `status` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '状态',
  `is_verified` tinyint(1) DEFAULT NULL COMMENT '是否认证',
  `rating` decimal(3,1) DEFAULT NULL COMMENT '评分',
  `order_count` int DEFAULT NULL COMMENT '订单数量',
  `introduction` text COLLATE utf8mb4_unicode_ci COMMENT '实验室简介',
  `equipment_list` json DEFAULT NULL COMMENT '设备清单',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT NULL COMMENT '更新时间',
  `code` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '实验室编号',
  `logo` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '实验室Logo',
  `cover_image` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '封面图片',
  `lab_type` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT 'university' COMMENT '实验室类型',
  `department` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '所属院系/部门',
  `contact_name` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '联系人姓名',
  `qualification` text COLLATE utf8mb4_unicode_ci COMMENT '资质描述',
  `certification` json DEFAULT NULL COMMENT '资质证书列表',
  `business_license` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '营业执照',
  `description` text COLLATE utf8mb4_unicode_ci COMMENT '实验室介绍',
  `specialties` json DEFAULT NULL COMMENT '专业领域',
  `equipments_summary` text COLLATE utf8mb4_unicode_ci COMMENT '设备概况',
  `service_areas` json DEFAULT NULL COMMENT '服务区域',
  `service_categories` json DEFAULT NULL COMMENT '服务分类ID列表',
  `min_order_amount` decimal(10,2) DEFAULT '0.00' COMMENT '起订金额',
  `total_orders` int DEFAULT '0' COMMENT '总订单数',
  `completed_orders` int DEFAULT '0' COMMENT '完成订单数',
  `commission_rate` decimal(5,2) DEFAULT '20.00' COMMENT '平台佣金比例',
  `admin_user_id` bigint DEFAULT NULL COMMENT '管理员用户ID',
  `approved_at` datetime DEFAULT NULL COMMENT '审核通过时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `lab_no` (`lab_no`),
  UNIQUE KEY `code` (`code`),
  KEY `ix_laboratories_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of laboratories
-- ----------------------------
BEGIN;
INSERT INTO `laboratories` (`id`, `lab_no`, `name`, `short_name`, `type`, `level`, `institution`, `province`, `city`, `address`, `contact_person`, `contact_phone`, `contact_email`, `status`, `is_verified`, `rating`, `order_count`, `introduction`, `equipment_list`, `created_at`, `updated_at`, `code`, `logo`, `cover_image`, `lab_type`, `department`, `contact_name`, `qualification`, `certification`, `business_license`, `description`, `specialties`, `equipments_summary`, `service_areas`, `service_categories`, `min_order_amount`, `total_orders`, `completed_orders`, `commission_rate`, `admin_user_id`, `approved_at`) VALUES (4, 'LAB1768185974000', '清华大学材料学院分析测试中心', '清华材料中心', '高校实验室', '国家级', '清华大学材料', '浙江省', '北京市', '北京市测试中心地址1号', '老师A', '010-71310165', NULL, 'active', 1, 4.9, 1250, '清华大学材料学院分析测试中心提供专业的材料分析和检测服务。', NULL, '2026-01-12 10:46:14', '2026-01-12 19:09:29', NULL, NULL, NULL, 'UNIVERSITY', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0.00, 5, 0, 20.00, NULL, NULL);
INSERT INTO `laboratories` (`id`, `lab_no`, `name`, `short_name`, `type`, `level`, `institution`, `province`, `city`, `address`, `contact_person`, `contact_phone`, `contact_email`, `status`, `is_verified`, `rating`, `order_count`, `introduction`, `equipment_list`, `created_at`, `updated_at`, `code`, `logo`, `cover_image`, `lab_type`, `department`, `contact_name`, `qualification`, `certification`, `business_license`, `description`, `specialties`, `equipments_summary`, `service_areas`, `service_categories`, `min_order_amount`, `total_orders`, `completed_orders`, `commission_rate`, `admin_user_id`, `approved_at`) VALUES (5, 'LAB1768185974001', '北京大学化学与分子工程学院测试中心', '北大化学中心', '高校实验室', '国家级', '北京大学化学与分子工程', '北京市', '北京市', '北京市测试中心地址2号', '老师B', '010-82504876', NULL, 'active', 1, 4.8, 980, '北京大学化学与分子工程学院测试中心提供专业的材料分析和检测服务。', NULL, '2026-01-12 10:46:14', '2026-01-12 16:55:34', NULL, NULL, NULL, 'UNIVERSITY', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0.00, 1, 0, 20.00, NULL, NULL);
INSERT INTO `laboratories` (`id`, `lab_no`, `name`, `short_name`, `type`, `level`, `institution`, `province`, `city`, `address`, `contact_person`, `contact_phone`, `contact_email`, `status`, `is_verified`, `rating`, `order_count`, `introduction`, `equipment_list`, `created_at`, `updated_at`, `code`, `logo`, `cover_image`, `lab_type`, `department`, `contact_name`, `qualification`, `certification`, `business_license`, `description`, `specialties`, `equipments_summary`, `service_areas`, `service_categories`, `min_order_amount`, `total_orders`, `completed_orders`, `commission_rate`, `admin_user_id`, `approved_at`) VALUES (6, 'LAB1768185974002', '上海交通大学分析测试中心', '交大测试中心', '高校实验室', '省部级', '上海交通', '上海市', '上海市', '上海市测试中心地址3号', '老师C', '010-68044265', NULL, 'active', 1, 4.7, 756, '上海交通大学分析测试中心提供专业的材料分析和检测服务。', NULL, '2026-01-12 10:46:14', '2026-01-12 19:09:08', NULL, NULL, NULL, 'UNIVERSITY', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0.00, 1, 0, 20.00, NULL, NULL);
INSERT INTO `laboratories` (`id`, `lab_no`, `name`, `short_name`, `type`, `level`, `institution`, `province`, `city`, `address`, `contact_person`, `contact_phone`, `contact_email`, `status`, `is_verified`, `rating`, `order_count`, `introduction`, `equipment_list`, `created_at`, `updated_at`, `code`, `logo`, `cover_image`, `lab_type`, `department`, `contact_name`, `qualification`, `certification`, `business_license`, `description`, `specialties`, `equipments_summary`, `service_areas`, `service_categories`, `min_order_amount`, `total_orders`, `completed_orders`, `commission_rate`, `admin_user_id`, `approved_at`) VALUES (7, 'LAB1768185974003', '复旦大学材料科学系测试中心', '复旦材料中心', '高校实验室', '省部级', '复旦', '浙江省', '上海市', '上海市测试中心地址4号', '老师D', '010-98556767', NULL, 'active', 1, 4.6, 623, '复旦大学材料科学系测试中心提供专业的材料分析和检测服务。', NULL, '2026-01-12 10:46:14', NULL, NULL, NULL, NULL, 'UNIVERSITY', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0.00, 0, 0, 20.00, NULL, NULL);
INSERT INTO `laboratories` (`id`, `lab_no`, `name`, `short_name`, `type`, `level`, `institution`, `province`, `city`, `address`, `contact_person`, `contact_phone`, `contact_email`, `status`, `is_verified`, `rating`, `order_count`, `introduction`, `equipment_list`, `created_at`, `updated_at`, `code`, `logo`, `cover_image`, `lab_type`, `department`, `contact_name`, `qualification`, `certification`, `business_license`, `description`, `specialties`, `equipments_summary`, `service_areas`, `service_categories`, `min_order_amount`, `total_orders`, `completed_orders`, `commission_rate`, `admin_user_id`, `approved_at`) VALUES (8, 'LAB1768185974004', '浙江大学材料科学与工程学院', '浙大材料学院', '高校实验室', '国家级', '浙江大学材料科学与工程', '浙江省', '浙江省', '浙江省测试中心地址5号', '老师E', '010-10130198', NULL, 'active', 1, 4.8, 890, '浙江大学材料科学与工程学院提供专业的材料分析和检测服务。', NULL, '2026-01-12 10:46:14', '2026-01-12 14:21:35', NULL, NULL, NULL, 'UNIVERSITY', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0.00, 1, 0, 20.00, NULL, NULL);
INSERT INTO `laboratories` (`id`, `lab_no`, `name`, `short_name`, `type`, `level`, `institution`, `province`, `city`, `address`, `contact_person`, `contact_phone`, `contact_email`, `status`, `is_verified`, `rating`, `order_count`, `introduction`, `equipment_list`, `created_at`, `updated_at`, `code`, `logo`, `cover_image`, `lab_type`, `department`, `contact_name`, `qualification`, `certification`, `business_license`, `description`, `specialties`, `equipments_summary`, `service_areas`, `service_categories`, `min_order_amount`, `total_orders`, `completed_orders`, `commission_rate`, `admin_user_id`, `approved_at`) VALUES (9, 'LAB001', '平台实验室', '平台实验室', 'comprehensive', 'national', '科研检测服务平台', '北京市', '北京市', '北京市海淀区中关村科技园', NULL, '010-12345678', 'lab@eceshi.com', 'active', 1, 4.9, 1000, NULL, NULL, '2026-01-12 17:04:40', NULL, 'platform', NULL, NULL, 'third_party', NULL, '张工程师', NULL, NULL, NULL, '平台自营综合检测实验室，提供全方位检测服务', NULL, NULL, NULL, NULL, 0.00, 0, 0, 20.00, NULL, NULL);
INSERT INTO `laboratories` (`id`, `lab_no`, `name`, `short_name`, `type`, `level`, `institution`, `province`, `city`, `address`, `contact_person`, `contact_phone`, `contact_email`, `status`, `is_verified`, `rating`, `order_count`, `introduction`, `equipment_list`, `created_at`, `updated_at`, `code`, `logo`, `cover_image`, `lab_type`, `department`, `contact_name`, `qualification`, `certification`, `business_license`, `description`, `specialties`, `equipments_summary`, `service_areas`, `service_categories`, `min_order_amount`, `total_orders`, `completed_orders`, `commission_rate`, `admin_user_id`, `approved_at`) VALUES (10, 'LAB002', '清华大学材料分析中心', '清华材料中心', 'material', 'national', '清华大学', '北京市', '北京市', '北京市海淀区清华园1号', NULL, '010-62785678', 'material@tsinghua.edu.cn', 'active', 1, 4.8, 500, NULL, NULL, '2026-01-12 17:04:40', NULL, 'tsinghua', NULL, NULL, 'university', NULL, '李教授', NULL, NULL, NULL, '清华大学材料科学与工程学院分析测试中心', NULL, NULL, NULL, NULL, 0.00, 0, 0, 20.00, NULL, NULL);
INSERT INTO `laboratories` (`id`, `lab_no`, `name`, `short_name`, `type`, `level`, `institution`, `province`, `city`, `address`, `contact_person`, `contact_phone`, `contact_email`, `status`, `is_verified`, `rating`, `order_count`, `introduction`, `equipment_list`, `created_at`, `updated_at`, `code`, `logo`, `cover_image`, `lab_type`, `department`, `contact_name`, `qualification`, `certification`, `business_license`, `description`, `specialties`, `equipments_summary`, `service_areas`, `service_categories`, `min_order_amount`, `total_orders`, `completed_orders`, `commission_rate`, `admin_user_id`, `approved_at`) VALUES (11, 'LAB003', '中科院化学所分析中心', '中科院化学所', 'chemistry', 'national', '中国科学院化学研究所', '北京市', '北京市', '北京市海淀区中关村北一街2号', NULL, '010-62554678', 'analysis@iccas.ac.cn', 'active', 1, 4.9, 800, NULL, NULL, '2026-01-12 17:04:40', NULL, 'cas_chemistry', NULL, NULL, 'research', NULL, '王研究员', NULL, NULL, NULL, '中国科学院化学研究所公共分析测试平台', NULL, NULL, NULL, NULL, 0.00, 0, 0, 20.00, NULL, NULL);
COMMIT;

-- ----------------------------
-- Table structure for lottery_chances
-- ----------------------------
DROP TABLE IF EXISTS `lottery_chances`;
CREATE TABLE `lottery_chances` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL COMMENT '用户ID',
  `source_type` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '来源类型: order/signin/invite/activity',
  `source_id` bigint DEFAULT NULL COMMENT '来源ID（订单ID等）',
  `is_used` tinyint(1) DEFAULT NULL COMMENT '是否已使用',
  `used_at` datetime DEFAULT NULL COMMENT '使用时间',
  `record_id` bigint DEFAULT NULL COMMENT '使用后的抽奖记录ID',
  `expire_at` datetime DEFAULT NULL COMMENT '过期时间',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '获得时间',
  PRIMARY KEY (`id`),
  KEY `ix_lottery_chances_id` (`id`),
  KEY `ix_lottery_chances_user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of lottery_chances
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for lottery_prizes
-- ----------------------------
DROP TABLE IF EXISTS `lottery_prizes`;
CREATE TABLE `lottery_prizes` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '奖品名称',
  `prize_type` enum('COUPON','CASH','POINTS','GIFT','EMPTY') COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '奖品类型',
  `icon` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '奖品图标',
  `value` decimal(10,2) DEFAULT NULL COMMENT '奖品价值',
  `coupon_id` bigint DEFAULT NULL COMMENT '关联优惠券ID',
  `points_amount` int DEFAULT NULL COMMENT '积分数量',
  `probability` int DEFAULT NULL COMMENT '中奖概率（万分比）',
  `daily_limit` int DEFAULT NULL COMMENT '每日限量（0表示不限）',
  `total_limit` int DEFAULT NULL COMMENT '总限量（0表示不限）',
  `issued_count` int DEFAULT NULL COMMENT '已发放数量',
  `is_active` tinyint(1) DEFAULT NULL COMMENT '是否启用',
  `sort_order` int DEFAULT NULL COMMENT '排序',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `ix_lottery_prizes_id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of lottery_prizes
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for lottery_records
-- ----------------------------
DROP TABLE IF EXISTS `lottery_records`;
CREATE TABLE `lottery_records` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL COMMENT '用户ID',
  `prize_id` bigint NOT NULL COMMENT '奖品ID',
  `prize_name` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '奖品名称',
  `prize_type` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '奖品类型',
  `prize_value` decimal(10,2) DEFAULT NULL COMMENT '奖品价值',
  `prize_icon` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '奖品图标',
  `status` enum('UNCLAIMED','CLAIMED','EXPIRED') COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '领取状态',
  `claimed_at` datetime DEFAULT NULL COMMENT '领取时间',
  `expire_at` datetime DEFAULT NULL COMMENT '过期时间',
  `coupon_id` bigint DEFAULT NULL COMMENT '发放的优惠券ID',
  `order_id` bigint DEFAULT NULL COMMENT '关联的订单ID（获得抽奖机会的订单）',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '中奖时间',
  PRIMARY KEY (`id`),
  KEY `ix_lottery_records_user_id` (`user_id`),
  KEY `ix_lottery_records_id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of lottery_records
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for order_fees
-- ----------------------------
DROP TABLE IF EXISTS `order_fees`;
CREATE TABLE `order_fees` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `order_id` bigint NOT NULL COMMENT '订单ID',
  `fee_type` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '费用类型',
  `fee_name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '费用名称',
  `amount` decimal(10,2) NOT NULL COMMENT '金额',
  `remark` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '备注',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  KEY `ix_order_fees_order_id` (`order_id`),
  KEY `ix_order_fees_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of order_fees
-- ----------------------------
BEGIN;
INSERT INTO `order_fees` (`id`, `order_id`, `fee_type`, `fee_name`, `amount`, `remark`, `created_at`) VALUES (1, 1, 'project', '检测费用', 280.00, NULL, '2025-12-21 23:13:48');
INSERT INTO `order_fees` (`id`, `order_id`, `fee_type`, `fee_name`, `amount`, `remark`, `created_at`) VALUES (2, 1, 'shipping', '运费', 20.00, NULL, '2025-12-21 23:13:48');
INSERT INTO `order_fees` (`id`, `order_id`, `fee_type`, `fee_name`, `amount`, `remark`, `created_at`) VALUES (3, 2, 'project', '检测费用', 180.00, NULL, '2026-01-11 14:40:29');
INSERT INTO `order_fees` (`id`, `order_id`, `fee_type`, `fee_name`, `amount`, `remark`, `created_at`) VALUES (4, 2, 'shipping', '运费', 20.00, NULL, '2026-01-11 14:40:29');
INSERT INTO `order_fees` (`id`, `order_id`, `fee_type`, `fee_name`, `amount`, `remark`, `created_at`) VALUES (5, 3, 'project', '检测费用', 180.00, NULL, '2026-01-11 14:56:51');
INSERT INTO `order_fees` (`id`, `order_id`, `fee_type`, `fee_name`, `amount`, `remark`, `created_at`) VALUES (6, 3, 'shipping', '运费', 20.00, NULL, '2026-01-11 14:56:51');
INSERT INTO `order_fees` (`id`, `order_id`, `fee_type`, `fee_name`, `amount`, `remark`, `created_at`) VALUES (7, 4, 'project', '检测费用', 180.00, NULL, '2026-01-11 14:57:05');
INSERT INTO `order_fees` (`id`, `order_id`, `fee_type`, `fee_name`, `amount`, `remark`, `created_at`) VALUES (8, 4, 'shipping', '运费', 20.00, NULL, '2026-01-11 14:57:05');
INSERT INTO `order_fees` (`id`, `order_id`, `fee_type`, `fee_name`, `amount`, `remark`, `created_at`) VALUES (9, 5, 'project', '检测费用', 180.00, NULL, '2026-01-11 15:02:40');
INSERT INTO `order_fees` (`id`, `order_id`, `fee_type`, `fee_name`, `amount`, `remark`, `created_at`) VALUES (10, 5, 'shipping', '运费', 20.00, NULL, '2026-01-11 15:02:40');
INSERT INTO `order_fees` (`id`, `order_id`, `fee_type`, `fee_name`, `amount`, `remark`, `created_at`) VALUES (11, 6, 'project', '检测费用', 180.00, NULL, '2026-01-11 15:44:42');
INSERT INTO `order_fees` (`id`, `order_id`, `fee_type`, `fee_name`, `amount`, `remark`, `created_at`) VALUES (12, 6, 'shipping', '运费', 20.00, NULL, '2026-01-11 15:44:42');
INSERT INTO `order_fees` (`id`, `order_id`, `fee_type`, `fee_name`, `amount`, `remark`, `created_at`) VALUES (13, 7, 'project', '检测费用', 180.00, NULL, '2026-01-11 15:45:09');
INSERT INTO `order_fees` (`id`, `order_id`, `fee_type`, `fee_name`, `amount`, `remark`, `created_at`) VALUES (14, 7, 'shipping', '运费', 20.00, NULL, '2026-01-11 15:45:09');
INSERT INTO `order_fees` (`id`, `order_id`, `fee_type`, `fee_name`, `amount`, `remark`, `created_at`) VALUES (15, 8, 'project', '检测费用', 180.00, NULL, '2026-01-11 15:48:44');
INSERT INTO `order_fees` (`id`, `order_id`, `fee_type`, `fee_name`, `amount`, `remark`, `created_at`) VALUES (16, 8, 'shipping', '运费', 20.00, NULL, '2026-01-11 15:48:44');
INSERT INTO `order_fees` (`id`, `order_id`, `fee_type`, `fee_name`, `amount`, `remark`, `created_at`) VALUES (17, 9, 'project', '检测费用', 180.00, NULL, '2026-01-11 15:49:43');
INSERT INTO `order_fees` (`id`, `order_id`, `fee_type`, `fee_name`, `amount`, `remark`, `created_at`) VALUES (18, 9, 'shipping', '运费', 20.00, NULL, '2026-01-11 15:49:43');
INSERT INTO `order_fees` (`id`, `order_id`, `fee_type`, `fee_name`, `amount`, `remark`, `created_at`) VALUES (19, 10, 'project', '检测费用', 180.00, NULL, '2026-01-11 16:10:11');
INSERT INTO `order_fees` (`id`, `order_id`, `fee_type`, `fee_name`, `amount`, `remark`, `created_at`) VALUES (20, 10, 'shipping', '运费', 20.00, NULL, '2026-01-11 16:10:11');
INSERT INTO `order_fees` (`id`, `order_id`, `fee_type`, `fee_name`, `amount`, `remark`, `created_at`) VALUES (21, 11, 'project', '检测费用', 320.00, NULL, '2026-01-11 16:18:20');
INSERT INTO `order_fees` (`id`, `order_id`, `fee_type`, `fee_name`, `amount`, `remark`, `created_at`) VALUES (22, 11, 'shipping', '运费', 20.00, NULL, '2026-01-11 16:18:20');
INSERT INTO `order_fees` (`id`, `order_id`, `fee_type`, `fee_name`, `amount`, `remark`, `created_at`) VALUES (23, 12, 'project', '检测费用', 130.00, NULL, '2026-01-11 16:23:20');
INSERT INTO `order_fees` (`id`, `order_id`, `fee_type`, `fee_name`, `amount`, `remark`, `created_at`) VALUES (24, 12, 'shipping', '运费', 20.00, NULL, '2026-01-11 16:23:20');
INSERT INTO `order_fees` (`id`, `order_id`, `fee_type`, `fee_name`, `amount`, `remark`, `created_at`) VALUES (25, 13, 'project', '检测费用', 130.00, NULL, '2026-01-11 16:53:35');
INSERT INTO `order_fees` (`id`, `order_id`, `fee_type`, `fee_name`, `amount`, `remark`, `created_at`) VALUES (26, 13, 'shipping', '运费', 20.00, NULL, '2026-01-11 16:53:35');
INSERT INTO `order_fees` (`id`, `order_id`, `fee_type`, `fee_name`, `amount`, `remark`, `created_at`) VALUES (27, 14, 'project', '检测费用', 180.00, NULL, '2026-01-12 09:44:21');
INSERT INTO `order_fees` (`id`, `order_id`, `fee_type`, `fee_name`, `amount`, `remark`, `created_at`) VALUES (28, 15, 'project', '检测费用', 180.00, NULL, '2026-01-12 09:44:37');
INSERT INTO `order_fees` (`id`, `order_id`, `fee_type`, `fee_name`, `amount`, `remark`, `created_at`) VALUES (29, 16, 'project', '检测费用', 180.00, NULL, '2026-01-12 09:44:45');
INSERT INTO `order_fees` (`id`, `order_id`, `fee_type`, `fee_name`, `amount`, `remark`, `created_at`) VALUES (30, 89, 'project', '检测费用', 180.00, NULL, '2026-01-16 18:28:29');
INSERT INTO `order_fees` (`id`, `order_id`, `fee_type`, `fee_name`, `amount`, `remark`, `created_at`) VALUES (31, 89, 'shipping', '运费', 20.00, NULL, '2026-01-16 18:28:29');
INSERT INTO `order_fees` (`id`, `order_id`, `fee_type`, `fee_name`, `amount`, `remark`, `created_at`) VALUES (32, 90, 'project', '检测费用', 180.00, NULL, '2026-01-16 18:58:05');
INSERT INTO `order_fees` (`id`, `order_id`, `fee_type`, `fee_name`, `amount`, `remark`, `created_at`) VALUES (33, 90, 'shipping', '运费', 20.00, NULL, '2026-01-16 18:58:05');
COMMIT;

-- ----------------------------
-- Table structure for order_option_selections
-- ----------------------------
DROP TABLE IF EXISTS `order_option_selections`;
CREATE TABLE `order_option_selections` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `order_id` bigint NOT NULL COMMENT '订单ID',
  `option_id` bigint NOT NULL COMMENT '选项ID',
  `option_name` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '选项名称快照',
  `option_path` varchar(1000) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '选项路径快照（如：基础检测 > 样品处理 > 研磨）',
  `input_value` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '输入类型的值',
  `calculated_price` decimal(10,2) DEFAULT NULL COMMENT '计算后的价格',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  KEY `ix_order_option_selections_option_id` (`option_id`),
  KEY `ix_order_option_selections_order_id` (`order_id`),
  KEY `ix_order_option_selections_id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of order_option_selections
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for order_reviews
-- ----------------------------
DROP TABLE IF EXISTS `order_reviews`;
CREATE TABLE `order_reviews` (
  `id` int NOT NULL AUTO_INCREMENT,
  `order_id` int NOT NULL COMMENT '订单ID',
  `user_id` int NOT NULL COMMENT '用户ID',
  `project_id` int NOT NULL COMMENT '项目ID',
  `service_rating` int DEFAULT NULL COMMENT '服务质量评分',
  `quality_rating` int DEFAULT NULL COMMENT '检测效果评分',
  `logistics_rating` int DEFAULT NULL COMMENT '物流配送评分',
  `content` text COLLATE utf8mb4_unicode_ci COMMENT '评价内容',
  `images` text COLLATE utf8mb4_unicode_ci COMMENT '评价图片（JSON数组）',
  `tags` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '评价标签（逗号分隔）',
  `is_anonymous` tinyint(1) DEFAULT NULL COMMENT '是否匿名',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '评价时间',
  PRIMARY KEY (`id`),
  KEY `ix_order_reviews_user_id` (`user_id`),
  KEY `ix_order_reviews_order_id` (`order_id`),
  KEY `ix_order_reviews_project_id` (`project_id`),
  KEY `ix_order_reviews_id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of order_reviews
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for order_samples
-- ----------------------------
DROP TABLE IF EXISTS `order_samples`;
CREATE TABLE `order_samples` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `order_id` bigint NOT NULL COMMENT '订单ID',
  `sample_name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '样品名称',
  `sample_type` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '样品类型',
  `sample_desc` text COLLATE utf8mb4_unicode_ci COMMENT '样品描述',
  `quantity` int DEFAULT NULL COMMENT '样品数量',
  `photos` json DEFAULT NULL COMMENT '样品照片',
  `test_params` json DEFAULT NULL COMMENT '检测参数',
  `special_requirements` text COLLATE utf8mb4_unicode_ci COMMENT '特殊要求',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  KEY `ix_order_samples_order_id` (`order_id`),
  KEY `ix_order_samples_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=111 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of order_samples
-- ----------------------------
BEGIN;
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (1, 1, '111', NULL, NULL, 1, '[]', '{\"danger_type\": null, \"sample_state\": null, \"storage_requirement\": null}', '11', '2025-12-21 23:13:48');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (2, 2, '222', 'powder', NULL, 1, '[]', '{\"danger_type\": null, \"sample_state\": \"dry\", \"storage_requirement\": null}', '', '2026-01-11 14:40:29');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (3, 3, '11', NULL, '11', 1, '[]', '{\"danger_type\": \"易燃\", \"sample_state\": \"溶液\", \"storage_requirement\": \"干燥\"}', 'deee', '2026-01-11 14:56:51');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (4, 4, '11', NULL, '11', 1, '[]', '{\"danger_type\": \"易燃\", \"sample_state\": \"溶液\", \"storage_requirement\": \"干燥\"}', 'deee', '2026-01-11 14:57:05');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (5, 5, '11', NULL, '11', 1, '[]', '{\"danger_type\": \"易燃\", \"sample_state\": \"溶液\", \"storage_requirement\": \"干燥\"}', 'deee', '2026-01-11 15:02:40');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (6, 6, '11', NULL, '11', 1, '[]', '{\"danger_type\": \"易燃\", \"sample_state\": \"溶液\", \"storage_requirement\": \"干燥\"}', 'deee', '2026-01-11 15:44:42');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (7, 7, '22', NULL, '22', 1, '[]', '{\"danger_type\": \"氧化性\", \"sample_state\": \"其它\", \"storage_requirement\": \"干燥\"}', '22', '2026-01-11 15:45:09');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (8, 8, '22', NULL, '22', 1, '[]', '{\"danger_type\": \"氧化性\", \"sample_state\": \"其它\", \"storage_requirement\": \"干燥\"}', '22', '2026-01-11 15:48:44');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (9, 9, '额外', 'powder', NULL, 1, '[]', '{\"danger_type\": null, \"sample_state\": \"dry\", \"storage_requirement\": null}', '', '2026-01-11 15:49:43');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (10, 10, '33', 'powder', NULL, 1, '[]', '{\"danger_type\": null, \"sample_state\": \"dry\", \"storage_requirement\": null}', '', '2026-01-11 16:10:11');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (11, 11, '11', 'powder', NULL, 1, '[]', '{\"danger_type\": null, \"sample_state\": \"dry\", \"storage_requirement\": null}', '', '2026-01-11 16:18:20');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (12, 12, '111', 'powder', NULL, 1, '[]', '{\"danger_type\": null, \"sample_state\": \"dry\", \"storage_requirement\": null}', '', '2026-01-11 16:23:20');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (13, 13, '222', 'powder', NULL, 1, '[]', '{\"danger_type\": null, \"sample_state\": \"dry\", \"storage_requirement\": null}', '', '2026-01-11 16:53:35');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (14, 14, '1', NULL, '1', 1, '[]', '{\"danger_type\": \"无\", \"sample_state\": \"其它\", \"storage_requirement\": \"无\"}', '无', '2026-01-12 09:44:21');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (15, 15, '1', NULL, '1', 1, '[]', '{\"danger_type\": \"无\", \"sample_state\": \"其它\", \"storage_requirement\": \"无\"}', '无', '2026-01-12 09:44:37');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (16, 16, '1', NULL, '1', 1, '[]', '{\"danger_type\": \"无\", \"sample_state\": \"其它\", \"storage_requirement\": \"无\"}', '无', '2026-01-12 09:44:45');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (17, 17, '样品-ORD17681879679784-1', '溶液', '测试样品1', 1, '[]', '{}', '', '2026-01-12 11:19:27');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (18, 18, '样品-ORD17681879674085-1', '薄膜', '测试样品1', 1, '[]', '{}', '', '2026-01-12 11:19:27');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (19, 18, '样品-ORD17681879674085-2', '粉末', '测试样品2', 1, '[]', '{}', '', '2026-01-12 11:19:27');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (20, 18, '样品-ORD17681879674085-3', '块体', '测试样品3', 1, '[]', '{}', '', '2026-01-12 11:19:27');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (21, 19, '样品-ORD17681879674119-1', '块体', '测试样品1', 1, '[]', '{}', '', '2026-01-12 11:19:27');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (22, 19, '样品-ORD17681879674119-2', '溶液', '测试样品2', 1, '[]', '{}', '', '2026-01-12 11:19:27');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (23, 20, '样品-ORD17681879672814-1', '溶液', '测试样品1', 1, '[]', '{}', '', '2026-01-12 11:19:27');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (24, 20, '样品-ORD17681879672814-2', '块体', '测试样品2', 1, '[]', '{}', '', '2026-01-12 11:19:27');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (25, 20, '样品-ORD17681879672814-3', '薄膜', '测试样品3', 1, '[]', '{}', '', '2026-01-12 11:19:27');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (26, 21, '样品-ORD17681879671305-1', '粉末', '测试样品1', 1, '[]', '{}', '', '2026-01-12 11:19:27');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (27, 21, '样品-ORD17681879671305-2', '溶液', '测试样品2', 1, '[]', '{}', '', '2026-01-12 11:19:27');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (28, 21, '样品-ORD17681879671305-3', '溶液', '测试样品3', 1, '[]', '{}', '', '2026-01-12 11:19:27');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (29, 22, '样品-ORD17681879673852-1', '薄膜', '测试样品1', 1, '[]', '{}', '', '2026-01-12 11:19:27');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (30, 22, '样品-ORD17681879673852-2', '块体', '测试样品2', 1, '[]', '{}', '', '2026-01-12 11:19:27');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (31, 23, '样品-ORD17681879678276-1', '溶液', '测试样品1', 1, '[]', '{}', '', '2026-01-12 11:19:27');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (32, 23, '样品-ORD17681879678276-2', '粉末', '测试样品2', 1, '[]', '{}', '', '2026-01-12 11:19:27');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (33, 24, '样品-ORD17681879674325-1', '溶液', '测试样品1', 1, '[]', '{}', '', '2026-01-12 11:19:27');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (34, 24, '样品-ORD17681879674325-2', '薄膜', '测试样品2', 1, '[]', '{}', '', '2026-01-12 11:19:27');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (35, 25, '样品-ORD17681879677592-1', '粉末', '测试样品1', 1, '[]', '{}', '', '2026-01-12 11:19:27');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (36, 25, '样品-ORD17681879677592-2', '块体', '测试样品2', 1, '[]', '{}', '', '2026-01-12 11:19:27');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (37, 25, '样品-ORD17681879677592-3', '粉末', '测试样品3', 1, '[]', '{}', '', '2026-01-12 11:19:27');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (38, 26, '样品-ORD17681879679828-1', '溶液', '测试样品1', 1, '[]', '{}', '', '2026-01-12 11:19:27');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (39, 26, '样品-ORD17681879679828-2', '溶液', '测试样品2', 1, '[]', '{}', '', '2026-01-12 11:19:27');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (40, 26, '样品-ORD17681879679828-3', '溶液', '测试样品3', 1, '[]', '{}', '', '2026-01-12 11:19:27');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (41, 35, '样品-ORD17681887533026-1', '粉末', '测试样品1', 1, '[]', '{}', '', '2026-01-12 11:32:33');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (42, 35, '样品-ORD17681887533026-2', '块体', '测试样品2', 1, '[]', '{}', '', '2026-01-12 11:32:33');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (43, 35, '样品-ORD17681887533026-3', '粉末', '测试样品3', 1, '[]', '{}', '', '2026-01-12 11:32:33');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (44, 36, '样品-ORD17681887539199-1', '薄膜', '测试样品1', 1, '[]', '{}', '', '2026-01-12 11:32:33');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (45, 36, '样品-ORD17681887539199-2', '溶液', '测试样品2', 1, '[]', '{}', '', '2026-01-12 11:32:33');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (46, 36, '样品-ORD17681887539199-3', '薄膜', '测试样品3', 1, '[]', '{}', '', '2026-01-12 11:32:33');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (47, 37, '样品-ORD17681887531868-1', '薄膜', '测试样品1', 1, '[]', '{}', '', '2026-01-12 11:32:33');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (48, 37, '样品-ORD17681887531868-2', '块体', '测试样品2', 1, '[]', '{}', '', '2026-01-12 11:32:33');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (49, 37, '样品-ORD17681887531868-3', '块体', '测试样品3', 1, '[]', '{}', '', '2026-01-12 11:32:33');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (50, 38, '样品-ORD17681887539122-1', '溶液', '测试样品1', 1, '[]', '{}', '', '2026-01-12 11:32:33');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (51, 38, '样品-ORD17681887539122-2', '溶液', '测试样品2', 1, '[]', '{}', '', '2026-01-12 11:32:33');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (52, 38, '样品-ORD17681887539122-3', '薄膜', '测试样品3', 1, '[]', '{}', '', '2026-01-12 11:32:33');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (53, 39, '样品-ORD17681887532001-1', '块体', '测试样品1', 1, '[]', '{}', '', '2026-01-12 11:32:33');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (54, 39, '样品-ORD17681887532001-2', '粉末', '测试样品2', 1, '[]', '{}', '', '2026-01-12 11:32:33');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (55, 39, '样品-ORD17681887532001-3', '溶液', '测试样品3', 1, '[]', '{}', '', '2026-01-12 11:32:33');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (56, 40, '样品-ORD17681887537320-1', '块体', '测试样品1', 1, '[]', '{}', '', '2026-01-12 11:32:33');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (57, 40, '样品-ORD17681887537320-2', '薄膜', '测试样品2', 1, '[]', '{}', '', '2026-01-12 11:32:33');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (58, 40, '样品-ORD17681887537320-3', '溶液', '测试样品3', 1, '[]', '{}', '', '2026-01-12 11:32:33');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (59, 41, '样品-ORD17681887535145-1', '粉末', '测试样品1', 1, '[]', '{}', '', '2026-01-12 11:32:33');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (60, 41, '样品-ORD17681887535145-2', '溶液', '测试样品2', 1, '[]', '{}', '', '2026-01-12 11:32:33');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (61, 42, '样品-ORD17681887537192-1', '块体', '测试样品1', 1, '[]', '{}', '', '2026-01-12 11:32:33');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (62, 43, '样品-ORD17681887533968-1', '薄膜', '测试样品1', 1, '[]', '{}', '', '2026-01-12 11:32:33');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (63, 43, '样品-ORD17681887533968-2', '块体', '测试样品2', 1, '[]', '{}', '', '2026-01-12 11:32:33');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (64, 44, '样品-ORD17681887535952-1', '薄膜', '测试样品1', 1, '[]', '{}', '', '2026-01-12 11:32:33');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (65, 44, '样品-ORD17681887535952-2', '薄膜', '测试样品2', 1, '[]', '{}', '', '2026-01-12 11:32:33');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (66, 44, '样品-ORD17681887535952-3', '薄膜', '测试样品3', 1, '[]', '{}', '', '2026-01-12 11:32:33');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (67, 53, '样品-ORD17681891933625-1', '溶液', '测试样品1', 1, '[]', '{}', '', '2026-01-12 11:39:53');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (68, 53, '样品-ORD17681891933625-2', '薄膜', '测试样品2', 1, '[]', '{}', '', '2026-01-12 11:39:53');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (69, 53, '样品-ORD17681891933625-3', '溶液', '测试样品3', 1, '[]', '{}', '', '2026-01-12 11:39:53');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (70, 54, '样品-ORD17681891932164-1', '薄膜', '测试样品1', 1, '[]', '{}', '', '2026-01-12 11:39:53');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (71, 55, '样品-ORD17681891939778-1', '溶液', '测试样品1', 1, '[]', '{}', '', '2026-01-12 11:39:53');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (72, 55, '样品-ORD17681891939778-2', '薄膜', '测试样品2', 1, '[]', '{}', '', '2026-01-12 11:39:53');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (73, 55, '样品-ORD17681891939778-3', '粉末', '测试样品3', 1, '[]', '{}', '', '2026-01-12 11:39:53');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (74, 56, '样品-ORD17681891935196-1', '薄膜', '测试样品1', 1, '[]', '{}', '', '2026-01-12 11:39:53');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (75, 56, '样品-ORD17681891935196-2', '溶液', '测试样品2', 1, '[]', '{}', '', '2026-01-12 11:39:53');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (76, 57, '样品-ORD17681891939645-1', '粉末', '测试样品1', 1, '[]', '{}', '', '2026-01-12 11:39:53');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (77, 57, '样品-ORD17681891939645-2', '溶液', '测试样品2', 1, '[]', '{}', '', '2026-01-12 11:39:53');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (78, 57, '样品-ORD17681891939645-3', '溶液', '测试样品3', 1, '[]', '{}', '', '2026-01-12 11:39:53');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (79, 58, '样品-ORD17681891934890-1', '薄膜', '测试样品1', 1, '[]', '{}', '', '2026-01-12 11:39:53');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (80, 58, '样品-ORD17681891934890-2', '薄膜', '测试样品2', 1, '[]', '{}', '', '2026-01-12 11:39:53');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (81, 59, '样品-ORD17681891936744-1', '溶液', '测试样品1', 1, '[]', '{}', '', '2026-01-12 11:39:53');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (82, 60, '样品-ORD17681891932202-1', '粉末', '测试样品1', 1, '[]', '{}', '', '2026-01-12 11:39:53');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (83, 60, '样品-ORD17681891932202-2', '粉末', '测试样品2', 1, '[]', '{}', '', '2026-01-12 11:39:53');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (84, 61, '样品-ORD17681891939196-1', '薄膜', '测试样品1', 1, '[]', '{}', '', '2026-01-12 11:39:53');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (85, 62, '样品-ORD17681891935229-1', '粉末', '测试样品1', 1, '[]', '{}', '', '2026-01-12 11:39:53');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (86, 62, '样品-ORD17681891935229-2', '粉末', '测试样品2', 1, '[]', '{}', '', '2026-01-12 11:39:53');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (87, 62, '样品-ORD17681891935229-3', '溶液', '测试样品3', 1, '[]', '{}', '', '2026-01-12 11:39:53');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (88, 71, '样品-ORD17681956197430-1', '粉末', '测试样品1', 1, '[]', '{}', '', '2026-01-12 13:26:59');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (89, 71, '样品-ORD17681956197430-2', '溶液', '测试样品2', 1, '[]', '{}', '', '2026-01-12 13:26:59');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (90, 71, '样品-ORD17681956197430-3', '块体', '测试样品3', 1, '[]', '{}', '', '2026-01-12 13:26:59');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (91, 72, '样品-ORD17681956191665-1', '薄膜', '测试样品1', 1, '[]', '{}', '', '2026-01-12 13:26:59');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (92, 73, '样品-ORD17681956196323-1', '粉末', '测试样品1', 1, '[]', '{}', '', '2026-01-12 13:26:59');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (93, 73, '样品-ORD17681956196323-2', '薄膜', '测试样品2', 1, '[]', '{}', '', '2026-01-12 13:26:59');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (94, 73, '样品-ORD17681956196323-3', '溶液', '测试样品3', 1, '[]', '{}', '', '2026-01-12 13:26:59');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (95, 74, '样品-ORD17681956199469-1', '粉末', '测试样品1', 1, '[]', '{}', '', '2026-01-12 13:26:59');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (96, 75, '样品-ORD17681956195895-1', '块体', '测试样品1', 1, '[]', '{}', '', '2026-01-12 13:26:59');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (97, 75, '样品-ORD17681956195895-2', '块体', '测试样品2', 1, '[]', '{}', '', '2026-01-12 13:26:59');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (98, 75, '样品-ORD17681956195895-3', '溶液', '测试样品3', 1, '[]', '{}', '', '2026-01-12 13:26:59');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (99, 76, '样品-ORD17681956196594-1', '溶液', '测试样品1', 1, '[]', '{}', '', '2026-01-12 13:26:59');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (100, 77, '样品-ORD17681956192718-1', '薄膜', '测试样品1', 1, '[]', '{}', '', '2026-01-12 13:26:59');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (101, 77, '样品-ORD17681956192718-2', '薄膜', '测试样品2', 1, '[]', '{}', '', '2026-01-12 13:26:59');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (102, 77, '样品-ORD17681956192718-3', '粉末', '测试样品3', 1, '[]', '{}', '', '2026-01-12 13:26:59');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (103, 78, '样品-ORD17681956192042-1', '粉末', '测试样品1', 1, '[]', '{}', '', '2026-01-12 13:26:59');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (104, 79, '样品-ORD17681956197397-1', '薄膜', '测试样品1', 1, '[]', '{}', '', '2026-01-12 13:26:59');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (105, 79, '样品-ORD17681956197397-2', '薄膜', '测试样品2', 1, '[]', '{}', '', '2026-01-12 13:26:59');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (106, 79, '样品-ORD17681956197397-3', '薄膜', '测试样品3', 1, '[]', '{}', '', '2026-01-12 13:26:59');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (107, 80, '样品-ORD17681956193565-1', '溶液', '测试样品1', 1, '[]', '{}', '', '2026-01-12 13:26:59');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (108, 80, '样品-ORD17681956193565-2', '薄膜', '测试样品2', 1, '[]', '{}', '', '2026-01-12 13:26:59');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (109, 89, '00', 'bulk', NULL, 1, '[]', '{\"danger_type\": null, \"sample_state\": \"wet\", \"storage_requirement\": null}', '', '2026-01-16 18:28:29');
INSERT INTO `order_samples` (`id`, `order_id`, `sample_name`, `sample_type`, `sample_desc`, `quantity`, `photos`, `test_params`, `special_requirements`, `created_at`) VALUES (110, 90, '00', 'powder', NULL, 1, '[]', '{\"danger_type\": null, \"sample_state\": \"dry\", \"storage_requirement\": null}', '', '2026-01-16 18:58:05');
COMMIT;

-- ----------------------------
-- Table structure for order_status_history
-- ----------------------------
DROP TABLE IF EXISTS `order_status_history`;
CREATE TABLE `order_status_history` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `order_id` bigint NOT NULL COMMENT '订单ID',
  `from_status` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '原状态',
  `to_status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '新状态',
  `operator_id` bigint DEFAULT NULL COMMENT '操作人ID',
  `operator_type` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '操作人类型',
  `remark` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '备注',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  KEY `ix_order_status_history_id` (`id`),
  KEY `ix_order_status_history_order_id` (`order_id`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of order_status_history
-- ----------------------------
BEGIN;
INSERT INTO `order_status_history` (`id`, `order_id`, `from_status`, `to_status`, `operator_id`, `operator_type`, `remark`, `created_at`) VALUES (1, 1, NULL, 'pending_payment', 19, 'user', '创建订单', '2025-12-21 23:13:48');
INSERT INTO `order_status_history` (`id`, `order_id`, `from_status`, `to_status`, `operator_id`, `operator_type`, `remark`, `created_at`) VALUES (2, 2, NULL, 'pending_payment', 19, 'user', '创建订单', '2026-01-11 14:40:29');
INSERT INTO `order_status_history` (`id`, `order_id`, `from_status`, `to_status`, `operator_id`, `operator_type`, `remark`, `created_at`) VALUES (3, 3, NULL, 'pending_payment', 11, 'user', '创建订单', '2026-01-11 14:56:51');
INSERT INTO `order_status_history` (`id`, `order_id`, `from_status`, `to_status`, `operator_id`, `operator_type`, `remark`, `created_at`) VALUES (4, 4, NULL, 'pending_payment', 11, 'user', '创建订单', '2026-01-11 14:57:05');
INSERT INTO `order_status_history` (`id`, `order_id`, `from_status`, `to_status`, `operator_id`, `operator_type`, `remark`, `created_at`) VALUES (5, 5, NULL, 'pending_payment', 11, 'user', '创建订单', '2026-01-11 15:02:40');
INSERT INTO `order_status_history` (`id`, `order_id`, `from_status`, `to_status`, `operator_id`, `operator_type`, `remark`, `created_at`) VALUES (6, 6, NULL, 'pending_payment', 11, 'user', '创建订单', '2026-01-11 15:44:42');
INSERT INTO `order_status_history` (`id`, `order_id`, `from_status`, `to_status`, `operator_id`, `operator_type`, `remark`, `created_at`) VALUES (7, 7, NULL, 'pending_payment', 11, 'user', '创建订单', '2026-01-11 15:45:09');
INSERT INTO `order_status_history` (`id`, `order_id`, `from_status`, `to_status`, `operator_id`, `operator_type`, `remark`, `created_at`) VALUES (8, 8, NULL, 'pending_payment', 11, 'user', '创建订单', '2026-01-11 15:48:44');
INSERT INTO `order_status_history` (`id`, `order_id`, `from_status`, `to_status`, `operator_id`, `operator_type`, `remark`, `created_at`) VALUES (9, 9, NULL, 'pending_payment', 19, 'user', '创建订单', '2026-01-11 15:49:44');
INSERT INTO `order_status_history` (`id`, `order_id`, `from_status`, `to_status`, `operator_id`, `operator_type`, `remark`, `created_at`) VALUES (10, 10, NULL, 'pending_payment', 19, 'user', '创建订单', '2026-01-11 16:10:11');
INSERT INTO `order_status_history` (`id`, `order_id`, `from_status`, `to_status`, `operator_id`, `operator_type`, `remark`, `created_at`) VALUES (11, 11, NULL, 'pending_payment', 19, 'user', '创建订单', '2026-01-11 16:18:20');
INSERT INTO `order_status_history` (`id`, `order_id`, `from_status`, `to_status`, `operator_id`, `operator_type`, `remark`, `created_at`) VALUES (12, 12, NULL, 'pending_payment', 19, 'user', '创建订单', '2026-01-11 16:23:20');
INSERT INTO `order_status_history` (`id`, `order_id`, `from_status`, `to_status`, `operator_id`, `operator_type`, `remark`, `created_at`) VALUES (13, 13, NULL, 'pending_payment', 19, 'user', '创建订单', '2026-01-11 16:53:35');
INSERT INTO `order_status_history` (`id`, `order_id`, `from_status`, `to_status`, `operator_id`, `operator_type`, `remark`, `created_at`) VALUES (14, 14, NULL, 'pending_payment', 13, 'user', '创建订单', '2026-01-12 09:44:21');
INSERT INTO `order_status_history` (`id`, `order_id`, `from_status`, `to_status`, `operator_id`, `operator_type`, `remark`, `created_at`) VALUES (15, 15, NULL, 'pending_payment', 13, 'user', '创建订单', '2026-01-12 09:44:37');
INSERT INTO `order_status_history` (`id`, `order_id`, `from_status`, `to_status`, `operator_id`, `operator_type`, `remark`, `created_at`) VALUES (16, 16, NULL, 'pending_payment', 13, 'user', '创建订单', '2026-01-12 09:44:45');
INSERT INTO `order_status_history` (`id`, `order_id`, `from_status`, `to_status`, `operator_id`, `operator_type`, `remark`, `created_at`) VALUES (17, 80, 'paid', 'assigned', 12, 'admin', '指派给实验室: 浙江大学材料科学与工程学院', '2026-01-12 14:21:35');
INSERT INTO `order_status_history` (`id`, `order_id`, `from_status`, `to_status`, `operator_id`, `operator_type`, `remark`, `created_at`) VALUES (18, 75, 'paid', 'assigned', 12, 'admin', '指派给实验室: 清华大学材料学院分析测试中心', '2026-01-12 14:21:47');
INSERT INTO `order_status_history` (`id`, `order_id`, `from_status`, `to_status`, `operator_id`, `operator_type`, `remark`, `created_at`) VALUES (19, 35, 'pending_assign', 'assigned', 12, 'admin', '指派给实验室: 清华大学材料学院分析测试中心', '2026-01-12 14:21:53');
INSERT INTO `order_status_history` (`id`, `order_id`, `from_status`, `to_status`, `operator_id`, `operator_type`, `remark`, `created_at`) VALUES (20, 74, 'pending_assign', 'assigned', 12, 'admin', '指派给实验室: 清华大学材料学院分析测试中心', '2026-01-12 14:22:00');
INSERT INTO `order_status_history` (`id`, `order_id`, `from_status`, `to_status`, `operator_id`, `operator_type`, `remark`, `created_at`) VALUES (21, 55, 'paid', 'assigned', 12, 'admin', '指派给实验室: 北京大学化学与分子工程学院测试中心', '2026-01-12 16:55:34');
INSERT INTO `order_status_history` (`id`, `order_id`, `from_status`, `to_status`, `operator_id`, `operator_type`, `remark`, `created_at`) VALUES (22, 73, 'pending_assign', 'assigned', 12, 'admin', '指派给实验室: 上海交通大学分析测试中心', '2026-01-12 19:09:08');
INSERT INTO `order_status_history` (`id`, `order_id`, `from_status`, `to_status`, `operator_id`, `operator_type`, `remark`, `created_at`) VALUES (23, 22, 'pending_assign', 'assigned', 12, 'admin', '指派给实验室: 清华大学材料学院分析测试中心', '2026-01-12 19:09:23');
INSERT INTO `order_status_history` (`id`, `order_id`, `from_status`, `to_status`, `operator_id`, `operator_type`, `remark`, `created_at`) VALUES (24, 58, 'pending_assign', 'assigned', 12, 'admin', '指派给实验室: 清华大学材料学院分析测试中心', '2026-01-12 19:09:29');
INSERT INTO `order_status_history` (`id`, `order_id`, `from_status`, `to_status`, `operator_id`, `operator_type`, `remark`, `created_at`) VALUES (25, 89, NULL, 'pending_payment', 19, 'user', '创建订单', '2026-01-16 18:28:29');
INSERT INTO `order_status_history` (`id`, `order_id`, `from_status`, `to_status`, `operator_id`, `operator_type`, `remark`, `created_at`) VALUES (26, 90, NULL, 'pending_payment', 19, 'user', '创建订单', '2026-01-16 18:58:05');
COMMIT;

-- ----------------------------
-- Table structure for orders
-- ----------------------------
DROP TABLE IF EXISTS `orders`;
CREATE TABLE `orders` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `order_no` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '订单号',
  `user_id` bigint NOT NULL COMMENT '用户ID',
  `project_id` bigint NOT NULL COMMENT '项目ID',
  `project_name` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '项目名称',
  `lab_id` bigint NOT NULL COMMENT '实验室ID',
  `lab_name` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '实验室名称',
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '订单状态',
  `project_fee` decimal(10,2) NOT NULL COMMENT '项目费用',
  `urgent_fee` decimal(10,2) DEFAULT NULL COMMENT '加急费用',
  `shipping_fee` decimal(10,2) DEFAULT NULL COMMENT '运费',
  `discount_amount` decimal(10,2) DEFAULT NULL COMMENT '优惠金额',
  `total_fee` decimal(10,2) NOT NULL COMMENT '总金额',
  `paid_fee` decimal(10,2) DEFAULT NULL COMMENT '已支付金额',
  `sample_count` int DEFAULT NULL COMMENT '样品数量',
  `shipping_method` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '配送方式',
  `receiver_name` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '收件人',
  `receiver_phone` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '收件人电话',
  `receiver_address` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '收件地址',
  `payment_method` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '支付方式',
  `payment_time` datetime DEFAULT NULL COMMENT '支付时间',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `paid_at` datetime DEFAULT NULL COMMENT '支付时间',
  `confirmed_at` datetime DEFAULT NULL COMMENT '确认时间',
  `started_at` datetime DEFAULT NULL COMMENT '开始实验时间',
  `completed_at` datetime DEFAULT NULL COMMENT '完成时间',
  `cancelled_at` datetime DEFAULT NULL COMMENT '取消时间',
  `remark` text COLLATE utf8mb4_unicode_ci COMMENT '用户备注',
  `cancel_reason` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '取消原因',
  `is_urgent` tinyint(1) DEFAULT NULL COMMENT '是否加急',
  `estimated_completion_time` datetime DEFAULT NULL COMMENT '预计完成时间',
  `is_draft` tinyint(1) DEFAULT '0' COMMENT '是否为草稿',
  `invoice_status` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT 'none' COMMENT '开票状态',
  `invoice_id` bigint DEFAULT NULL COMMENT '关联发票ID',
  `payment_status` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT 'unpaid' COMMENT '支付状态',
  `credit_amount` decimal(10,2) DEFAULT '0.00' COMMENT '信用支付金额',
  `assigned_lab_id` bigint DEFAULT NULL COMMENT '指派实验室ID',
  `assigned_user_id` bigint DEFAULT NULL COMMENT '指派操作员ID',
  `assigned_at` datetime DEFAULT NULL COMMENT '指派时间',
  `assigned_staff_id` bigint DEFAULT NULL COMMENT '指派实验人员ID',
  `assigned_staff_name` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '指派实验人员姓名',
  PRIMARY KEY (`id`),
  UNIQUE KEY `order_no` (`order_no`),
  KEY `ix_orders_user_id` (`user_id`),
  KEY `ix_orders_lab_id` (`lab_id`),
  KEY `ix_orders_status` (`status`),
  KEY `ix_orders_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=91 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of orders
-- ----------------------------
BEGIN;
INSERT INTO `orders` (`id`, `order_no`, `user_id`, `project_id`, `project_name`, `lab_id`, `lab_name`, `status`, `project_fee`, `urgent_fee`, `shipping_fee`, `discount_amount`, `total_fee`, `paid_fee`, `sample_count`, `shipping_method`, `receiver_name`, `receiver_phone`, `receiver_address`, `payment_method`, `payment_time`, `created_at`, `paid_at`, `confirmed_at`, `started_at`, `completed_at`, `cancelled_at`, `remark`, `cancel_reason`, `is_urgent`, `estimated_completion_time`, `is_draft`, `invoice_status`, `invoice_id`, `payment_status`, `credit_amount`, `assigned_lab_id`, `assigned_user_id`, `assigned_at`, `assigned_staff_id`, `assigned_staff_name`) VALUES (1, 'ORD1766330028758382', 19, 2, '透射电镜（TEM）', 1, '平台实验室', 'pending_payment', 280.00, 0.00, 20.00, 0.00, 300.00, 0.00, 1, 'express', '111', '18888888888', 'Not applicablejinan88jinan', NULL, NULL, '2025-12-21 23:13:48', NULL, NULL, NULL, NULL, NULL, '11', NULL, 0, NULL, 0, 'none', NULL, 'unpaid', 0.00, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `orders` (`id`, `order_no`, `user_id`, `project_id`, `project_name`, `lab_id`, `lab_name`, `status`, `project_fee`, `urgent_fee`, `shipping_fee`, `discount_amount`, `total_fee`, `paid_fee`, `sample_count`, `shipping_method`, `receiver_name`, `receiver_phone`, `receiver_address`, `payment_method`, `payment_time`, `created_at`, `paid_at`, `confirmed_at`, `started_at`, `completed_at`, `cancelled_at`, `remark`, `cancel_reason`, `is_urgent`, `estimated_completion_time`, `is_draft`, `invoice_status`, `invoice_id`, `payment_status`, `credit_amount`, `assigned_lab_id`, `assigned_user_id`, `assigned_at`, `assigned_staff_id`, `assigned_staff_name`) VALUES (2, 'ORD1768113629263697', 19, 1, '扫描电镜（SEM）', 1, '平台实验室', 'pending_payment', 180.00, 0.00, 20.00, 0.00, 200.00, 0.00, 1, 'express', '111', '18888888888', 'Not applicablejinan88jinan', NULL, NULL, '2026-01-11 14:40:29', NULL, NULL, NULL, NULL, NULL, '', NULL, 0, NULL, 0, 'none', NULL, 'unpaid', 0.00, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `orders` (`id`, `order_no`, `user_id`, `project_id`, `project_name`, `lab_id`, `lab_name`, `status`, `project_fee`, `urgent_fee`, `shipping_fee`, `discount_amount`, `total_fee`, `paid_fee`, `sample_count`, `shipping_method`, `receiver_name`, `receiver_phone`, `receiver_address`, `payment_method`, `payment_time`, `created_at`, `paid_at`, `confirmed_at`, `started_at`, `completed_at`, `cancelled_at`, `remark`, `cancel_reason`, `is_urgent`, `estimated_completion_time`, `is_draft`, `invoice_status`, `invoice_id`, `payment_status`, `credit_amount`, `assigned_lab_id`, `assigned_user_id`, `assigned_at`, `assigned_staff_id`, `assigned_staff_name`) VALUES (3, 'ORD1768114611840661', 11, 1, '扫描电镜（SEM）', 1, '平台实验室', 'pending_payment', 180.00, 0.00, 20.00, 0.00, 200.00, 0.00, 1, 'express', '11', '13000000001', '北京市北京市海淀区1111', NULL, NULL, '2026-01-11 14:56:51', NULL, NULL, NULL, NULL, NULL, 'deee', NULL, 0, NULL, 0, 'none', NULL, 'unpaid', 0.00, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `orders` (`id`, `order_no`, `user_id`, `project_id`, `project_name`, `lab_id`, `lab_name`, `status`, `project_fee`, `urgent_fee`, `shipping_fee`, `discount_amount`, `total_fee`, `paid_fee`, `sample_count`, `shipping_method`, `receiver_name`, `receiver_phone`, `receiver_address`, `payment_method`, `payment_time`, `created_at`, `paid_at`, `confirmed_at`, `started_at`, `completed_at`, `cancelled_at`, `remark`, `cancel_reason`, `is_urgent`, `estimated_completion_time`, `is_draft`, `invoice_status`, `invoice_id`, `payment_status`, `credit_amount`, `assigned_lab_id`, `assigned_user_id`, `assigned_at`, `assigned_staff_id`, `assigned_staff_name`) VALUES (4, 'ORD1768114625666466', 11, 1, '扫描电镜（SEM）', 1, '平台实验室', 'pending_payment', 180.00, 0.00, 20.00, 0.00, 200.00, 0.00, 1, 'express', '11', '13000000001', '北京市北京市海淀区1111', NULL, NULL, '2026-01-11 14:57:05', NULL, NULL, NULL, NULL, NULL, 'deee', NULL, 0, NULL, 0, 'none', NULL, 'unpaid', 0.00, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `orders` (`id`, `order_no`, `user_id`, `project_id`, `project_name`, `lab_id`, `lab_name`, `status`, `project_fee`, `urgent_fee`, `shipping_fee`, `discount_amount`, `total_fee`, `paid_fee`, `sample_count`, `shipping_method`, `receiver_name`, `receiver_phone`, `receiver_address`, `payment_method`, `payment_time`, `created_at`, `paid_at`, `confirmed_at`, `started_at`, `completed_at`, `cancelled_at`, `remark`, `cancel_reason`, `is_urgent`, `estimated_completion_time`, `is_draft`, `invoice_status`, `invoice_id`, `payment_status`, `credit_amount`, `assigned_lab_id`, `assigned_user_id`, `assigned_at`, `assigned_staff_id`, `assigned_staff_name`) VALUES (5, 'ORD1768114960284495', 11, 1, '扫描电镜（SEM）', 1, '平台实验室', 'pending_payment', 180.00, 0.00, 20.00, 0.00, 200.00, 0.00, 1, 'express', '11', '13000000001', '北京市北京市海淀区1111', NULL, NULL, '2026-01-11 15:02:40', NULL, NULL, NULL, NULL, NULL, 'deee', NULL, 0, NULL, 0, 'none', NULL, 'unpaid', 0.00, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `orders` (`id`, `order_no`, `user_id`, `project_id`, `project_name`, `lab_id`, `lab_name`, `status`, `project_fee`, `urgent_fee`, `shipping_fee`, `discount_amount`, `total_fee`, `paid_fee`, `sample_count`, `shipping_method`, `receiver_name`, `receiver_phone`, `receiver_address`, `payment_method`, `payment_time`, `created_at`, `paid_at`, `confirmed_at`, `started_at`, `completed_at`, `cancelled_at`, `remark`, `cancel_reason`, `is_urgent`, `estimated_completion_time`, `is_draft`, `invoice_status`, `invoice_id`, `payment_status`, `credit_amount`, `assigned_lab_id`, `assigned_user_id`, `assigned_at`, `assigned_staff_id`, `assigned_staff_name`) VALUES (6, 'ORD17681174824006', 11, 1, '扫描电镜（SEM）', 1, '平台实验室', 'pending_payment', 180.00, 0.00, 20.00, 0.00, 200.00, 0.00, 1, 'express', '11', '13000000001', '北京市北京市海淀区1111', NULL, NULL, '2026-01-11 15:44:42', NULL, NULL, NULL, NULL, NULL, 'deee', NULL, 0, NULL, 0, 'none', NULL, 'unpaid', 0.00, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `orders` (`id`, `order_no`, `user_id`, `project_id`, `project_name`, `lab_id`, `lab_name`, `status`, `project_fee`, `urgent_fee`, `shipping_fee`, `discount_amount`, `total_fee`, `paid_fee`, `sample_count`, `shipping_method`, `receiver_name`, `receiver_phone`, `receiver_address`, `payment_method`, `payment_time`, `created_at`, `paid_at`, `confirmed_at`, `started_at`, `completed_at`, `cancelled_at`, `remark`, `cancel_reason`, `is_urgent`, `estimated_completion_time`, `is_draft`, `invoice_status`, `invoice_id`, `payment_status`, `credit_amount`, `assigned_lab_id`, `assigned_user_id`, `assigned_at`, `assigned_staff_id`, `assigned_staff_name`) VALUES (7, 'ORD1768117509917339', 11, 1, '扫描电镜（SEM）', 1, '平台实验室', 'pending_payment', 180.00, 0.00, 20.00, 0.00, 200.00, 0.00, 1, 'express', '11', '13000000001', '北京市北京市海淀区1111', NULL, NULL, '2026-01-11 15:45:09', NULL, NULL, NULL, NULL, NULL, '22', NULL, 0, NULL, 0, 'none', NULL, 'unpaid', 0.00, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `orders` (`id`, `order_no`, `user_id`, `project_id`, `project_name`, `lab_id`, `lab_name`, `status`, `project_fee`, `urgent_fee`, `shipping_fee`, `discount_amount`, `total_fee`, `paid_fee`, `sample_count`, `shipping_method`, `receiver_name`, `receiver_phone`, `receiver_address`, `payment_method`, `payment_time`, `created_at`, `paid_at`, `confirmed_at`, `started_at`, `completed_at`, `cancelled_at`, `remark`, `cancel_reason`, `is_urgent`, `estimated_completion_time`, `is_draft`, `invoice_status`, `invoice_id`, `payment_status`, `credit_amount`, `assigned_lab_id`, `assigned_user_id`, `assigned_at`, `assigned_staff_id`, `assigned_staff_name`) VALUES (8, 'ORD1768117724910493', 11, 1, '扫描电镜（SEM）', 1, '平台实验室', 'pending_payment', 180.00, 0.00, 20.00, 0.00, 200.00, 0.00, 1, 'express', '11', '13000000001', '北京市北京市海淀区1111', NULL, NULL, '2026-01-11 15:48:44', NULL, NULL, NULL, NULL, NULL, '22', NULL, 0, NULL, 0, 'none', NULL, 'unpaid', 0.00, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `orders` (`id`, `order_no`, `user_id`, `project_id`, `project_name`, `lab_id`, `lab_name`, `status`, `project_fee`, `urgent_fee`, `shipping_fee`, `discount_amount`, `total_fee`, `paid_fee`, `sample_count`, `shipping_method`, `receiver_name`, `receiver_phone`, `receiver_address`, `payment_method`, `payment_time`, `created_at`, `paid_at`, `confirmed_at`, `started_at`, `completed_at`, `cancelled_at`, `remark`, `cancel_reason`, `is_urgent`, `estimated_completion_time`, `is_draft`, `invoice_status`, `invoice_id`, `payment_status`, `credit_amount`, `assigned_lab_id`, `assigned_user_id`, `assigned_at`, `assigned_staff_id`, `assigned_staff_name`) VALUES (9, 'ORD1768117783928120', 19, 1, '扫描电镜（SEM）', 1, '平台实验室', 'pending_payment', 180.00, 0.00, 20.00, 0.00, 200.00, 0.00, 1, 'express', '111', '18888888888', 'Not applicablejinan88jinan', NULL, NULL, '2026-01-11 15:49:43', NULL, NULL, NULL, NULL, NULL, '', NULL, 0, NULL, 0, 'none', NULL, 'unpaid', 0.00, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `orders` (`id`, `order_no`, `user_id`, `project_id`, `project_name`, `lab_id`, `lab_name`, `status`, `project_fee`, `urgent_fee`, `shipping_fee`, `discount_amount`, `total_fee`, `paid_fee`, `sample_count`, `shipping_method`, `receiver_name`, `receiver_phone`, `receiver_address`, `payment_method`, `payment_time`, `created_at`, `paid_at`, `confirmed_at`, `started_at`, `completed_at`, `cancelled_at`, `remark`, `cancel_reason`, `is_urgent`, `estimated_completion_time`, `is_draft`, `invoice_status`, `invoice_id`, `payment_status`, `credit_amount`, `assigned_lab_id`, `assigned_user_id`, `assigned_at`, `assigned_staff_id`, `assigned_staff_name`) VALUES (10, 'ORD1768119011550792', 19, 1, '扫描电镜（SEM）', 1, '平台实验室', 'pending_payment', 180.00, 0.00, 20.00, 0.00, 200.00, 0.00, 1, 'express', '111', '18888888888', 'Not applicablejinan88jinan', NULL, NULL, '2026-01-11 16:10:11', NULL, NULL, NULL, NULL, NULL, '', NULL, 0, NULL, 0, 'none', NULL, 'unpaid', 0.00, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `orders` (`id`, `order_no`, `user_id`, `project_id`, `project_name`, `lab_id`, `lab_name`, `status`, `project_fee`, `urgent_fee`, `shipping_fee`, `discount_amount`, `total_fee`, `paid_fee`, `sample_count`, `shipping_method`, `receiver_name`, `receiver_phone`, `receiver_address`, `payment_method`, `payment_time`, `created_at`, `paid_at`, `confirmed_at`, `started_at`, `completed_at`, `cancelled_at`, `remark`, `cancel_reason`, `is_urgent`, `estimated_completion_time`, `is_draft`, `invoice_status`, `invoice_id`, `payment_status`, `credit_amount`, `assigned_lab_id`, `assigned_user_id`, `assigned_at`, `assigned_staff_id`, `assigned_staff_name`) VALUES (11, 'ORD1768119500405125', 19, 8, '气相色谱-质谱联用（GC-MS）', 1, '平台实验室', 'pending_payment', 320.00, 0.00, 20.00, 0.00, 340.00, 0.00, 1, 'express', '111', '18888888888', 'Not applicablejinan88jinan', NULL, NULL, '2026-01-11 16:18:20', NULL, NULL, NULL, NULL, NULL, '', NULL, 0, NULL, 0, 'none', NULL, 'unpaid', 0.00, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `orders` (`id`, `order_no`, `user_id`, `project_id`, `project_name`, `lab_id`, `lab_name`, `status`, `project_fee`, `urgent_fee`, `shipping_fee`, `discount_amount`, `total_fee`, `paid_fee`, `sample_count`, `shipping_method`, `receiver_name`, `receiver_phone`, `receiver_address`, `payment_method`, `payment_time`, `created_at`, `paid_at`, `confirmed_at`, `started_at`, `completed_at`, `cancelled_at`, `remark`, `cancel_reason`, `is_urgent`, `estimated_completion_time`, `is_draft`, `invoice_status`, `invoice_id`, `payment_status`, `credit_amount`, `assigned_lab_id`, `assigned_user_id`, `assigned_at`, `assigned_staff_id`, `assigned_staff_name`) VALUES (12, 'ORD1768119800518983', 19, 3, 'X射线衍射（XRD）', 1, '平台实验室', 'pending_payment', 130.00, 0.00, 20.00, 0.00, 150.00, 0.00, 1, 'express', '111', '18888888888', 'Not applicablejinan88jinan', NULL, NULL, '2026-01-11 16:23:20', NULL, NULL, NULL, NULL, NULL, '', NULL, 0, NULL, 0, 'none', NULL, 'unpaid', 0.00, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `orders` (`id`, `order_no`, `user_id`, `project_id`, `project_name`, `lab_id`, `lab_name`, `status`, `project_fee`, `urgent_fee`, `shipping_fee`, `discount_amount`, `total_fee`, `paid_fee`, `sample_count`, `shipping_method`, `receiver_name`, `receiver_phone`, `receiver_address`, `payment_method`, `payment_time`, `created_at`, `paid_at`, `confirmed_at`, `started_at`, `completed_at`, `cancelled_at`, `remark`, `cancel_reason`, `is_urgent`, `estimated_completion_time`, `is_draft`, `invoice_status`, `invoice_id`, `payment_status`, `credit_amount`, `assigned_lab_id`, `assigned_user_id`, `assigned_at`, `assigned_staff_id`, `assigned_staff_name`) VALUES (13, 'ORD1768121615426274', 19, 3, 'X射线衍射（XRD）', 1, '平台实验室', 'pending_payment', 130.00, 0.00, 20.00, 0.00, 150.00, 0.00, 1, 'express', '111', '18888888888', 'Not applicablejinan88jinan', NULL, NULL, '2026-01-11 16:53:35', NULL, NULL, NULL, NULL, NULL, '', NULL, 0, NULL, 0, 'none', NULL, 'unpaid', 0.00, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `orders` (`id`, `order_no`, `user_id`, `project_id`, `project_name`, `lab_id`, `lab_name`, `status`, `project_fee`, `urgent_fee`, `shipping_fee`, `discount_amount`, `total_fee`, `paid_fee`, `sample_count`, `shipping_method`, `receiver_name`, `receiver_phone`, `receiver_address`, `payment_method`, `payment_time`, `created_at`, `paid_at`, `confirmed_at`, `started_at`, `completed_at`, `cancelled_at`, `remark`, `cancel_reason`, `is_urgent`, `estimated_completion_time`, `is_draft`, `invoice_status`, `invoice_id`, `payment_status`, `credit_amount`, `assigned_lab_id`, `assigned_user_id`, `assigned_at`, `assigned_staff_id`, `assigned_staff_name`) VALUES (14, 'ORD1768182261215319', 13, 1, '扫描电镜（SEM）', 1, '平台实验室', '派遣', 180.00, 0.00, 0.00, 0.00, 180.00, 0.00, 1, 'self', NULL, NULL, NULL, NULL, NULL, '2026-01-12 09:44:21', NULL, NULL, NULL, NULL, NULL, '无', NULL, 0, NULL, 0, 'none', NULL, 'unpaid', 0.00, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `orders` (`id`, `order_no`, `user_id`, `project_id`, `project_name`, `lab_id`, `lab_name`, `status`, `project_fee`, `urgent_fee`, `shipping_fee`, `discount_amount`, `total_fee`, `paid_fee`, `sample_count`, `shipping_method`, `receiver_name`, `receiver_phone`, `receiver_address`, `payment_method`, `payment_time`, `created_at`, `paid_at`, `confirmed_at`, `started_at`, `completed_at`, `cancelled_at`, `remark`, `cancel_reason`, `is_urgent`, `estimated_completion_time`, `is_draft`, `invoice_status`, `invoice_id`, `payment_status`, `credit_amount`, `assigned_lab_id`, `assigned_user_id`, `assigned_at`, `assigned_staff_id`, `assigned_staff_name`) VALUES (15, 'ORD1768182277986402', 13, 1, '扫描电镜（SEM）', 1, '平台实验室', 'pending_payment', 180.00, 0.00, 0.00, 0.00, 180.00, 0.00, 1, 'self', NULL, NULL, NULL, NULL, NULL, '2026-01-12 09:44:37', NULL, NULL, NULL, NULL, NULL, '无', NULL, 0, NULL, 0, 'none', NULL, 'unpaid', 0.00, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `orders` (`id`, `order_no`, `user_id`, `project_id`, `project_name`, `lab_id`, `lab_name`, `status`, `project_fee`, `urgent_fee`, `shipping_fee`, `discount_amount`, `total_fee`, `paid_fee`, `sample_count`, `shipping_method`, `receiver_name`, `receiver_phone`, `receiver_address`, `payment_method`, `payment_time`, `created_at`, `paid_at`, `confirmed_at`, `started_at`, `completed_at`, `cancelled_at`, `remark`, `cancel_reason`, `is_urgent`, `estimated_completion_time`, `is_draft`, `invoice_status`, `invoice_id`, `payment_status`, `credit_amount`, `assigned_lab_id`, `assigned_user_id`, `assigned_at`, `assigned_staff_id`, `assigned_staff_name`) VALUES (16, 'ORD1768182285100959', 13, 1, '扫描电镜（SEM）', 1, '平台实验室', 'pending_payment', 180.00, 0.00, 0.00, 0.00, 180.00, 0.00, 1, 'self', NULL, NULL, NULL, NULL, NULL, '2026-01-12 09:44:45', NULL, NULL, NULL, NULL, NULL, '无', NULL, 0, NULL, 0, 'none', NULL, 'unpaid', 0.00, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `orders` (`id`, `order_no`, `user_id`, `project_id`, `project_name`, `lab_id`, `lab_name`, `status`, `project_fee`, `urgent_fee`, `shipping_fee`, `discount_amount`, `total_fee`, `paid_fee`, `sample_count`, `shipping_method`, `receiver_name`, `receiver_phone`, `receiver_address`, `payment_method`, `payment_time`, `created_at`, `paid_at`, `confirmed_at`, `started_at`, `completed_at`, `cancelled_at`, `remark`, `cancel_reason`, `is_urgent`, `estimated_completion_time`, `is_draft`, `invoice_status`, `invoice_id`, `payment_status`, `credit_amount`, `assigned_lab_id`, `assigned_user_id`, `assigned_at`, `assigned_staff_id`, `assigned_staff_name`) VALUES (17, 'ORD17681879679784', 24, 3, 'X射线衍射（XRD）', 4, '清华大学材料学院分析测试中心', 'pending_assign', 130.00, 0.00, 0.00, 0.00, 130.00, 130.00, 1, 'express', '张三', '13800138001', '测试地址1号', 'alipay', '2026-01-10 14:19:28', '2026-01-10 22:19:28', '2026-01-11 03:19:28', NULL, NULL, NULL, NULL, '测试订单-待分配#1', NULL, 0, '2026-01-19 11:19:28', 0, 'none', NULL, 'paid', 0.00, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `orders` (`id`, `order_no`, `user_id`, `project_id`, `project_name`, `lab_id`, `lab_name`, `status`, `project_fee`, `urgent_fee`, `shipping_fee`, `discount_amount`, `total_fee`, `paid_fee`, `sample_count`, `shipping_method`, `receiver_name`, `receiver_phone`, `receiver_address`, `payment_method`, `payment_time`, `created_at`, `paid_at`, `confirmed_at`, `started_at`, `completed_at`, `cancelled_at`, `remark`, `cancel_reason`, `is_urgent`, `estimated_completion_time`, `is_draft`, `invoice_status`, `invoice_id`, `payment_status`, `credit_amount`, `assigned_lab_id`, `assigned_user_id`, `assigned_at`, `assigned_staff_id`, `assigned_staff_name`) VALUES (18, 'ORD17681879674085', 24, 3, 'X射线衍射（XRD）', 4, '清华大学材料学院分析测试中心', 'paid', 130.00, 0.00, 0.00, 0.00, 130.00, 130.00, 3, 'express', '张三', '13800138001', '测试地址2号', 'balance', '2026-01-10 21:19:28', '2026-01-09 16:19:28', '2026-01-11 21:19:28', NULL, NULL, NULL, NULL, '测试订单-待分配#2', NULL, 1, '2026-01-17 11:19:28', 0, 'none', NULL, 'paid', 0.00, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `orders` (`id`, `order_no`, `user_id`, `project_id`, `project_name`, `lab_id`, `lab_name`, `status`, `project_fee`, `urgent_fee`, `shipping_fee`, `discount_amount`, `total_fee`, `paid_fee`, `sample_count`, `shipping_method`, `receiver_name`, `receiver_phone`, `receiver_address`, `payment_method`, `payment_time`, `created_at`, `paid_at`, `confirmed_at`, `started_at`, `completed_at`, `cancelled_at`, `remark`, `cancel_reason`, `is_urgent`, `estimated_completion_time`, `is_draft`, `invoice_status`, `invoice_id`, `payment_status`, `credit_amount`, `assigned_lab_id`, `assigned_user_id`, `assigned_at`, `assigned_staff_id`, `assigned_staff_name`) VALUES (19, 'ORD17681879674119', 26, 8, '气相色谱-质谱联用（GC-MS）', 4, '清华大学材料学院分析测试中心', 'paid', 320.00, 0.00, 0.00, 0.00, 320.00, 320.00, 2, 'express', '王五', '13800138003', '测试地址3号', 'wechat', '2026-01-10 11:19:28', '2026-01-10 05:19:28', '2026-01-11 03:19:28', NULL, NULL, NULL, NULL, '测试订单-待分配#3', NULL, 1, '2026-01-15 11:19:28', 0, 'none', NULL, 'paid', 0.00, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `orders` (`id`, `order_no`, `user_id`, `project_id`, `project_name`, `lab_id`, `lab_name`, `status`, `project_fee`, `urgent_fee`, `shipping_fee`, `discount_amount`, `total_fee`, `paid_fee`, `sample_count`, `shipping_method`, `receiver_name`, `receiver_phone`, `receiver_address`, `payment_method`, `payment_time`, `created_at`, `paid_at`, `confirmed_at`, `started_at`, `completed_at`, `cancelled_at`, `remark`, `cancel_reason`, `is_urgent`, `estimated_completion_time`, `is_draft`, `invoice_status`, `invoice_id`, `payment_status`, `credit_amount`, `assigned_lab_id`, `assigned_user_id`, `assigned_at`, `assigned_staff_id`, `assigned_staff_name`) VALUES (20, 'ORD17681879672814', 25, 8, '气相色谱-质谱联用（GC-MS）', 4, '清华大学材料学院分析测试中心', 'paid', 320.00, 0.00, 0.00, 0.00, 320.00, 320.00, 3, 'express', '李四', '13800138002', '测试地址4号', 'alipay', '2026-01-11 23:19:28', '2026-01-10 12:19:28', '2026-01-11 17:19:28', NULL, NULL, NULL, NULL, '测试订单-待分配#4', NULL, 1, '2026-01-19 11:19:28', 0, 'none', NULL, 'paid', 0.00, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `orders` (`id`, `order_no`, `user_id`, `project_id`, `project_name`, `lab_id`, `lab_name`, `status`, `project_fee`, `urgent_fee`, `shipping_fee`, `discount_amount`, `total_fee`, `paid_fee`, `sample_count`, `shipping_method`, `receiver_name`, `receiver_phone`, `receiver_address`, `payment_method`, `payment_time`, `created_at`, `paid_at`, `confirmed_at`, `started_at`, `completed_at`, `cancelled_at`, `remark`, `cancel_reason`, `is_urgent`, `estimated_completion_time`, `is_draft`, `invoice_status`, `invoice_id`, `payment_status`, `credit_amount`, `assigned_lab_id`, `assigned_user_id`, `assigned_at`, `assigned_staff_id`, `assigned_staff_name`) VALUES (21, 'ORD17681879671305', 24, 3, 'X射线衍射（XRD）', 4, '清华大学材料学院分析测试中心', 'paid', 130.00, 0.00, 0.00, 0.00, 130.00, 130.00, 3, 'express', '张三', '13800138001', '测试地址5号', 'wechat', '2026-01-12 07:19:28', '2026-01-11 09:19:28', '2026-01-11 06:19:28', NULL, NULL, NULL, NULL, '测试订单-待分配#5', NULL, 1, '2026-01-16 11:19:28', 0, 'none', NULL, 'paid', 0.00, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `orders` (`id`, `order_no`, `user_id`, `project_id`, `project_name`, `lab_id`, `lab_name`, `status`, `project_fee`, `urgent_fee`, `shipping_fee`, `discount_amount`, `total_fee`, `paid_fee`, `sample_count`, `shipping_method`, `receiver_name`, `receiver_phone`, `receiver_address`, `payment_method`, `payment_time`, `created_at`, `paid_at`, `confirmed_at`, `started_at`, `completed_at`, `cancelled_at`, `remark`, `cancel_reason`, `is_urgent`, `estimated_completion_time`, `is_draft`, `invoice_status`, `invoice_id`, `payment_status`, `credit_amount`, `assigned_lab_id`, `assigned_user_id`, `assigned_at`, `assigned_staff_id`, `assigned_staff_name`) VALUES (22, 'ORD17681879673852', 24, 6, '万能材料试验机', 4, '清华大学材料学院分析测试中心', 'assigned', 230.00, 0.00, 0.00, 0.00, 230.00, 230.00, 2, 'express', '张三', '13800138001', '测试地址6号', 'balance', '2026-01-11 05:19:28', '2026-01-12 04:19:28', '2026-01-11 00:19:28', NULL, NULL, NULL, NULL, '测试订单-待分配#6', NULL, 0, '2026-01-15 11:19:28', 0, 'none', NULL, 'paid', 0.00, 4, 12, '2026-01-12 11:09:24', NULL, NULL);
INSERT INTO `orders` (`id`, `order_no`, `user_id`, `project_id`, `project_name`, `lab_id`, `lab_name`, `status`, `project_fee`, `urgent_fee`, `shipping_fee`, `discount_amount`, `total_fee`, `paid_fee`, `sample_count`, `shipping_method`, `receiver_name`, `receiver_phone`, `receiver_address`, `payment_method`, `payment_time`, `created_at`, `paid_at`, `confirmed_at`, `started_at`, `completed_at`, `cancelled_at`, `remark`, `cancel_reason`, `is_urgent`, `estimated_completion_time`, `is_draft`, `invoice_status`, `invoice_id`, `payment_status`, `credit_amount`, `assigned_lab_id`, `assigned_user_id`, `assigned_at`, `assigned_staff_id`, `assigned_staff_name`) VALUES (23, 'ORD17681879678276', 25, 4, '红外光谱（FTIR）', 4, '清华大学材料学院分析测试中心', 'pending_assign', 90.00, 0.00, 0.00, 0.00, 90.00, 90.00, 2, 'express', '李四', '13800138002', '测试地址7号', 'balance', '2026-01-11 01:19:28', '2026-01-11 00:19:28', '2026-01-12 09:19:28', NULL, NULL, NULL, NULL, '测试订单-待分配#7', NULL, 1, '2026-01-18 11:19:28', 0, 'none', NULL, 'paid', 0.00, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `orders` (`id`, `order_no`, `user_id`, `project_id`, `project_name`, `lab_id`, `lab_name`, `status`, `project_fee`, `urgent_fee`, `shipping_fee`, `discount_amount`, `total_fee`, `paid_fee`, `sample_count`, `shipping_method`, `receiver_name`, `receiver_phone`, `receiver_address`, `payment_method`, `payment_time`, `created_at`, `paid_at`, `confirmed_at`, `started_at`, `completed_at`, `cancelled_at`, `remark`, `cancel_reason`, `is_urgent`, `estimated_completion_time`, `is_draft`, `invoice_status`, `invoice_id`, `payment_status`, `credit_amount`, `assigned_lab_id`, `assigned_user_id`, `assigned_at`, `assigned_staff_id`, `assigned_staff_name`) VALUES (24, 'ORD17681879674325', 24, 7, '核磁共振（NMR）', 4, '清华大学材料学院分析测试中心', 'pending_assign', 380.00, 0.00, 0.00, 0.00, 380.00, 380.00, 2, 'express', '张三', '13800138001', '测试地址8号', 'alipay', '2026-01-10 22:19:28', '2026-01-11 16:19:28', '2026-01-11 20:19:28', NULL, NULL, NULL, NULL, '测试订单-待分配#8', NULL, 1, '2026-01-18 11:19:28', 0, 'none', NULL, 'paid', 0.00, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `orders` (`id`, `order_no`, `user_id`, `project_id`, `project_name`, `lab_id`, `lab_name`, `status`, `project_fee`, `urgent_fee`, `shipping_fee`, `discount_amount`, `total_fee`, `paid_fee`, `sample_count`, `shipping_method`, `receiver_name`, `receiver_phone`, `receiver_address`, `payment_method`, `payment_time`, `created_at`, `paid_at`, `confirmed_at`, `started_at`, `completed_at`, `cancelled_at`, `remark`, `cancel_reason`, `is_urgent`, `estimated_completion_time`, `is_draft`, `invoice_status`, `invoice_id`, `payment_status`, `credit_amount`, `assigned_lab_id`, `assigned_user_id`, `assigned_at`, `assigned_staff_id`, `assigned_staff_name`) VALUES (25, 'ORD17681879677592', 24, 6, '万能材料试验机', 4, '清华大学材料学院分析测试中心', 'pending_assign', 230.00, 0.00, 0.00, 0.00, 230.00, 230.00, 3, 'express', '张三', '13800138001', '测试地址9号', 'balance', '2026-01-11 16:19:28', '2026-01-11 02:19:28', '2026-01-11 12:19:28', NULL, NULL, NULL, NULL, '测试订单-待分配#9', NULL, 0, '2026-01-18 11:19:28', 0, 'none', NULL, 'paid', 0.00, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `orders` (`id`, `order_no`, `user_id`, `project_id`, `project_name`, `lab_id`, `lab_name`, `status`, `project_fee`, `urgent_fee`, `shipping_fee`, `discount_amount`, `total_fee`, `paid_fee`, `sample_count`, `shipping_method`, `receiver_name`, `receiver_phone`, `receiver_address`, `payment_method`, `payment_time`, `created_at`, `paid_at`, `confirmed_at`, `started_at`, `completed_at`, `cancelled_at`, `remark`, `cancel_reason`, `is_urgent`, `estimated_completion_time`, `is_draft`, `invoice_status`, `invoice_id`, `payment_status`, `credit_amount`, `assigned_lab_id`, `assigned_user_id`, `assigned_at`, `assigned_staff_id`, `assigned_staff_name`) VALUES (26, 'ORD17681879679828', 24, 6, '万能材料试验机', 4, '清华大学材料学院分析测试中心', 'paid', 230.00, 0.00, 0.00, 0.00, 230.00, 230.00, 3, 'express', '张三', '13800138001', '测试地址10号', 'alipay', '2026-01-11 04:19:28', '2026-01-10 00:19:28', '2026-01-11 23:19:28', NULL, NULL, NULL, NULL, '测试订单-待分配#10', NULL, 1, '2026-01-17 11:19:28', 0, 'none', NULL, 'paid', 0.00, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `orders` (`id`, `order_no`, `user_id`, `project_id`, `project_name`, `lab_id`, `lab_name`, `status`, `project_fee`, `urgent_fee`, `shipping_fee`, `discount_amount`, `total_fee`, `paid_fee`, `sample_count`, `shipping_method`, `receiver_name`, `receiver_phone`, `receiver_address`, `payment_method`, `payment_time`, `created_at`, `paid_at`, `confirmed_at`, `started_at`, `completed_at`, `cancelled_at`, `remark`, `cancel_reason`, `is_urgent`, `estimated_completion_time`, `is_draft`, `invoice_status`, `invoice_id`, `payment_status`, `credit_amount`, `assigned_lab_id`, `assigned_user_id`, `assigned_at`, `assigned_staff_id`, `assigned_staff_name`) VALUES (27, 'ORD17681879673627', 25, 6, '万能材料试验机', 5, '北京大学化学与分子工程学院测试中心', 'assigned', 230.00, 0.00, 0.00, 0.00, 230.00, 230.00, 1, 'express', '李四', '13800138002', '测试地址1号', 'balance', '2026-01-08 11:19:28', '2026-01-08 11:19:28', '2026-01-05 11:19:28', NULL, NULL, NULL, NULL, '测试订单-已分配待接单#1', NULL, 0, NULL, 0, 'none', NULL, 'paid', 0.00, 5, 32, '2026-01-11 21:19:28', NULL, NULL);
INSERT INTO `orders` (`id`, `order_no`, `user_id`, `project_id`, `project_name`, `lab_id`, `lab_name`, `status`, `project_fee`, `urgent_fee`, `shipping_fee`, `discount_amount`, `total_fee`, `paid_fee`, `sample_count`, `shipping_method`, `receiver_name`, `receiver_phone`, `receiver_address`, `payment_method`, `payment_time`, `created_at`, `paid_at`, `confirmed_at`, `started_at`, `completed_at`, `cancelled_at`, `remark`, `cancel_reason`, `is_urgent`, `estimated_completion_time`, `is_draft`, `invoice_status`, `invoice_id`, `payment_status`, `credit_amount`, `assigned_lab_id`, `assigned_user_id`, `assigned_at`, `assigned_staff_id`, `assigned_staff_name`) VALUES (28, 'ORD17681879678511', 25, 7, '核磁共振（NMR）', 7, '复旦大学材料科学系测试中心', 'assigned', 380.00, 0.00, 0.00, 0.00, 380.00, 380.00, 1, 'express', '李四', '13800138002', '测试地址2号', 'balance', '2026-01-05 11:19:28', '2026-01-05 11:19:28', '2026-01-08 11:19:28', NULL, NULL, NULL, NULL, '测试订单-已分配待接单#2', NULL, 0, NULL, 0, 'none', NULL, 'paid', 0.00, 7, 32, '2026-01-11 18:19:28', NULL, NULL);
INSERT INTO `orders` (`id`, `order_no`, `user_id`, `project_id`, `project_name`, `lab_id`, `lab_name`, `status`, `project_fee`, `urgent_fee`, `shipping_fee`, `discount_amount`, `total_fee`, `paid_fee`, `sample_count`, `shipping_method`, `receiver_name`, `receiver_phone`, `receiver_address`, `payment_method`, `payment_time`, `created_at`, `paid_at`, `confirmed_at`, `started_at`, `completed_at`, `cancelled_at`, `remark`, `cancel_reason`, `is_urgent`, `estimated_completion_time`, `is_draft`, `invoice_status`, `invoice_id`, `payment_status`, `credit_amount`, `assigned_lab_id`, `assigned_user_id`, `assigned_at`, `assigned_staff_id`, `assigned_staff_name`) VALUES (29, 'ORD17681879678650', 24, 6, '万能材料试验机', 6, '上海交通大学分析测试中心', 'accepted', 230.00, 0.00, 0.00, 0.00, 230.00, 230.00, 1, 'express', '张三', '13800138001', '测试地址1号', 'balance', '2026-01-08 11:19:28', '2026-01-09 11:19:28', '2026-01-11 11:19:28', NULL, NULL, NULL, NULL, '测试订单-实验室已接单#1', NULL, 0, NULL, 0, 'none', NULL, 'paid', 0.00, 6, 32, '2026-01-12 03:19:28', NULL, NULL);
INSERT INTO `orders` (`id`, `order_no`, `user_id`, `project_id`, `project_name`, `lab_id`, `lab_name`, `status`, `project_fee`, `urgent_fee`, `shipping_fee`, `discount_amount`, `total_fee`, `paid_fee`, `sample_count`, `shipping_method`, `receiver_name`, `receiver_phone`, `receiver_address`, `payment_method`, `payment_time`, `created_at`, `paid_at`, `confirmed_at`, `started_at`, `completed_at`, `cancelled_at`, `remark`, `cancel_reason`, `is_urgent`, `estimated_completion_time`, `is_draft`, `invoice_status`, `invoice_id`, `payment_status`, `credit_amount`, `assigned_lab_id`, `assigned_user_id`, `assigned_at`, `assigned_staff_id`, `assigned_staff_name`) VALUES (30, 'ORD17681879677482', 24, 4, '红外光谱（FTIR）', 7, '复旦大学材料科学系测试中心', 'accepted', 90.00, 0.00, 0.00, 0.00, 90.00, 90.00, 1, 'express', '张三', '13800138001', '测试地址2号', 'balance', '2026-01-08 11:19:28', '2026-01-01 11:19:28', '2026-01-07 11:19:28', NULL, NULL, NULL, NULL, '测试订单-实验室已接单#2', NULL, 0, NULL, 0, 'none', NULL, 'paid', 0.00, 7, 32, '2026-01-11 11:19:28', NULL, NULL);
INSERT INTO `orders` (`id`, `order_no`, `user_id`, `project_id`, `project_name`, `lab_id`, `lab_name`, `status`, `project_fee`, `urgent_fee`, `shipping_fee`, `discount_amount`, `total_fee`, `paid_fee`, `sample_count`, `shipping_method`, `receiver_name`, `receiver_phone`, `receiver_address`, `payment_method`, `payment_time`, `created_at`, `paid_at`, `confirmed_at`, `started_at`, `completed_at`, `cancelled_at`, `remark`, `cancel_reason`, `is_urgent`, `estimated_completion_time`, `is_draft`, `invoice_status`, `invoice_id`, `payment_status`, `credit_amount`, `assigned_lab_id`, `assigned_user_id`, `assigned_at`, `assigned_staff_id`, `assigned_staff_name`) VALUES (31, 'ORD17681879679983', 24, 3, 'X射线衍射（XRD）', 4, '清华大学材料学院分析测试中心', 'testing', 130.00, 0.00, 0.00, 0.00, 130.00, 130.00, 1, 'express', '张三', '13800138001', '测试地址1号', 'balance', '2026-01-07 11:19:28', '2026-01-05 11:19:28', '2026-01-06 11:19:28', '2026-01-10 11:19:28', '2026-01-11 11:19:28', NULL, NULL, '测试订单-检测中#1', NULL, 0, NULL, 0, 'none', NULL, 'paid', 0.00, 4, 32, '2026-01-11 14:19:28', NULL, NULL);
INSERT INTO `orders` (`id`, `order_no`, `user_id`, `project_id`, `project_name`, `lab_id`, `lab_name`, `status`, `project_fee`, `urgent_fee`, `shipping_fee`, `discount_amount`, `total_fee`, `paid_fee`, `sample_count`, `shipping_method`, `receiver_name`, `receiver_phone`, `receiver_address`, `payment_method`, `payment_time`, `created_at`, `paid_at`, `confirmed_at`, `started_at`, `completed_at`, `cancelled_at`, `remark`, `cancel_reason`, `is_urgent`, `estimated_completion_time`, `is_draft`, `invoice_status`, `invoice_id`, `payment_status`, `credit_amount`, `assigned_lab_id`, `assigned_user_id`, `assigned_at`, `assigned_staff_id`, `assigned_staff_name`) VALUES (32, 'ORD17681879674201', 25, 2, '透射电镜（TEM）', 7, '复旦大学材料科学系测试中心', 'testing', 280.00, 0.00, 0.00, 0.00, 280.00, 280.00, 1, 'express', '李四', '13800138002', '测试地址2号', 'balance', '2026-01-08 11:19:28', '2025-12-29 11:19:28', '2026-01-08 11:19:28', '2026-01-10 11:19:28', '2026-01-11 11:19:28', NULL, NULL, '测试订单-检测中#2', NULL, 0, NULL, 0, 'none', NULL, 'paid', 0.00, 7, 32, '2026-01-12 04:19:28', NULL, NULL);
INSERT INTO `orders` (`id`, `order_no`, `user_id`, `project_id`, `project_name`, `lab_id`, `lab_name`, `status`, `project_fee`, `urgent_fee`, `shipping_fee`, `discount_amount`, `total_fee`, `paid_fee`, `sample_count`, `shipping_method`, `receiver_name`, `receiver_phone`, `receiver_address`, `payment_method`, `payment_time`, `created_at`, `paid_at`, `confirmed_at`, `started_at`, `completed_at`, `cancelled_at`, `remark`, `cancel_reason`, `is_urgent`, `estimated_completion_time`, `is_draft`, `invoice_status`, `invoice_id`, `payment_status`, `credit_amount`, `assigned_lab_id`, `assigned_user_id`, `assigned_at`, `assigned_staff_id`, `assigned_staff_name`) VALUES (33, 'ORD17681879676616', 24, 8, '气相色谱-质谱联用（GC-MS）', 8, '浙江大学材料科学与工程学院', 'completed', 320.00, 0.00, 0.00, 0.00, 320.00, 320.00, 1, 'express', '张三', '13800138001', '测试地址1号', 'balance', '2026-01-09 11:19:28', '2026-01-05 11:19:28', '2026-01-09 11:19:28', '2026-01-10 11:19:28', '2026-01-09 11:19:28', '2026-01-11 11:19:28', NULL, '测试订单-已完成#1', NULL, 0, NULL, 0, 'none', NULL, 'paid', 0.00, 8, 32, '2026-01-12 10:19:28', NULL, NULL);
INSERT INTO `orders` (`id`, `order_no`, `user_id`, `project_id`, `project_name`, `lab_id`, `lab_name`, `status`, `project_fee`, `urgent_fee`, `shipping_fee`, `discount_amount`, `total_fee`, `paid_fee`, `sample_count`, `shipping_method`, `receiver_name`, `receiver_phone`, `receiver_address`, `payment_method`, `payment_time`, `created_at`, `paid_at`, `confirmed_at`, `started_at`, `completed_at`, `cancelled_at`, `remark`, `cancel_reason`, `is_urgent`, `estimated_completion_time`, `is_draft`, `invoice_status`, `invoice_id`, `payment_status`, `credit_amount`, `assigned_lab_id`, `assigned_user_id`, `assigned_at`, `assigned_staff_id`, `assigned_staff_name`) VALUES (34, 'ORD17681879676642', 26, 7, '核磁共振（NMR）', 8, '浙江大学材料科学与工程学院', 'completed', 380.00, 0.00, 0.00, 0.00, 380.00, 380.00, 1, 'express', '王五', '13800138003', '测试地址2号', 'balance', '2026-01-07 11:19:28', '2026-01-01 11:19:28', '2026-01-11 11:19:28', '2026-01-11 11:19:28', '2026-01-09 11:19:28', '2026-01-11 11:19:28', NULL, '测试订单-已完成#2', NULL, 0, NULL, 0, 'none', NULL, 'paid', 0.00, 8, 32, '2026-01-11 19:19:28', NULL, NULL);
INSERT INTO `orders` (`id`, `order_no`, `user_id`, `project_id`, `project_name`, `lab_id`, `lab_name`, `status`, `project_fee`, `urgent_fee`, `shipping_fee`, `discount_amount`, `total_fee`, `paid_fee`, `sample_count`, `shipping_method`, `receiver_name`, `receiver_phone`, `receiver_address`, `payment_method`, `payment_time`, `created_at`, `paid_at`, `confirmed_at`, `started_at`, `completed_at`, `cancelled_at`, `remark`, `cancel_reason`, `is_urgent`, `estimated_completion_time`, `is_draft`, `invoice_status`, `invoice_id`, `payment_status`, `credit_amount`, `assigned_lab_id`, `assigned_user_id`, `assigned_at`, `assigned_staff_id`, `assigned_staff_name`) VALUES (35, 'ORD17681887533026', 26, 5, '热重分析（TGA）', 4, '清华大学材料学院分析测试中心', 'assigned', 160.00, 0.00, 0.00, 0.00, 160.00, 160.00, 3, 'express', '王五', '13800138003', '测试地址1号', 'alipay', '2026-01-11 21:32:34', '2026-01-12 06:32:34', '2026-01-12 10:32:34', NULL, NULL, NULL, NULL, '测试订单-待分配#1', NULL, 1, '2026-01-17 11:32:34', 0, 'none', NULL, 'paid', 0.00, 4, 12, '2026-01-12 06:21:54', NULL, NULL);
INSERT INTO `orders` (`id`, `order_no`, `user_id`, `project_id`, `project_name`, `lab_id`, `lab_name`, `status`, `project_fee`, `urgent_fee`, `shipping_fee`, `discount_amount`, `total_fee`, `paid_fee`, `sample_count`, `shipping_method`, `receiver_name`, `receiver_phone`, `receiver_address`, `payment_method`, `payment_time`, `created_at`, `paid_at`, `confirmed_at`, `started_at`, `completed_at`, `cancelled_at`, `remark`, `cancel_reason`, `is_urgent`, `estimated_completion_time`, `is_draft`, `invoice_status`, `invoice_id`, `payment_status`, `credit_amount`, `assigned_lab_id`, `assigned_user_id`, `assigned_at`, `assigned_staff_id`, `assigned_staff_name`) VALUES (36, 'ORD17681887539199', 25, 4, '红外光谱（FTIR）', 4, '清华大学材料学院分析测试中心', 'pending_assign', 90.00, 0.00, 0.00, 0.00, 90.00, 90.00, 3, 'express', '李四', '13800138002', '测试地址2号', 'wechat', '2026-01-12 05:32:34', '2026-01-10 01:32:34', '2026-01-11 15:32:34', NULL, NULL, NULL, NULL, '测试订单-待分配#2', NULL, 0, '2026-01-17 11:32:34', 0, 'none', NULL, 'paid', 0.00, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `orders` (`id`, `order_no`, `user_id`, `project_id`, `project_name`, `lab_id`, `lab_name`, `status`, `project_fee`, `urgent_fee`, `shipping_fee`, `discount_amount`, `total_fee`, `paid_fee`, `sample_count`, `shipping_method`, `receiver_name`, `receiver_phone`, `receiver_address`, `payment_method`, `payment_time`, `created_at`, `paid_at`, `confirmed_at`, `started_at`, `completed_at`, `cancelled_at`, `remark`, `cancel_reason`, `is_urgent`, `estimated_completion_time`, `is_draft`, `invoice_status`, `invoice_id`, `payment_status`, `credit_amount`, `assigned_lab_id`, `assigned_user_id`, `assigned_at`, `assigned_staff_id`, `assigned_staff_name`) VALUES (37, 'ORD17681887531868', 26, 4, '红外光谱（FTIR）', 4, '清华大学材料学院分析测试中心', 'paid', 90.00, 0.00, 0.00, 0.00, 90.00, 90.00, 3, 'express', '王五', '13800138003', '测试地址3号', 'alipay', '2026-01-10 12:32:34', '2026-01-11 18:32:34', '2026-01-12 01:32:34', NULL, NULL, NULL, NULL, '测试订单-待分配#3', NULL, 1, '2026-01-17 11:32:34', 0, 'none', NULL, 'paid', 0.00, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `orders` (`id`, `order_no`, `user_id`, `project_id`, `project_name`, `lab_id`, `lab_name`, `status`, `project_fee`, `urgent_fee`, `shipping_fee`, `discount_amount`, `total_fee`, `paid_fee`, `sample_count`, `shipping_method`, `receiver_name`, `receiver_phone`, `receiver_address`, `payment_method`, `payment_time`, `created_at`, `paid_at`, `confirmed_at`, `started_at`, `completed_at`, `cancelled_at`, `remark`, `cancel_reason`, `is_urgent`, `estimated_completion_time`, `is_draft`, `invoice_status`, `invoice_id`, `payment_status`, `credit_amount`, `assigned_lab_id`, `assigned_user_id`, `assigned_at`, `assigned_staff_id`, `assigned_staff_name`) VALUES (38, 'ORD17681887539122', 25, 1, '扫描电镜（SEM）', 4, '清华大学材料学院分析测试中心', 'pending_assign', 180.00, 0.00, 0.00, 0.00, 180.00, 180.00, 3, 'express', '李四', '13800138002', '测试地址4号', 'wechat', '2026-01-10 22:32:34', '2026-01-11 04:32:34', '2026-01-12 00:32:34', NULL, NULL, NULL, NULL, '测试订单-待分配#4', NULL, 0, '2026-01-17 11:32:34', 0, 'none', NULL, 'paid', 0.00, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `orders` (`id`, `order_no`, `user_id`, `project_id`, `project_name`, `lab_id`, `lab_name`, `status`, `project_fee`, `urgent_fee`, `shipping_fee`, `discount_amount`, `total_fee`, `paid_fee`, `sample_count`, `shipping_method`, `receiver_name`, `receiver_phone`, `receiver_address`, `payment_method`, `payment_time`, `created_at`, `paid_at`, `confirmed_at`, `started_at`, `completed_at`, `cancelled_at`, `remark`, `cancel_reason`, `is_urgent`, `estimated_completion_time`, `is_draft`, `invoice_status`, `invoice_id`, `payment_status`, `credit_amount`, `assigned_lab_id`, `assigned_user_id`, `assigned_at`, `assigned_staff_id`, `assigned_staff_name`) VALUES (39, 'ORD17681887532001', 26, 8, '气相色谱-质谱联用（GC-MS）', 4, '清华大学材料学院分析测试中心', 'pending_assign', 320.00, 0.00, 0.00, 0.00, 320.00, 320.00, 3, 'express', '王五', '13800138003', '测试地址5号', 'balance', '2026-01-10 16:32:34', '2026-01-10 12:32:34', '2026-01-11 06:32:34', NULL, NULL, NULL, NULL, '测试订单-待分配#5', NULL, 1, '2026-01-16 11:32:34', 0, 'none', NULL, 'paid', 0.00, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `orders` (`id`, `order_no`, `user_id`, `project_id`, `project_name`, `lab_id`, `lab_name`, `status`, `project_fee`, `urgent_fee`, `shipping_fee`, `discount_amount`, `total_fee`, `paid_fee`, `sample_count`, `shipping_method`, `receiver_name`, `receiver_phone`, `receiver_address`, `payment_method`, `payment_time`, `created_at`, `paid_at`, `confirmed_at`, `started_at`, `completed_at`, `cancelled_at`, `remark`, `cancel_reason`, `is_urgent`, `estimated_completion_time`, `is_draft`, `invoice_status`, `invoice_id`, `payment_status`, `credit_amount`, `assigned_lab_id`, `assigned_user_id`, `assigned_at`, `assigned_staff_id`, `assigned_staff_name`) VALUES (40, 'ORD17681887537320', 26, 2, '透射电镜（TEM）', 4, '清华大学材料学院分析测试中心', 'paid', 280.00, 0.00, 0.00, 0.00, 280.00, 280.00, 3, 'express', '王五', '13800138003', '测试地址6号', 'wechat', '2026-01-12 00:32:34', '2026-01-11 18:32:34', '2026-01-12 09:32:34', NULL, NULL, NULL, NULL, '测试订单-待分配#6', NULL, 0, '2026-01-18 11:32:34', 0, 'none', NULL, 'paid', 0.00, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `orders` (`id`, `order_no`, `user_id`, `project_id`, `project_name`, `lab_id`, `lab_name`, `status`, `project_fee`, `urgent_fee`, `shipping_fee`, `discount_amount`, `total_fee`, `paid_fee`, `sample_count`, `shipping_method`, `receiver_name`, `receiver_phone`, `receiver_address`, `payment_method`, `payment_time`, `created_at`, `paid_at`, `confirmed_at`, `started_at`, `completed_at`, `cancelled_at`, `remark`, `cancel_reason`, `is_urgent`, `estimated_completion_time`, `is_draft`, `invoice_status`, `invoice_id`, `payment_status`, `credit_amount`, `assigned_lab_id`, `assigned_user_id`, `assigned_at`, `assigned_staff_id`, `assigned_staff_name`) VALUES (41, 'ORD17681887535145', 25, 1, '扫描电镜（SEM）', 4, '清华大学材料学院分析测试中心', 'paid', 180.00, 0.00, 0.00, 0.00, 180.00, 180.00, 2, 'express', '李四', '13800138002', '测试地址7号', 'alipay', '2026-01-12 07:32:34', '2026-01-10 23:32:34', '2026-01-10 14:32:34', NULL, NULL, NULL, NULL, '测试订单-待分配#7', NULL, 1, '2026-01-18 11:32:34', 0, 'none', NULL, 'paid', 0.00, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `orders` (`id`, `order_no`, `user_id`, `project_id`, `project_name`, `lab_id`, `lab_name`, `status`, `project_fee`, `urgent_fee`, `shipping_fee`, `discount_amount`, `total_fee`, `paid_fee`, `sample_count`, `shipping_method`, `receiver_name`, `receiver_phone`, `receiver_address`, `payment_method`, `payment_time`, `created_at`, `paid_at`, `confirmed_at`, `started_at`, `completed_at`, `cancelled_at`, `remark`, `cancel_reason`, `is_urgent`, `estimated_completion_time`, `is_draft`, `invoice_status`, `invoice_id`, `payment_status`, `credit_amount`, `assigned_lab_id`, `assigned_user_id`, `assigned_at`, `assigned_staff_id`, `assigned_staff_name`) VALUES (42, 'ORD17681887537192', 25, 1, '扫描电镜（SEM）', 4, '清华大学材料学院分析测试中心', 'pending_assign', 180.00, 0.00, 0.00, 0.00, 180.00, 180.00, 1, 'express', '李四', '13800138002', '测试地址8号', 'alipay', '2026-01-10 14:32:34', '2026-01-11 03:32:34', '2026-01-10 21:32:34', NULL, NULL, NULL, NULL, '测试订单-待分配#8', NULL, 0, '2026-01-18 11:32:34', 0, 'none', NULL, 'paid', 0.00, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `orders` (`id`, `order_no`, `user_id`, `project_id`, `project_name`, `lab_id`, `lab_name`, `status`, `project_fee`, `urgent_fee`, `shipping_fee`, `discount_amount`, `total_fee`, `paid_fee`, `sample_count`, `shipping_method`, `receiver_name`, `receiver_phone`, `receiver_address`, `payment_method`, `payment_time`, `created_at`, `paid_at`, `confirmed_at`, `started_at`, `completed_at`, `cancelled_at`, `remark`, `cancel_reason`, `is_urgent`, `estimated_completion_time`, `is_draft`, `invoice_status`, `invoice_id`, `payment_status`, `credit_amount`, `assigned_lab_id`, `assigned_user_id`, `assigned_at`, `assigned_staff_id`, `assigned_staff_name`) VALUES (43, 'ORD17681887533968', 26, 7, '核磁共振（NMR）', 4, '清华大学材料学院分析测试中心', 'pending_assign', 380.00, 0.00, 0.00, 0.00, 380.00, 380.00, 2, 'express', '王五', '13800138003', '测试地址9号', 'alipay', '2026-01-12 04:32:34', '2026-01-10 06:32:34', '2026-01-12 07:32:34', NULL, NULL, NULL, NULL, '测试订单-待分配#9', NULL, 1, '2026-01-17 11:32:34', 0, 'none', NULL, 'paid', 0.00, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `orders` (`id`, `order_no`, `user_id`, `project_id`, `project_name`, `lab_id`, `lab_name`, `status`, `project_fee`, `urgent_fee`, `shipping_fee`, `discount_amount`, `total_fee`, `paid_fee`, `sample_count`, `shipping_method`, `receiver_name`, `receiver_phone`, `receiver_address`, `payment_method`, `payment_time`, `created_at`, `paid_at`, `confirmed_at`, `started_at`, `completed_at`, `cancelled_at`, `remark`, `cancel_reason`, `is_urgent`, `estimated_completion_time`, `is_draft`, `invoice_status`, `invoice_id`, `payment_status`, `credit_amount`, `assigned_lab_id`, `assigned_user_id`, `assigned_at`, `assigned_staff_id`, `assigned_staff_name`) VALUES (44, 'ORD17681887535952', 25, 1, '扫描电镜（SEM）', 4, '清华大学材料学院分析测试中心', 'paid', 180.00, 0.00, 0.00, 0.00, 180.00, 180.00, 3, 'express', '李四', '13800138002', '测试地址10号', 'balance', '2026-01-12 02:32:34', '2026-01-09 18:32:34', '2026-01-11 01:32:34', NULL, NULL, NULL, NULL, '测试订单-待分配#10', NULL, 1, '2026-01-15 11:32:34', 0, 'none', NULL, 'paid', 0.00, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `orders` (`id`, `order_no`, `user_id`, `project_id`, `project_name`, `lab_id`, `lab_name`, `status`, `project_fee`, `urgent_fee`, `shipping_fee`, `discount_amount`, `total_fee`, `paid_fee`, `sample_count`, `shipping_method`, `receiver_name`, `receiver_phone`, `receiver_address`, `payment_method`, `payment_time`, `created_at`, `paid_at`, `confirmed_at`, `started_at`, `completed_at`, `cancelled_at`, `remark`, `cancel_reason`, `is_urgent`, `estimated_completion_time`, `is_draft`, `invoice_status`, `invoice_id`, `payment_status`, `credit_amount`, `assigned_lab_id`, `assigned_user_id`, `assigned_at`, `assigned_staff_id`, `assigned_staff_name`) VALUES (45, 'ORD17681887537606', 24, 1, '扫描电镜（SEM）', 6, '上海交通大学分析测试中心', 'assigned', 180.00, 0.00, 0.00, 0.00, 180.00, 180.00, 1, 'express', '张三', '13800138001', '测试地址1号', 'balance', '2026-01-08 11:32:34', '2025-12-29 11:32:34', '2026-01-06 11:32:34', NULL, NULL, NULL, NULL, '测试订单-已分配待接单#1', NULL, 0, NULL, 0, 'none', NULL, 'paid', 0.00, 6, 32, '2026-01-11 12:32:34', NULL, NULL);
INSERT INTO `orders` (`id`, `order_no`, `user_id`, `project_id`, `project_name`, `lab_id`, `lab_name`, `status`, `project_fee`, `urgent_fee`, `shipping_fee`, `discount_amount`, `total_fee`, `paid_fee`, `sample_count`, `shipping_method`, `receiver_name`, `receiver_phone`, `receiver_address`, `payment_method`, `payment_time`, `created_at`, `paid_at`, `confirmed_at`, `started_at`, `completed_at`, `cancelled_at`, `remark`, `cancel_reason`, `is_urgent`, `estimated_completion_time`, `is_draft`, `invoice_status`, `invoice_id`, `payment_status`, `credit_amount`, `assigned_lab_id`, `assigned_user_id`, `assigned_at`, `assigned_staff_id`, `assigned_staff_name`) VALUES (46, 'ORD17681887539740', 26, 1, '扫描电镜（SEM）', 7, '复旦大学材料科学系测试中心', 'assigned', 180.00, 0.00, 0.00, 0.00, 180.00, 180.00, 1, 'express', '王五', '13800138003', '测试地址2号', 'balance', '2026-01-10 11:32:34', '2025-12-29 11:32:34', '2026-01-06 11:32:34', NULL, NULL, NULL, NULL, '测试订单-已分配待接单#2', NULL, 0, NULL, 0, 'none', NULL, 'paid', 0.00, 7, 32, '2026-01-12 01:32:34', NULL, NULL);
INSERT INTO `orders` (`id`, `order_no`, `user_id`, `project_id`, `project_name`, `lab_id`, `lab_name`, `status`, `project_fee`, `urgent_fee`, `shipping_fee`, `discount_amount`, `total_fee`, `paid_fee`, `sample_count`, `shipping_method`, `receiver_name`, `receiver_phone`, `receiver_address`, `payment_method`, `payment_time`, `created_at`, `paid_at`, `confirmed_at`, `started_at`, `completed_at`, `cancelled_at`, `remark`, `cancel_reason`, `is_urgent`, `estimated_completion_time`, `is_draft`, `invoice_status`, `invoice_id`, `payment_status`, `credit_amount`, `assigned_lab_id`, `assigned_user_id`, `assigned_at`, `assigned_staff_id`, `assigned_staff_name`) VALUES (47, 'ORD17681887536778', 25, 7, '核磁共振（NMR）', 4, '清华大学材料学院分析测试中心', 'accepted', 380.00, 0.00, 0.00, 0.00, 380.00, 380.00, 1, 'express', '李四', '13800138002', '测试地址1号', 'balance', '2026-01-08 11:32:34', '2026-01-04 11:32:34', '2026-01-06 11:32:34', NULL, NULL, NULL, NULL, '测试订单-实验室已接单#1', NULL, 0, NULL, 0, 'none', NULL, 'paid', 0.00, 4, 32, '2026-01-11 13:32:34', NULL, NULL);
INSERT INTO `orders` (`id`, `order_no`, `user_id`, `project_id`, `project_name`, `lab_id`, `lab_name`, `status`, `project_fee`, `urgent_fee`, `shipping_fee`, `discount_amount`, `total_fee`, `paid_fee`, `sample_count`, `shipping_method`, `receiver_name`, `receiver_phone`, `receiver_address`, `payment_method`, `payment_time`, `created_at`, `paid_at`, `confirmed_at`, `started_at`, `completed_at`, `cancelled_at`, `remark`, `cancel_reason`, `is_urgent`, `estimated_completion_time`, `is_draft`, `invoice_status`, `invoice_id`, `payment_status`, `credit_amount`, `assigned_lab_id`, `assigned_user_id`, `assigned_at`, `assigned_staff_id`, `assigned_staff_name`) VALUES (48, 'ORD17681887539241', 26, 2, '透射电镜（TEM）', 8, '浙江大学材料科学与工程学院', 'accepted', 280.00, 0.00, 0.00, 0.00, 280.00, 280.00, 1, 'express', '王五', '13800138003', '测试地址2号', 'balance', '2026-01-08 11:32:34', '2026-01-09 11:32:34', '2026-01-05 11:32:34', NULL, NULL, NULL, NULL, '测试订单-实验室已接单#2', NULL, 0, NULL, 0, 'none', NULL, 'paid', 0.00, 8, 32, '2026-01-11 16:32:34', NULL, NULL);
INSERT INTO `orders` (`id`, `order_no`, `user_id`, `project_id`, `project_name`, `lab_id`, `lab_name`, `status`, `project_fee`, `urgent_fee`, `shipping_fee`, `discount_amount`, `total_fee`, `paid_fee`, `sample_count`, `shipping_method`, `receiver_name`, `receiver_phone`, `receiver_address`, `payment_method`, `payment_time`, `created_at`, `paid_at`, `confirmed_at`, `started_at`, `completed_at`, `cancelled_at`, `remark`, `cancel_reason`, `is_urgent`, `estimated_completion_time`, `is_draft`, `invoice_status`, `invoice_id`, `payment_status`, `credit_amount`, `assigned_lab_id`, `assigned_user_id`, `assigned_at`, `assigned_staff_id`, `assigned_staff_name`) VALUES (49, 'ORD17681887539288', 24, 8, '气相色谱-质谱联用（GC-MS）', 6, '上海交通大学分析测试中心', 'testing', 320.00, 0.00, 0.00, 0.00, 320.00, 320.00, 1, 'express', '张三', '13800138001', '测试地址1号', 'balance', '2026-01-11 11:32:34', '2026-01-10 11:32:34', '2026-01-07 11:32:34', '2026-01-10 11:32:34', '2026-01-10 11:32:34', NULL, NULL, '测试订单-检测中#1', NULL, 0, NULL, 0, 'none', NULL, 'paid', 0.00, 6, 32, '2026-01-11 23:32:34', NULL, NULL);
INSERT INTO `orders` (`id`, `order_no`, `user_id`, `project_id`, `project_name`, `lab_id`, `lab_name`, `status`, `project_fee`, `urgent_fee`, `shipping_fee`, `discount_amount`, `total_fee`, `paid_fee`, `sample_count`, `shipping_method`, `receiver_name`, `receiver_phone`, `receiver_address`, `payment_method`, `payment_time`, `created_at`, `paid_at`, `confirmed_at`, `started_at`, `completed_at`, `cancelled_at`, `remark`, `cancel_reason`, `is_urgent`, `estimated_completion_time`, `is_draft`, `invoice_status`, `invoice_id`, `payment_status`, `credit_amount`, `assigned_lab_id`, `assigned_user_id`, `assigned_at`, `assigned_staff_id`, `assigned_staff_name`) VALUES (50, 'ORD17681887538803', 24, 5, '热重分析（TGA）', 5, '北京大学化学与分子工程学院测试中心', 'testing', 160.00, 0.00, 0.00, 0.00, 160.00, 160.00, 1, 'express', '张三', '13800138001', '测试地址2号', 'balance', '2026-01-09 11:32:34', '2025-12-29 11:32:34', '2026-01-11 11:32:34', '2026-01-09 11:32:34', '2026-01-11 11:32:34', NULL, NULL, '测试订单-检测中#2', NULL, 0, NULL, 0, 'none', NULL, 'paid', 0.00, 5, 32, '2026-01-12 08:32:34', NULL, NULL);
INSERT INTO `orders` (`id`, `order_no`, `user_id`, `project_id`, `project_name`, `lab_id`, `lab_name`, `status`, `project_fee`, `urgent_fee`, `shipping_fee`, `discount_amount`, `total_fee`, `paid_fee`, `sample_count`, `shipping_method`, `receiver_name`, `receiver_phone`, `receiver_address`, `payment_method`, `payment_time`, `created_at`, `paid_at`, `confirmed_at`, `started_at`, `completed_at`, `cancelled_at`, `remark`, `cancel_reason`, `is_urgent`, `estimated_completion_time`, `is_draft`, `invoice_status`, `invoice_id`, `payment_status`, `credit_amount`, `assigned_lab_id`, `assigned_user_id`, `assigned_at`, `assigned_staff_id`, `assigned_staff_name`) VALUES (51, 'ORD17681887533290', 25, 1, '扫描电镜（SEM）', 8, '浙江大学材料科学与工程学院', 'completed', 180.00, 0.00, 0.00, 0.00, 180.00, 180.00, 1, 'express', '李四', '13800138002', '测试地址1号', 'balance', '2026-01-10 11:32:34', '2025-12-30 11:32:34', '2026-01-09 11:32:34', '2026-01-09 11:32:34', '2026-01-10 11:32:34', '2026-01-11 11:32:34', NULL, '测试订单-已完成#1', NULL, 0, NULL, 0, 'none', NULL, 'paid', 0.00, 8, 32, '2026-01-12 04:32:34', NULL, NULL);
INSERT INTO `orders` (`id`, `order_no`, `user_id`, `project_id`, `project_name`, `lab_id`, `lab_name`, `status`, `project_fee`, `urgent_fee`, `shipping_fee`, `discount_amount`, `total_fee`, `paid_fee`, `sample_count`, `shipping_method`, `receiver_name`, `receiver_phone`, `receiver_address`, `payment_method`, `payment_time`, `created_at`, `paid_at`, `confirmed_at`, `started_at`, `completed_at`, `cancelled_at`, `remark`, `cancel_reason`, `is_urgent`, `estimated_completion_time`, `is_draft`, `invoice_status`, `invoice_id`, `payment_status`, `credit_amount`, `assigned_lab_id`, `assigned_user_id`, `assigned_at`, `assigned_staff_id`, `assigned_staff_name`) VALUES (52, 'ORD17681887535159', 25, 3, 'X射线衍射（XRD）', 4, '清华大学材料学院分析测试中心', 'completed', 130.00, 0.00, 0.00, 0.00, 130.00, 130.00, 1, 'express', '李四', '13800138002', '测试地址2号', 'balance', '2026-01-11 11:32:34', '2026-01-02 11:32:34', '2026-01-08 11:32:34', '2026-01-10 11:32:34', '2026-01-09 11:32:34', '2026-01-11 11:32:34', NULL, '测试订单-已完成#2', NULL, 0, NULL, 0, 'none', NULL, 'paid', 0.00, 4, 32, '2026-01-11 22:32:34', NULL, NULL);
INSERT INTO `orders` (`id`, `order_no`, `user_id`, `project_id`, `project_name`, `lab_id`, `lab_name`, `status`, `project_fee`, `urgent_fee`, `shipping_fee`, `discount_amount`, `total_fee`, `paid_fee`, `sample_count`, `shipping_method`, `receiver_name`, `receiver_phone`, `receiver_address`, `payment_method`, `payment_time`, `created_at`, `paid_at`, `confirmed_at`, `started_at`, `completed_at`, `cancelled_at`, `remark`, `cancel_reason`, `is_urgent`, `estimated_completion_time`, `is_draft`, `invoice_status`, `invoice_id`, `payment_status`, `credit_amount`, `assigned_lab_id`, `assigned_user_id`, `assigned_at`, `assigned_staff_id`, `assigned_staff_name`) VALUES (53, 'ORD17681891933625', 24, 1, '扫描电镜（SEM）', 4, '清华大学材料学院分析测试中心', 'pending_assign', 180.00, 0.00, 0.00, 0.00, 180.00, 180.00, 3, 'express', '张三', '13800138001', '测试地址1号', 'alipay', '2026-01-10 19:39:53', '2026-01-09 16:39:53', '2026-01-10 18:39:53', NULL, NULL, NULL, NULL, '测试订单-待分配#1', NULL, 0, '2026-01-16 11:39:53', 0, 'none', NULL, 'paid', 0.00, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `orders` (`id`, `order_no`, `user_id`, `project_id`, `project_name`, `lab_id`, `lab_name`, `status`, `project_fee`, `urgent_fee`, `shipping_fee`, `discount_amount`, `total_fee`, `paid_fee`, `sample_count`, `shipping_method`, `receiver_name`, `receiver_phone`, `receiver_address`, `payment_method`, `payment_time`, `created_at`, `paid_at`, `confirmed_at`, `started_at`, `completed_at`, `cancelled_at`, `remark`, `cancel_reason`, `is_urgent`, `estimated_completion_time`, `is_draft`, `invoice_status`, `invoice_id`, `payment_status`, `credit_amount`, `assigned_lab_id`, `assigned_user_id`, `assigned_at`, `assigned_staff_id`, `assigned_staff_name`) VALUES (54, 'ORD17681891932164', 25, 2, '透射电镜（TEM）', 4, '清华大学材料学院分析测试中心', 'pending_assign', 280.00, 0.00, 0.00, 0.00, 280.00, 280.00, 1, 'express', '李四', '13800138002', '测试地址2号', 'wechat', '2026-01-11 17:39:53', '2026-01-11 00:39:53', '2026-01-10 15:39:53', NULL, NULL, NULL, NULL, '测试订单-待分配#2', NULL, 0, '2026-01-18 11:39:53', 0, 'none', NULL, 'paid', 0.00, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `orders` (`id`, `order_no`, `user_id`, `project_id`, `project_name`, `lab_id`, `lab_name`, `status`, `project_fee`, `urgent_fee`, `shipping_fee`, `discount_amount`, `total_fee`, `paid_fee`, `sample_count`, `shipping_method`, `receiver_name`, `receiver_phone`, `receiver_address`, `payment_method`, `payment_time`, `created_at`, `paid_at`, `confirmed_at`, `started_at`, `completed_at`, `cancelled_at`, `remark`, `cancel_reason`, `is_urgent`, `estimated_completion_time`, `is_draft`, `invoice_status`, `invoice_id`, `payment_status`, `credit_amount`, `assigned_lab_id`, `assigned_user_id`, `assigned_at`, `assigned_staff_id`, `assigned_staff_name`) VALUES (55, 'ORD17681891939778', 25, 7, '核磁共振（NMR）', 4, '清华大学材料学院分析测试中心', 'assigned', 380.00, 0.00, 0.00, 0.00, 380.00, 380.00, 3, 'express', '李四', '13800138002', '测试地址3号', 'alipay', '2026-01-12 07:39:53', '2026-01-12 05:39:53', '2026-01-12 04:39:53', NULL, NULL, NULL, NULL, '测试订单-待分配#3', NULL, 1, '2026-01-15 11:39:53', 0, 'none', NULL, 'paid', 0.00, 5, 12, '2026-01-12 08:55:35', NULL, NULL);
INSERT INTO `orders` (`id`, `order_no`, `user_id`, `project_id`, `project_name`, `lab_id`, `lab_name`, `status`, `project_fee`, `urgent_fee`, `shipping_fee`, `discount_amount`, `total_fee`, `paid_fee`, `sample_count`, `shipping_method`, `receiver_name`, `receiver_phone`, `receiver_address`, `payment_method`, `payment_time`, `created_at`, `paid_at`, `confirmed_at`, `started_at`, `completed_at`, `cancelled_at`, `remark`, `cancel_reason`, `is_urgent`, `estimated_completion_time`, `is_draft`, `invoice_status`, `invoice_id`, `payment_status`, `credit_amount`, `assigned_lab_id`, `assigned_user_id`, `assigned_at`, `assigned_staff_id`, `assigned_staff_name`) VALUES (56, 'ORD17681891935196', 25, 1, '扫描电镜（SEM）', 4, '清华大学材料学院分析测试中心', 'paid', 180.00, 0.00, 0.00, 0.00, 180.00, 180.00, 2, 'express', '李四', '13800138002', '测试地址4号', 'alipay', '2026-01-11 13:39:53', '2026-01-09 15:39:53', '2026-01-12 00:39:53', NULL, NULL, NULL, NULL, '测试订单-待分配#4', NULL, 0, '2026-01-18 11:39:53', 0, 'none', NULL, 'paid', 0.00, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `orders` (`id`, `order_no`, `user_id`, `project_id`, `project_name`, `lab_id`, `lab_name`, `status`, `project_fee`, `urgent_fee`, `shipping_fee`, `discount_amount`, `total_fee`, `paid_fee`, `sample_count`, `shipping_method`, `receiver_name`, `receiver_phone`, `receiver_address`, `payment_method`, `payment_time`, `created_at`, `paid_at`, `confirmed_at`, `started_at`, `completed_at`, `cancelled_at`, `remark`, `cancel_reason`, `is_urgent`, `estimated_completion_time`, `is_draft`, `invoice_status`, `invoice_id`, `payment_status`, `credit_amount`, `assigned_lab_id`, `assigned_user_id`, `assigned_at`, `assigned_staff_id`, `assigned_staff_name`) VALUES (57, 'ORD17681891939645', 24, 6, '万能材料试验机', 4, '清华大学材料学院分析测试中心', 'paid', 230.00, 0.00, 0.00, 0.00, 230.00, 230.00, 3, 'express', '张三', '13800138001', '测试地址5号', 'balance', '2026-01-11 18:39:54', '2026-01-10 17:39:54', '2026-01-10 22:39:54', NULL, NULL, NULL, NULL, '测试订单-待分配#5', NULL, 1, '2026-01-19 11:39:54', 0, 'none', NULL, 'paid', 0.00, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `orders` (`id`, `order_no`, `user_id`, `project_id`, `project_name`, `lab_id`, `lab_name`, `status`, `project_fee`, `urgent_fee`, `shipping_fee`, `discount_amount`, `total_fee`, `paid_fee`, `sample_count`, `shipping_method`, `receiver_name`, `receiver_phone`, `receiver_address`, `payment_method`, `payment_time`, `created_at`, `paid_at`, `confirmed_at`, `started_at`, `completed_at`, `cancelled_at`, `remark`, `cancel_reason`, `is_urgent`, `estimated_completion_time`, `is_draft`, `invoice_status`, `invoice_id`, `payment_status`, `credit_amount`, `assigned_lab_id`, `assigned_user_id`, `assigned_at`, `assigned_staff_id`, `assigned_staff_name`) VALUES (58, 'ORD17681891934890', 24, 3, 'X射线衍射（XRD）', 4, '清华大学材料学院分析测试中心', 'assigned', 130.00, 0.00, 0.00, 0.00, 130.00, 130.00, 2, 'express', '张三', '13800138001', '测试地址6号', 'alipay', '2026-01-11 06:39:54', '2026-01-12 01:39:54', '2026-01-12 04:39:54', NULL, NULL, NULL, NULL, '测试订单-待分配#6', NULL, 0, '2026-01-16 11:39:54', 0, 'none', NULL, 'paid', 0.00, 4, 12, '2026-01-12 11:09:29', NULL, NULL);
INSERT INTO `orders` (`id`, `order_no`, `user_id`, `project_id`, `project_name`, `lab_id`, `lab_name`, `status`, `project_fee`, `urgent_fee`, `shipping_fee`, `discount_amount`, `total_fee`, `paid_fee`, `sample_count`, `shipping_method`, `receiver_name`, `receiver_phone`, `receiver_address`, `payment_method`, `payment_time`, `created_at`, `paid_at`, `confirmed_at`, `started_at`, `completed_at`, `cancelled_at`, `remark`, `cancel_reason`, `is_urgent`, `estimated_completion_time`, `is_draft`, `invoice_status`, `invoice_id`, `payment_status`, `credit_amount`, `assigned_lab_id`, `assigned_user_id`, `assigned_at`, `assigned_staff_id`, `assigned_staff_name`) VALUES (59, 'ORD17681891936744', 26, 7, '核磁共振（NMR）', 4, '清华大学材料学院分析测试中心', 'pending_assign', 380.00, 0.00, 0.00, 0.00, 380.00, 380.00, 1, 'express', '王五', '13800138003', '测试地址7号', 'alipay', '2026-01-10 23:39:54', '2026-01-11 01:39:54', '2026-01-11 03:39:54', NULL, NULL, NULL, NULL, '测试订单-待分配#7', NULL, 0, '2026-01-19 11:39:54', 0, 'none', NULL, 'paid', 0.00, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `orders` (`id`, `order_no`, `user_id`, `project_id`, `project_name`, `lab_id`, `lab_name`, `status`, `project_fee`, `urgent_fee`, `shipping_fee`, `discount_amount`, `total_fee`, `paid_fee`, `sample_count`, `shipping_method`, `receiver_name`, `receiver_phone`, `receiver_address`, `payment_method`, `payment_time`, `created_at`, `paid_at`, `confirmed_at`, `started_at`, `completed_at`, `cancelled_at`, `remark`, `cancel_reason`, `is_urgent`, `estimated_completion_time`, `is_draft`, `invoice_status`, `invoice_id`, `payment_status`, `credit_amount`, `assigned_lab_id`, `assigned_user_id`, `assigned_at`, `assigned_staff_id`, `assigned_staff_name`) VALUES (60, 'ORD17681891932202', 26, 1, '扫描电镜（SEM）', 4, '清华大学材料学院分析测试中心', 'paid', 180.00, 0.00, 0.00, 0.00, 180.00, 180.00, 2, 'express', '王五', '13800138003', '测试地址8号', 'balance', '2026-01-12 09:39:54', '2026-01-10 12:39:54', '2026-01-11 12:39:54', NULL, NULL, NULL, NULL, '测试订单-待分配#8', NULL, 0, '2026-01-18 11:39:54', 0, 'none', NULL, 'paid', 0.00, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `orders` (`id`, `order_no`, `user_id`, `project_id`, `project_name`, `lab_id`, `lab_name`, `status`, `project_fee`, `urgent_fee`, `shipping_fee`, `discount_amount`, `total_fee`, `paid_fee`, `sample_count`, `shipping_method`, `receiver_name`, `receiver_phone`, `receiver_address`, `payment_method`, `payment_time`, `created_at`, `paid_at`, `confirmed_at`, `started_at`, `completed_at`, `cancelled_at`, `remark`, `cancel_reason`, `is_urgent`, `estimated_completion_time`, `is_draft`, `invoice_status`, `invoice_id`, `payment_status`, `credit_amount`, `assigned_lab_id`, `assigned_user_id`, `assigned_at`, `assigned_staff_id`, `assigned_staff_name`) VALUES (61, 'ORD17681891939196', 24, 2, '透射电镜（TEM）', 4, '清华大学材料学院分析测试中心', 'pending_assign', 280.00, 0.00, 0.00, 0.00, 280.00, 280.00, 1, 'express', '张三', '13800138001', '测试地址9号', 'wechat', '2026-01-12 02:39:54', '2026-01-11 00:39:54', '2026-01-12 04:39:54', NULL, NULL, NULL, NULL, '测试订单-待分配#9', NULL, 1, '2026-01-15 11:39:54', 0, 'none', NULL, 'paid', 0.00, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `orders` (`id`, `order_no`, `user_id`, `project_id`, `project_name`, `lab_id`, `lab_name`, `status`, `project_fee`, `urgent_fee`, `shipping_fee`, `discount_amount`, `total_fee`, `paid_fee`, `sample_count`, `shipping_method`, `receiver_name`, `receiver_phone`, `receiver_address`, `payment_method`, `payment_time`, `created_at`, `paid_at`, `confirmed_at`, `started_at`, `completed_at`, `cancelled_at`, `remark`, `cancel_reason`, `is_urgent`, `estimated_completion_time`, `is_draft`, `invoice_status`, `invoice_id`, `payment_status`, `credit_amount`, `assigned_lab_id`, `assigned_user_id`, `assigned_at`, `assigned_staff_id`, `assigned_staff_name`) VALUES (62, 'ORD17681891935229', 26, 4, '红外光谱（FTIR）', 4, '清华大学材料学院分析测试中心', 'paid', 90.00, 0.00, 0.00, 0.00, 90.00, 90.00, 3, 'express', '王五', '13800138003', '测试地址10号', 'alipay', '2026-01-12 00:39:54', '2026-01-10 05:39:54', '2026-01-11 13:39:54', NULL, NULL, NULL, NULL, '测试订单-待分配#10', NULL, 0, '2026-01-17 11:39:54', 0, 'none', NULL, 'paid', 0.00, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `orders` (`id`, `order_no`, `user_id`, `project_id`, `project_name`, `lab_id`, `lab_name`, `status`, `project_fee`, `urgent_fee`, `shipping_fee`, `discount_amount`, `total_fee`, `paid_fee`, `sample_count`, `shipping_method`, `receiver_name`, `receiver_phone`, `receiver_address`, `payment_method`, `payment_time`, `created_at`, `paid_at`, `confirmed_at`, `started_at`, `completed_at`, `cancelled_at`, `remark`, `cancel_reason`, `is_urgent`, `estimated_completion_time`, `is_draft`, `invoice_status`, `invoice_id`, `payment_status`, `credit_amount`, `assigned_lab_id`, `assigned_user_id`, `assigned_at`, `assigned_staff_id`, `assigned_staff_name`) VALUES (63, 'ORD17681891937042', 26, 4, '红外光谱（FTIR）', 5, '北京大学化学与分子工程学院测试中心', 'assigned', 90.00, 0.00, 0.00, 0.00, 90.00, 90.00, 1, 'express', '王五', '13800138003', '测试地址1号', 'balance', '2026-01-07 11:39:54', '2026-01-11 11:39:54', '2026-01-10 11:39:54', NULL, NULL, NULL, NULL, '测试订单-已分配待接单#1', NULL, 0, NULL, 0, 'none', NULL, 'paid', 0.00, 5, 32, '2026-01-11 22:39:54', NULL, NULL);
INSERT INTO `orders` (`id`, `order_no`, `user_id`, `project_id`, `project_name`, `lab_id`, `lab_name`, `status`, `project_fee`, `urgent_fee`, `shipping_fee`, `discount_amount`, `total_fee`, `paid_fee`, `sample_count`, `shipping_method`, `receiver_name`, `receiver_phone`, `receiver_address`, `payment_method`, `payment_time`, `created_at`, `paid_at`, `confirmed_at`, `started_at`, `completed_at`, `cancelled_at`, `remark`, `cancel_reason`, `is_urgent`, `estimated_completion_time`, `is_draft`, `invoice_status`, `invoice_id`, `payment_status`, `credit_amount`, `assigned_lab_id`, `assigned_user_id`, `assigned_at`, `assigned_staff_id`, `assigned_staff_name`) VALUES (64, 'ORD17681891935657', 25, 7, '核磁共振（NMR）', 6, '上海交通大学分析测试中心', 'assigned', 380.00, 0.00, 0.00, 0.00, 380.00, 380.00, 1, 'express', '李四', '13800138002', '测试地址2号', 'balance', '2026-01-07 11:39:54', '2026-01-10 11:39:54', '2026-01-11 11:39:54', NULL, NULL, NULL, NULL, '测试订单-已分配待接单#2', NULL, 0, NULL, 0, 'none', NULL, 'paid', 0.00, 6, 32, '2026-01-12 00:39:54', NULL, NULL);
INSERT INTO `orders` (`id`, `order_no`, `user_id`, `project_id`, `project_name`, `lab_id`, `lab_name`, `status`, `project_fee`, `urgent_fee`, `shipping_fee`, `discount_amount`, `total_fee`, `paid_fee`, `sample_count`, `shipping_method`, `receiver_name`, `receiver_phone`, `receiver_address`, `payment_method`, `payment_time`, `created_at`, `paid_at`, `confirmed_at`, `started_at`, `completed_at`, `cancelled_at`, `remark`, `cancel_reason`, `is_urgent`, `estimated_completion_time`, `is_draft`, `invoice_status`, `invoice_id`, `payment_status`, `credit_amount`, `assigned_lab_id`, `assigned_user_id`, `assigned_at`, `assigned_staff_id`, `assigned_staff_name`) VALUES (65, 'ORD17681891938590', 26, 7, '核磁共振（NMR）', 4, '清华大学材料学院分析测试中心', 'accepted', 380.00, 0.00, 0.00, 0.00, 380.00, 380.00, 1, 'express', '王五', '13800138003', '测试地址1号', 'balance', '2026-01-07 11:39:54', '2026-01-02 11:39:54', '2026-01-05 11:39:54', NULL, NULL, NULL, NULL, '测试订单-实验室已接单#1', NULL, 0, NULL, 0, 'none', NULL, 'paid', 0.00, 4, 32, '2026-01-11 19:39:54', NULL, NULL);
INSERT INTO `orders` (`id`, `order_no`, `user_id`, `project_id`, `project_name`, `lab_id`, `lab_name`, `status`, `project_fee`, `urgent_fee`, `shipping_fee`, `discount_amount`, `total_fee`, `paid_fee`, `sample_count`, `shipping_method`, `receiver_name`, `receiver_phone`, `receiver_address`, `payment_method`, `payment_time`, `created_at`, `paid_at`, `confirmed_at`, `started_at`, `completed_at`, `cancelled_at`, `remark`, `cancel_reason`, `is_urgent`, `estimated_completion_time`, `is_draft`, `invoice_status`, `invoice_id`, `payment_status`, `credit_amount`, `assigned_lab_id`, `assigned_user_id`, `assigned_at`, `assigned_staff_id`, `assigned_staff_name`) VALUES (66, 'ORD17681891932252', 25, 5, '热重分析（TGA）', 8, '浙江大学材料科学与工程学院', 'accepted', 160.00, 0.00, 0.00, 0.00, 160.00, 160.00, 1, 'express', '李四', '13800138002', '测试地址2号', 'balance', '2026-01-06 11:39:54', '2026-01-09 11:39:54', '2026-01-10 11:39:54', NULL, NULL, NULL, NULL, '测试订单-实验室已接单#2', NULL, 0, NULL, 0, 'none', NULL, 'paid', 0.00, 8, 32, '2026-01-11 23:39:54', NULL, NULL);
INSERT INTO `orders` (`id`, `order_no`, `user_id`, `project_id`, `project_name`, `lab_id`, `lab_name`, `status`, `project_fee`, `urgent_fee`, `shipping_fee`, `discount_amount`, `total_fee`, `paid_fee`, `sample_count`, `shipping_method`, `receiver_name`, `receiver_phone`, `receiver_address`, `payment_method`, `payment_time`, `created_at`, `paid_at`, `confirmed_at`, `started_at`, `completed_at`, `cancelled_at`, `remark`, `cancel_reason`, `is_urgent`, `estimated_completion_time`, `is_draft`, `invoice_status`, `invoice_id`, `payment_status`, `credit_amount`, `assigned_lab_id`, `assigned_user_id`, `assigned_at`, `assigned_staff_id`, `assigned_staff_name`) VALUES (67, 'ORD17681891933280', 25, 1, '扫描电镜（SEM）', 5, '北京大学化学与分子工程学院测试中心', 'testing', 180.00, 0.00, 0.00, 0.00, 180.00, 180.00, 1, 'express', '李四', '13800138002', '测试地址1号', 'balance', '2026-01-09 11:39:54', '2026-01-11 11:39:54', '2026-01-11 11:39:54', '2026-01-11 11:39:54', '2026-01-09 11:39:54', NULL, NULL, '测试订单-检测中#1', NULL, 0, NULL, 0, 'none', NULL, 'paid', 0.00, 5, 32, '2026-01-11 21:39:54', NULL, NULL);
INSERT INTO `orders` (`id`, `order_no`, `user_id`, `project_id`, `project_name`, `lab_id`, `lab_name`, `status`, `project_fee`, `urgent_fee`, `shipping_fee`, `discount_amount`, `total_fee`, `paid_fee`, `sample_count`, `shipping_method`, `receiver_name`, `receiver_phone`, `receiver_address`, `payment_method`, `payment_time`, `created_at`, `paid_at`, `confirmed_at`, `started_at`, `completed_at`, `cancelled_at`, `remark`, `cancel_reason`, `is_urgent`, `estimated_completion_time`, `is_draft`, `invoice_status`, `invoice_id`, `payment_status`, `credit_amount`, `assigned_lab_id`, `assigned_user_id`, `assigned_at`, `assigned_staff_id`, `assigned_staff_name`) VALUES (68, 'ORD17681891938580', 24, 4, '红外光谱（FTIR）', 5, '北京大学化学与分子工程学院测试中心', 'testing', 90.00, 0.00, 0.00, 0.00, 90.00, 90.00, 1, 'express', '张三', '13800138001', '测试地址2号', 'balance', '2026-01-09 11:39:54', '2025-12-29 11:39:54', '2026-01-05 11:39:54', '2026-01-10 11:39:54', '2026-01-10 11:39:54', NULL, NULL, '测试订单-检测中#2', NULL, 0, NULL, 0, 'none', NULL, 'paid', 0.00, 5, 32, '2026-01-12 04:39:54', NULL, NULL);
INSERT INTO `orders` (`id`, `order_no`, `user_id`, `project_id`, `project_name`, `lab_id`, `lab_name`, `status`, `project_fee`, `urgent_fee`, `shipping_fee`, `discount_amount`, `total_fee`, `paid_fee`, `sample_count`, `shipping_method`, `receiver_name`, `receiver_phone`, `receiver_address`, `payment_method`, `payment_time`, `created_at`, `paid_at`, `confirmed_at`, `started_at`, `completed_at`, `cancelled_at`, `remark`, `cancel_reason`, `is_urgent`, `estimated_completion_time`, `is_draft`, `invoice_status`, `invoice_id`, `payment_status`, `credit_amount`, `assigned_lab_id`, `assigned_user_id`, `assigned_at`, `assigned_staff_id`, `assigned_staff_name`) VALUES (69, 'ORD17681891939723', 26, 5, '热重分析（TGA）', 6, '上海交通大学分析测试中心', 'completed', 160.00, 0.00, 0.00, 0.00, 160.00, 160.00, 1, 'express', '王五', '13800138003', '测试地址1号', 'balance', '2026-01-07 11:39:54', '2026-01-03 11:39:54', '2026-01-09 11:39:54', '2026-01-08 11:39:54', '2026-01-11 11:39:54', '2026-01-11 11:39:54', NULL, '测试订单-已完成#1', NULL, 0, NULL, 0, 'none', NULL, 'paid', 0.00, 6, 32, '2026-01-12 05:39:54', NULL, NULL);
INSERT INTO `orders` (`id`, `order_no`, `user_id`, `project_id`, `project_name`, `lab_id`, `lab_name`, `status`, `project_fee`, `urgent_fee`, `shipping_fee`, `discount_amount`, `total_fee`, `paid_fee`, `sample_count`, `shipping_method`, `receiver_name`, `receiver_phone`, `receiver_address`, `payment_method`, `payment_time`, `created_at`, `paid_at`, `confirmed_at`, `started_at`, `completed_at`, `cancelled_at`, `remark`, `cancel_reason`, `is_urgent`, `estimated_completion_time`, `is_draft`, `invoice_status`, `invoice_id`, `payment_status`, `credit_amount`, `assigned_lab_id`, `assigned_user_id`, `assigned_at`, `assigned_staff_id`, `assigned_staff_name`) VALUES (70, 'ORD17681891936633', 24, 7, '核磁共振（NMR）', 5, '北京大学化学与分子工程学院测试中心', 'completed', 380.00, 0.00, 0.00, 0.00, 380.00, 380.00, 1, 'express', '张三', '13800138001', '测试地址2号', 'balance', '2026-01-08 11:39:54', '2026-01-07 11:39:54', '2026-01-06 11:39:54', '2026-01-07 11:39:54', '2026-01-09 11:39:54', '2026-01-11 11:39:54', NULL, '测试订单-已完成#2', NULL, 0, NULL, 0, 'none', NULL, 'paid', 0.00, 5, 32, '2026-01-11 18:39:54', NULL, NULL);
INSERT INTO `orders` (`id`, `order_no`, `user_id`, `project_id`, `project_name`, `lab_id`, `lab_name`, `status`, `project_fee`, `urgent_fee`, `shipping_fee`, `discount_amount`, `total_fee`, `paid_fee`, `sample_count`, `shipping_method`, `receiver_name`, `receiver_phone`, `receiver_address`, `payment_method`, `payment_time`, `created_at`, `paid_at`, `confirmed_at`, `started_at`, `completed_at`, `cancelled_at`, `remark`, `cancel_reason`, `is_urgent`, `estimated_completion_time`, `is_draft`, `invoice_status`, `invoice_id`, `payment_status`, `credit_amount`, `assigned_lab_id`, `assigned_user_id`, `assigned_at`, `assigned_staff_id`, `assigned_staff_name`) VALUES (71, 'ORD17681956197430', 25, 6, '万能材料试验机', 4, '清华大学材料学院分析测试中心', 'pending_assign', 230.00, 0.00, 0.00, 0.00, 230.00, 230.00, 3, 'express', '李四', '13800138002', '测试地址1号', 'balance', '2026-01-11 18:26:59', '2026-01-10 15:26:59', '2026-01-11 12:26:59', NULL, NULL, NULL, NULL, '测试订单-待分配#1', NULL, 0, '2026-01-16 13:26:59', 0, 'none', NULL, 'paid', 0.00, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `orders` (`id`, `order_no`, `user_id`, `project_id`, `project_name`, `lab_id`, `lab_name`, `status`, `project_fee`, `urgent_fee`, `shipping_fee`, `discount_amount`, `total_fee`, `paid_fee`, `sample_count`, `shipping_method`, `receiver_name`, `receiver_phone`, `receiver_address`, `payment_method`, `payment_time`, `created_at`, `paid_at`, `confirmed_at`, `started_at`, `completed_at`, `cancelled_at`, `remark`, `cancel_reason`, `is_urgent`, `estimated_completion_time`, `is_draft`, `invoice_status`, `invoice_id`, `payment_status`, `credit_amount`, `assigned_lab_id`, `assigned_user_id`, `assigned_at`, `assigned_staff_id`, `assigned_staff_name`) VALUES (72, 'ORD17681956191665', 26, 2, '透射电镜（TEM）', 4, '清华大学材料学院分析测试中心', 'pending_assign', 280.00, 0.00, 0.00, 0.00, 280.00, 280.00, 1, 'express', '王五', '13800138003', '测试地址2号', 'wechat', '2026-01-12 06:26:59', '2026-01-10 19:26:59', '2026-01-10 15:26:59', NULL, NULL, NULL, NULL, '测试订单-待分配#2', NULL, 1, '2026-01-15 13:26:59', 0, 'none', NULL, 'paid', 0.00, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `orders` (`id`, `order_no`, `user_id`, `project_id`, `project_name`, `lab_id`, `lab_name`, `status`, `project_fee`, `urgent_fee`, `shipping_fee`, `discount_amount`, `total_fee`, `paid_fee`, `sample_count`, `shipping_method`, `receiver_name`, `receiver_phone`, `receiver_address`, `payment_method`, `payment_time`, `created_at`, `paid_at`, `confirmed_at`, `started_at`, `completed_at`, `cancelled_at`, `remark`, `cancel_reason`, `is_urgent`, `estimated_completion_time`, `is_draft`, `invoice_status`, `invoice_id`, `payment_status`, `credit_amount`, `assigned_lab_id`, `assigned_user_id`, `assigned_at`, `assigned_staff_id`, `assigned_staff_name`) VALUES (73, 'ORD17681956196323', 26, 7, '核磁共振（NMR）', 4, '清华大学材料学院分析测试中心', 'assigned', 380.00, 0.00, 0.00, 0.00, 380.00, 380.00, 3, 'express', '王五', '13800138003', '测试地址3号', 'alipay', '2026-01-12 08:26:59', '2026-01-12 05:26:59', '2026-01-10 19:26:59', NULL, NULL, NULL, NULL, '测试订单-待分配#3', NULL, 0, '2026-01-16 13:26:59', 0, 'none', NULL, 'paid', 0.00, 6, 12, '2026-01-12 11:09:08', NULL, NULL);
INSERT INTO `orders` (`id`, `order_no`, `user_id`, `project_id`, `project_name`, `lab_id`, `lab_name`, `status`, `project_fee`, `urgent_fee`, `shipping_fee`, `discount_amount`, `total_fee`, `paid_fee`, `sample_count`, `shipping_method`, `receiver_name`, `receiver_phone`, `receiver_address`, `payment_method`, `payment_time`, `created_at`, `paid_at`, `confirmed_at`, `started_at`, `completed_at`, `cancelled_at`, `remark`, `cancel_reason`, `is_urgent`, `estimated_completion_time`, `is_draft`, `invoice_status`, `invoice_id`, `payment_status`, `credit_amount`, `assigned_lab_id`, `assigned_user_id`, `assigned_at`, `assigned_staff_id`, `assigned_staff_name`) VALUES (74, 'ORD17681956199469', 26, 4, '红外光谱（FTIR）', 4, '清华大学材料学院分析测试中心', 'assigned', 90.00, 0.00, 0.00, 0.00, 90.00, 90.00, 1, 'express', '王五', '13800138003', '测试地址4号', 'balance', '2026-01-12 10:26:59', '2026-01-12 06:26:59', '2026-01-11 07:26:59', NULL, NULL, NULL, NULL, '测试订单-待分配#4', NULL, 1, '2026-01-16 13:26:59', 0, 'none', NULL, 'paid', 0.00, 4, 12, '2026-01-12 06:22:00', NULL, NULL);
INSERT INTO `orders` (`id`, `order_no`, `user_id`, `project_id`, `project_name`, `lab_id`, `lab_name`, `status`, `project_fee`, `urgent_fee`, `shipping_fee`, `discount_amount`, `total_fee`, `paid_fee`, `sample_count`, `shipping_method`, `receiver_name`, `receiver_phone`, `receiver_address`, `payment_method`, `payment_time`, `created_at`, `paid_at`, `confirmed_at`, `started_at`, `completed_at`, `cancelled_at`, `remark`, `cancel_reason`, `is_urgent`, `estimated_completion_time`, `is_draft`, `invoice_status`, `invoice_id`, `payment_status`, `credit_amount`, `assigned_lab_id`, `assigned_user_id`, `assigned_at`, `assigned_staff_id`, `assigned_staff_name`) VALUES (75, 'ORD17681956195895', 26, 5, '热重分析（TGA）', 4, '清华大学材料学院分析测试中心', 'assigned', 160.00, 0.00, 0.00, 0.00, 160.00, 160.00, 3, 'express', '王五', '13800138003', '测试地址5号', 'balance', '2026-01-11 18:26:59', '2026-01-12 08:26:59', '2026-01-11 09:26:59', NULL, NULL, NULL, NULL, '测试订单-待分配#5', NULL, 1, '2026-01-16 13:26:59', 0, 'none', NULL, 'paid', 0.00, 4, 12, '2026-01-12 06:21:47', NULL, NULL);
INSERT INTO `orders` (`id`, `order_no`, `user_id`, `project_id`, `project_name`, `lab_id`, `lab_name`, `status`, `project_fee`, `urgent_fee`, `shipping_fee`, `discount_amount`, `total_fee`, `paid_fee`, `sample_count`, `shipping_method`, `receiver_name`, `receiver_phone`, `receiver_address`, `payment_method`, `payment_time`, `created_at`, `paid_at`, `confirmed_at`, `started_at`, `completed_at`, `cancelled_at`, `remark`, `cancel_reason`, `is_urgent`, `estimated_completion_time`, `is_draft`, `invoice_status`, `invoice_id`, `payment_status`, `credit_amount`, `assigned_lab_id`, `assigned_user_id`, `assigned_at`, `assigned_staff_id`, `assigned_staff_name`) VALUES (76, 'ORD17681956196594', 25, 8, '气相色谱-质谱联用（GC-MS）', 4, '清华大学材料学院分析测试中心', 'pending_assign', 320.00, 0.00, 0.00, 0.00, 320.00, 320.00, 1, 'express', '李四', '13800138002', '测试地址6号', 'wechat', '2026-01-10 15:26:59', '2026-01-10 23:26:59', '2026-01-11 02:26:59', NULL, NULL, NULL, NULL, '测试订单-待分配#6', NULL, 1, '2026-01-15 13:26:59', 0, 'none', NULL, 'paid', 0.00, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `orders` (`id`, `order_no`, `user_id`, `project_id`, `project_name`, `lab_id`, `lab_name`, `status`, `project_fee`, `urgent_fee`, `shipping_fee`, `discount_amount`, `total_fee`, `paid_fee`, `sample_count`, `shipping_method`, `receiver_name`, `receiver_phone`, `receiver_address`, `payment_method`, `payment_time`, `created_at`, `paid_at`, `confirmed_at`, `started_at`, `completed_at`, `cancelled_at`, `remark`, `cancel_reason`, `is_urgent`, `estimated_completion_time`, `is_draft`, `invoice_status`, `invoice_id`, `payment_status`, `credit_amount`, `assigned_lab_id`, `assigned_user_id`, `assigned_at`, `assigned_staff_id`, `assigned_staff_name`) VALUES (77, 'ORD17681956192718', 25, 2, '透射电镜（TEM）', 4, '清华大学材料学院分析测试中心', 'pending_assign', 280.00, 0.00, 0.00, 0.00, 280.00, 280.00, 3, 'express', '李四', '13800138002', '测试地址7号', 'alipay', '2026-01-12 11:26:59', '2026-01-10 01:26:59', '2026-01-11 00:26:59', NULL, NULL, NULL, NULL, '测试订单-待分配#7', NULL, 0, '2026-01-18 13:26:59', 0, 'none', NULL, 'paid', 0.00, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `orders` (`id`, `order_no`, `user_id`, `project_id`, `project_name`, `lab_id`, `lab_name`, `status`, `project_fee`, `urgent_fee`, `shipping_fee`, `discount_amount`, `total_fee`, `paid_fee`, `sample_count`, `shipping_method`, `receiver_name`, `receiver_phone`, `receiver_address`, `payment_method`, `payment_time`, `created_at`, `paid_at`, `confirmed_at`, `started_at`, `completed_at`, `cancelled_at`, `remark`, `cancel_reason`, `is_urgent`, `estimated_completion_time`, `is_draft`, `invoice_status`, `invoice_id`, `payment_status`, `credit_amount`, `assigned_lab_id`, `assigned_user_id`, `assigned_at`, `assigned_staff_id`, `assigned_staff_name`) VALUES (78, 'ORD17681956192042', 24, 7, '核磁共振（NMR）', 4, '清华大学材料学院分析测试中心', 'pending_assign', 380.00, 0.00, 0.00, 0.00, 380.00, 380.00, 1, 'express', '张三', '13800138001', '测试地址8号', 'alipay', '2026-01-11 07:26:59', '2026-01-11 07:26:59', '2026-01-10 18:26:59', NULL, NULL, NULL, NULL, '测试订单-待分配#8', NULL, 1, '2026-01-15 13:26:59', 0, 'none', NULL, 'paid', 0.00, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `orders` (`id`, `order_no`, `user_id`, `project_id`, `project_name`, `lab_id`, `lab_name`, `status`, `project_fee`, `urgent_fee`, `shipping_fee`, `discount_amount`, `total_fee`, `paid_fee`, `sample_count`, `shipping_method`, `receiver_name`, `receiver_phone`, `receiver_address`, `payment_method`, `payment_time`, `created_at`, `paid_at`, `confirmed_at`, `started_at`, `completed_at`, `cancelled_at`, `remark`, `cancel_reason`, `is_urgent`, `estimated_completion_time`, `is_draft`, `invoice_status`, `invoice_id`, `payment_status`, `credit_amount`, `assigned_lab_id`, `assigned_user_id`, `assigned_at`, `assigned_staff_id`, `assigned_staff_name`) VALUES (79, 'ORD17681956197397', 24, 1, '扫描电镜（SEM）', 4, '清华大学材料学院分析测试中心', 'paid', 180.00, 0.00, 0.00, 0.00, 180.00, 180.00, 3, 'express', '张三', '13800138001', '测试地址9号', 'balance', '2026-01-12 03:26:59', '2026-01-10 18:26:59', '2026-01-11 09:26:59', NULL, NULL, NULL, NULL, '测试订单-待分配#9', NULL, 0, '2026-01-19 13:26:59', 0, 'none', NULL, 'paid', 0.00, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `orders` (`id`, `order_no`, `user_id`, `project_id`, `project_name`, `lab_id`, `lab_name`, `status`, `project_fee`, `urgent_fee`, `shipping_fee`, `discount_amount`, `total_fee`, `paid_fee`, `sample_count`, `shipping_method`, `receiver_name`, `receiver_phone`, `receiver_address`, `payment_method`, `payment_time`, `created_at`, `paid_at`, `confirmed_at`, `started_at`, `completed_at`, `cancelled_at`, `remark`, `cancel_reason`, `is_urgent`, `estimated_completion_time`, `is_draft`, `invoice_status`, `invoice_id`, `payment_status`, `credit_amount`, `assigned_lab_id`, `assigned_user_id`, `assigned_at`, `assigned_staff_id`, `assigned_staff_name`) VALUES (80, 'ORD17681956193565', 24, 3, 'X射线衍射（XRD）', 4, '清华大学材料学院分析测试中心', 'assigned', 130.00, 0.00, 0.00, 0.00, 130.00, 130.00, 2, 'express', '张三', '13800138001', '测试地址10号', 'wechat', '2026-01-11 01:26:59', '2026-01-12 09:26:59', '2026-01-12 10:26:59', NULL, NULL, NULL, NULL, '测试订单-待分配#10', NULL, 0, '2026-01-16 13:26:59', 0, 'none', NULL, 'paid', 0.00, 8, 12, '2026-01-12 06:21:35', NULL, NULL);
INSERT INTO `orders` (`id`, `order_no`, `user_id`, `project_id`, `project_name`, `lab_id`, `lab_name`, `status`, `project_fee`, `urgent_fee`, `shipping_fee`, `discount_amount`, `total_fee`, `paid_fee`, `sample_count`, `shipping_method`, `receiver_name`, `receiver_phone`, `receiver_address`, `payment_method`, `payment_time`, `created_at`, `paid_at`, `confirmed_at`, `started_at`, `completed_at`, `cancelled_at`, `remark`, `cancel_reason`, `is_urgent`, `estimated_completion_time`, `is_draft`, `invoice_status`, `invoice_id`, `payment_status`, `credit_amount`, `assigned_lab_id`, `assigned_user_id`, `assigned_at`, `assigned_staff_id`, `assigned_staff_name`) VALUES (81, 'ORD17681956195020', 24, 1, '扫描电镜（SEM）', 5, '北京大学化学与分子工程学院测试中心', 'assigned', 180.00, 0.00, 0.00, 0.00, 180.00, 180.00, 1, 'express', '张三', '13800138001', '测试地址1号', 'balance', '2026-01-06 13:26:59', '2026-01-01 13:26:59', '2026-01-07 13:26:59', NULL, NULL, NULL, NULL, '测试订单-已分配待接单#1', NULL, 0, NULL, 0, 'none', NULL, 'paid', 0.00, 5, 32, '2026-01-12 02:26:59', NULL, NULL);
INSERT INTO `orders` (`id`, `order_no`, `user_id`, `project_id`, `project_name`, `lab_id`, `lab_name`, `status`, `project_fee`, `urgent_fee`, `shipping_fee`, `discount_amount`, `total_fee`, `paid_fee`, `sample_count`, `shipping_method`, `receiver_name`, `receiver_phone`, `receiver_address`, `payment_method`, `payment_time`, `created_at`, `paid_at`, `confirmed_at`, `started_at`, `completed_at`, `cancelled_at`, `remark`, `cancel_reason`, `is_urgent`, `estimated_completion_time`, `is_draft`, `invoice_status`, `invoice_id`, `payment_status`, `credit_amount`, `assigned_lab_id`, `assigned_user_id`, `assigned_at`, `assigned_staff_id`, `assigned_staff_name`) VALUES (82, 'ORD17681956198687', 25, 1, '扫描电镜（SEM）', 5, '北京大学化学与分子工程学院测试中心', 'assigned', 180.00, 0.00, 0.00, 0.00, 180.00, 180.00, 1, 'express', '李四', '13800138002', '测试地址2号', 'balance', '2026-01-11 13:26:59', '2026-01-06 13:26:59', '2026-01-06 13:26:59', NULL, NULL, NULL, NULL, '测试订单-已分配待接单#2', NULL, 0, NULL, 0, 'none', NULL, 'paid', 0.00, 5, 32, '2026-01-11 20:26:59', NULL, NULL);
INSERT INTO `orders` (`id`, `order_no`, `user_id`, `project_id`, `project_name`, `lab_id`, `lab_name`, `status`, `project_fee`, `urgent_fee`, `shipping_fee`, `discount_amount`, `total_fee`, `paid_fee`, `sample_count`, `shipping_method`, `receiver_name`, `receiver_phone`, `receiver_address`, `payment_method`, `payment_time`, `created_at`, `paid_at`, `confirmed_at`, `started_at`, `completed_at`, `cancelled_at`, `remark`, `cancel_reason`, `is_urgent`, `estimated_completion_time`, `is_draft`, `invoice_status`, `invoice_id`, `payment_status`, `credit_amount`, `assigned_lab_id`, `assigned_user_id`, `assigned_at`, `assigned_staff_id`, `assigned_staff_name`) VALUES (83, 'ORD17681956198428', 25, 5, '热重分析（TGA）', 4, '清华大学材料学院分析测试中心', 'accepted', 160.00, 0.00, 0.00, 0.00, 160.00, 160.00, 1, 'express', '李四', '13800138002', '测试地址1号', 'balance', '2026-01-08 13:26:59', '2026-01-04 13:26:59', '2026-01-09 13:26:59', NULL, NULL, NULL, NULL, '测试订单-实验室已接单#1', NULL, 0, NULL, 0, 'none', NULL, 'paid', 0.00, 4, 32, '2026-01-11 14:26:59', NULL, NULL);
INSERT INTO `orders` (`id`, `order_no`, `user_id`, `project_id`, `project_name`, `lab_id`, `lab_name`, `status`, `project_fee`, `urgent_fee`, `shipping_fee`, `discount_amount`, `total_fee`, `paid_fee`, `sample_count`, `shipping_method`, `receiver_name`, `receiver_phone`, `receiver_address`, `payment_method`, `payment_time`, `created_at`, `paid_at`, `confirmed_at`, `started_at`, `completed_at`, `cancelled_at`, `remark`, `cancel_reason`, `is_urgent`, `estimated_completion_time`, `is_draft`, `invoice_status`, `invoice_id`, `payment_status`, `credit_amount`, `assigned_lab_id`, `assigned_user_id`, `assigned_at`, `assigned_staff_id`, `assigned_staff_name`) VALUES (84, 'ORD17681956191219', 24, 7, '核磁共振（NMR）', 5, '北京大学化学与分子工程学院测试中心', 'accepted', 380.00, 0.00, 0.00, 0.00, 380.00, 380.00, 1, 'express', '张三', '13800138001', '测试地址2号', 'balance', '2026-01-09 13:26:59', '2026-01-11 13:26:59', '2026-01-05 13:26:59', NULL, NULL, NULL, NULL, '测试订单-实验室已接单#2', NULL, 0, NULL, 0, 'none', NULL, 'paid', 0.00, 5, 32, '2026-01-11 20:26:59', NULL, NULL);
INSERT INTO `orders` (`id`, `order_no`, `user_id`, `project_id`, `project_name`, `lab_id`, `lab_name`, `status`, `project_fee`, `urgent_fee`, `shipping_fee`, `discount_amount`, `total_fee`, `paid_fee`, `sample_count`, `shipping_method`, `receiver_name`, `receiver_phone`, `receiver_address`, `payment_method`, `payment_time`, `created_at`, `paid_at`, `confirmed_at`, `started_at`, `completed_at`, `cancelled_at`, `remark`, `cancel_reason`, `is_urgent`, `estimated_completion_time`, `is_draft`, `invoice_status`, `invoice_id`, `payment_status`, `credit_amount`, `assigned_lab_id`, `assigned_user_id`, `assigned_at`, `assigned_staff_id`, `assigned_staff_name`) VALUES (85, 'ORD17681956198452', 25, 3, 'X射线衍射（XRD）', 7, '复旦大学材料科学系测试中心', 'testing', 130.00, 0.00, 0.00, 0.00, 130.00, 130.00, 1, 'express', '李四', '13800138002', '测试地址1号', 'balance', '2026-01-10 13:26:59', '2025-12-31 13:26:59', '2026-01-08 13:26:59', '2026-01-08 13:26:59', '2026-01-10 13:26:59', NULL, NULL, '测试订单-检测中#1', NULL, 0, NULL, 0, 'none', NULL, 'paid', 0.00, 7, 32, '2026-01-12 08:26:59', NULL, NULL);
INSERT INTO `orders` (`id`, `order_no`, `user_id`, `project_id`, `project_name`, `lab_id`, `lab_name`, `status`, `project_fee`, `urgent_fee`, `shipping_fee`, `discount_amount`, `total_fee`, `paid_fee`, `sample_count`, `shipping_method`, `receiver_name`, `receiver_phone`, `receiver_address`, `payment_method`, `payment_time`, `created_at`, `paid_at`, `confirmed_at`, `started_at`, `completed_at`, `cancelled_at`, `remark`, `cancel_reason`, `is_urgent`, `estimated_completion_time`, `is_draft`, `invoice_status`, `invoice_id`, `payment_status`, `credit_amount`, `assigned_lab_id`, `assigned_user_id`, `assigned_at`, `assigned_staff_id`, `assigned_staff_name`) VALUES (86, 'ORD17681956195638', 26, 6, '万能材料试验机', 7, '复旦大学材料科学系测试中心', 'testing', 230.00, 0.00, 0.00, 0.00, 230.00, 230.00, 1, 'express', '王五', '13800138003', '测试地址2号', 'balance', '2026-01-07 13:26:59', '2025-12-31 13:26:59', '2026-01-09 13:26:59', '2026-01-09 13:26:59', '2026-01-11 13:26:59', NULL, NULL, '测试订单-检测中#2', NULL, 0, NULL, 0, 'none', NULL, 'paid', 0.00, 7, 32, '2026-01-12 06:26:59', NULL, NULL);
INSERT INTO `orders` (`id`, `order_no`, `user_id`, `project_id`, `project_name`, `lab_id`, `lab_name`, `status`, `project_fee`, `urgent_fee`, `shipping_fee`, `discount_amount`, `total_fee`, `paid_fee`, `sample_count`, `shipping_method`, `receiver_name`, `receiver_phone`, `receiver_address`, `payment_method`, `payment_time`, `created_at`, `paid_at`, `confirmed_at`, `started_at`, `completed_at`, `cancelled_at`, `remark`, `cancel_reason`, `is_urgent`, `estimated_completion_time`, `is_draft`, `invoice_status`, `invoice_id`, `payment_status`, `credit_amount`, `assigned_lab_id`, `assigned_user_id`, `assigned_at`, `assigned_staff_id`, `assigned_staff_name`) VALUES (87, 'ORD17681956195566', 26, 2, '透射电镜（TEM）', 8, '浙江大学材料科学与工程学院', 'completed', 280.00, 0.00, 0.00, 0.00, 280.00, 280.00, 1, 'express', '王五', '13800138003', '测试地址1号', 'balance', '2026-01-07 13:26:59', '2025-12-31 13:26:59', '2026-01-08 13:26:59', '2026-01-08 13:26:59', '2026-01-10 13:26:59', '2026-01-11 13:26:59', NULL, '测试订单-已完成#1', NULL, 0, NULL, 0, 'none', NULL, 'paid', 0.00, 8, 32, '2026-01-11 21:26:59', NULL, NULL);
INSERT INTO `orders` (`id`, `order_no`, `user_id`, `project_id`, `project_name`, `lab_id`, `lab_name`, `status`, `project_fee`, `urgent_fee`, `shipping_fee`, `discount_amount`, `total_fee`, `paid_fee`, `sample_count`, `shipping_method`, `receiver_name`, `receiver_phone`, `receiver_address`, `payment_method`, `payment_time`, `created_at`, `paid_at`, `confirmed_at`, `started_at`, `completed_at`, `cancelled_at`, `remark`, `cancel_reason`, `is_urgent`, `estimated_completion_time`, `is_draft`, `invoice_status`, `invoice_id`, `payment_status`, `credit_amount`, `assigned_lab_id`, `assigned_user_id`, `assigned_at`, `assigned_staff_id`, `assigned_staff_name`) VALUES (88, 'ORD17681956198565', 24, 7, '核磁共振（NMR）', 4, '清华大学材料学院分析测试中心', 'completed', 380.00, 0.00, 0.00, 0.00, 380.00, 380.00, 1, 'express', '张三', '13800138001', '测试地址2号', 'balance', '2026-01-05 13:26:59', '2025-12-30 13:26:59', '2026-01-08 13:26:59', '2026-01-08 13:26:59', '2026-01-10 13:26:59', '2026-01-11 13:26:59', NULL, '测试订单-已完成#2', NULL, 0, NULL, 0, 'none', NULL, 'paid', 0.00, 4, 32, '2026-01-11 16:26:59', NULL, NULL);
INSERT INTO `orders` (`id`, `order_no`, `user_id`, `project_id`, `project_name`, `lab_id`, `lab_name`, `status`, `project_fee`, `urgent_fee`, `shipping_fee`, `discount_amount`, `total_fee`, `paid_fee`, `sample_count`, `shipping_method`, `receiver_name`, `receiver_phone`, `receiver_address`, `payment_method`, `payment_time`, `created_at`, `paid_at`, `confirmed_at`, `started_at`, `completed_at`, `cancelled_at`, `remark`, `cancel_reason`, `is_urgent`, `estimated_completion_time`, `is_draft`, `invoice_status`, `invoice_id`, `payment_status`, `credit_amount`, `assigned_lab_id`, `assigned_user_id`, `assigned_at`, `assigned_staff_id`, `assigned_staff_name`) VALUES (89, 'ORD1768559309145919', 19, 1, '扫描电镜（SEM）', 1, '平台实验室', 'pending_payment', 180.00, 0.00, 20.00, 0.00, 200.00, 0.00, 1, 'express', '111', '18888888888', 'Not applicablejinan88jinan', NULL, NULL, '2026-01-16 18:28:29', NULL, NULL, NULL, NULL, NULL, '', NULL, 0, NULL, 0, 'none', NULL, 'unpaid', 0.00, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `orders` (`id`, `order_no`, `user_id`, `project_id`, `project_name`, `lab_id`, `lab_name`, `status`, `project_fee`, `urgent_fee`, `shipping_fee`, `discount_amount`, `total_fee`, `paid_fee`, `sample_count`, `shipping_method`, `receiver_name`, `receiver_phone`, `receiver_address`, `payment_method`, `payment_time`, `created_at`, `paid_at`, `confirmed_at`, `started_at`, `completed_at`, `cancelled_at`, `remark`, `cancel_reason`, `is_urgent`, `estimated_completion_time`, `is_draft`, `invoice_status`, `invoice_id`, `payment_status`, `credit_amount`, `assigned_lab_id`, `assigned_user_id`, `assigned_at`, `assigned_staff_id`, `assigned_staff_name`) VALUES (90, 'ORD1768561085471116', 19, 1, '扫描电镜（SEM）', 1, '平台实验室', 'pending_payment', 180.00, 0.00, 20.00, 0.00, 200.00, 0.00, 1, 'express', '111', '18888888888', 'Not applicablejinan88jinan', NULL, NULL, '2026-01-16 18:58:05', NULL, NULL, NULL, NULL, NULL, '', NULL, 0, NULL, 0, 'none', NULL, 'unpaid', 0.00, NULL, NULL, NULL, NULL, NULL);
COMMIT;

-- ----------------------------
-- Table structure for payment_orders
-- ----------------------------
DROP TABLE IF EXISTS `payment_orders`;
CREATE TABLE `payment_orders` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '订单ID',
  `user_id` int NOT NULL COMMENT '用户ID',
  `order_no` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '订单号',
  `service_type` enum('SUPER_RECOVERY','IMAGE_RECOVERY','WECHAT_RECOVERY','VIDEO_RECOVERY','FILE_RECOVERY','AUDIO_RECOVERY') COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '服务类型',
  `amount` decimal(10,2) NOT NULL COMMENT '订单金额',
  `paid_amount` decimal(10,2) DEFAULT NULL COMMENT '已支付金额',
  `payment_method` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '支付方式',
  `payment_channel` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '支付渠道',
  `third_party_order_no` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '第三方订单号',
  `status` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '订单状态',
  `paid_at` datetime DEFAULT NULL COMMENT '支付时间',
  `expires_at` datetime DEFAULT NULL COMMENT '过期时间',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_payment_orders_order_no` (`order_no`),
  KEY `ix_payment_orders_user_id` (`user_id`),
  KEY `ix_payment_orders_id` (`id`),
  CONSTRAINT `payment_orders_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of payment_orders
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for payments
-- ----------------------------
DROP TABLE IF EXISTS `payments`;
CREATE TABLE `payments` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `payment_no` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '支付单号',
  `order_id` bigint NOT NULL COMMENT '订单ID',
  `order_no` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '订单号',
  `user_id` bigint NOT NULL COMMENT '用户ID',
  `payment_method` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '支付方式',
  `payment_channel` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '支付渠道',
  `amount` decimal(10,2) NOT NULL COMMENT '支付金额',
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '支付状态',
  `trade_no` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '第三方交易号',
  `paid_at` datetime DEFAULT NULL COMMENT '支付时间',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `payment_no` (`payment_no`),
  KEY `ix_payments_id` (`id`),
  KEY `ix_payments_order_id` (`order_id`),
  KEY `ix_payments_user_id` (`user_id`),
  KEY `ix_payments_trade_no` (`trade_no`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of payments
-- ----------------------------
BEGIN;
INSERT INTO `payments` (`id`, `payment_no`, `order_id`, `order_no`, `user_id`, `payment_method`, `payment_channel`, `amount`, `status`, `trade_no`, `paid_at`, `created_at`) VALUES (1, 'PAY17681146122597', 3, 'ORD1768114611840661', 11, 'wechat', 'wechat_jsapi', 200.00, 'pending', NULL, NULL, '2026-01-11 14:56:52');
INSERT INTO `payments` (`id`, `payment_no`, `order_id`, `order_no`, `user_id`, `payment_method`, `payment_channel`, `amount`, `status`, `trade_no`, `paid_at`, `created_at`) VALUES (2, 'PAY1768114625743172', 4, 'ORD1768114625666466', 11, 'wechat', 'wechat_jsapi', 200.00, 'pending', NULL, NULL, '2026-01-11 14:57:05');
INSERT INTO `payments` (`id`, `payment_no`, `order_id`, `order_no`, `user_id`, `payment_method`, `payment_channel`, `amount`, `status`, `trade_no`, `paid_at`, `created_at`) VALUES (3, 'PAY1768114960343876', 5, 'ORD1768114960284495', 11, 'wechat', 'wechat_jsapi', 200.00, 'pending', NULL, NULL, '2026-01-11 15:02:40');
INSERT INTO `payments` (`id`, `payment_no`, `order_id`, `order_no`, `user_id`, `payment_method`, `payment_channel`, `amount`, `status`, `trade_no`, `paid_at`, `created_at`) VALUES (4, 'PAY1768117482104064', 6, 'ORD17681174824006', 11, 'wechat', 'wechat_jsapi', 200.00, 'pending', NULL, NULL, '2026-01-11 15:44:42');
INSERT INTO `payments` (`id`, `payment_no`, `order_id`, `order_no`, `user_id`, `payment_method`, `payment_channel`, `amount`, `status`, `trade_no`, `paid_at`, `created_at`) VALUES (5, 'PAY1768117509966615', 7, 'ORD1768117509917339', 11, 'wechat', 'wechat_jsapi', 200.00, 'pending', NULL, NULL, '2026-01-11 15:45:09');
INSERT INTO `payments` (`id`, `payment_no`, `order_id`, `order_no`, `user_id`, `payment_method`, `payment_channel`, `amount`, `status`, `trade_no`, `paid_at`, `created_at`) VALUES (6, 'PAY1768117724984950', 8, 'ORD1768117724910493', 11, 'wechat', 'wechat_jsapi', 200.00, 'pending', NULL, NULL, '2026-01-11 15:48:44');
INSERT INTO `payments` (`id`, `payment_no`, `order_id`, `order_no`, `user_id`, `payment_method`, `payment_channel`, `amount`, `status`, `trade_no`, `paid_at`, `created_at`) VALUES (7, 'PAY1768119834695972', 12, 'ORD1768119800518983', 19, 'wechat', 'wechat_jsapi', 150.00, 'pending', NULL, NULL, '2026-01-11 16:23:54');
INSERT INTO `payments` (`id`, `payment_no`, `order_id`, `order_no`, `user_id`, `payment_method`, `payment_channel`, `amount`, `status`, `trade_no`, `paid_at`, `created_at`) VALUES (8, 'PAY1768120083277480', 12, 'ORD1768119800518983', 19, 'wechat', 'wechat_jsapi', 150.00, 'pending', NULL, NULL, '2026-01-11 16:28:03');
INSERT INTO `payments` (`id`, `payment_no`, `order_id`, `order_no`, `user_id`, `payment_method`, `payment_channel`, `amount`, `status`, `trade_no`, `paid_at`, `created_at`) VALUES (9, 'PAY1768121525', 12, 'ORD1768119800518983', 19, 'alipay', 'h5', 150.00, 'pending', 'ORDER_12_20260111165205', NULL, '2026-01-11 16:52:05');
INSERT INTO `payments` (`id`, `payment_no`, `order_id`, `order_no`, `user_id`, `payment_method`, `payment_channel`, `amount`, `status`, `trade_no`, `paid_at`, `created_at`) VALUES (10, 'PAY1768121618298163', 13, 'ORD1768121615426274', 19, 'wechat', 'wechat_h5', 150.00, 'pending', NULL, NULL, '2026-01-11 16:53:38');
INSERT INTO `payments` (`id`, `payment_no`, `order_id`, `order_no`, `user_id`, `payment_method`, `payment_channel`, `amount`, `status`, `trade_no`, `paid_at`, `created_at`) VALUES (11, 'PAY1768182261930467', 14, 'ORD1768182261215319', 13, 'wechat', 'wechat_jsapi', 180.00, 'pending', NULL, NULL, '2026-01-12 09:44:21');
INSERT INTO `payments` (`id`, `payment_no`, `order_id`, `order_no`, `user_id`, `payment_method`, `payment_channel`, `amount`, `status`, `trade_no`, `paid_at`, `created_at`) VALUES (12, 'PAY1768559314570768', 89, 'ORD1768559309145919', 19, 'wechat', 'wechat_jsapi', 200.00, 'pending', NULL, NULL, '2026-01-16 18:28:34');
INSERT INTO `payments` (`id`, `payment_no`, `order_id`, `order_no`, `user_id`, `payment_method`, `payment_channel`, `amount`, `status`, `trade_no`, `paid_at`, `created_at`) VALUES (13, 'PAY1768561053190743', 89, 'ORD1768559309145919', 19, 'alipay', NULL, 200.00, 'pending', 'ORDER_89_20260116185733', NULL, '2026-01-16 18:57:33');
COMMIT;

-- ----------------------------
-- Table structure for permissions
-- ----------------------------
DROP TABLE IF EXISTS `permissions`;
CREATE TABLE `permissions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '权限名称',
  `code` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '权限编码',
  `module` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '所属模块',
  `description` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '权限描述',
  `is_active` tinyint(1) DEFAULT NULL COMMENT '是否启用',
  `sort_order` int DEFAULT NULL COMMENT '排序',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`),
  KEY `ix_permissions_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of permissions
-- ----------------------------
BEGIN;
INSERT INTO `permissions` (`id`, `name`, `code`, `module`, `description`, `is_active`, `sort_order`, `created_at`) VALUES (1, 'user:view', 'user:view', NULL, 'user:view权限', 1, 0, '2026-01-12 10:36:37');
INSERT INTO `permissions` (`id`, `name`, `code`, `module`, `description`, `is_active`, `sort_order`, `created_at`) VALUES (2, 'user:edit', 'user:edit', NULL, 'user:edit权限', 1, 0, '2026-01-12 10:36:37');
INSERT INTO `permissions` (`id`, `name`, `code`, `module`, `description`, `is_active`, `sort_order`, `created_at`) VALUES (3, 'user:delete', 'user:delete', NULL, 'user:delete权限', 1, 0, '2026-01-12 10:36:37');
INSERT INTO `permissions` (`id`, `name`, `code`, `module`, `description`, `is_active`, `sort_order`, `created_at`) VALUES (4, 'user:certification', 'user:certification', NULL, 'user:certification权限', 1, 0, '2026-01-12 10:36:37');
INSERT INTO `permissions` (`id`, `name`, `code`, `module`, `description`, `is_active`, `sort_order`, `created_at`) VALUES (5, 'order:view', 'order:view', NULL, 'order:view权限', 1, 0, '2026-01-12 10:36:37');
INSERT INTO `permissions` (`id`, `name`, `code`, `module`, `description`, `is_active`, `sort_order`, `created_at`) VALUES (6, 'order:edit', 'order:edit', NULL, 'order:edit权限', 1, 0, '2026-01-12 10:36:37');
INSERT INTO `permissions` (`id`, `name`, `code`, `module`, `description`, `is_active`, `sort_order`, `created_at`) VALUES (7, 'order:delete', 'order:delete', NULL, 'order:delete权限', 1, 0, '2026-01-12 10:36:37');
INSERT INTO `permissions` (`id`, `name`, `code`, `module`, `description`, `is_active`, `sort_order`, `created_at`) VALUES (8, 'order:assign', 'order:assign', NULL, 'order:assign权限', 1, 0, '2026-01-12 10:36:37');
INSERT INTO `permissions` (`id`, `name`, `code`, `module`, `description`, `is_active`, `sort_order`, `created_at`) VALUES (9, 'order:export', 'order:export', NULL, 'order:export权限', 1, 0, '2026-01-12 10:36:37');
INSERT INTO `permissions` (`id`, `name`, `code`, `module`, `description`, `is_active`, `sort_order`, `created_at`) VALUES (10, 'project:view', 'project:view', NULL, 'project:view权限', 1, 0, '2026-01-12 10:36:37');
INSERT INTO `permissions` (`id`, `name`, `code`, `module`, `description`, `is_active`, `sort_order`, `created_at`) VALUES (11, 'project:create', 'project:create', NULL, 'project:create权限', 1, 0, '2026-01-12 10:36:37');
INSERT INTO `permissions` (`id`, `name`, `code`, `module`, `description`, `is_active`, `sort_order`, `created_at`) VALUES (12, 'project:edit', 'project:edit', NULL, 'project:edit权限', 1, 0, '2026-01-12 10:36:37');
INSERT INTO `permissions` (`id`, `name`, `code`, `module`, `description`, `is_active`, `sort_order`, `created_at`) VALUES (13, 'project:delete', 'project:delete', NULL, 'project:delete权限', 1, 0, '2026-01-12 10:36:37');
INSERT INTO `permissions` (`id`, `name`, `code`, `module`, `description`, `is_active`, `sort_order`, `created_at`) VALUES (14, 'lab:view', 'lab:view', NULL, 'lab:view权限', 1, 0, '2026-01-12 10:36:37');
INSERT INTO `permissions` (`id`, `name`, `code`, `module`, `description`, `is_active`, `sort_order`, `created_at`) VALUES (15, 'lab:create', 'lab:create', NULL, 'lab:create权限', 1, 0, '2026-01-12 10:36:37');
INSERT INTO `permissions` (`id`, `name`, `code`, `module`, `description`, `is_active`, `sort_order`, `created_at`) VALUES (16, 'lab:edit', 'lab:edit', NULL, 'lab:edit权限', 1, 0, '2026-01-12 10:36:37');
INSERT INTO `permissions` (`id`, `name`, `code`, `module`, `description`, `is_active`, `sort_order`, `created_at`) VALUES (17, 'lab:delete', 'lab:delete', NULL, 'lab:delete权限', 1, 0, '2026-01-12 10:36:37');
INSERT INTO `permissions` (`id`, `name`, `code`, `module`, `description`, `is_active`, `sort_order`, `created_at`) VALUES (18, 'lab:approve', 'lab:approve', NULL, 'lab:approve权限', 1, 0, '2026-01-12 10:36:37');
INSERT INTO `permissions` (`id`, `name`, `code`, `module`, `description`, `is_active`, `sort_order`, `created_at`) VALUES (19, 'finance:view', 'finance:view', NULL, 'finance:view权限', 1, 0, '2026-01-12 10:36:37');
INSERT INTO `permissions` (`id`, `name`, `code`, `module`, `description`, `is_active`, `sort_order`, `created_at`) VALUES (20, 'finance:recharge', 'finance:recharge', NULL, 'finance:recharge权限', 1, 0, '2026-01-12 10:36:37');
INSERT INTO `permissions` (`id`, `name`, `code`, `module`, `description`, `is_active`, `sort_order`, `created_at`) VALUES (21, 'finance:refund', 'finance:refund', NULL, 'finance:refund权限', 1, 0, '2026-01-12 10:36:37');
INSERT INTO `permissions` (`id`, `name`, `code`, `module`, `description`, `is_active`, `sort_order`, `created_at`) VALUES (22, 'finance:withdraw', 'finance:withdraw', NULL, 'finance:withdraw权限', 1, 0, '2026-01-12 10:36:37');
INSERT INTO `permissions` (`id`, `name`, `code`, `module`, `description`, `is_active`, `sort_order`, `created_at`) VALUES (23, 'finance:report', 'finance:report', NULL, 'finance:report权限', 1, 0, '2026-01-12 10:36:37');
INSERT INTO `permissions` (`id`, `name`, `code`, `module`, `description`, `is_active`, `sort_order`, `created_at`) VALUES (24, 'coupon:view', 'coupon:view', NULL, 'coupon:view权限', 1, 0, '2026-01-12 10:36:37');
INSERT INTO `permissions` (`id`, `name`, `code`, `module`, `description`, `is_active`, `sort_order`, `created_at`) VALUES (25, 'coupon:create', 'coupon:create', NULL, 'coupon:create权限', 1, 0, '2026-01-12 10:36:37');
INSERT INTO `permissions` (`id`, `name`, `code`, `module`, `description`, `is_active`, `sort_order`, `created_at`) VALUES (26, 'coupon:edit', 'coupon:edit', NULL, 'coupon:edit权限', 1, 0, '2026-01-12 10:36:37');
INSERT INTO `permissions` (`id`, `name`, `code`, `module`, `description`, `is_active`, `sort_order`, `created_at`) VALUES (27, 'coupon:delete', 'coupon:delete', NULL, 'coupon:delete权限', 1, 0, '2026-01-12 10:36:37');
INSERT INTO `permissions` (`id`, `name`, `code`, `module`, `description`, `is_active`, `sort_order`, `created_at`) VALUES (28, 'content:banner', 'content:banner', NULL, 'content:banner权限', 1, 0, '2026-01-12 10:36:37');
INSERT INTO `permissions` (`id`, `name`, `code`, `module`, `description`, `is_active`, `sort_order`, `created_at`) VALUES (29, 'content:announcement', 'content:announcement', NULL, 'content:announcement权限', 1, 0, '2026-01-12 10:36:37');
INSERT INTO `permissions` (`id`, `name`, `code`, `module`, `description`, `is_active`, `sort_order`, `created_at`) VALUES (30, 'content:help', 'content:help', NULL, 'content:help权限', 1, 0, '2026-01-12 10:36:37');
INSERT INTO `permissions` (`id`, `name`, `code`, `module`, `description`, `is_active`, `sort_order`, `created_at`) VALUES (31, 'report:view', 'report:view', NULL, 'report:view权限', 1, 0, '2026-01-12 10:36:37');
INSERT INTO `permissions` (`id`, `name`, `code`, `module`, `description`, `is_active`, `sort_order`, `created_at`) VALUES (32, 'report:export', 'report:export', NULL, 'report:export权限', 1, 0, '2026-01-12 10:36:37');
INSERT INTO `permissions` (`id`, `name`, `code`, `module`, `description`, `is_active`, `sort_order`, `created_at`) VALUES (33, 'system:config', 'system:config', NULL, 'system:config权限', 1, 0, '2026-01-12 10:36:37');
INSERT INTO `permissions` (`id`, `name`, `code`, `module`, `description`, `is_active`, `sort_order`, `created_at`) VALUES (34, 'system:role', 'system:role', NULL, 'system:role权限', 1, 0, '2026-01-12 10:36:37');
INSERT INTO `permissions` (`id`, `name`, `code`, `module`, `description`, `is_active`, `sort_order`, `created_at`) VALUES (35, 'system:log', 'system:log', NULL, 'system:log权限', 1, 0, '2026-01-12 10:36:37');
COMMIT;

-- ----------------------------
-- Table structure for points_exchange_records
-- ----------------------------
DROP TABLE IF EXISTS `points_exchange_records`;
CREATE TABLE `points_exchange_records` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '兑换ID',
  `user_id` int NOT NULL COMMENT '用户ID',
  `goods_id` int NOT NULL COMMENT '商品ID',
  `points` int NOT NULL COMMENT '兑换消耗积分',
  `status` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '兑换状态：pending,confirmed,shipped,completed,cancelled',
  `express_company` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '快递公司',
  `express_no` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '快递单号',
  `address_snapshot` text COLLATE utf8mb4_unicode_ci COMMENT '地址快照（JSON）',
  `created_at` datetime DEFAULT NULL COMMENT '创建时间',
  `updated_at` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `goods_id` (`goods_id`),
  KEY `ix_points_exchange_records_user_id` (`user_id`),
  KEY `ix_points_exchange_records_id` (`id`),
  CONSTRAINT `points_exchange_records_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `points_exchange_records_ibfk_2` FOREIGN KEY (`goods_id`) REFERENCES `points_goods` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of points_exchange_records
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for points_goods
-- ----------------------------
DROP TABLE IF EXISTS `points_goods`;
CREATE TABLE `points_goods` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '商品ID',
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '商品名称',
  `points` int NOT NULL COMMENT '所需积分',
  `category` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '商品分类',
  `image` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '商品图片',
  `description` text COLLATE utf8mb4_unicode_ci COMMENT '商品描述',
  `stock` int DEFAULT NULL COMMENT '库存数量',
  `is_active` tinyint(1) DEFAULT NULL COMMENT '是否上架',
  `sort_order` int DEFAULT NULL COMMENT '排序',
  `created_at` datetime DEFAULT NULL COMMENT '创建时间',
  `updated_at` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `ix_points_goods_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of points_goods
-- ----------------------------
BEGIN;
INSERT INTO `points_goods` (`id`, `name`, `points`, `category`, `image`, `description`, `stock`, `is_active`, `sort_order`, `created_at`, `updated_at`) VALUES (1, '测试', 100, '优惠券', '', '', 10, 1, 0, '2026-01-12 09:05:46', '2026-01-12 09:05:46');
INSERT INTO `points_goods` (`id`, `name`, `points`, `category`, `image`, `description`, `stock`, `is_active`, `sort_order`, `created_at`, `updated_at`) VALUES (2, '满100减10优惠券', 100, '优惠券', NULL, '满100元可用，立减10元', 1000, 1, 1, '2026-01-12 09:11:12', '2026-01-12 09:11:12');
INSERT INTO `points_goods` (`id`, `name`, `points`, `category`, `image`, `description`, `stock`, `is_active`, `sort_order`, `created_at`, `updated_at`) VALUES (3, '满500减50优惠券', 500, '优惠券', NULL, '满500元可用，立减50元', 500, 1, 2, '2026-01-12 09:11:12', '2026-01-12 09:11:12');
INSERT INTO `points_goods` (`id`, `name`, `points`, `category`, `image`, `description`, `stock`, `is_active`, `sort_order`, `created_at`, `updated_at`) VALUES (4, '500元测试现金抵用券', 13440, '优惠券', NULL, '测试专用，价值500元现金抵用券', 50, 1, 3, '2026-01-12 09:11:12', '2026-01-12 09:11:12');
INSERT INTO `points_goods` (`id`, `name`, `points`, `category`, `image`, `description`, `stock`, `is_active`, `sort_order`, `created_at`, `updated_at`) VALUES (5, '100元测试现金抵用券', 2688, '优惠券', NULL, '测试专用，价值100元现金抵用券', 100, 1, 4, '2026-01-12 09:11:12', '2026-01-12 09:11:12');
INSERT INTO `points_goods` (`id`, `name`, `points`, `category`, `image`, `description`, `stock`, `is_active`, `sort_order`, `created_at`, `updated_at`) VALUES (6, '京东E卡50元', 2000, '京东E卡', NULL, '京东购物卡，面值50元', 100, 1, 5, '2026-01-12 09:11:12', '2026-01-12 09:11:12');
INSERT INTO `points_goods` (`id`, `name`, `points`, `category`, `image`, `description`, `stock`, `is_active`, `sort_order`, `created_at`, `updated_at`) VALUES (7, '京东E卡100元', 3500, '京东E卡', NULL, '京东购物卡，面值100元', 50, 1, 6, '2026-01-12 09:11:12', '2026-01-12 09:11:12');
INSERT INTO `points_goods` (`id`, `name`, `points`, `category`, `image`, `description`, `stock`, `is_active`, `sort_order`, `created_at`, `updated_at`) VALUES (8, '小熊电煮锅', 3032, '实物礼', NULL, '小熊多功能电煮锅，1.5L容量，适合宿舍使用', 30, 1, 7, '2026-01-12 09:11:12', '2026-01-12 09:11:12');
INSERT INTO `points_goods` (`id`, `name`, `points`, `category`, `image`, `description`, `stock`, `is_active`, `sort_order`, `created_at`, `updated_at`) VALUES (9, '小米电动牙刷T200', 3544, '实物礼', NULL, '小米米家电动牙刷，声波震动，2分钟智能定时', 25, 1, 8, '2026-01-12 09:11:12', '2026-01-12 09:11:12');
INSERT INTO `points_goods` (`id`, `name`, `points`, `category`, `image`, `description`, `stock`, `is_active`, `sort_order`, `created_at`, `updated_at`) VALUES (10, '骨传导耳机', 6638, '实物礼', NULL, '骨传导运动耳机，不入耳设计，适合运动使用', 20, 1, 9, '2026-01-12 09:11:12', '2026-01-12 09:11:12');
INSERT INTO `points_goods` (`id`, `name`, `points`, `category`, `image`, `description`, `stock`, `is_active`, `sort_order`, `created_at`, `updated_at`) VALUES (11, '苏泊尔养生壶', 5794, '实物礼', NULL, '苏泊尔多功能养生壶，1.5L容量，24小时预约', 15, 1, 10, '2026-01-12 09:11:12', '2026-01-12 09:11:12');
INSERT INTO `points_goods` (`id`, `name`, `points`, `category`, `image`, `description`, `stock`, `is_active`, `sort_order`, `created_at`, `updated_at`) VALUES (12, '测试商品A', 500, '测试商品', NULL, '测试用商品A，积分500', 999, 1, 11, '2026-01-12 09:11:12', '2026-01-12 09:11:12');
INSERT INTO `points_goods` (`id`, `name`, `points`, `category`, `image`, `description`, `stock`, `is_active`, `sort_order`, `created_at`, `updated_at`) VALUES (13, '测试商品B', 1000, '测试商品', NULL, '测试用商品B，积分1000', 999, 1, 12, '2026-01-12 09:11:12', '2026-01-12 09:11:12');
INSERT INTO `points_goods` (`id`, `name`, `points`, `category`, `image`, `description`, `stock`, `is_active`, `sort_order`, `created_at`, `updated_at`) VALUES (14, '测试商品C', 2000, '测试商品', NULL, '测试用商品C，积分2000', 999, 1, 13, '2026-01-12 09:11:12', '2026-01-12 09:11:12');
COMMIT;

-- ----------------------------
-- Table structure for points_records
-- ----------------------------
DROP TABLE IF EXISTS `points_records`;
CREATE TABLE `points_records` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '记录ID',
  `user_id` int NOT NULL COMMENT '用户ID',
  `points` int NOT NULL COMMENT '积分变动（正数为增加，负数为减少）',
  `type` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '积分类型：order,exchange,signin,invite等',
  `related_id` int DEFAULT NULL COMMENT '关联ID（订单ID、兑换ID等）',
  `description` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '积分描述',
  `created_at` datetime DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`),
  KEY `ix_points_records_id` (`id`),
  KEY `ix_points_records_user_id` (`user_id`),
  CONSTRAINT `points_records_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=97 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of points_records
-- ----------------------------
BEGIN;
INSERT INTO `points_records` (`id`, `user_id`, `points`, `type`, `related_id`, `description`, `created_at`) VALUES (1, 24, 20, 'signup', NULL, '积分记录1', '2026-01-12 02:55:04');
INSERT INTO `points_records` (`id`, `user_id`, `points`, `type`, `related_id`, `description`, `created_at`) VALUES (2, 24, 20, 'invite', NULL, '积分记录2', '2026-01-12 02:55:04');
INSERT INTO `points_records` (`id`, `user_id`, `points`, `type`, `related_id`, `description`, `created_at`) VALUES (3, 24, 100, 'signup', NULL, '积分记录3', '2026-01-12 02:55:04');
INSERT INTO `points_records` (`id`, `user_id`, `points`, `type`, `related_id`, `description`, `created_at`) VALUES (4, 24, 10, 'order', NULL, '积分记录4', '2026-01-12 02:55:04');
INSERT INTO `points_records` (`id`, `user_id`, `points`, `type`, `related_id`, `description`, `created_at`) VALUES (5, 24, 50, 'review', NULL, '积分记录5', '2026-01-12 02:55:04');
INSERT INTO `points_records` (`id`, `user_id`, `points`, `type`, `related_id`, `description`, `created_at`) VALUES (6, 24, 10, 'review', NULL, '积分记录6', '2026-01-12 02:55:04');
INSERT INTO `points_records` (`id`, `user_id`, `points`, `type`, `related_id`, `description`, `created_at`) VALUES (7, 25, 100, 'order', NULL, '积分记录1', '2026-01-12 02:55:04');
INSERT INTO `points_records` (`id`, `user_id`, `points`, `type`, `related_id`, `description`, `created_at`) VALUES (8, 25, 100, 'review', NULL, '积分记录2', '2026-01-12 02:55:04');
INSERT INTO `points_records` (`id`, `user_id`, `points`, `type`, `related_id`, `description`, `created_at`) VALUES (9, 25, 100, 'order', NULL, '积分记录3', '2026-01-12 02:55:04');
INSERT INTO `points_records` (`id`, `user_id`, `points`, `type`, `related_id`, `description`, `created_at`) VALUES (10, 25, 20, 'daily', NULL, '积分记录4', '2026-01-12 02:55:04');
INSERT INTO `points_records` (`id`, `user_id`, `points`, `type`, `related_id`, `description`, `created_at`) VALUES (11, 25, 20, 'invite', NULL, '积分记录5', '2026-01-12 02:55:04');
INSERT INTO `points_records` (`id`, `user_id`, `points`, `type`, `related_id`, `description`, `created_at`) VALUES (12, 25, 100, 'signup', NULL, '积分记录6', '2026-01-12 02:55:04');
INSERT INTO `points_records` (`id`, `user_id`, `points`, `type`, `related_id`, `description`, `created_at`) VALUES (13, 25, 20, 'review', NULL, '积分记录7', '2026-01-12 02:55:04');
INSERT INTO `points_records` (`id`, `user_id`, `points`, `type`, `related_id`, `description`, `created_at`) VALUES (14, 25, 10, 'signup', NULL, '积分记录8', '2026-01-12 02:55:04');
INSERT INTO `points_records` (`id`, `user_id`, `points`, `type`, `related_id`, `description`, `created_at`) VALUES (15, 25, 10, 'daily', NULL, '积分记录9', '2026-01-12 02:55:04');
INSERT INTO `points_records` (`id`, `user_id`, `points`, `type`, `related_id`, `description`, `created_at`) VALUES (16, 25, 100, 'invite', NULL, '积分记录10', '2026-01-12 02:55:04');
INSERT INTO `points_records` (`id`, `user_id`, `points`, `type`, `related_id`, `description`, `created_at`) VALUES (17, 25, 20, 'order', NULL, '积分记录11', '2026-01-12 02:55:04');
INSERT INTO `points_records` (`id`, `user_id`, `points`, `type`, `related_id`, `description`, `created_at`) VALUES (18, 25, 20, 'order', NULL, '积分记录12', '2026-01-12 02:55:04');
INSERT INTO `points_records` (`id`, `user_id`, `points`, `type`, `related_id`, `description`, `created_at`) VALUES (19, 25, 20, 'order', NULL, '积分记录13', '2026-01-12 02:55:04');
INSERT INTO `points_records` (`id`, `user_id`, `points`, `type`, `related_id`, `description`, `created_at`) VALUES (20, 25, 50, 'daily', NULL, '积分记录14', '2026-01-12 02:55:04');
INSERT INTO `points_records` (`id`, `user_id`, `points`, `type`, `related_id`, `description`, `created_at`) VALUES (21, 26, 10, 'invite', NULL, '积分记录1', '2026-01-12 02:55:04');
INSERT INTO `points_records` (`id`, `user_id`, `points`, `type`, `related_id`, `description`, `created_at`) VALUES (22, 26, 50, 'review', NULL, '积分记录2', '2026-01-12 02:55:04');
INSERT INTO `points_records` (`id`, `user_id`, `points`, `type`, `related_id`, `description`, `created_at`) VALUES (23, 26, 20, 'daily', NULL, '积分记录3', '2026-01-12 02:55:04');
INSERT INTO `points_records` (`id`, `user_id`, `points`, `type`, `related_id`, `description`, `created_at`) VALUES (24, 26, 100, 'signup', NULL, '积分记录4', '2026-01-12 02:55:04');
INSERT INTO `points_records` (`id`, `user_id`, `points`, `type`, `related_id`, `description`, `created_at`) VALUES (25, 26, 100, 'invite', NULL, '积分记录5', '2026-01-12 02:55:04');
INSERT INTO `points_records` (`id`, `user_id`, `points`, `type`, `related_id`, `description`, `created_at`) VALUES (26, 26, 10, 'daily', NULL, '积分记录6', '2026-01-12 02:55:04');
INSERT INTO `points_records` (`id`, `user_id`, `points`, `type`, `related_id`, `description`, `created_at`) VALUES (27, 26, 10, 'daily', NULL, '积分记录7', '2026-01-12 02:55:04');
INSERT INTO `points_records` (`id`, `user_id`, `points`, `type`, `related_id`, `description`, `created_at`) VALUES (28, 26, 10, 'invite', NULL, '积分记录8', '2026-01-12 02:55:04');
INSERT INTO `points_records` (`id`, `user_id`, `points`, `type`, `related_id`, `description`, `created_at`) VALUES (29, 26, 50, 'signup', NULL, '积分记录9', '2026-01-12 02:55:04');
INSERT INTO `points_records` (`id`, `user_id`, `points`, `type`, `related_id`, `description`, `created_at`) VALUES (30, 26, 10, 'review', NULL, '积分记录10', '2026-01-12 02:55:04');
INSERT INTO `points_records` (`id`, `user_id`, `points`, `type`, `related_id`, `description`, `created_at`) VALUES (31, 26, 10, 'order', NULL, '积分记录11', '2026-01-12 02:55:04');
INSERT INTO `points_records` (`id`, `user_id`, `points`, `type`, `related_id`, `description`, `created_at`) VALUES (32, 26, 50, 'signup', NULL, '积分记录12', '2026-01-12 02:55:04');
INSERT INTO `points_records` (`id`, `user_id`, `points`, `type`, `related_id`, `description`, `created_at`) VALUES (33, 26, 100, 'daily', NULL, '积分记录13', '2026-01-12 02:55:04');
INSERT INTO `points_records` (`id`, `user_id`, `points`, `type`, `related_id`, `description`, `created_at`) VALUES (34, 26, 20, 'signup', NULL, '积分记录14', '2026-01-12 02:55:04');
INSERT INTO `points_records` (`id`, `user_id`, `points`, `type`, `related_id`, `description`, `created_at`) VALUES (35, 26, 10, 'signup', NULL, '积分记录15', '2026-01-12 02:55:04');
INSERT INTO `points_records` (`id`, `user_id`, `points`, `type`, `related_id`, `description`, `created_at`) VALUES (36, 26, 100, 'order', NULL, '积分记录16', '2026-01-12 02:55:04');
INSERT INTO `points_records` (`id`, `user_id`, `points`, `type`, `related_id`, `description`, `created_at`) VALUES (37, 26, 50, 'signup', NULL, '积分记录17', '2026-01-12 02:55:04');
INSERT INTO `points_records` (`id`, `user_id`, `points`, `type`, `related_id`, `description`, `created_at`) VALUES (38, 26, 20, 'invite', NULL, '积分记录18', '2026-01-12 02:55:04');
INSERT INTO `points_records` (`id`, `user_id`, `points`, `type`, `related_id`, `description`, `created_at`) VALUES (39, 26, 20, 'daily', NULL, '积分记录19', '2026-01-12 02:55:04');
INSERT INTO `points_records` (`id`, `user_id`, `points`, `type`, `related_id`, `description`, `created_at`) VALUES (40, 26, 20, 'daily', NULL, '积分记录20', '2026-01-12 02:55:04');
INSERT INTO `points_records` (`id`, `user_id`, `points`, `type`, `related_id`, `description`, `created_at`) VALUES (41, 27, 100, 'review', NULL, '积分记录1', '2026-01-12 02:55:04');
INSERT INTO `points_records` (`id`, `user_id`, `points`, `type`, `related_id`, `description`, `created_at`) VALUES (42, 27, 20, 'signup', NULL, '积分记录2', '2026-01-12 02:55:04');
INSERT INTO `points_records` (`id`, `user_id`, `points`, `type`, `related_id`, `description`, `created_at`) VALUES (43, 27, 100, 'order', NULL, '积分记录3', '2026-01-12 02:55:04');
INSERT INTO `points_records` (`id`, `user_id`, `points`, `type`, `related_id`, `description`, `created_at`) VALUES (44, 27, 10, 'signup', NULL, '积分记录4', '2026-01-12 02:55:04');
INSERT INTO `points_records` (`id`, `user_id`, `points`, `type`, `related_id`, `description`, `created_at`) VALUES (45, 27, 10, 'review', NULL, '积分记录5', '2026-01-12 02:55:04');
INSERT INTO `points_records` (`id`, `user_id`, `points`, `type`, `related_id`, `description`, `created_at`) VALUES (46, 27, 50, 'daily', NULL, '积分记录6', '2026-01-12 02:55:04');
INSERT INTO `points_records` (`id`, `user_id`, `points`, `type`, `related_id`, `description`, `created_at`) VALUES (47, 27, 20, 'order', NULL, '积分记录7', '2026-01-12 02:55:04');
INSERT INTO `points_records` (`id`, `user_id`, `points`, `type`, `related_id`, `description`, `created_at`) VALUES (48, 27, 50, 'daily', NULL, '积分记录8', '2026-01-12 02:55:04');
INSERT INTO `points_records` (`id`, `user_id`, `points`, `type`, `related_id`, `description`, `created_at`) VALUES (49, 28, 100, 'daily', NULL, '积分记录1', '2026-01-12 02:55:04');
INSERT INTO `points_records` (`id`, `user_id`, `points`, `type`, `related_id`, `description`, `created_at`) VALUES (50, 28, 50, 'signup', NULL, '积分记录2', '2026-01-12 02:55:04');
INSERT INTO `points_records` (`id`, `user_id`, `points`, `type`, `related_id`, `description`, `created_at`) VALUES (51, 28, 100, 'daily', NULL, '积分记录3', '2026-01-12 02:55:04');
INSERT INTO `points_records` (`id`, `user_id`, `points`, `type`, `related_id`, `description`, `created_at`) VALUES (52, 28, 100, 'daily', NULL, '积分记录4', '2026-01-12 02:55:04');
INSERT INTO `points_records` (`id`, `user_id`, `points`, `type`, `related_id`, `description`, `created_at`) VALUES (53, 28, 50, 'daily', NULL, '积分记录5', '2026-01-12 02:55:04');
INSERT INTO `points_records` (`id`, `user_id`, `points`, `type`, `related_id`, `description`, `created_at`) VALUES (54, 28, 100, 'order', NULL, '积分记录6', '2026-01-12 02:55:04');
INSERT INTO `points_records` (`id`, `user_id`, `points`, `type`, `related_id`, `description`, `created_at`) VALUES (55, 28, 10, 'invite', NULL, '积分记录7', '2026-01-12 02:55:04');
INSERT INTO `points_records` (`id`, `user_id`, `points`, `type`, `related_id`, `description`, `created_at`) VALUES (56, 28, 100, 'daily', NULL, '积分记录8', '2026-01-12 02:55:04');
INSERT INTO `points_records` (`id`, `user_id`, `points`, `type`, `related_id`, `description`, `created_at`) VALUES (57, 28, 10, 'invite', NULL, '积分记录9', '2026-01-12 02:55:04');
INSERT INTO `points_records` (`id`, `user_id`, `points`, `type`, `related_id`, `description`, `created_at`) VALUES (58, 28, 100, 'signup', NULL, '积分记录10', '2026-01-12 02:55:04');
INSERT INTO `points_records` (`id`, `user_id`, `points`, `type`, `related_id`, `description`, `created_at`) VALUES (59, 28, 10, 'order', NULL, '积分记录11', '2026-01-12 02:55:04');
INSERT INTO `points_records` (`id`, `user_id`, `points`, `type`, `related_id`, `description`, `created_at`) VALUES (60, 28, 20, 'signup', NULL, '积分记录12', '2026-01-12 02:55:04');
INSERT INTO `points_records` (`id`, `user_id`, `points`, `type`, `related_id`, `description`, `created_at`) VALUES (61, 28, 20, 'order', NULL, '积分记录13', '2026-01-12 02:55:04');
INSERT INTO `points_records` (`id`, `user_id`, `points`, `type`, `related_id`, `description`, `created_at`) VALUES (62, 28, 10, 'invite', NULL, '积分记录14', '2026-01-12 02:55:04');
INSERT INTO `points_records` (`id`, `user_id`, `points`, `type`, `related_id`, `description`, `created_at`) VALUES (63, 28, 10, 'signup', NULL, '积分记录15', '2026-01-12 02:55:04');
INSERT INTO `points_records` (`id`, `user_id`, `points`, `type`, `related_id`, `description`, `created_at`) VALUES (64, 28, 20, 'review', NULL, '积分记录16', '2026-01-12 02:55:04');
INSERT INTO `points_records` (`id`, `user_id`, `points`, `type`, `related_id`, `description`, `created_at`) VALUES (65, 29, 10, 'review', NULL, '积分记录1', '2026-01-12 02:55:04');
INSERT INTO `points_records` (`id`, `user_id`, `points`, `type`, `related_id`, `description`, `created_at`) VALUES (66, 29, 10, 'review', NULL, '积分记录2', '2026-01-12 02:55:04');
INSERT INTO `points_records` (`id`, `user_id`, `points`, `type`, `related_id`, `description`, `created_at`) VALUES (67, 29, 50, 'invite', NULL, '积分记录3', '2026-01-12 02:55:04');
INSERT INTO `points_records` (`id`, `user_id`, `points`, `type`, `related_id`, `description`, `created_at`) VALUES (68, 29, 10, 'invite', NULL, '积分记录4', '2026-01-12 02:55:04');
INSERT INTO `points_records` (`id`, `user_id`, `points`, `type`, `related_id`, `description`, `created_at`) VALUES (69, 29, 100, 'signup', NULL, '积分记录5', '2026-01-12 02:55:04');
INSERT INTO `points_records` (`id`, `user_id`, `points`, `type`, `related_id`, `description`, `created_at`) VALUES (70, 29, 20, 'review', NULL, '积分记录6', '2026-01-12 02:55:04');
INSERT INTO `points_records` (`id`, `user_id`, `points`, `type`, `related_id`, `description`, `created_at`) VALUES (71, 29, 10, 'order', NULL, '积分记录7', '2026-01-12 02:55:04');
INSERT INTO `points_records` (`id`, `user_id`, `points`, `type`, `related_id`, `description`, `created_at`) VALUES (72, 29, 50, 'signup', NULL, '积分记录8', '2026-01-12 02:55:04');
INSERT INTO `points_records` (`id`, `user_id`, `points`, `type`, `related_id`, `description`, `created_at`) VALUES (73, 29, 10, 'signup', NULL, '积分记录9', '2026-01-12 02:55:04');
INSERT INTO `points_records` (`id`, `user_id`, `points`, `type`, `related_id`, `description`, `created_at`) VALUES (74, 29, 50, 'invite', NULL, '积分记录10', '2026-01-12 02:55:04');
INSERT INTO `points_records` (`id`, `user_id`, `points`, `type`, `related_id`, `description`, `created_at`) VALUES (75, 29, 10, 'signup', NULL, '积分记录11', '2026-01-12 02:55:04');
INSERT INTO `points_records` (`id`, `user_id`, `points`, `type`, `related_id`, `description`, `created_at`) VALUES (76, 30, 100, 'review', NULL, '积分记录1', '2026-01-12 02:55:04');
INSERT INTO `points_records` (`id`, `user_id`, `points`, `type`, `related_id`, `description`, `created_at`) VALUES (77, 30, 20, 'signup', NULL, '积分记录2', '2026-01-12 02:55:04');
INSERT INTO `points_records` (`id`, `user_id`, `points`, `type`, `related_id`, `description`, `created_at`) VALUES (78, 30, 50, 'review', NULL, '积分记录3', '2026-01-12 02:55:04');
INSERT INTO `points_records` (`id`, `user_id`, `points`, `type`, `related_id`, `description`, `created_at`) VALUES (79, 30, 50, 'signup', NULL, '积分记录4', '2026-01-12 02:55:04');
INSERT INTO `points_records` (`id`, `user_id`, `points`, `type`, `related_id`, `description`, `created_at`) VALUES (80, 30, 20, 'signup', NULL, '积分记录5', '2026-01-12 02:55:04');
INSERT INTO `points_records` (`id`, `user_id`, `points`, `type`, `related_id`, `description`, `created_at`) VALUES (81, 30, 50, 'review', NULL, '积分记录6', '2026-01-12 02:55:04');
INSERT INTO `points_records` (`id`, `user_id`, `points`, `type`, `related_id`, `description`, `created_at`) VALUES (82, 30, 100, 'order', NULL, '积分记录7', '2026-01-12 02:55:04');
INSERT INTO `points_records` (`id`, `user_id`, `points`, `type`, `related_id`, `description`, `created_at`) VALUES (83, 30, 50, 'signup', NULL, '积分记录8', '2026-01-12 02:55:04');
INSERT INTO `points_records` (`id`, `user_id`, `points`, `type`, `related_id`, `description`, `created_at`) VALUES (84, 30, 20, 'daily', NULL, '积分记录9', '2026-01-12 02:55:04');
INSERT INTO `points_records` (`id`, `user_id`, `points`, `type`, `related_id`, `description`, `created_at`) VALUES (85, 30, 20, 'signup', NULL, '积分记录10', '2026-01-12 02:55:04');
INSERT INTO `points_records` (`id`, `user_id`, `points`, `type`, `related_id`, `description`, `created_at`) VALUES (86, 31, 100, 'invite', NULL, '积分记录1', '2026-01-12 02:55:04');
INSERT INTO `points_records` (`id`, `user_id`, `points`, `type`, `related_id`, `description`, `created_at`) VALUES (87, 31, 50, 'invite', NULL, '积分记录2', '2026-01-12 02:55:04');
INSERT INTO `points_records` (`id`, `user_id`, `points`, `type`, `related_id`, `description`, `created_at`) VALUES (88, 31, 10, 'review', NULL, '积分记录3', '2026-01-12 02:55:04');
INSERT INTO `points_records` (`id`, `user_id`, `points`, `type`, `related_id`, `description`, `created_at`) VALUES (89, 31, 10, 'daily', NULL, '积分记录4', '2026-01-12 02:55:04');
INSERT INTO `points_records` (`id`, `user_id`, `points`, `type`, `related_id`, `description`, `created_at`) VALUES (90, 31, 10, 'order', NULL, '积分记录5', '2026-01-12 02:55:04');
INSERT INTO `points_records` (`id`, `user_id`, `points`, `type`, `related_id`, `description`, `created_at`) VALUES (91, 31, 10, 'daily', NULL, '积分记录6', '2026-01-12 02:55:04');
INSERT INTO `points_records` (`id`, `user_id`, `points`, `type`, `related_id`, `description`, `created_at`) VALUES (92, 31, 10, 'order', NULL, '积分记录7', '2026-01-12 02:55:04');
INSERT INTO `points_records` (`id`, `user_id`, `points`, `type`, `related_id`, `description`, `created_at`) VALUES (93, 31, 100, 'invite', NULL, '积分记录8', '2026-01-12 02:55:04');
INSERT INTO `points_records` (`id`, `user_id`, `points`, `type`, `related_id`, `description`, `created_at`) VALUES (94, 31, 20, 'daily', NULL, '积分记录9', '2026-01-12 02:55:04');
INSERT INTO `points_records` (`id`, `user_id`, `points`, `type`, `related_id`, `description`, `created_at`) VALUES (95, 31, 50, 'signup', NULL, '积分记录10', '2026-01-12 02:55:04');
INSERT INTO `points_records` (`id`, `user_id`, `points`, `type`, `related_id`, `description`, `created_at`) VALUES (96, 31, 10, 'daily', NULL, '积分记录11', '2026-01-12 02:55:04');
COMMIT;

-- ----------------------------
-- Table structure for project_categories
-- ----------------------------
DROP TABLE IF EXISTS `project_categories`;
CREATE TABLE `project_categories` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `name` varchar(100) NOT NULL COMMENT '分类名称',
  `code` varchar(50) DEFAULT NULL COMMENT '分类代码',
  `parent_id` bigint DEFAULT NULL COMMENT '父分类ID',
  `level` int DEFAULT '1' COMMENT '层级',
  `description` text COMMENT '分类描述',
  `is_hot` tinyint(1) DEFAULT '0' COMMENT '是否热门',
  `icon` varchar(200) DEFAULT NULL COMMENT '图标',
  `cover_image` varchar(500) DEFAULT NULL COMMENT '封面图',
  `sort_order` int DEFAULT '0' COMMENT '排序',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `is_active` tinyint(1) DEFAULT '1' COMMENT '是否启用',
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`),
  KEY `idx_sort` (`sort_order`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='项目分类表';

-- ----------------------------
-- Records of project_categories
-- ----------------------------
BEGIN;
INSERT INTO `project_categories` (`id`, `name`, `code`, `parent_id`, `level`, `description`, `is_hot`, `icon`, `cover_image`, `sort_order`, `created_at`, `is_active`) VALUES (1, '微观形貌', NULL, NULL, 1, '扫描电镜、透射电镜等形貌观察', 0, '🔬', NULL, 1, '2025-10-18 18:16:06', 1);
INSERT INTO `project_categories` (`id`, `name`, `code`, `parent_id`, `level`, `description`, `is_hot`, `icon`, `cover_image`, `sort_order`, `created_at`, `is_active`) VALUES (2, '成分分析', NULL, NULL, 1, 'XRD、FTIR、NMR等成分检测', 0, '🧪', NULL, 2, '2025-10-18 18:16:06', 1);
INSERT INTO `project_categories` (`id`, `name`, `code`, `parent_id`, `level`, `description`, `is_hot`, `icon`, `cover_image`, `sort_order`, `created_at`, `is_active`) VALUES (3, '热学性能', NULL, NULL, 1, 'TGA、DSC等热性能测试', 0, '🌡️', NULL, 3, '2025-10-18 18:16:06', 1);
INSERT INTO `project_categories` (`id`, `name`, `code`, `parent_id`, `level`, `description`, `is_hot`, `icon`, `cover_image`, `sort_order`, `created_at`, `is_active`) VALUES (4, '力学性能', NULL, NULL, 1, '拉伸、压缩等力学测试', 0, '💪', NULL, 4, '2025-10-18 18:16:06', 1);
INSERT INTO `project_categories` (`id`, `name`, `code`, `parent_id`, `level`, `description`, `is_hot`, `icon`, `cover_image`, `sort_order`, `created_at`, `is_active`) VALUES (5, '生物医药', '', NULL, 1, '', 0, '', NULL, 5, '2025-12-30 15:28:55', 1);
INSERT INTO `project_categories` (`id`, `name`, `code`, `parent_id`, `level`, `description`, `is_hot`, `icon`, `cover_image`, `sort_order`, `created_at`, `is_active`) VALUES (6, '材料分析', 'material', NULL, 1, '材料成分、结构、性能分析', 0, '🔬', NULL, 1, '2026-01-12 10:31:05', 1);
INSERT INTO `project_categories` (`id`, `name`, `code`, `parent_id`, `level`, `description`, `is_hot`, `icon`, `cover_image`, `sort_order`, `created_at`, `is_active`) VALUES (7, '表面分析', 'surface', NULL, 1, '表面形貌、成分、结构分析', 0, '🔍', NULL, 2, '2026-01-12 10:31:05', 1);
INSERT INTO `project_categories` (`id`, `name`, `code`, `parent_id`, `level`, `description`, `is_hot`, `icon`, `cover_image`, `sort_order`, `created_at`, `is_active`) VALUES (8, '热分析', 'thermal', NULL, 1, '热性能、热稳定性分析', 0, '🌡️', NULL, 3, '2026-01-12 10:31:05', 1);
INSERT INTO `project_categories` (`id`, `name`, `code`, `parent_id`, `level`, `description`, `is_hot`, `icon`, `cover_image`, `sort_order`, `created_at`, `is_active`) VALUES (9, '光谱分析', 'spectrum', NULL, 1, '各类光谱测试分析', 0, '🌈', NULL, 4, '2026-01-12 10:31:05', 1);
INSERT INTO `project_categories` (`id`, `name`, `code`, `parent_id`, `level`, `description`, `is_hot`, `icon`, `cover_image`, `sort_order`, `created_at`, `is_active`) VALUES (10, '力学测试', 'mechanical', NULL, 1, '力学性能测试', 0, '💪', NULL, 5, '2026-01-12 10:31:05', 1);
INSERT INTO `project_categories` (`id`, `name`, `code`, `parent_id`, `level`, `description`, `is_hot`, `icon`, `cover_image`, `sort_order`, `created_at`, `is_active`) VALUES (11, '环境检测', 'environment', NULL, 1, '环境样品检测分析', 0, '🌿', NULL, 6, '2026-01-12 10:31:05', 1);
INSERT INTO `project_categories` (`id`, `name`, `code`, `parent_id`, `level`, `description`, `is_hot`, `icon`, `cover_image`, `sort_order`, `created_at`, `is_active`) VALUES (12, '生物医学', 'biomedical', NULL, 1, '生物医学相关检测', 0, '🧬', NULL, 7, '2026-01-12 10:31:05', 1);
INSERT INTO `project_categories` (`id`, `name`, `code`, `parent_id`, `level`, `description`, `is_hot`, `icon`, `cover_image`, `sort_order`, `created_at`, `is_active`) VALUES (13, '电化学', 'electrochemistry', NULL, 1, '电化学性能测试', 0, '⚡', NULL, 8, '2026-01-12 10:31:05', 1);
COMMIT;

-- ----------------------------
-- Table structure for project_favorites
-- ----------------------------
DROP TABLE IF EXISTS `project_favorites`;
CREATE TABLE `project_favorites` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL COMMENT '用户ID',
  `project_id` int NOT NULL COMMENT '项目ID',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '收藏时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_user_project` (`user_id`,`project_id`),
  KEY `ix_project_favorites_user_id` (`user_id`),
  KEY `ix_project_favorites_id` (`id`),
  KEY `ix_project_favorites_project_id` (`project_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of project_favorites
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for project_options
-- ----------------------------
DROP TABLE IF EXISTS `project_options`;
CREATE TABLE `project_options` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `project_id` bigint DEFAULT NULL COMMENT '关联项目ID',
  `category_id` bigint DEFAULT NULL COMMENT '关联分类ID（与project_id二选一）',
  `parent_id` bigint DEFAULT NULL COMMENT '父选项ID（null为根选项）',
  `level` int DEFAULT NULL COMMENT '层级深度',
  `path` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '物化路径 如 /1/5/12/',
  `name` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '选项名称',
  `option_type` enum('single','multi','input') COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '选项类型: single/multi/input',
  `price` decimal(10,2) DEFAULT NULL COMMENT '价格调整',
  `price_type` enum('fixed','per_sample','percentage') COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '价格类型: fixed/per_sample/percentage',
  `hint_text` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '红色提示文字',
  `placeholder` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '输入框占位符（input类型时使用）',
  `sort_order` int DEFAULT NULL COMMENT '排序',
  `is_required` tinyint(1) DEFAULT NULL COMMENT '是否必填',
  `is_active` tinyint(1) DEFAULT NULL COMMENT '是否启用',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `ix_project_options_category_id` (`category_id`),
  KEY `ix_project_options_project_id` (`project_id`),
  KEY `ix_project_options_parent_id` (`parent_id`),
  KEY `ix_project_options_id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of project_options
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for project_reviews
-- ----------------------------
DROP TABLE IF EXISTS `project_reviews`;
CREATE TABLE `project_reviews` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `project_id` bigint NOT NULL COMMENT '项目ID',
  `user_id` bigint NOT NULL COMMENT '用户ID',
  `order_id` bigint DEFAULT NULL COMMENT '订单ID',
  `rating` int NOT NULL COMMENT '评分',
  `content` text COMMENT '评价内容',
  `images` json DEFAULT NULL COMMENT '评价图片',
  `status` varchar(20) DEFAULT 'pending' COMMENT '状态',
  `reply` text COMMENT '商家回复',
  `reply_at` datetime DEFAULT NULL COMMENT '回复时间',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  KEY `idx_project` (`project_id`),
  KEY `idx_user` (`user_id`),
  KEY `idx_order` (`order_id`),
  KEY `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='项目评价表';

-- ----------------------------
-- Records of project_reviews
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for projects
-- ----------------------------
DROP TABLE IF EXISTS `projects`;
CREATE TABLE `projects` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `project_no` varchar(32) NOT NULL COMMENT '项目编号',
  `name` varchar(200) NOT NULL COMMENT '项目名称',
  `category_id` bigint NOT NULL COMMENT '分类ID',
  `lab_id` bigint NOT NULL COMMENT '实验室ID',
  `original_price` decimal(10,2) NOT NULL COMMENT '原价',
  `current_price` decimal(10,2) NOT NULL COMMENT '现价',
  `unit` varchar(20) DEFAULT '样品' COMMENT '单位',
  `service_cycle_min` int DEFAULT NULL COMMENT '最短服务周期',
  `service_cycle_max` int DEFAULT NULL COMMENT '最长服务周期',
  `equipment_name` varchar(200) DEFAULT NULL COMMENT '仪器名称',
  `equipment_model` varchar(200) DEFAULT NULL COMMENT '仪器型号',
  `introduction` text COMMENT '项目介绍',
  `sample_requirements` text COMMENT '样品要求',
  `test_parameters` json DEFAULT NULL COMMENT '检测参数',
  `booking_notice` text COMMENT '预约须知',
  `faq` json DEFAULT NULL COMMENT '常见问题',
  `cover_image` varchar(500) DEFAULT NULL COMMENT '封面图',
  `detail_images` json DEFAULT NULL COMMENT '详情图',
  `status` varchar(20) DEFAULT 'active' COMMENT '状态',
  `is_hot` tinyint(1) DEFAULT '0' COMMENT '是否热门',
  `is_recommended` tinyint(1) DEFAULT '0' COMMENT '是否推荐',
  `view_count` int DEFAULT '0' COMMENT '浏览量',
  `order_count` int DEFAULT '0' COMMENT '订单量',
  `booking_count` int DEFAULT '0' COMMENT '预约量',
  `satisfaction` decimal(5,2) DEFAULT '100.00' COMMENT '满意度',
  `sort_order` int DEFAULT '0' COMMENT '排序',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `project_no` (`project_no`),
  KEY `idx_category` (`category_id`),
  KEY `idx_lab` (`lab_id`),
  KEY `idx_status` (`status`),
  KEY `idx_hot` (`is_hot`),
  KEY `idx_recommended` (`is_recommended`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='项目表';

-- ----------------------------
-- Records of projects
-- ----------------------------
BEGIN;
INSERT INTO `projects` (`id`, `project_no`, `name`, `category_id`, `lab_id`, `original_price`, `current_price`, `unit`, `service_cycle_min`, `service_cycle_max`, `equipment_name`, `equipment_model`, `introduction`, `sample_requirements`, `test_parameters`, `booking_notice`, `faq`, `cover_image`, `detail_images`, `status`, `is_hot`, `is_recommended`, `view_count`, `order_count`, `booking_count`, `satisfaction`, `sort_order`, `created_at`, `updated_at`) VALUES (1, 'PRJ001', '扫描电镜（SEM）', 1, 1, 200.00, 180.00, '样品', 3, 5, 'Zeiss Sigma 300', NULL, '扫描电子显微镜，观察样品表面形貌，分辨率可达纳米级别。适用于材料表面结构分析、断口分析等。', '样品尺寸不超过50mm；样品需导电或喷金处理；干燥样品', NULL, NULL, NULL, 'https://picsum.photos/400/300?random=1', NULL, 'active', 1, 0, 74, 0, 0, 100.00, 1, '2025-10-18 18:16:06', '2026-01-16 18:28:09');
INSERT INTO `projects` (`id`, `project_no`, `name`, `category_id`, `lab_id`, `original_price`, `current_price`, `unit`, `service_cycle_min`, `service_cycle_max`, `equipment_name`, `equipment_model`, `introduction`, `sample_requirements`, `test_parameters`, `booking_notice`, `faq`, `cover_image`, `detail_images`, `status`, `is_hot`, `is_recommended`, `view_count`, `order_count`, `booking_count`, `satisfaction`, `sort_order`, `created_at`, `updated_at`) VALUES (2, 'PRJ002', '透射电镜（TEM）', 1, 1, 300.00, 280.00, '样品', 5, 7, 'FEI Tecnai G2 F20', NULL, '透射电子显微镜，可观察样品内部结构，分辨率达到原子级别。适用于纳米材料结构分析、晶体结构研究等。', '样品厚度小于100nm；样品需制备成薄片；导电样品', NULL, NULL, NULL, 'https://picsum.photos/400/300?random=2', NULL, 'active', 1, 0, 20, 0, 0, 100.00, 2, '2025-10-18 18:16:06', '2025-12-30 14:40:13');
INSERT INTO `projects` (`id`, `project_no`, `name`, `category_id`, `lab_id`, `original_price`, `current_price`, `unit`, `service_cycle_min`, `service_cycle_max`, `equipment_name`, `equipment_model`, `introduction`, `sample_requirements`, `test_parameters`, `booking_notice`, `faq`, `cover_image`, `detail_images`, `status`, `is_hot`, `is_recommended`, `view_count`, `order_count`, `booking_count`, `satisfaction`, `sort_order`, `created_at`, `updated_at`) VALUES (3, 'PRJ003', 'X射线衍射（XRD）', 2, 1, 150.00, 130.00, '样品', 2, 3, 'Bruker D8 Advance', NULL, 'X射线衍射仪，用于物质晶体结构分析、相组成分析、晶粒大小测定等。', '粉末样品或块状样品；样品量≥100mg；平整表面', NULL, NULL, NULL, 'https://picsum.photos/400/300?random=3', NULL, 'active', 0, 0, 6, 0, 0, 100.00, 3, '2025-10-18 18:16:06', '2026-01-11 16:23:11');
INSERT INTO `projects` (`id`, `project_no`, `name`, `category_id`, `lab_id`, `original_price`, `current_price`, `unit`, `service_cycle_min`, `service_cycle_max`, `equipment_name`, `equipment_model`, `introduction`, `sample_requirements`, `test_parameters`, `booking_notice`, `faq`, `cover_image`, `detail_images`, `status`, `is_hot`, `is_recommended`, `view_count`, `order_count`, `booking_count`, `satisfaction`, `sort_order`, `created_at`, `updated_at`) VALUES (4, 'PRJ004', '红外光谱（FTIR）', 2, 1, 100.00, 90.00, '样品', 1, 2, 'Thermo Nicolet iS50', NULL, '傅里叶变换红外光谱仪，用于有机物、无机物的定性定量分析，官能团鉴定。', '固体或液体样品；样品量≥10mg；避免强吸湿性', NULL, NULL, NULL, 'https://picsum.photos/400/300?random=4', NULL, 'active', 0, 0, 6, 0, 0, 100.00, 4, '2025-10-18 18:16:06', '2025-11-23 21:15:20');
INSERT INTO `projects` (`id`, `project_no`, `name`, `category_id`, `lab_id`, `original_price`, `current_price`, `unit`, `service_cycle_min`, `service_cycle_max`, `equipment_name`, `equipment_model`, `introduction`, `sample_requirements`, `test_parameters`, `booking_notice`, `faq`, `cover_image`, `detail_images`, `status`, `is_hot`, `is_recommended`, `view_count`, `order_count`, `booking_count`, `satisfaction`, `sort_order`, `created_at`, `updated_at`) VALUES (5, 'PRJ005', '热重分析（TGA）', 3, 1, 180.00, 160.00, '样品', 2, 3, 'TA Instruments Q500', NULL, '热重分析仪，测量样品质量随温度变化关系，用于材料热稳定性、分解温度测定等。', '样品量5-20mg；粉末或小块状；不挥发性溶剂', NULL, NULL, NULL, 'https://picsum.photos/400/300?random=5', NULL, 'active', 0, 0, 7, 0, 0, 100.00, 5, '2025-10-18 18:16:06', '2025-11-23 22:58:58');
INSERT INTO `projects` (`id`, `project_no`, `name`, `category_id`, `lab_id`, `original_price`, `current_price`, `unit`, `service_cycle_min`, `service_cycle_max`, `equipment_name`, `equipment_model`, `introduction`, `sample_requirements`, `test_parameters`, `booking_notice`, `faq`, `cover_image`, `detail_images`, `status`, `is_hot`, `is_recommended`, `view_count`, `order_count`, `booking_count`, `satisfaction`, `sort_order`, `created_at`, `updated_at`) VALUES (6, 'PRJ006', '万能材料试验机', 4, 1, 250.00, 230.00, '样品', 3, 5, 'Instron 5969', NULL, '万能材料试验机，用于材料拉伸、压缩、弯曲、剪切等力学性能测试。', '标准试样；尺寸符合国标；表面光滑', NULL, NULL, NULL, 'https://picsum.photos/400/300?random=6', NULL, 'active', 1, 0, 6, 0, 0, 100.00, 6, '2025-10-18 18:16:06', '2025-12-30 14:41:19');
INSERT INTO `projects` (`id`, `project_no`, `name`, `category_id`, `lab_id`, `original_price`, `current_price`, `unit`, `service_cycle_min`, `service_cycle_max`, `equipment_name`, `equipment_model`, `introduction`, `sample_requirements`, `test_parameters`, `booking_notice`, `faq`, `cover_image`, `detail_images`, `status`, `is_hot`, `is_recommended`, `view_count`, `order_count`, `booking_count`, `satisfaction`, `sort_order`, `created_at`, `updated_at`) VALUES (7, 'PRJ007', '核磁共振（NMR）', 2, 1, 400.00, 380.00, '样品', 5, 7, 'Bruker Avance III 400', NULL, '核磁共振波谱仪，用于有机化合物结构鉴定、纯度分析、反应机理研究等。', '样品量≥5mg；溶于氘代溶剂；高纯度样品', NULL, NULL, NULL, 'https://picsum.photos/400/300?random=7', NULL, 'active', 0, 0, 11, 0, 0, 100.00, 7, '2025-10-18 18:16:06', '2025-11-23 21:35:30');
INSERT INTO `projects` (`id`, `project_no`, `name`, `category_id`, `lab_id`, `original_price`, `current_price`, `unit`, `service_cycle_min`, `service_cycle_max`, `equipment_name`, `equipment_model`, `introduction`, `sample_requirements`, `test_parameters`, `booking_notice`, `faq`, `cover_image`, `detail_images`, `status`, `is_hot`, `is_recommended`, `view_count`, `order_count`, `booking_count`, `satisfaction`, `sort_order`, `created_at`, `updated_at`) VALUES (8, 'PRJ008', '气相色谱-质谱联用（GC-MS）', 2, 1, 350.00, 320.00, '样品', 4, 6, 'Agilent 7890B-5977A', NULL, '气相色谱-质谱联用仪，用于复杂混合物分离鉴定、有机物定性定量分析。', '液体或可挥发固体；样品量≥1ml；不含颗粒物', NULL, NULL, NULL, 'https://picsum.photos/400/300?random=8', NULL, 'active', 1, 0, 4, 0, 0, 100.00, 8, '2025-10-18 18:16:06', '2026-01-11 16:18:13');
INSERT INTO `projects` (`id`, `project_no`, `name`, `category_id`, `lab_id`, `original_price`, `current_price`, `unit`, `service_cycle_min`, `service_cycle_max`, `equipment_name`, `equipment_model`, `introduction`, `sample_requirements`, `test_parameters`, `booking_notice`, `faq`, `cover_image`, `detail_images`, `status`, `is_hot`, `is_recommended`, `view_count`, `order_count`, `booking_count`, `satisfaction`, `sort_order`, `created_at`, `updated_at`) VALUES (9, 'PRJ0001', '能谱分析（EDS）', 6, 9, 180.00, 150.00, '点', 2, 3, 'Oxford X-Max', NULL, '元素成分定性和半定量分析', NULL, NULL, NULL, NULL, NULL, NULL, 'active', 0, 0, 110, 11, 0, 100.00, 0, '2026-01-12 17:04:40', NULL);
INSERT INTO `projects` (`id`, `project_no`, `name`, `category_id`, `lab_id`, `original_price`, `current_price`, `unit`, `service_cycle_min`, `service_cycle_max`, `equipment_name`, `equipment_model`, `introduction`, `sample_requirements`, `test_parameters`, `booking_notice`, `faq`, `cover_image`, `detail_images`, `status`, `is_hot`, `is_recommended`, `view_count`, `order_count`, `booking_count`, `satisfaction`, `sort_order`, `created_at`, `updated_at`) VALUES (10, 'PRJ0002', 'X射线光电子能谱（XPS）', 7, 10, 480.00, 400.00, '样', 5, 7, 'Thermo ESCALAB 250Xi', NULL, '表面元素组成和化学态分析', NULL, NULL, NULL, NULL, NULL, NULL, 'active', 1, 1, 125, 12, 0, 100.00, 0, '2026-01-12 17:04:40', '2026-01-16 19:55:29');
INSERT INTO `projects` (`id`, `project_no`, `name`, `category_id`, `lab_id`, `original_price`, `current_price`, `unit`, `service_cycle_min`, `service_cycle_max`, `equipment_name`, `equipment_model`, `introduction`, `sample_requirements`, `test_parameters`, `booking_notice`, `faq`, `cover_image`, `detail_images`, `status`, `is_hot`, `is_recommended`, `view_count`, `order_count`, `booking_count`, `satisfaction`, `sort_order`, `created_at`, `updated_at`) VALUES (11, 'PRJ0003', '原子力显微镜（AFM）', 7, 9, 360.00, 300.00, '样', 3, 5, 'Bruker Dimension Icon', NULL, '纳米级表面形貌和力学性能测量', NULL, NULL, NULL, NULL, NULL, NULL, 'active', 0, 0, 130, 13, 0, 100.00, 0, '2026-01-12 17:04:40', NULL);
INSERT INTO `projects` (`id`, `project_no`, `name`, `category_id`, `lab_id`, `original_price`, `current_price`, `unit`, `service_cycle_min`, `service_cycle_max`, `equipment_name`, `equipment_model`, `introduction`, `sample_requirements`, `test_parameters`, `booking_notice`, `faq`, `cover_image`, `detail_images`, `status`, `is_hot`, `is_recommended`, `view_count`, `order_count`, `booking_count`, `satisfaction`, `sort_order`, `created_at`, `updated_at`) VALUES (12, 'PRJ0004', '接触角测量', 7, 9, 120.00, 100.00, '样', 1, 2, 'Dataphysics OCA25', NULL, '表面润湿性和表面能测量', NULL, NULL, NULL, NULL, NULL, NULL, 'active', 0, 0, 140, 14, 0, 100.00, 0, '2026-01-12 17:04:40', NULL);
INSERT INTO `projects` (`id`, `project_no`, `name`, `category_id`, `lab_id`, `original_price`, `current_price`, `unit`, `service_cycle_min`, `service_cycle_max`, `equipment_name`, `equipment_model`, `introduction`, `sample_requirements`, `test_parameters`, `booking_notice`, `faq`, `cover_image`, `detail_images`, `status`, `is_hot`, `is_recommended`, `view_count`, `order_count`, `booking_count`, `satisfaction`, `sort_order`, `created_at`, `updated_at`) VALUES (13, 'PRJ0005', '差示扫描量热（DSC）', 8, 9, 240.00, 200.00, '样', 2, 3, 'TA Q2000', NULL, '相变温度、熔点、结晶度测量', NULL, NULL, NULL, NULL, NULL, NULL, 'active', 0, 0, 151, 15, 0, 100.00, 0, '2026-01-12 17:04:40', '2026-01-13 10:56:14');
INSERT INTO `projects` (`id`, `project_no`, `name`, `category_id`, `lab_id`, `original_price`, `current_price`, `unit`, `service_cycle_min`, `service_cycle_max`, `equipment_name`, `equipment_model`, `introduction`, `sample_requirements`, `test_parameters`, `booking_notice`, `faq`, `cover_image`, `detail_images`, `status`, `is_hot`, `is_recommended`, `view_count`, `order_count`, `booking_count`, `satisfaction`, `sort_order`, `created_at`, `updated_at`) VALUES (14, 'PRJ0006', '热机械分析（TMA）', 8, 11, 300.00, 250.00, '样', 3, 5, 'TA Q400', NULL, '热膨胀系数和软化温度测量', NULL, NULL, NULL, NULL, NULL, NULL, 'active', 0, 0, 160, 16, 0, 100.00, 0, '2026-01-12 17:04:40', NULL);
INSERT INTO `projects` (`id`, `project_no`, `name`, `category_id`, `lab_id`, `original_price`, `current_price`, `unit`, `service_cycle_min`, `service_cycle_max`, `equipment_name`, `equipment_model`, `introduction`, `sample_requirements`, `test_parameters`, `booking_notice`, `faq`, `cover_image`, `detail_images`, `status`, `is_hot`, `is_recommended`, `view_count`, `order_count`, `booking_count`, `satisfaction`, `sort_order`, `created_at`, `updated_at`) VALUES (15, 'PRJ0007', '傅里叶红外光谱（FTIR）', 9, 9, 180.00, 150.00, '样', 1, 2, 'Thermo Nicolet iS50', NULL, '有机官能团和分子结构分析', NULL, NULL, NULL, NULL, NULL, NULL, 'active', 1, 1, 179, 17, 0, 100.00, 0, '2026-01-12 17:04:40', '2026-01-16 20:16:31');
INSERT INTO `projects` (`id`, `project_no`, `name`, `category_id`, `lab_id`, `original_price`, `current_price`, `unit`, `service_cycle_min`, `service_cycle_max`, `equipment_name`, `equipment_model`, `introduction`, `sample_requirements`, `test_parameters`, `booking_notice`, `faq`, `cover_image`, `detail_images`, `status`, `is_hot`, `is_recommended`, `view_count`, `order_count`, `booking_count`, `satisfaction`, `sort_order`, `created_at`, `updated_at`) VALUES (16, 'PRJ0008', '拉曼光谱', 9, 9, 240.00, 200.00, '样', 2, 3, 'Horiba LabRAM HR', NULL, '分子振动和晶体结构分析', NULL, NULL, NULL, NULL, NULL, NULL, 'active', 0, 0, 180, 18, 0, 100.00, 0, '2026-01-12 17:04:40', NULL);
INSERT INTO `projects` (`id`, `project_no`, `name`, `category_id`, `lab_id`, `original_price`, `current_price`, `unit`, `service_cycle_min`, `service_cycle_max`, `equipment_name`, `equipment_model`, `introduction`, `sample_requirements`, `test_parameters`, `booking_notice`, `faq`, `cover_image`, `detail_images`, `status`, `is_hot`, `is_recommended`, `view_count`, `order_count`, `booking_count`, `satisfaction`, `sort_order`, `created_at`, `updated_at`) VALUES (17, 'PRJ0009', '紫外可见光谱（UV-Vis）', 9, 9, 120.00, 100.00, '样', 1, 2, 'Shimadzu UV-2600', NULL, '光吸收特性和浓度测量', NULL, NULL, NULL, NULL, NULL, NULL, 'active', 0, 0, 190, 19, 0, 100.00, 0, '2026-01-12 17:04:40', NULL);
INSERT INTO `projects` (`id`, `project_no`, `name`, `category_id`, `lab_id`, `original_price`, `current_price`, `unit`, `service_cycle_min`, `service_cycle_max`, `equipment_name`, `equipment_model`, `introduction`, `sample_requirements`, `test_parameters`, `booking_notice`, `faq`, `cover_image`, `detail_images`, `status`, `is_hot`, `is_recommended`, `view_count`, `order_count`, `booking_count`, `satisfaction`, `sort_order`, `created_at`, `updated_at`) VALUES (18, 'PRJ0010', '荧光光谱（PL）', 9, 10, 240.00, 200.00, '样', 2, 3, 'Edinburgh FLS1000', NULL, '荧光特性和量子效率测量', NULL, NULL, NULL, NULL, NULL, NULL, 'active', 0, 0, 201, 20, 0, 100.00, 0, '2026-01-12 17:04:40', '2026-01-13 10:56:22');
INSERT INTO `projects` (`id`, `project_no`, `name`, `category_id`, `lab_id`, `original_price`, `current_price`, `unit`, `service_cycle_min`, `service_cycle_max`, `equipment_name`, `equipment_model`, `introduction`, `sample_requirements`, `test_parameters`, `booking_notice`, `faq`, `cover_image`, `detail_images`, `status`, `is_hot`, `is_recommended`, `view_count`, `order_count`, `booking_count`, `satisfaction`, `sort_order`, `created_at`, `updated_at`) VALUES (19, 'PRJ0011', '万能材料试验', 10, 9, 180.00, 150.00, '样', 2, 3, 'Instron 5967', NULL, '拉伸、压缩、弯曲力学性能测试', NULL, NULL, NULL, NULL, NULL, NULL, 'active', 0, 0, 210, 21, 0, 100.00, 0, '2026-01-12 17:04:40', NULL);
INSERT INTO `projects` (`id`, `project_no`, `name`, `category_id`, `lab_id`, `original_price`, `current_price`, `unit`, `service_cycle_min`, `service_cycle_max`, `equipment_name`, `equipment_model`, `introduction`, `sample_requirements`, `test_parameters`, `booking_notice`, `faq`, `cover_image`, `detail_images`, `status`, `is_hot`, `is_recommended`, `view_count`, `order_count`, `booking_count`, `satisfaction`, `sort_order`, `created_at`, `updated_at`) VALUES (20, 'PRJ0012', '纳米压痕测试', 10, 10, 360.00, 300.00, '点', 3, 5, 'Hysitron TI950', NULL, '纳米硬度和弹性模量测量', NULL, NULL, NULL, NULL, NULL, NULL, 'active', 0, 0, 222, 22, 0, 100.00, 0, '2026-01-12 17:04:40', '2026-01-13 10:56:26');
INSERT INTO `projects` (`id`, `project_no`, `name`, `category_id`, `lab_id`, `original_price`, `current_price`, `unit`, `service_cycle_min`, `service_cycle_max`, `equipment_name`, `equipment_model`, `introduction`, `sample_requirements`, `test_parameters`, `booking_notice`, `faq`, `cover_image`, `detail_images`, `status`, `is_hot`, `is_recommended`, `view_count`, `order_count`, `booking_count`, `satisfaction`, `sort_order`, `created_at`, `updated_at`) VALUES (21, 'PRJ0013', '动态力学分析（DMA）', 10, 9, 300.00, 250.00, '样', 2, 4, 'TA Q800', NULL, '动态力学性能和阻尼特性分析', NULL, NULL, NULL, NULL, NULL, NULL, 'active', 0, 0, 230, 23, 0, 100.00, 0, '2026-01-12 17:04:40', NULL);
INSERT INTO `projects` (`id`, `project_no`, `name`, `category_id`, `lab_id`, `original_price`, `current_price`, `unit`, `service_cycle_min`, `service_cycle_max`, `equipment_name`, `equipment_model`, `introduction`, `sample_requirements`, `test_parameters`, `booking_notice`, `faq`, `cover_image`, `detail_images`, `status`, `is_hot`, `is_recommended`, `view_count`, `order_count`, `booking_count`, `satisfaction`, `sort_order`, `created_at`, `updated_at`) VALUES (22, 'PRJ0014', '循环伏安测试（CV）', 13, 11, 180.00, 150.00, '样', 2, 3, 'CHI 760E', NULL, '电化学氧化还原特性分析', NULL, NULL, NULL, NULL, NULL, NULL, 'active', 0, 0, 240, 24, 0, 100.00, 0, '2026-01-12 17:04:40', NULL);
INSERT INTO `projects` (`id`, `project_no`, `name`, `category_id`, `lab_id`, `original_price`, `current_price`, `unit`, `service_cycle_min`, `service_cycle_max`, `equipment_name`, `equipment_model`, `introduction`, `sample_requirements`, `test_parameters`, `booking_notice`, `faq`, `cover_image`, `detail_images`, `status`, `is_hot`, `is_recommended`, `view_count`, `order_count`, `booking_count`, `satisfaction`, `sort_order`, `created_at`, `updated_at`) VALUES (23, 'PRJ0015', '电化学阻抗谱（EIS）', 13, 11, 240.00, 200.00, '样', 2, 3, 'Gamry Reference 3000', NULL, '电极界面和电化学动力学分析', NULL, NULL, NULL, NULL, NULL, NULL, 'active', 0, 0, 250, 25, 0, 100.00, 0, '2026-01-12 17:04:40', NULL);
INSERT INTO `projects` (`id`, `project_no`, `name`, `category_id`, `lab_id`, `original_price`, `current_price`, `unit`, `service_cycle_min`, `service_cycle_max`, `equipment_name`, `equipment_model`, `introduction`, `sample_requirements`, `test_parameters`, `booking_notice`, `faq`, `cover_image`, `detail_images`, `status`, `is_hot`, `is_recommended`, `view_count`, `order_count`, `booking_count`, `satisfaction`, `sort_order`, `created_at`, `updated_at`) VALUES (24, 'PRJ0016', '电池充放电测试', 13, 9, 360.00, 300.00, '样', 7, 14, 'LAND CT2001A', NULL, '电池容量和循环性能测试', NULL, NULL, NULL, NULL, NULL, NULL, 'active', 0, 0, 260, 26, 0, 100.00, 0, '2026-01-12 17:04:40', NULL);
COMMIT;

-- ----------------------------
-- Table structure for quick_replies
-- ----------------------------
DROP TABLE IF EXISTS `quick_replies`;
CREATE TABLE `quick_replies` (
  `id` int NOT NULL AUTO_INCREMENT,
  `question` varchar(500) NOT NULL COMMENT '问题',
  `answer` text NOT NULL COMMENT '回答',
  `category` varchar(50) DEFAULT NULL COMMENT '分类',
  `sort_order` int DEFAULT '0' COMMENT '排序',
  `is_active` tinyint(1) DEFAULT '1' COMMENT '是否启用',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='快捷回复';

-- ----------------------------
-- Records of quick_replies
-- ----------------------------
BEGIN;
INSERT INTO `quick_replies` (`id`, `question`, `answer`, `category`, `sort_order`, `is_active`, `created_at`) VALUES (1, '检测需要多长时间？', '一般检测周期为3-7个工作日，具体时间取决于检测项目的复杂程度。加急服务可缩短至1-3个工作日，需额外支付加急费用。', '常见问题', 1, 1, '2025-12-07 11:55:39');
INSERT INTO `quick_replies` (`id`, `question`, `answer`, `category`, `sort_order`, `is_active`, `created_at`) VALUES (2, '如何查看检测进度？', '您可以在\"我的订单\"页面查看订单状态，或使用\"样品追踪\"功能实时了解检测进度。', '常见问题', 2, 1, '2025-12-07 11:55:39');
INSERT INTO `quick_replies` (`id`, `question`, `answer`, `category`, `sort_order`, `is_active`, `created_at`) VALUES (3, '报告可以加急吗？', '可以的，我们提供加急服务。下单时选择加急选项或联系客服说明需求，加急费用根据项目不同有所差异。', '常见问题', 3, 1, '2025-12-07 11:55:39');
INSERT INTO `quick_replies` (`id`, `question`, `answer`, `category`, `sort_order`, `is_active`, `created_at`) VALUES (4, '如何申请发票？', '订单完成后，在\"我的发票\"页面申请开具发票，支持增值税普通发票和专用发票。发票将在申请后3-5个工作日内开具。', '发票相关', 4, 1, '2025-12-07 11:55:39');
INSERT INTO `quick_replies` (`id`, `question`, `answer`, `category`, `sort_order`, `is_active`, `created_at`) VALUES (5, '样品会退还吗？', '根据检测类型不同：破坏性检测的样品不退还；非破坏性检测的样品可申请退还，需承担运费。', '样品相关', 5, 1, '2025-12-07 11:55:39');
COMMIT;

-- ----------------------------
-- Table structure for recharge_records
-- ----------------------------
DROP TABLE IF EXISTS `recharge_records`;
CREATE TABLE `recharge_records` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '充值记录ID',
  `user_id` int NOT NULL COMMENT '用户ID',
  `recharge_no` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '充值单号',
  `amount` decimal(10,2) NOT NULL COMMENT '充值金额',
  `actual_amount` decimal(10,2) DEFAULT NULL COMMENT '实际到账金额（含赠送）',
  `bonus_amount` decimal(10,2) DEFAULT NULL COMMENT '赠送金额',
  `payment_method` enum('WECHAT','ALIPAY') COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '支付方式',
  `payment_no` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '支付单号',
  `transaction_id` varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '第三方交易号',
  `status` enum('PENDING','SUCCESS','FAILED','REFUNDED') COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '充值状态',
  `remark` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '备注',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `paid_at` datetime DEFAULT NULL COMMENT '支付时间',
  `completed_at` datetime DEFAULT NULL COMMENT '完成时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_recharge_records_recharge_no` (`recharge_no`),
  KEY `ix_recharge_records_user_id` (`user_id`),
  KEY `ix_recharge_records_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of recharge_records
-- ----------------------------
BEGIN;
INSERT INTO `recharge_records` (`id`, `user_id`, `recharge_no`, `amount`, `actual_amount`, `bonus_amount`, `payment_method`, `payment_no`, `transaction_id`, `status`, `remark`, `created_at`, `paid_at`, `completed_at`) VALUES (1, 11, 'RC17609348422118441', 100.00, 105.00, 5.00, 'WECHAT', NULL, NULL, 'PENDING', NULL, '2025-10-20 12:34:02', NULL, NULL);
INSERT INTO `recharge_records` (`id`, `user_id`, `recharge_no`, `amount`, `actual_amount`, `bonus_amount`, `payment_method`, `payment_no`, `transaction_id`, `status`, `remark`, `created_at`, `paid_at`, `completed_at`) VALUES (2, 11, 'RC17609439414237508', 100.00, 105.00, 5.00, 'WECHAT', NULL, NULL, 'PENDING', NULL, '2025-10-20 15:05:41', NULL, NULL);
INSERT INTO `recharge_records` (`id`, `user_id`, `recharge_no`, `amount`, `actual_amount`, `bonus_amount`, `payment_method`, `payment_no`, `transaction_id`, `status`, `remark`, `created_at`, `paid_at`, `completed_at`) VALUES (3, 11, 'RC17609440438022540', 100.00, 105.00, 5.00, 'WECHAT', NULL, NULL, 'PENDING', NULL, '2025-10-20 15:07:23', NULL, NULL);
INSERT INTO `recharge_records` (`id`, `user_id`, `recharge_no`, `amount`, `actual_amount`, `bonus_amount`, `payment_method`, `payment_no`, `transaction_id`, `status`, `remark`, `created_at`, `paid_at`, `completed_at`) VALUES (4, 11, 'RC17609443089927783', 100.00, 105.00, 5.00, 'WECHAT', NULL, NULL, 'PENDING', NULL, '2025-10-20 15:11:48', NULL, NULL);
INSERT INTO `recharge_records` (`id`, `user_id`, `recharge_no`, `amount`, `actual_amount`, `bonus_amount`, `payment_method`, `payment_no`, `transaction_id`, `status`, `remark`, `created_at`, `paid_at`, `completed_at`) VALUES (5, 11, 'RC17609452670098000', 100.00, 105.00, 5.00, 'WECHAT', NULL, NULL, 'PENDING', NULL, '2025-10-20 15:27:47', NULL, NULL);
INSERT INTO `recharge_records` (`id`, `user_id`, `recharge_no`, `amount`, `actual_amount`, `bonus_amount`, `payment_method`, `payment_no`, `transaction_id`, `status`, `remark`, `created_at`, `paid_at`, `completed_at`) VALUES (6, 11, 'RC17609452772342864', 100.00, 105.00, 5.00, 'WECHAT', NULL, NULL, 'PENDING', NULL, '2025-10-20 15:27:57', NULL, NULL);
INSERT INTO `recharge_records` (`id`, `user_id`, `recharge_no`, `amount`, `actual_amount`, `bonus_amount`, `payment_method`, `payment_no`, `transaction_id`, `status`, `remark`, `created_at`, `paid_at`, `completed_at`) VALUES (7, 11, 'RC17609460270802158', 100.00, 105.00, 5.00, 'WECHAT', NULL, NULL, 'PENDING', NULL, '2025-10-20 15:40:27', NULL, NULL);
INSERT INTO `recharge_records` (`id`, `user_id`, `recharge_no`, `amount`, `actual_amount`, `bonus_amount`, `payment_method`, `payment_no`, `transaction_id`, `status`, `remark`, `created_at`, `paid_at`, `completed_at`) VALUES (8, 11, 'RC17609460375242424', 100.00, 105.00, 5.00, 'WECHAT', NULL, NULL, 'PENDING', NULL, '2025-10-20 15:40:37', NULL, NULL);
INSERT INTO `recharge_records` (`id`, `user_id`, `recharge_no`, `amount`, `actual_amount`, `bonus_amount`, `payment_method`, `payment_no`, `transaction_id`, `status`, `remark`, `created_at`, `paid_at`, `completed_at`) VALUES (9, 11, 'RC17609462951549213', 100.00, 105.00, 5.00, 'WECHAT', NULL, NULL, 'PENDING', NULL, '2025-10-20 15:44:55', NULL, NULL);
INSERT INTO `recharge_records` (`id`, `user_id`, `recharge_no`, `amount`, `actual_amount`, `bonus_amount`, `payment_method`, `payment_no`, `transaction_id`, `status`, `remark`, `created_at`, `paid_at`, `completed_at`) VALUES (10, 11, 'RC17609463073536225', 100.00, 105.00, 5.00, 'WECHAT', NULL, NULL, 'PENDING', NULL, '2025-10-20 15:45:07', NULL, NULL);
INSERT INTO `recharge_records` (`id`, `user_id`, `recharge_no`, `amount`, `actual_amount`, `bonus_amount`, `payment_method`, `payment_no`, `transaction_id`, `status`, `remark`, `created_at`, `paid_at`, `completed_at`) VALUES (11, 11, 'RC17609469277553915', 100.00, 105.00, 5.00, 'WECHAT', NULL, NULL, 'PENDING', NULL, '2025-10-20 15:55:27', NULL, NULL);
INSERT INTO `recharge_records` (`id`, `user_id`, `recharge_no`, `amount`, `actual_amount`, `bonus_amount`, `payment_method`, `payment_no`, `transaction_id`, `status`, `remark`, `created_at`, `paid_at`, `completed_at`) VALUES (12, 11, 'RC17609469497091495', 100.00, 105.00, 5.00, 'WECHAT', NULL, NULL, 'PENDING', NULL, '2025-10-20 15:55:49', NULL, NULL);
INSERT INTO `recharge_records` (`id`, `user_id`, `recharge_no`, `amount`, `actual_amount`, `bonus_amount`, `payment_method`, `payment_no`, `transaction_id`, `status`, `remark`, `created_at`, `paid_at`, `completed_at`) VALUES (13, 11, 'RC17609470453728072', 100.00, 105.00, 5.00, 'WECHAT', NULL, NULL, 'PENDING', NULL, '2025-10-20 15:57:25', NULL, NULL);
INSERT INTO `recharge_records` (`id`, `user_id`, `recharge_no`, `amount`, `actual_amount`, `bonus_amount`, `payment_method`, `payment_no`, `transaction_id`, `status`, `remark`, `created_at`, `paid_at`, `completed_at`) VALUES (14, 11, 'RC17609470741264859', 1.00, 1.00, 0.00, 'WECHAT', NULL, '4200002837202510206466406783', 'SUCCESS', NULL, '2025-10-20 15:57:54', '2025-10-20 16:12:12', '2025-10-20 16:12:12');
INSERT INTO `recharge_records` (`id`, `user_id`, `recharge_no`, `amount`, `actual_amount`, `bonus_amount`, `payment_method`, `payment_no`, `transaction_id`, `status`, `remark`, `created_at`, `paid_at`, `completed_at`) VALUES (15, 11, 'RC17609473870979138', 1.00, 1.00, 0.00, 'WECHAT', NULL, '4200002938202510205150536186', 'SUCCESS', NULL, '2025-10-20 16:03:07', '2025-10-20 16:17:34', '2025-10-20 16:17:34');
INSERT INTO `recharge_records` (`id`, `user_id`, `recharge_no`, `amount`, `actual_amount`, `bonus_amount`, `payment_method`, `payment_no`, `transaction_id`, `status`, `remark`, `created_at`, `paid_at`, `completed_at`) VALUES (16, 11, 'RC17609484342061416', 1.00, 1.00, 0.00, 'WECHAT', NULL, '4200002924202510203101186614', 'SUCCESS', NULL, '2025-10-20 16:20:34', '2025-10-20 16:20:47', '2025-10-20 16:20:47');
INSERT INTO `recharge_records` (`id`, `user_id`, `recharge_no`, `amount`, `actual_amount`, `bonus_amount`, `payment_method`, `payment_no`, `transaction_id`, `status`, `remark`, `created_at`, `paid_at`, `completed_at`) VALUES (17, 11, 'RC17639104465414523', 100.00, 105.00, 5.00, 'WECHAT', NULL, NULL, 'PENDING', NULL, '2025-11-23 23:07:26', NULL, NULL);
INSERT INTO `recharge_records` (`id`, `user_id`, `recharge_no`, `amount`, `actual_amount`, `bonus_amount`, `payment_method`, `payment_no`, `transaction_id`, `status`, `remark`, `created_at`, `paid_at`, `completed_at`) VALUES (18, 11, 'RC17663210911839054', 100.00, 105.00, 5.00, 'WECHAT', NULL, NULL, 'PENDING', NULL, '2025-12-21 20:44:51', NULL, NULL);
INSERT INTO `recharge_records` (`id`, `user_id`, `recharge_no`, `amount`, `actual_amount`, `bonus_amount`, `payment_method`, `payment_no`, `transaction_id`, `status`, `remark`, `created_at`, `paid_at`, `completed_at`) VALUES (19, 11, 'RC17663211309059436', 1.00, 1.00, 0.00, 'WECHAT', NULL, NULL, 'PENDING', NULL, '2025-12-21 20:45:30', NULL, NULL);
INSERT INTO `recharge_records` (`id`, `user_id`, `recharge_no`, `amount`, `actual_amount`, `bonus_amount`, `payment_method`, `payment_no`, `transaction_id`, `status`, `remark`, `created_at`, `paid_at`, `completed_at`) VALUES (20, 11, 'RC17663214230096042', 1.00, 1.00, 0.00, 'WECHAT', NULL, NULL, 'SUCCESS', NULL, '2025-12-21 20:50:23', NULL, '2025-12-30 07:26:49');
INSERT INTO `recharge_records` (`id`, `user_id`, `recharge_no`, `amount`, `actual_amount`, `bonus_amount`, `payment_method`, `payment_no`, `transaction_id`, `status`, `remark`, `created_at`, `paid_at`, `completed_at`) VALUES (21, 11, 'RC17670881961027348', 100.00, 105.00, 5.00, 'WECHAT', NULL, NULL, 'PENDING', NULL, '2025-12-30 17:49:56', NULL, NULL);
INSERT INTO `recharge_records` (`id`, `user_id`, `recharge_no`, `amount`, `actual_amount`, `bonus_amount`, `payment_method`, `payment_no`, `transaction_id`, `status`, `remark`, `created_at`, `paid_at`, `completed_at`) VALUES (22, 13, 'RC17681819534776068', 2000.00, 2300.00, 300.00, 'WECHAT', NULL, NULL, 'SUCCESS', NULL, '2026-01-12 09:39:13', NULL, '2026-01-12 11:16:23');
COMMIT;

-- ----------------------------
-- Table structure for recovery_tasks
-- ----------------------------
DROP TABLE IF EXISTS `recovery_tasks`;
CREATE TABLE `recovery_tasks` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '任务ID',
  `user_id` int NOT NULL COMMENT '用户ID',
  `membership_id` int DEFAULT NULL COMMENT '会员ID',
  `task_no` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '任务编号',
  `service_type` enum('SUPER_RECOVERY','IMAGE_RECOVERY','WECHAT_RECOVERY','VIDEO_RECOVERY','FILE_RECOVERY','AUDIO_RECOVERY') COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '服务类型',
  `status` enum('PENDING','SCANNING','SCANNED','RECOVERING','COMPLETED','FAILED','CANCELLED') COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '任务状态',
  `device_type` enum('ANDROID','IOS','WINDOWS','MAC','OTHER') COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '设备类型',
  `device_model` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '设备型号',
  `device_os_version` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '系统版本',
  `device_storage_size` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '存储容量',
  `recovery_types` text COLLATE utf8mb4_unicode_ci COMMENT '恢复类型列表，JSON格式',
  `scan_deep` tinyint(1) DEFAULT NULL COMMENT '是否深度扫描',
  `progress_percent` int DEFAULT NULL COMMENT '进度百分比',
  `scanned_files_count` int DEFAULT NULL COMMENT '已扫描文件数',
  `recoverable_files_count` int DEFAULT NULL COMMENT '可恢复文件数',
  `recovered_files_count` int DEFAULT NULL COMMENT '已恢复文件数',
  `result_summary` text COLLATE utf8mb4_unicode_ci COMMENT '恢复结果摘要',
  `result_files_url` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '恢复文件下载链接',
  `engineer_id` int DEFAULT NULL COMMENT '负责工程师ID',
  `engineer_notes` text COLLATE utf8mb4_unicode_ci COMMENT '工程师备注',
  `started_at` datetime DEFAULT NULL COMMENT '开始时间',
  `completed_at` datetime DEFAULT NULL COMMENT '完成时间',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_recovery_tasks_task_no` (`task_no`),
  KEY `membership_id` (`membership_id`),
  KEY `ix_recovery_tasks_user_id` (`user_id`),
  KEY `ix_recovery_tasks_id` (`id`),
  CONSTRAINT `recovery_tasks_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `recovery_tasks_ibfk_2` FOREIGN KEY (`membership_id`) REFERENCES `user_memberships` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of recovery_tasks
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for repayments
-- ----------------------------
DROP TABLE IF EXISTS `repayments`;
CREATE TABLE `repayments` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL COMMENT '用户ID',
  `repayment_no` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '还款单号',
  `amount` decimal(10,2) NOT NULL COMMENT '还款金额',
  `payment_method` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '支付方式: wechat/alipay/balance/transfer',
  `debt_ids` text COLLATE utf8mb4_unicode_ci COMMENT '关联的欠款ID列表，JSON格式',
  `transaction_id` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '第三方支付交易号',
  `status` enum('PENDING','SUCCESS','FAILED') COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '还款状态',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `paid_at` datetime DEFAULT NULL COMMENT '支付完成时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_repayments_repayment_no` (`repayment_no`),
  KEY `ix_repayments_id` (`id`),
  KEY `ix_repayments_user_id` (`user_id`),
  CONSTRAINT `repayments_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of repayments
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for reports
-- ----------------------------
DROP TABLE IF EXISTS `reports`;
CREATE TABLE `reports` (
  `id` int NOT NULL AUTO_INCREMENT,
  `report_no` varchar(50) NOT NULL COMMENT '报告编号',
  `user_id` int NOT NULL COMMENT '用户ID',
  `order_id` int NOT NULL COMMENT '订单ID',
  `order_no` varchar(50) DEFAULT NULL COMMENT '订单号',
  `project_name` varchar(200) DEFAULT NULL COMMENT '项目名称',
  `sample_name` varchar(200) DEFAULT NULL COMMENT '样品名称',
  `status` varchar(20) DEFAULT 'pending' COMMENT '状态',
  `file_url` varchar(500) DEFAULT NULL COMMENT '报告文件URL',
  `file_size` int DEFAULT NULL COMMENT '文件大小',
  `download_count` int DEFAULT '0' COMMENT '下载次数',
  `completed_at` datetime DEFAULT NULL COMMENT '完成时间',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `report_no` (`report_no`),
  KEY `idx_user` (`user_id`),
  KEY `idx_order` (`order_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='检测报告';

-- ----------------------------
-- Records of reports
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for role_permissions
-- ----------------------------
DROP TABLE IF EXISTS `role_permissions`;
CREATE TABLE `role_permissions` (
  `role_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`role_id`,`permission_id`),
  KEY `permission_id` (`permission_id`),
  CONSTRAINT `role_permissions_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`),
  CONSTRAINT `role_permissions_ibfk_2` FOREIGN KEY (`permission_id`) REFERENCES `permissions` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of role_permissions
-- ----------------------------
BEGIN;
INSERT INTO `role_permissions` (`role_id`, `permission_id`) VALUES (1, 1);
INSERT INTO `role_permissions` (`role_id`, `permission_id`) VALUES (2, 1);
INSERT INTO `role_permissions` (`role_id`, `permission_id`) VALUES (3, 1);
INSERT INTO `role_permissions` (`role_id`, `permission_id`) VALUES (4, 1);
INSERT INTO `role_permissions` (`role_id`, `permission_id`) VALUES (5, 1);
INSERT INTO `role_permissions` (`role_id`, `permission_id`) VALUES (1, 2);
INSERT INTO `role_permissions` (`role_id`, `permission_id`) VALUES (2, 2);
INSERT INTO `role_permissions` (`role_id`, `permission_id`) VALUES (1, 3);
INSERT INTO `role_permissions` (`role_id`, `permission_id`) VALUES (1, 4);
INSERT INTO `role_permissions` (`role_id`, `permission_id`) VALUES (2, 4);
INSERT INTO `role_permissions` (`role_id`, `permission_id`) VALUES (1, 5);
INSERT INTO `role_permissions` (`role_id`, `permission_id`) VALUES (2, 5);
INSERT INTO `role_permissions` (`role_id`, `permission_id`) VALUES (3, 5);
INSERT INTO `role_permissions` (`role_id`, `permission_id`) VALUES (4, 5);
INSERT INTO `role_permissions` (`role_id`, `permission_id`) VALUES (5, 5);
INSERT INTO `role_permissions` (`role_id`, `permission_id`) VALUES (6, 5);
INSERT INTO `role_permissions` (`role_id`, `permission_id`) VALUES (7, 5);
INSERT INTO `role_permissions` (`role_id`, `permission_id`) VALUES (1, 6);
INSERT INTO `role_permissions` (`role_id`, `permission_id`) VALUES (2, 6);
INSERT INTO `role_permissions` (`role_id`, `permission_id`) VALUES (3, 6);
INSERT INTO `role_permissions` (`role_id`, `permission_id`) VALUES (1, 7);
INSERT INTO `role_permissions` (`role_id`, `permission_id`) VALUES (1, 8);
INSERT INTO `role_permissions` (`role_id`, `permission_id`) VALUES (2, 8);
INSERT INTO `role_permissions` (`role_id`, `permission_id`) VALUES (3, 8);
INSERT INTO `role_permissions` (`role_id`, `permission_id`) VALUES (1, 9);
INSERT INTO `role_permissions` (`role_id`, `permission_id`) VALUES (2, 9);
INSERT INTO `role_permissions` (`role_id`, `permission_id`) VALUES (4, 9);
INSERT INTO `role_permissions` (`role_id`, `permission_id`) VALUES (1, 10);
INSERT INTO `role_permissions` (`role_id`, `permission_id`) VALUES (2, 10);
INSERT INTO `role_permissions` (`role_id`, `permission_id`) VALUES (3, 10);
INSERT INTO `role_permissions` (`role_id`, `permission_id`) VALUES (5, 10);
INSERT INTO `role_permissions` (`role_id`, `permission_id`) VALUES (1, 11);
INSERT INTO `role_permissions` (`role_id`, `permission_id`) VALUES (2, 11);
INSERT INTO `role_permissions` (`role_id`, `permission_id`) VALUES (1, 12);
INSERT INTO `role_permissions` (`role_id`, `permission_id`) VALUES (2, 12);
INSERT INTO `role_permissions` (`role_id`, `permission_id`) VALUES (1, 13);
INSERT INTO `role_permissions` (`role_id`, `permission_id`) VALUES (1, 14);
INSERT INTO `role_permissions` (`role_id`, `permission_id`) VALUES (2, 14);
INSERT INTO `role_permissions` (`role_id`, `permission_id`) VALUES (3, 14);
INSERT INTO `role_permissions` (`role_id`, `permission_id`) VALUES (6, 14);
INSERT INTO `role_permissions` (`role_id`, `permission_id`) VALUES (1, 15);
INSERT INTO `role_permissions` (`role_id`, `permission_id`) VALUES (1, 16);
INSERT INTO `role_permissions` (`role_id`, `permission_id`) VALUES (2, 16);
INSERT INTO `role_permissions` (`role_id`, `permission_id`) VALUES (6, 16);
INSERT INTO `role_permissions` (`role_id`, `permission_id`) VALUES (1, 17);
INSERT INTO `role_permissions` (`role_id`, `permission_id`) VALUES (1, 18);
INSERT INTO `role_permissions` (`role_id`, `permission_id`) VALUES (2, 18);
INSERT INTO `role_permissions` (`role_id`, `permission_id`) VALUES (1, 19);
INSERT INTO `role_permissions` (`role_id`, `permission_id`) VALUES (2, 19);
INSERT INTO `role_permissions` (`role_id`, `permission_id`) VALUES (4, 19);
INSERT INTO `role_permissions` (`role_id`, `permission_id`) VALUES (1, 20);
INSERT INTO `role_permissions` (`role_id`, `permission_id`) VALUES (2, 20);
INSERT INTO `role_permissions` (`role_id`, `permission_id`) VALUES (4, 20);
INSERT INTO `role_permissions` (`role_id`, `permission_id`) VALUES (1, 21);
INSERT INTO `role_permissions` (`role_id`, `permission_id`) VALUES (2, 21);
INSERT INTO `role_permissions` (`role_id`, `permission_id`) VALUES (4, 21);
INSERT INTO `role_permissions` (`role_id`, `permission_id`) VALUES (1, 22);
INSERT INTO `role_permissions` (`role_id`, `permission_id`) VALUES (4, 22);
INSERT INTO `role_permissions` (`role_id`, `permission_id`) VALUES (1, 23);
INSERT INTO `role_permissions` (`role_id`, `permission_id`) VALUES (4, 23);
INSERT INTO `role_permissions` (`role_id`, `permission_id`) VALUES (1, 24);
INSERT INTO `role_permissions` (`role_id`, `permission_id`) VALUES (2, 24);
INSERT INTO `role_permissions` (`role_id`, `permission_id`) VALUES (1, 25);
INSERT INTO `role_permissions` (`role_id`, `permission_id`) VALUES (2, 25);
INSERT INTO `role_permissions` (`role_id`, `permission_id`) VALUES (1, 26);
INSERT INTO `role_permissions` (`role_id`, `permission_id`) VALUES (2, 26);
INSERT INTO `role_permissions` (`role_id`, `permission_id`) VALUES (1, 27);
INSERT INTO `role_permissions` (`role_id`, `permission_id`) VALUES (1, 28);
INSERT INTO `role_permissions` (`role_id`, `permission_id`) VALUES (2, 28);
INSERT INTO `role_permissions` (`role_id`, `permission_id`) VALUES (3, 28);
INSERT INTO `role_permissions` (`role_id`, `permission_id`) VALUES (1, 29);
INSERT INTO `role_permissions` (`role_id`, `permission_id`) VALUES (2, 29);
INSERT INTO `role_permissions` (`role_id`, `permission_id`) VALUES (3, 29);
INSERT INTO `role_permissions` (`role_id`, `permission_id`) VALUES (1, 30);
INSERT INTO `role_permissions` (`role_id`, `permission_id`) VALUES (2, 30);
INSERT INTO `role_permissions` (`role_id`, `permission_id`) VALUES (3, 30);
INSERT INTO `role_permissions` (`role_id`, `permission_id`) VALUES (1, 31);
INSERT INTO `role_permissions` (`role_id`, `permission_id`) VALUES (2, 31);
INSERT INTO `role_permissions` (`role_id`, `permission_id`) VALUES (4, 31);
INSERT INTO `role_permissions` (`role_id`, `permission_id`) VALUES (1, 32);
INSERT INTO `role_permissions` (`role_id`, `permission_id`) VALUES (2, 32);
INSERT INTO `role_permissions` (`role_id`, `permission_id`) VALUES (4, 32);
INSERT INTO `role_permissions` (`role_id`, `permission_id`) VALUES (1, 33);
INSERT INTO `role_permissions` (`role_id`, `permission_id`) VALUES (1, 34);
INSERT INTO `role_permissions` (`role_id`, `permission_id`) VALUES (1, 35);
COMMIT;

-- ----------------------------
-- Table structure for roles
-- ----------------------------
DROP TABLE IF EXISTS `roles`;
CREATE TABLE `roles` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '角色名称',
  `code` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '角色编码',
  `description` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '角色描述',
  `is_system` tinyint(1) DEFAULT NULL COMMENT '是否系统内置角色',
  `is_active` tinyint(1) DEFAULT NULL COMMENT '是否启用',
  `sort_order` int DEFAULT NULL COMMENT '排序',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `code` (`code`),
  KEY `ix_roles_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of roles
-- ----------------------------
BEGIN;
INSERT INTO `roles` (`id`, `name`, `code`, `description`, `is_system`, `is_active`, `sort_order`, `created_at`, `updated_at`) VALUES (1, '超级管理员', 'super_admin', '超级管理员角色', 1, 1, 0, '2026-01-12 10:36:37', '2026-01-12 10:36:37');
INSERT INTO `roles` (`id`, `name`, `code`, `description`, `is_system`, `is_active`, `sort_order`, `created_at`, `updated_at`) VALUES (2, '管理员', 'admin', '管理员角色', 1, 1, 0, '2026-01-12 10:36:37', '2026-01-12 10:36:37');
INSERT INTO `roles` (`id`, `name`, `code`, `description`, `is_system`, `is_active`, `sort_order`, `created_at`, `updated_at`) VALUES (3, '运营人员', 'operator', '运营人员角色', 1, 1, 0, '2026-01-12 10:36:37', '2026-01-12 10:36:37');
INSERT INTO `roles` (`id`, `name`, `code`, `description`, `is_system`, `is_active`, `sort_order`, `created_at`, `updated_at`) VALUES (4, '财务人员', 'finance', '财务人员角色', 1, 1, 0, '2026-01-12 10:36:37', '2026-01-12 10:36:37');
INSERT INTO `roles` (`id`, `name`, `code`, `description`, `is_system`, `is_active`, `sort_order`, `created_at`, `updated_at`) VALUES (5, '客服人员', 'cs', '客服人员角色', 1, 1, 0, '2026-01-12 10:36:37', '2026-01-12 10:36:37');
INSERT INTO `roles` (`id`, `name`, `code`, `description`, `is_system`, `is_active`, `sort_order`, `created_at`, `updated_at`) VALUES (6, '实验室管理员', 'lab_admin', '实验室管理员角色', 1, 1, 0, '2026-01-12 10:36:37', '2026-01-12 10:36:37');
INSERT INTO `roles` (`id`, `name`, `code`, `description`, `is_system`, `is_active`, `sort_order`, `created_at`, `updated_at`) VALUES (7, '实验室技术员', 'lab_technician', '实验室技术员角色', 1, 1, 0, '2026-01-12 10:36:37', '2026-01-12 10:36:37');
INSERT INTO `roles` (`id`, `name`, `code`, `description`, `is_system`, `is_active`, `sort_order`, `created_at`, `updated_at`) VALUES (8, '普通用户', 'user', '普通用户角色', 1, 1, 0, '2026-01-12 10:36:37', '2026-01-12 10:36:37');
COMMIT;

-- ----------------------------
-- Table structure for sample_groups
-- ----------------------------
DROP TABLE IF EXISTS `sample_groups`;
CREATE TABLE `sample_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `order_id` bigint DEFAULT NULL COMMENT '关联订单（提交后）',
  `user_id` int NOT NULL COMMENT '用户ID',
  `project_id` bigint NOT NULL COMMENT '项目ID',
  `group_name` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '分组名称/测试目的',
  `group_index` int DEFAULT NULL COMMENT '分组序号',
  `option_selections` json DEFAULT NULL COMMENT '该组选择的选项',
  `options_fee` decimal(10,2) DEFAULT NULL COMMENT '选项费用',
  `is_collapsed` tinyint(1) DEFAULT NULL COMMENT '是否收起',
  `status` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '状态: draft/submitted',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `ix_sample_groups_user_id` (`user_id`),
  KEY `ix_sample_groups_order_id` (`order_id`),
  KEY `ix_sample_groups_project_id` (`project_id`),
  KEY `ix_sample_groups_id` (`id`),
  CONSTRAINT `sample_groups_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`),
  CONSTRAINT `sample_groups_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `sample_groups_ibfk_3` FOREIGN KEY (`project_id`) REFERENCES `projects` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of sample_groups
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for sample_items
-- ----------------------------
DROP TABLE IF EXISTS `sample_items`;
CREATE TABLE `sample_items` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` bigint NOT NULL COMMENT '关联样品组',
  `sample_no` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '样品编号（英文+数字+下划线）',
  `sample_name` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '样品名称',
  `sample_composition` text COLLATE utf8mb4_unicode_ci COMMENT '样品成分',
  `sample_state` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '样品状态',
  `danger_type` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '危险性',
  `storage_requirement` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '存放要求',
  `quantity` int DEFAULT NULL COMMENT '数量',
  `remark` text COLLATE utf8mb4_unicode_ci COMMENT '备注',
  `photos` json DEFAULT NULL COMMENT '样品照片',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  KEY `ix_sample_items_id` (`id`),
  KEY `ix_sample_items_group_id` (`group_id`),
  CONSTRAINT `sample_items_ibfk_1` FOREIGN KEY (`group_id`) REFERENCES `sample_groups` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of sample_items
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for sample_logistics
-- ----------------------------
DROP TABLE IF EXISTS `sample_logistics`;
CREATE TABLE `sample_logistics` (
  `id` int NOT NULL AUTO_INCREMENT,
  `order_id` int NOT NULL COMMENT '订单ID',
  `logistics_type` varchar(20) DEFAULT 'send' COMMENT '类型',
  `company` varchar(100) DEFAULT NULL COMMENT '快递公司',
  `tracking_no` varchar(100) DEFAULT NULL COMMENT '快递单号',
  `sender_name` varchar(100) DEFAULT NULL COMMENT '寄件人',
  `sender_phone` varchar(20) DEFAULT NULL COMMENT '寄件人电话',
  `sender_address` varchar(500) DEFAULT NULL COMMENT '寄件地址',
  `receiver_name` varchar(100) DEFAULT NULL COMMENT '收件人',
  `receiver_phone` varchar(20) DEFAULT NULL COMMENT '收件人电话',
  `receiver_address` varchar(500) DEFAULT NULL COMMENT '收件地址',
  `status` varchar(20) DEFAULT 'pending' COMMENT '状态',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_order` (`order_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='样品物流信息';

-- ----------------------------
-- Records of sample_logistics
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for sample_trackings
-- ----------------------------
DROP TABLE IF EXISTS `sample_trackings`;
CREATE TABLE `sample_trackings` (
  `id` int NOT NULL AUTO_INCREMENT,
  `order_id` int NOT NULL COMMENT '订单ID',
  `order_no` varchar(50) DEFAULT NULL COMMENT '订单号',
  `sample_name` varchar(200) DEFAULT NULL COMMENT '样品名称',
  `status` varchar(50) NOT NULL COMMENT '状态',
  `status_text` varchar(100) DEFAULT NULL COMMENT '状态描述',
  `location` varchar(200) DEFAULT NULL COMMENT '当前位置',
  `operator` varchar(100) DEFAULT NULL COMMENT '操作人',
  `remark` text COMMENT '备注',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_order` (`order_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='样品追踪记录';

-- ----------------------------
-- Records of sample_trackings
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for scan_results
-- ----------------------------
DROP TABLE IF EXISTS `scan_results`;
CREATE TABLE `scan_results` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '结果ID',
  `task_id` int NOT NULL COMMENT '任务ID',
  `file_type` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '文件类型',
  `file_name` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '文件名',
  `file_path` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '文件路径',
  `file_size` int DEFAULT NULL COMMENT '文件大小（字节）',
  `is_recoverable` tinyint(1) DEFAULT NULL COMMENT '是否可恢复',
  `recovery_quality` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '恢复质量：high/medium/low',
  `is_recovered` tinyint(1) DEFAULT NULL COMMENT '是否已恢复',
  `thumbnail_url` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '缩略图URL',
  `preview_url` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '预览URL',
  `original_created_at` datetime DEFAULT NULL COMMENT '原始创建时间',
  `original_modified_at` datetime DEFAULT NULL COMMENT '原始修改时间',
  `deleted_at` datetime DEFAULT NULL COMMENT '删除时间',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '扫描时间',
  PRIMARY KEY (`id`),
  KEY `ix_scan_results_task_id` (`task_id`),
  KEY `ix_scan_results_id` (`id`),
  CONSTRAINT `scan_results_ibfk_1` FOREIGN KEY (`task_id`) REFERENCES `recovery_tasks` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of scan_results
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for service_packages
-- ----------------------------
DROP TABLE IF EXISTS `service_packages`;
CREATE TABLE `service_packages` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '套餐ID',
  `service_type` enum('SUPER_RECOVERY','IMAGE_RECOVERY','WECHAT_RECOVERY','VIDEO_RECOVERY','FILE_RECOVERY','AUDIO_RECOVERY') COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '服务类型',
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '套餐名称',
  `description` text COLLATE utf8mb4_unicode_ci COMMENT '套餐描述',
  `price` decimal(10,2) NOT NULL COMMENT '现价',
  `original_price` decimal(10,2) DEFAULT NULL COMMENT '原价',
  `features` text COLLATE utf8mb4_unicode_ci COMMENT '功能特性列表，JSON格式',
  `max_recoveries` int DEFAULT NULL COMMENT '最大恢复次数，0表示无限制',
  `is_active` tinyint(1) DEFAULT NULL COMMENT '是否启用',
  `sort_order` int DEFAULT NULL COMMENT '排序',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `service_type` (`service_type`),
  KEY `ix_service_packages_id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of service_packages
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for sms_codes
-- ----------------------------
DROP TABLE IF EXISTS `sms_codes`;
CREATE TABLE `sms_codes` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `phone` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '手机号',
  `code` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '验证码',
  `is_used` tinyint(1) DEFAULT NULL COMMENT '是否已使用',
  `scene` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '使用场景(register/login/reset_password)',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `expires_at` datetime NOT NULL COMMENT '过期时间',
  PRIMARY KEY (`id`),
  KEY `ix_sms_codes_phone` (`phone`),
  KEY `ix_sms_codes_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of sms_codes
-- ----------------------------
BEGIN;
INSERT INTO `sms_codes` (`id`, `phone`, `code`, `is_used`, `scene`, `created_at`, `expires_at`) VALUES (1, '13800138000', '517378', 0, 'register', '2025-10-18 13:51:21', '2025-10-18 05:56:22');
INSERT INTO `sms_codes` (`id`, `phone`, `code`, `is_used`, `scene`, `created_at`, `expires_at`) VALUES (7, '18939409857', '141018', 0, 'login', '2025-12-21 20:44:18', '2025-12-21 12:49:19');
INSERT INTO `sms_codes` (`id`, `phone`, `code`, `is_used`, `scene`, `created_at`, `expires_at`) VALUES (14, '17819781949', '893950', 1, 'login', '2025-12-21 20:59:04', '2025-12-21 13:04:04');
INSERT INTO `sms_codes` (`id`, `phone`, `code`, `is_used`, `scene`, `created_at`, `expires_at`) VALUES (15, '18663764585', '765405', 1, 'login', '2025-12-21 22:34:49', '2025-12-21 14:39:50');
INSERT INTO `sms_codes` (`id`, `phone`, `code`, `is_used`, `scene`, `created_at`, `expires_at`) VALUES (28, '15939499857', '256062', 1, 'login', '2026-01-11 18:31:45', '2026-01-11 18:36:46');
INSERT INTO `sms_codes` (`id`, `phone`, `code`, `is_used`, `scene`, `created_at`, `expires_at`) VALUES (30, '15939409857', '249102', 1, 'login', '2026-01-12 19:02:58', '2026-01-12 19:07:58');
INSERT INTO `sms_codes` (`id`, `phone`, `code`, `is_used`, `scene`, `created_at`, `expires_at`) VALUES (32, '18888888888', '342291', 1, 'login', '2026-01-16 18:23:13', '2026-01-16 18:28:14');
COMMIT;

-- ----------------------------
-- Table structure for task_progress_logs
-- ----------------------------
DROP TABLE IF EXISTS `task_progress_logs`;
CREATE TABLE `task_progress_logs` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '日志ID',
  `task_id` int NOT NULL COMMENT '任务ID',
  `progress_percent` int DEFAULT NULL COMMENT '进度百分比',
  `current_step` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '当前步骤',
  `step_description` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '步骤描述',
  `files_scanned` int DEFAULT NULL COMMENT '已扫描文件数',
  `files_found` int DEFAULT NULL COMMENT '发现文件数',
  `files_recovered` int DEFAULT NULL COMMENT '已恢复文件数',
  `log_level` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '日志级别',
  `message` text COLLATE utf8mb4_unicode_ci COMMENT '日志消息',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  KEY `ix_task_progress_logs_id` (`id`),
  KEY `ix_task_progress_logs_task_id` (`task_id`),
  CONSTRAINT `task_progress_logs_ibfk_1` FOREIGN KEY (`task_id`) REFERENCES `recovery_tasks` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of task_progress_logs
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for user_addresses
-- ----------------------------
DROP TABLE IF EXISTS `user_addresses`;
CREATE TABLE `user_addresses` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL COMMENT '用户ID',
  `receiver_name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '收件人',
  `phone` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '手机号',
  `province` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '省',
  `city` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '市',
  `district` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '区',
  `detail_address` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '详细地址',
  `is_default` tinyint(1) DEFAULT NULL COMMENT '是否默认',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `ix_user_addresses_id` (`id`),
  KEY `ix_user_addresses_user_id` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of user_addresses
-- ----------------------------
BEGIN;
INSERT INTO `user_addresses` (`id`, `user_id`, `receiver_name`, `phone`, `province`, `city`, `district`, `detail_address`, `is_default`, `created_at`, `updated_at`) VALUES (1, 11, '11', '13000000001', '北京市', '北京市', '海淀区', '1111', 0, '2025-10-19 13:52:25', NULL);
INSERT INTO `user_addresses` (`id`, `user_id`, `receiver_name`, `phone`, `province`, `city`, `district`, `detail_address`, `is_default`, `created_at`, `updated_at`) VALUES (2, 13, '王泽华', '15939409857', '北京市', '北京市', '西城区', '北京大学', 0, '2025-10-20 00:03:49', '2026-01-12 09:43:29');
INSERT INTO `user_addresses` (`id`, `user_id`, `receiver_name`, `phone`, `province`, `city`, `district`, `detail_address`, `is_default`, `created_at`, `updated_at`) VALUES (3, 14, '刘', '17302076676', '广东省', '广州市', '天河区', '海珠广场', 1, '2025-10-20 11:16:53', NULL);
INSERT INTO `user_addresses` (`id`, `user_id`, `receiver_name`, `phone`, `province`, `city`, `district`, `detail_address`, `is_default`, `created_at`, `updated_at`) VALUES (4, 19, '111', '18888888888', 'Not applicable', 'jinan', '88', 'jinan', 0, '2025-12-21 23:09:51', NULL);
INSERT INTO `user_addresses` (`id`, `user_id`, `receiver_name`, `phone`, `province`, `city`, `district`, `detail_address`, `is_default`, `created_at`, `updated_at`) VALUES (5, 13, '王', '15888888888', '广东省', '广州市', '天河区', '中山大学化工学院', 1, '2026-01-12 09:43:29', NULL);
COMMIT;

-- ----------------------------
-- Table structure for user_certification
-- ----------------------------
DROP TABLE IF EXISTS `user_certification`;
CREATE TABLE `user_certification` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL COMMENT '用户ID',
  `enrollment_year` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '入学年份',
  `graduation_year` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '毕业年份',
  `province` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '省份',
  `city` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '城市',
  `university` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '高校',
  `department` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '院系',
  `supervisor_name` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '导师姓名',
  `supervisor_title` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '导师职称',
  `student_card_photo` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '学生证照片',
  `id_card_front` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '身份证正面',
  `id_card_back` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '身份证反面',
  `status` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '审核状态: pending/approved/rejected',
  `reject_reason` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '拒绝原因',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `certified_at` datetime DEFAULT NULL COMMENT '认证通过时间',
  PRIMARY KEY (`id`),
  KEY `ix_user_certification_user_id` (`user_id`),
  KEY `ix_user_certification_id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of user_certification
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for user_commission_settings
-- ----------------------------
DROP TABLE IF EXISTS `user_commission_settings`;
CREATE TABLE `user_commission_settings` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL COMMENT '用户ID',
  `commission_rate` decimal(5,2) DEFAULT NULL COMMENT '佣金比例（%）',
  `max_rate` decimal(5,2) DEFAULT NULL COMMENT '最大比例（%）',
  `effective_from` date DEFAULT NULL COMMENT '生效日期',
  `effective_to` date DEFAULT NULL COMMENT '失效日期',
  `created_by` int DEFAULT NULL COMMENT '设置人',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_user_commission_settings_user_id` (`user_id`),
  KEY `created_by` (`created_by`),
  KEY `ix_user_commission_settings_id` (`id`),
  CONSTRAINT `user_commission_settings_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `user_commission_settings_ibfk_2` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of user_commission_settings
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for user_coupons
-- ----------------------------
DROP TABLE IF EXISTS `user_coupons`;
CREATE TABLE `user_coupons` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '用户优惠券ID',
  `user_id` int NOT NULL COMMENT '用户ID',
  `coupon_id` int NOT NULL COMMENT '优惠券ID',
  `coupon_name` varchar(100) DEFAULT NULL COMMENT '优惠券名称',
  `coupon_type` varchar(20) DEFAULT NULL COMMENT '优惠券类型',
  `discount_value` decimal(10,2) DEFAULT NULL COMMENT '优惠值',
  `status` enum('UNUSED','USED','EXPIRED') DEFAULT 'UNUSED',
  `order_id` int DEFAULT NULL COMMENT '使用的订单ID',
  `used_at` datetime DEFAULT NULL COMMENT '使用时间',
  `received_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '领取时间',
  `expire_at` datetime NOT NULL COMMENT '过期时间',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_coupon_id` (`coupon_id`),
  KEY `idx_status` (`status`),
  KEY `idx_expire` (`expire_at`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='用户优惠券表';

-- ----------------------------
-- Records of user_coupons
-- ----------------------------
BEGIN;
INSERT INTO `user_coupons` (`id`, `user_id`, `coupon_id`, `coupon_name`, `coupon_type`, `discount_value`, `status`, `order_id`, `used_at`, `received_at`, `expire_at`, `created_at`, `updated_at`) VALUES (1, 12, 1, '新人专享券', 'cash', 10.00, 'UNUSED', NULL, NULL, '2025-11-23 22:36:39', '2025-12-23 22:36:39', '2025-11-23 22:36:39', '2025-11-23 22:36:39');
COMMIT;

-- ----------------------------
-- Table structure for user_groups
-- ----------------------------
DROP TABLE IF EXISTS `user_groups`;
CREATE TABLE `user_groups` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '团队ID',
  `name` varchar(100) NOT NULL COMMENT '团队名称',
  `avatar` varchar(255) DEFAULT NULL COMMENT '团队头像',
  `description` text COMMENT '团队描述',
  `owner_id` int NOT NULL COMMENT '负责人用户ID',
  `owner_name` varchar(50) DEFAULT NULL COMMENT '负责人姓名',
  `owner_phone` varchar(20) DEFAULT NULL COMMENT '负责人手机号',
  `university` varchar(100) DEFAULT NULL COMMENT '所属高校',
  `department` varchar(100) DEFAULT NULL COMMENT '所属院系',
  `invite_code` varchar(20) DEFAULT NULL COMMENT '邀请码',
  `member_count` int DEFAULT '1' COMMENT '成员数量',
  `total_orders` int DEFAULT '0' COMMENT '累计订单数',
  `total_spent` decimal(10,2) DEFAULT '0.00' COMMENT '累计消费金额',
  `status` enum('ACTIVE','INACTIVE','DISBANDED') DEFAULT 'ACTIVE',
  `is_certified` tinyint(1) DEFAULT '0' COMMENT '是否认证',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `invite_code` (`invite_code`),
  KEY `idx_owner_id` (`owner_id`),
  KEY `idx_invite_code` (`invite_code`),
  KEY `idx_owner_phone` (`owner_phone`),
  KEY `idx_status` (`status`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='用户团队表';

-- ----------------------------
-- Records of user_groups
-- ----------------------------
BEGIN;
INSERT INTO `user_groups` (`id`, `name`, `avatar`, `description`, `owner_id`, `owner_name`, `owner_phone`, `university`, `department`, `invite_code`, `member_count`, `total_orders`, `total_spent`, `status`, `is_certified`, `created_at`, `updated_at`) VALUES (1, '测试团队', 'https://example.com/avatar.jpg', '高校 - 北京市', 12, '张三', 'admin', '北京市', '海淀区', 'MHX4KQOB', 1, 0, 0.00, 'ACTIVE', 1, '2025-11-23 16:16:56', '2025-12-30 15:35:56');
COMMIT;

-- ----------------------------
-- Table structure for user_memberships
-- ----------------------------
DROP TABLE IF EXISTS `user_memberships`;
CREATE TABLE `user_memberships` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '会员ID',
  `user_id` int NOT NULL COMMENT '用户ID',
  `service_type` enum('SUPER_RECOVERY','IMAGE_RECOVERY','WECHAT_RECOVERY','VIDEO_RECOVERY','FILE_RECOVERY','AUDIO_RECOVERY') COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '服务类型',
  `is_active` tinyint(1) DEFAULT NULL COMMENT '是否激活',
  `expires_at` datetime DEFAULT NULL COMMENT '过期时间',
  `max_recoveries` int DEFAULT NULL COMMENT '最大恢复次数，0表示无限制',
  `used_recoveries` int DEFAULT NULL COMMENT '已使用恢复次数',
  `purchase_price` decimal(10,2) DEFAULT NULL COMMENT '购买价格',
  `purchase_order_no` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '购买订单号',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `ix_user_memberships_user_id` (`user_id`),
  KEY `ix_user_memberships_id` (`id`),
  CONSTRAINT `user_memberships_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of user_memberships
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for user_notifications
-- ----------------------------
DROP TABLE IF EXISTS `user_notifications`;
CREATE TABLE `user_notifications` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL COMMENT '用户ID',
  `title` varchar(200) NOT NULL COMMENT '标题',
  `content` text COMMENT '内容',
  `category` varchar(50) DEFAULT 'system' COMMENT '分类',
  `is_read` tinyint(1) DEFAULT '0' COMMENT '是否已读',
  `related_type` varchar(50) DEFAULT NULL COMMENT '关联类型',
  `related_id` int DEFAULT NULL COMMENT '关联ID',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_user_read` (`user_id`,`is_read`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='用户通知';

-- ----------------------------
-- Records of user_notifications
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for user_roles
-- ----------------------------
DROP TABLE IF EXISTS `user_roles`;
CREATE TABLE `user_roles` (
  `user_id` int NOT NULL,
  `role_id` int NOT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_id`,`role_id`),
  KEY `role_id` (`role_id`),
  CONSTRAINT `user_roles_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `user_roles_ibfk_2` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of user_roles
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '用户ID',
  `phone` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `password` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `nickname` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '昵称',
  `avatar` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '头像URL',
  `email` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '邮箱',
  `wechat_openid` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '微信OpenID',
  `wechat_unionid` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '微信UnionID',
  `is_certified` tinyint(1) DEFAULT NULL COMMENT '是否实名认证',
  `real_name` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '真实姓名',
  `id_card` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '身份证号',
  `membership_level` enum('NORMAL','SILVER','GOLD','PLATINUM') COLLATE utf8mb4_unicode_ci DEFAULT 'NORMAL',
  `credit_limit` decimal(10,2) DEFAULT NULL COMMENT '信用额度',
  `used_credit` decimal(10,2) DEFAULT NULL COMMENT '已用信用额度',
  `prepaid_balance` decimal(10,2) DEFAULT NULL COMMENT '预付余额',
  `points_balance` int DEFAULT NULL COMMENT '积分余额',
  `total_points_earned` int DEFAULT NULL COMMENT '累计获得积分',
  `total_points_used` int DEFAULT NULL COMMENT '累计使用积分',
  `total_spent` decimal(10,2) DEFAULT NULL COMMENT '累计消费金额',
  `total_orders` int DEFAULT NULL COMMENT '累计订单数',
  `status` enum('ACTIVE','INACTIVE','BANNED') COLLATE utf8mb4_unicode_ci DEFAULT 'ACTIVE',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  `last_login_at` datetime DEFAULT NULL COMMENT '最后登录时间',
  `is_admin` tinyint(1) DEFAULT '0' COMMENT '是否管理员',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_users_phone` (`phone`),
  UNIQUE KEY `idx_wechat_openid` (`wechat_openid`),
  KEY `ix_users_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of users
-- ----------------------------
BEGIN;
INSERT INTO `users` (`id`, `phone`, `password`, `nickname`, `avatar`, `email`, `wechat_openid`, `wechat_unionid`, `is_certified`, `real_name`, `id_card`, `membership_level`, `credit_limit`, `used_credit`, `prepaid_balance`, `points_balance`, `total_points_earned`, `total_points_used`, `total_spent`, `total_orders`, `status`, `created_at`, `updated_at`, `last_login_at`, `is_admin`) VALUES (1, '18663764585', '$2b$12$lk5hUspm9pidavlm17J0I.UH8z4McvfAlR1tR/piFLBqzDzDOaJWW', '用户4585', NULL, NULL, NULL, NULL, 0, NULL, NULL, 'NORMAL', 3000.00, 0.00, 0.00, 0, 0, 0, 0.00, 0, 'ACTIVE', '2025-10-18 13:54:57', '2025-12-21 22:35:26', '2025-12-21 14:35:26', 0);
INSERT INTO `users` (`id`, `phone`, `password`, `nickname`, `avatar`, `email`, `wechat_openid`, `wechat_unionid`, `is_certified`, `real_name`, `id_card`, `membership_level`, `credit_limit`, `used_credit`, `prepaid_balance`, `points_balance`, `total_points_earned`, `total_points_used`, `total_spent`, `total_orders`, `status`, `created_at`, `updated_at`, `last_login_at`, `is_admin`) VALUES (11, NULL, NULL, '微信用户3rhTPY', NULL, NULL, 'orB2m7V3L6LNKlpYO2mhaT3rhTPY', NULL, 0, NULL, NULL, 'NORMAL', 3000.00, 0.00, 4.00, 0, 0, 0, 0.00, 0, 'ACTIVE', '2025-10-18 17:20:51', '2026-01-11 14:56:24', '2026-01-11 06:56:24', 0);
INSERT INTO `users` (`id`, `phone`, `password`, `nickname`, `avatar`, `email`, `wechat_openid`, `wechat_unionid`, `is_certified`, `real_name`, `id_card`, `membership_level`, `credit_limit`, `used_credit`, `prepaid_balance`, `points_balance`, `total_points_earned`, `total_points_used`, `total_spent`, `total_orders`, `status`, `created_at`, `updated_at`, `last_login_at`, `is_admin`) VALUES (12, 'admin', '$2b$12$/3JHrrhnE9T/jcZUaR9IruW6qvXOo65IijCEL3IAa6ER0s8dfbq6W', '管理员', '/static/uploads/20251018/d099536d2f5b4a4b88c2fbf3cd9b6315.png', NULL, NULL, NULL, 1, NULL, NULL, 'NORMAL', 999999.00, 0.00, 0.00, 0, 0, 0, 0.00, 0, 'ACTIVE', '2025-10-18 17:47:06', '2026-01-16 13:22:56', '2026-01-16 05:22:57', 0);
INSERT INTO `users` (`id`, `phone`, `password`, `nickname`, `avatar`, `email`, `wechat_openid`, `wechat_unionid`, `is_certified`, `real_name`, `id_card`, `membership_level`, `credit_limit`, `used_credit`, `prepaid_balance`, `points_balance`, `total_points_earned`, `total_points_used`, `total_spent`, `total_orders`, `status`, `created_at`, `updated_at`, `last_login_at`, `is_admin`) VALUES (13, NULL, NULL, '微信用户0rmpgs', NULL, NULL, 'orB2m7SVODCoFs6ECSfviQ0rmpgs', NULL, 0, NULL, NULL, 'NORMAL', 3000.00, 0.00, 2300.00, 0, 0, 0, 0.00, 0, 'ACTIVE', '2025-10-19 23:58:31', '2026-01-12 19:16:23', '2026-01-12 01:38:22', 0);
INSERT INTO `users` (`id`, `phone`, `password`, `nickname`, `avatar`, `email`, `wechat_openid`, `wechat_unionid`, `is_certified`, `real_name`, `id_card`, `membership_level`, `credit_limit`, `used_credit`, `prepaid_balance`, `points_balance`, `total_points_earned`, `total_points_used`, `total_spent`, `total_orders`, `status`, `created_at`, `updated_at`, `last_login_at`, `is_admin`) VALUES (14, NULL, NULL, '微信用户F4ENsU', NULL, NULL, 'orB2m7TPBZc-HobpObc4IjF4ENsU', NULL, 0, NULL, NULL, 'NORMAL', 3000.00, 0.00, 0.00, 0, 0, 0, 0.00, 0, 'ACTIVE', '2025-10-20 11:15:59', '2025-10-20 11:15:59', '2025-10-20 03:15:59', 0);
INSERT INTO `users` (`id`, `phone`, `password`, `nickname`, `avatar`, `email`, `wechat_openid`, `wechat_unionid`, `is_certified`, `real_name`, `id_card`, `membership_level`, `credit_limit`, `used_credit`, `prepaid_balance`, `points_balance`, `total_points_earned`, `total_points_used`, `total_spent`, `total_orders`, `status`, `created_at`, `updated_at`, `last_login_at`, `is_admin`) VALUES (15, '13800138000', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzpLhJ632u', '测试用户', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'NORMAL', NULL, NULL, 1000.00, 100, NULL, NULL, NULL, NULL, 'ACTIVE', '2025-11-23 16:07:10', '2026-01-12 17:04:40', NULL, 0);
INSERT INTO `users` (`id`, `phone`, `password`, `nickname`, `avatar`, `email`, `wechat_openid`, `wechat_unionid`, `is_certified`, `real_name`, `id_card`, `membership_level`, `credit_limit`, `used_credit`, `prepaid_balance`, `points_balance`, `total_points_earned`, `total_points_used`, `total_spent`, `total_orders`, `status`, `created_at`, `updated_at`, `last_login_at`, `is_admin`) VALUES (16, NULL, NULL, '微信用户GMohko', NULL, NULL, 'orB2m7f85fTvYFRVt9RtmXGMohko', NULL, 0, NULL, NULL, 'NORMAL', 3000.00, 0.00, 0.00, 0, 0, 0, 0.00, 0, 'ACTIVE', '2025-11-23 23:13:19', '2025-11-23 23:13:23', '2025-11-23 15:13:24', 0);
INSERT INTO `users` (`id`, `phone`, `password`, `nickname`, `avatar`, `email`, `wechat_openid`, `wechat_unionid`, `is_certified`, `real_name`, `id_card`, `membership_level`, `credit_limit`, `used_credit`, `prepaid_balance`, `points_balance`, `total_points_earned`, `total_points_used`, `total_spent`, `total_orders`, `status`, `created_at`, `updated_at`, `last_login_at`, `is_admin`) VALUES (17, '15939409857', '$2b$12$KG6nwJlHIePH.Yr7meIngOuUNyE5kY8O3zHOsfdp2dIKpJs1Amr6.', '用户9857', '111', NULL, NULL, NULL, 0, NULL, NULL, 'NORMAL', 3000.00, 0.00, 0.00, 0, 0, 0, 0.00, 0, 'ACTIVE', '2025-12-21 20:46:52', '2026-01-12 19:03:05', '2026-01-12 11:03:06', 0);
INSERT INTO `users` (`id`, `phone`, `password`, `nickname`, `avatar`, `email`, `wechat_openid`, `wechat_unionid`, `is_certified`, `real_name`, `id_card`, `membership_level`, `credit_limit`, `used_credit`, `prepaid_balance`, `points_balance`, `total_points_earned`, `total_points_used`, `total_spent`, `total_orders`, `status`, `created_at`, `updated_at`, `last_login_at`, `is_admin`) VALUES (18, '17819781949', '$2b$12$PEjbvefj2CjIQSBx7G2USeJz7..gbGr2n4zQojWxPsT8tidN.9GUi', '用户1949', NULL, NULL, NULL, NULL, 0, NULL, NULL, 'NORMAL', 3000.00, 0.00, 0.00, 0, 0, 0, 0.00, 0, 'ACTIVE', '2025-12-21 20:48:18', '2025-12-21 20:59:13', '2025-12-21 12:59:14', 0);
INSERT INTO `users` (`id`, `phone`, `password`, `nickname`, `avatar`, `email`, `wechat_openid`, `wechat_unionid`, `is_certified`, `real_name`, `id_card`, `membership_level`, `credit_limit`, `used_credit`, `prepaid_balance`, `points_balance`, `total_points_earned`, `total_points_used`, `total_spent`, `total_orders`, `status`, `created_at`, `updated_at`, `last_login_at`, `is_admin`) VALUES (19, '18888888888', '$2b$12$t1YLa0kDnHk5f6rY2yjpG./17XI0STE/80v05EwepBQ3C/.4MvlCK', '用户8888', NULL, NULL, NULL, NULL, 0, NULL, NULL, 'NORMAL', 3000.00, 0.00, 0.00, 0, 0, 0, 0.00, 0, 'ACTIVE', '2025-12-21 22:39:27', '2026-01-16 18:23:21', '2026-01-16 10:23:22', 0);
INSERT INTO `users` (`id`, `phone`, `password`, `nickname`, `avatar`, `email`, `wechat_openid`, `wechat_unionid`, `is_certified`, `real_name`, `id_card`, `membership_level`, `credit_limit`, `used_credit`, `prepaid_balance`, `points_balance`, `total_points_earned`, `total_points_used`, `total_spent`, `total_orders`, `status`, `created_at`, `updated_at`, `last_login_at`, `is_admin`) VALUES (20, '15939499857', '$2b$12$4rSK7D4.X5vCf6jztjTDCO0uqhzBOP/fBlKU67nztahpM/m2cLoj2', '用户9857', NULL, NULL, NULL, NULL, 0, NULL, NULL, 'NORMAL', 3000.00, 0.00, 0.00, 0, 0, 0, 0.00, 0, 'ACTIVE', '2026-01-11 18:31:55', '2026-01-11 18:31:55', '2026-01-11 10:31:55', 0);
INSERT INTO `users` (`id`, `phone`, `password`, `nickname`, `avatar`, `email`, `wechat_openid`, `wechat_unionid`, `is_certified`, `real_name`, `id_card`, `membership_level`, `credit_limit`, `used_credit`, `prepaid_balance`, `points_balance`, `total_points_earned`, `total_points_used`, `total_spent`, `total_orders`, `status`, `created_at`, `updated_at`, `last_login_at`, `is_admin`) VALUES (22, NULL, NULL, '微信用户31iD0j', NULL, NULL, 'test_openid_31iD0j', NULL, 0, NULL, NULL, 'NORMAL', 3000.00, 0.00, 0.00, 0, 0, 0, 0.00, 0, 'ACTIVE', '2026-01-12 10:31:54', '2026-01-12 10:31:54', '2026-01-12 02:31:54', 0);
INSERT INTO `users` (`id`, `phone`, `password`, `nickname`, `avatar`, `email`, `wechat_openid`, `wechat_unionid`, `is_certified`, `real_name`, `id_card`, `membership_level`, `credit_limit`, `used_credit`, `prepaid_balance`, `points_balance`, `total_points_earned`, `total_points_used`, `total_spent`, `total_orders`, `status`, `created_at`, `updated_at`, `last_login_at`, `is_admin`) VALUES (23, NULL, NULL, '微信用户2A2Blv', NULL, NULL, 'test_openid_2A2Blv', NULL, 0, NULL, NULL, 'NORMAL', 3000.00, 0.00, 0.00, 0, 0, 0, 0.00, 0, 'ACTIVE', '2026-01-12 10:31:54', '2026-01-12 10:31:54', '2026-01-12 02:31:55', 0);
INSERT INTO `users` (`id`, `phone`, `password`, `nickname`, `avatar`, `email`, `wechat_openid`, `wechat_unionid`, `is_certified`, `real_name`, `id_card`, `membership_level`, `credit_limit`, `used_credit`, `prepaid_balance`, `points_balance`, `total_points_earned`, `total_points_used`, `total_spent`, `total_orders`, `status`, `created_at`, `updated_at`, `last_login_at`, `is_admin`) VALUES (24, '13800138001', '$2b$12$yVM1alLFptn3W56zS0hj0uqcCGdEk6EHbP4fjDcSz5mCubKK0zWAG', '张三', 'https://via.placeholder.com/150?text=张三', '13800138001@eceshi.com', NULL, NULL, 1, '张三', '110101199001011000', 'GOLD', 8125.00, 740.00, 500.00, 100, 6955, 1445, 11329.00, 20, 'INACTIVE', '2026-01-12 10:36:37', '2026-01-12 17:04:40', NULL, 0);
INSERT INTO `users` (`id`, `phone`, `password`, `nickname`, `avatar`, `email`, `wechat_openid`, `wechat_unionid`, `is_certified`, `real_name`, `id_card`, `membership_level`, `credit_limit`, `used_credit`, `prepaid_balance`, `points_balance`, `total_points_earned`, `total_points_used`, `total_spent`, `total_orders`, `status`, `created_at`, `updated_at`, `last_login_at`, `is_admin`) VALUES (25, '13800138002', '$2b$12$7c88FoyV1tHEzNl4jrepGOqB9NNd0UHar.mSo.VJynXYLf5ubPF72', '李四', 'https://via.placeholder.com/150?text=李四', '13800138002@eceshi.com', NULL, NULL, 1, '李四', '110101199001011001', 'SILVER', 7644.00, 5.00, 1485.00, 1347, 4098, 1338, 10731.00, 7, 'INACTIVE', '2026-01-12 10:36:38', '2026-01-12 10:36:38', NULL, 0);
INSERT INTO `users` (`id`, `phone`, `password`, `nickname`, `avatar`, `email`, `wechat_openid`, `wechat_unionid`, `is_certified`, `real_name`, `id_card`, `membership_level`, `credit_limit`, `used_credit`, `prepaid_balance`, `points_balance`, `total_points_earned`, `total_points_used`, `total_spent`, `total_orders`, `status`, `created_at`, `updated_at`, `last_login_at`, `is_admin`) VALUES (26, '13800138003', '$2b$12$fVLReSMp2B3TQhZwxb0WCe1Sllk5SDde0eGBWLRIlv1D6izPOz1JW', '王五', 'https://via.placeholder.com/150?text=王五', '13800138003@eceshi.com', NULL, NULL, 1, NULL, '110101199001011002', 'PLATINUM', 7352.00, 571.00, 1755.00, 1030, 8154, 2129, 14689.00, 13, 'ACTIVE', '2026-01-12 10:36:38', '2026-01-12 10:36:38', NULL, 0);
INSERT INTO `users` (`id`, `phone`, `password`, `nickname`, `avatar`, `email`, `wechat_openid`, `wechat_unionid`, `is_certified`, `real_name`, `id_card`, `membership_level`, `credit_limit`, `used_credit`, `prepaid_balance`, `points_balance`, `total_points_earned`, `total_points_used`, `total_spent`, `total_orders`, `status`, `created_at`, `updated_at`, `last_login_at`, `is_admin`) VALUES (27, '13800138004', '$2b$12$kwnX0CpWKtXi1zRZQtzOA.QDBeD79aRZNb2suW6u5XXF58ZPRNtjG', '赵六', 'https://via.placeholder.com/150?text=赵六', '13800138004@eceshi.com', NULL, NULL, 1, '赵六', NULL, 'SILVER', 9203.00, 774.00, 449.00, 2875, 5609, 3688, 10164.00, 16, 'ACTIVE', '2026-01-12 10:36:38', '2026-01-12 10:36:38', NULL, 0);
INSERT INTO `users` (`id`, `phone`, `password`, `nickname`, `avatar`, `email`, `wechat_openid`, `wechat_unionid`, `is_certified`, `real_name`, `id_card`, `membership_level`, `credit_limit`, `used_credit`, `prepaid_balance`, `points_balance`, `total_points_earned`, `total_points_used`, `total_spent`, `total_orders`, `status`, `created_at`, `updated_at`, `last_login_at`, `is_admin`) VALUES (28, '13800138005', '$2b$12$5Jgf7aSHB/vRLOQOmZUYRubY.3OM1351Cfd6sesJJOtmLVizzn7g2', '钱七', 'https://via.placeholder.com/150?text=钱七', '13800138005@eceshi.com', NULL, NULL, 0, '钱七', NULL, 'SILVER', 3381.00, 1032.00, 1294.00, 2447, 7353, 1463, 3102.00, 20, 'ACTIVE', '2026-01-12 10:36:38', '2026-01-12 10:36:38', NULL, 0);
INSERT INTO `users` (`id`, `phone`, `password`, `nickname`, `avatar`, `email`, `wechat_openid`, `wechat_unionid`, `is_certified`, `real_name`, `id_card`, `membership_level`, `credit_limit`, `used_credit`, `prepaid_balance`, `points_balance`, `total_points_earned`, `total_points_used`, `total_spent`, `total_orders`, `status`, `created_at`, `updated_at`, `last_login_at`, `is_admin`) VALUES (29, '13800138006', '$2b$12$f/jEhiCGKoXy7kq6i.Tdy.jXPBLsEJ3hYsLlnVeMlJNQRWUNdHih6', '孙八', 'https://via.placeholder.com/150?text=孙八', '13800138006@eceshi.com', NULL, NULL, 1, '孙八', NULL, 'GOLD', 1763.00, 1070.00, 3427.00, 2947, 6995, 1581, 17134.00, 17, 'ACTIVE', '2026-01-12 10:36:39', '2026-01-12 10:36:39', NULL, 0);
INSERT INTO `users` (`id`, `phone`, `password`, `nickname`, `avatar`, `email`, `wechat_openid`, `wechat_unionid`, `is_certified`, `real_name`, `id_card`, `membership_level`, `credit_limit`, `used_credit`, `prepaid_balance`, `points_balance`, `total_points_earned`, `total_points_used`, `total_spent`, `total_orders`, `status`, `created_at`, `updated_at`, `last_login_at`, `is_admin`) VALUES (30, '13800138007', '$2b$12$18BerElWdNoprMT4GSK.7O.xJeR18c16NIYaYw7GpGZX5wmkUvJry', '周九', 'https://via.placeholder.com/150?text=周九', '13800138007@eceshi.com', NULL, NULL, 1, '周九', '110101199001011006', 'PLATINUM', 2240.00, 388.00, 1754.00, 2701, 3076, 4276, 9943.00, 19, 'ACTIVE', '2026-01-12 10:36:39', '2026-01-12 10:36:39', NULL, 0);
INSERT INTO `users` (`id`, `phone`, `password`, `nickname`, `avatar`, `email`, `wechat_openid`, `wechat_unionid`, `is_certified`, `real_name`, `id_card`, `membership_level`, `credit_limit`, `used_credit`, `prepaid_balance`, `points_balance`, `total_points_earned`, `total_points_used`, `total_spent`, `total_orders`, `status`, `created_at`, `updated_at`, `last_login_at`, `is_admin`) VALUES (31, '13800138008', '$2b$12$2ueYkkto7P.XupCVklLHlO2JnC3tks8co4P7KtxIGBP8iwKWXin4S', '吴十', 'https://via.placeholder.com/150?text=吴十', '13800138008@eceshi.com', NULL, NULL, 0, '吴十', '110101199001011007', 'PLATINUM', 2202.00, 1480.00, 1242.00, 244, 7370, 173, 14354.00, 13, 'ACTIVE', '2026-01-12 10:36:39', '2026-01-12 10:36:39', NULL, 0);
INSERT INTO `users` (`id`, `phone`, `password`, `nickname`, `avatar`, `email`, `wechat_openid`, `wechat_unionid`, `is_certified`, `real_name`, `id_card`, `membership_level`, `credit_limit`, `used_credit`, `prepaid_balance`, `points_balance`, `total_points_earned`, `total_points_used`, `total_spent`, `total_orders`, `status`, `created_at`, `updated_at`, `last_login_at`, `is_admin`) VALUES (32, '13900000000', '$2b$12$O0EA60lQZzrmTx7phKSmM.Mwq4j6ODWEhLyDjbOHXEtFGWjSyNojS', '系统管理员', NULL, NULL, NULL, NULL, 0, NULL, NULL, 'NORMAL', 0.00, 0.00, 10000.00, 100, 0, 0, 0.00, 0, 'ACTIVE', '2026-01-12 11:19:27', '2026-01-12 17:04:40', NULL, 1);
INSERT INTO `users` (`id`, `phone`, `password`, `nickname`, `avatar`, `email`, `wechat_openid`, `wechat_unionid`, `is_certified`, `real_name`, `id_card`, `membership_level`, `credit_limit`, `used_credit`, `prepaid_balance`, `points_balance`, `total_points_earned`, `total_points_used`, `total_spent`, `total_orders`, `status`, `created_at`, `updated_at`, `last_login_at`, `is_admin`) VALUES (33, NULL, NULL, '微信用户4t7m0U', NULL, NULL, 'test_openid_4t7m0U', NULL, 0, NULL, NULL, 'NORMAL', 3000.00, 0.00, 0.00, 0, 0, 0, 0.00, 0, 'ACTIVE', '2026-01-12 15:09:31', '2026-01-12 15:09:32', '2026-01-12 07:09:32', 0);
INSERT INTO `users` (`id`, `phone`, `password`, `nickname`, `avatar`, `email`, `wechat_openid`, `wechat_unionid`, `is_certified`, `real_name`, `id_card`, `membership_level`, `credit_limit`, `used_credit`, `prepaid_balance`, `points_balance`, `total_points_earned`, `total_points_used`, `total_spent`, `total_orders`, `status`, `created_at`, `updated_at`, `last_login_at`, `is_admin`) VALUES (34, NULL, NULL, '微信用户1XyFll', NULL, NULL, 'test_openid_1XyFll', NULL, 0, NULL, NULL, 'NORMAL', 3000.00, 0.00, 0.00, 0, 0, 0, 0.00, 0, 'ACTIVE', '2026-01-13 11:04:11', '2026-01-13 11:04:11', '2026-01-13 03:04:11', 0);
COMMIT;

-- ----------------------------
-- Table structure for withdraw_records
-- ----------------------------
DROP TABLE IF EXISTS `withdraw_records`;
CREATE TABLE `withdraw_records` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '提现记录ID',
  `user_id` int NOT NULL COMMENT '用户ID',
  `amount` decimal(10,2) NOT NULL COMMENT '提现金额',
  `withdraw_type` varchar(20) DEFAULT 'invite_reward' COMMENT '提现类型',
  `account_type` varchar(20) DEFAULT NULL COMMENT '账户类型：alipay/wechat/bank',
  `account_name` varchar(50) DEFAULT NULL COMMENT '账户名',
  `account_number` varchar(100) DEFAULT NULL COMMENT '账户号码',
  `status` enum('PENDING','APPROVED','REJECTED','COMPLETED') DEFAULT 'PENDING',
  `reject_reason` text COMMENT '拒绝原因',
  `reviewer_id` int DEFAULT NULL COMMENT '审核人ID',
  `reviewed_at` datetime DEFAULT NULL COMMENT '审核时间',
  `transaction_no` varchar(100) DEFAULT NULL COMMENT '交易单号',
  `completed_at` datetime DEFAULT NULL COMMENT '完成时间',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='提现记录表';

-- ----------------------------
-- Records of withdraw_records
-- ----------------------------
BEGIN;
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;

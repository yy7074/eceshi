-- ============================================
-- 科研检测服务平台数据库 - MySQL 5.7兼容版本
-- 导出时间: $(date '+%Y-%m-%d %H:%M:%S')
-- 数据库版本: MySQL 5.7+
-- ============================================

-- 设置字符集
SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;

-- 禁用外键检查（导入时必须）
SET FOREIGN_KEY_CHECKS = 0;
SET UNIQUE_CHECKS = 0;
SET AUTOCOMMIT = 0;

-- 设置SQL模式（兼容MySQL 5.7）
SET SQL_MODE = 'NO_AUTO_VALUE_ON_ZERO';
SET time_zone = '+08:00';

-- MySQL dump 10.13  Distrib 9.2.0, for macos15.2 (arm64)
--
-- Host: localhost    Database: eceshi
-- ------------------------------------------------------
-- Server version	9.2.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `app_configs`
--

DROP TABLE IF EXISTS `app_configs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `app_configs` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '配置ID',
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
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app_configs`
--

/*!40000 ALTER TABLE `app_configs` DISABLE KEYS */;
/*!40000 ALTER TABLE `app_configs` ENABLE KEYS */;

--
-- Table structure for table `coupons`
--

DROP TABLE IF EXISTS `coupons`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `coupons` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '优惠券ID',
  `name` varchar(100) NOT NULL COMMENT '优惠券名称',
  `description` text COMMENT '优惠券描述',
  `type` enum('DISCOUNT','CASH','FULL_REDUCTION') DEFAULT 'CASH',
  `discount_rate` decimal(5,2) DEFAULT NULL COMMENT '折扣率（如0.9表示9折）',
  `cash_amount` decimal(10,2) DEFAULT NULL COMMENT '代金券金额',
  `full_amount` decimal(10,2) DEFAULT NULL COMMENT '满减门槛金额',
  `reduction_amount` decimal(10,2) DEFAULT NULL COMMENT '满减优惠金额',
  `min_order_amount` decimal(10,2) DEFAULT '0.00' COMMENT '最低订单金额',
  `max_discount_amount` decimal(10,2) DEFAULT NULL COMMENT '最大优惠金额',
  `total_quantity` int(11) DEFAULT '0' COMMENT '发行总量（0表示不限量）',
  `received_quantity` int(11) DEFAULT '0' COMMENT '已领取数量',
  `valid_days` int(11) DEFAULT '30' COMMENT '有效天数',
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
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `coupons`
--

/*!40000 ALTER TABLE `coupons` DISABLE KEYS */;
INSERT INTO `coupons` VALUES (1,'新人专享券','新用户专享，满50减10','CASH',NULL,10.00,NULL,NULL,50.00,NULL,1000,1,30,NULL,NULL,'ACTIVE','2025-11-23 22:35:58','2025-12-23 22:35:58','2025-11-23 22:35:58','2025-11-23 22:36:39'),(2,'满200减30','满200元减30元','FULL_REDUCTION',NULL,NULL,200.00,30.00,200.00,NULL,500,0,30,NULL,NULL,'ACTIVE','2025-11-23 22:35:58','2026-01-22 22:35:58','2025-11-23 22:35:58','2025-11-23 22:35:58'),(3,'9折优惠券','全场9折，最高优惠50元','DISCOUNT',0.90,NULL,NULL,NULL,100.00,50.00,300,0,30,NULL,NULL,'ACTIVE','2025-11-23 22:35:58','2026-02-21 22:35:58','2025-11-23 22:35:58','2025-11-23 22:35:58');
/*!40000 ALTER TABLE `coupons` ENABLE KEYS */;

--
-- Table structure for table `group_members`
--

DROP TABLE IF EXISTS `group_members`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `group_members` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '成员ID',
  `group_id` int(11) NOT NULL COMMENT '团队ID',
  `user_id` int(11) NOT NULL COMMENT '用户ID',
  `nickname` varchar(50) DEFAULT NULL COMMENT '昵称',
  `avatar` varchar(255) DEFAULT NULL COMMENT '头像',
  `phone` varchar(20) DEFAULT NULL COMMENT '手机号',
  `role` enum('OWNER','ADMIN','MEMBER') DEFAULT 'MEMBER',
  `order_count` int(11) DEFAULT '0' COMMENT '订单数量',
  `total_spent` decimal(10,2) DEFAULT '0.00' COMMENT '消费金额',
  `joined_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '加入时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_group_user` (`group_id`,`user_id`),
  KEY `idx_group_id` (`group_id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_role` (`role`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='团队成员表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `group_members`
--

/*!40000 ALTER TABLE `group_members` DISABLE KEYS */;
INSERT INTO `group_members` VALUES (1,1,12,'管理员','/static/uploads/20251018/d099536d2f5b4a4b88c2fbf3cd9b6315.png','admin','OWNER',0,0.00,'2025-11-23 16:16:56');
/*!40000 ALTER TABLE `group_members` ENABLE KEYS */;

--
-- Table structure for table `invite_config`
--

DROP TABLE IF EXISTS `invite_config`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `invite_config` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '配置ID',
  `inviter_reward` decimal(10,2) DEFAULT '10.00' COMMENT '邀请人奖励金额',
  `invitee_reward` decimal(10,2) DEFAULT '5.00' COMMENT '被邀请人奖励金额',
  `reward_type` varchar(20) DEFAULT 'balance' COMMENT '奖励类型',
  `min_order_amount` decimal(10,2) DEFAULT '0.00' COMMENT '最低订单金额要求',
  `reward_delay_days` int(11) DEFAULT '0' COMMENT '奖励延迟天数',
  `min_withdraw_amount` decimal(10,2) DEFAULT '10.00' COMMENT '最低提现金额',
  `withdraw_fee_rate` decimal(5,4) DEFAULT '0.0000' COMMENT '提现手续费率',
  `is_active` tinyint(1) DEFAULT '1' COMMENT '是否启用',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='邀请配置表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `invite_config`
--

/*!40000 ALTER TABLE `invite_config` DISABLE KEYS */;
INSERT INTO `invite_config` VALUES (1,10.00,5.00,'balance',50.00,0,10.00,0.0000,1,'2025-11-23 15:19:25','2025-11-23 15:19:25');
/*!40000 ALTER TABLE `invite_config` ENABLE KEYS */;

--
-- Table structure for table `invite_records`
--

DROP TABLE IF EXISTS `invite_records`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `invite_records` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '邀请记录ID',
  `inviter_id` int(11) NOT NULL COMMENT '邀请人用户ID',
  `invitee_id` int(11) NOT NULL COMMENT '被邀请人用户ID',
  `inviter_name` varchar(50) DEFAULT NULL COMMENT '邀请人昵称',
  `inviter_phone` varchar(20) DEFAULT NULL COMMENT '邀请人手机号',
  `invitee_name` varchar(50) DEFAULT NULL COMMENT '被邀请人昵称',
  `invitee_phone` varchar(20) DEFAULT NULL COMMENT '被邀请人手机号',
  `reward_amount` decimal(10,2) DEFAULT '0.00' COMMENT '奖励金额',
  `reward_type` varchar(20) DEFAULT 'balance' COMMENT '奖励类型：balance/points',
  `status` enum('PENDING','COMPLETED','WITHDRAWN') DEFAULT 'PENDING',
  `first_order_id` int(11) DEFAULT NULL COMMENT '被邀请人首单ID',
  `first_order_amount` decimal(10,2) DEFAULT NULL COMMENT '首单金额',
  `completed_at` datetime DEFAULT NULL COMMENT '完成时间',
  `invited_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '邀请时间',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_inviter_id` (`inviter_id`),
  KEY `idx_invitee_id` (`invitee_id`),
  KEY `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='邀请记录表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `invite_records`
--

/*!40000 ALTER TABLE `invite_records` DISABLE KEYS */;
/*!40000 ALTER TABLE `invite_records` ENABLE KEYS */;

--
-- Table structure for table `invoices`
--

DROP TABLE IF EXISTS `invoices`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `invoices` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `invoice_no` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '发票申请编号',
  `user_id` bigint(20) NOT NULL COMMENT '用户ID',
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
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `invoices`
--

/*!40000 ALTER TABLE `invoices` DISABLE KEYS */;
/*!40000 ALTER TABLE `invoices` ENABLE KEYS */;

--
-- Table structure for table `laboratories`
--

DROP TABLE IF EXISTS `laboratories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `laboratories` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
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
  `order_count` int(11) DEFAULT NULL COMMENT '订单数量',
  `introduction` text COLLATE utf8mb4_unicode_ci COMMENT '实验室简介',
  `equipment_list` json DEFAULT NULL COMMENT '设备清单',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `lab_no` (`lab_no`),
  KEY `ix_laboratories_id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `laboratories`
--

/*!40000 ALTER TABLE `laboratories` DISABLE KEYS */;
/*!40000 ALTER TABLE `laboratories` ENABLE KEYS */;

--
-- Table structure for table `lottery_chances`
--

DROP TABLE IF EXISTS `lottery_chances`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `lottery_chances` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` bigint(20) NOT NULL COMMENT '用户ID',
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
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lottery_chances`
--

/*!40000 ALTER TABLE `lottery_chances` DISABLE KEYS */;
/*!40000 ALTER TABLE `lottery_chances` ENABLE KEYS */;

--
-- Table structure for table `lottery_prizes`
--

DROP TABLE IF EXISTS `lottery_prizes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `lottery_prizes` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '奖品名称',
  `prize_type` enum('COUPON','CASH','POINTS','GIFT','EMPTY') COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '奖品类型',
  `icon` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '奖品图标',
  `value` decimal(10,2) DEFAULT NULL COMMENT '奖品价值',
  `coupon_id` bigint DEFAULT NULL COMMENT '关联优惠券ID',
  `points_amount` int(11) DEFAULT NULL COMMENT '积分数量',
  `probability` int(11) DEFAULT NULL COMMENT '中奖概率（万分比）',
  `daily_limit` int(11) DEFAULT NULL COMMENT '每日限量（0表示不限）',
  `total_limit` int(11) DEFAULT NULL COMMENT '总限量（0表示不限）',
  `issued_count` int(11) DEFAULT NULL COMMENT '已发放数量',
  `is_active` tinyint(1) DEFAULT NULL COMMENT '是否启用',
  `sort_order` int(11) DEFAULT NULL COMMENT '排序',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `ix_lottery_prizes_id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lottery_prizes`
--

/*!40000 ALTER TABLE `lottery_prizes` DISABLE KEYS */;
/*!40000 ALTER TABLE `lottery_prizes` ENABLE KEYS */;

--
-- Table structure for table `lottery_records`
--

DROP TABLE IF EXISTS `lottery_records`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `lottery_records` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` bigint(20) NOT NULL COMMENT '用户ID',
  `prize_id` bigint(20) NOT NULL COMMENT '奖品ID',
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
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lottery_records`
--

/*!40000 ALTER TABLE `lottery_records` DISABLE KEYS */;
/*!40000 ALTER TABLE `lottery_records` ENABLE KEYS */;

--
-- Table structure for table `order_fees`
--

DROP TABLE IF EXISTS `order_fees`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order_fees` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `order_id` bigint(20) NOT NULL COMMENT '订单ID',
  `fee_type` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '费用类型',
  `fee_name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '费用名称',
  `amount` decimal(10,2) NOT NULL COMMENT '金额',
  `remark` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '备注',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  KEY `ix_order_fees_order_id` (`order_id`),
  KEY `ix_order_fees_id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_fees`
--

/*!40000 ALTER TABLE `order_fees` DISABLE KEYS */;
/*!40000 ALTER TABLE `order_fees` ENABLE KEYS */;

--
-- Table structure for table `order_reviews`
--

DROP TABLE IF EXISTS `order_reviews`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order_reviews` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `order_id` int(11) NOT NULL COMMENT '订单ID',
  `user_id` int(11) NOT NULL COMMENT '用户ID',
  `project_id` int(11) NOT NULL COMMENT '项目ID',
  `service_rating` int(11) DEFAULT NULL COMMENT '服务质量评分',
  `quality_rating` int(11) DEFAULT NULL COMMENT '检测效果评分',
  `logistics_rating` int(11) DEFAULT NULL COMMENT '物流配送评分',
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
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_reviews`
--

/*!40000 ALTER TABLE `order_reviews` DISABLE KEYS */;
/*!40000 ALTER TABLE `order_reviews` ENABLE KEYS */;

--
-- Table structure for table `order_samples`
--

DROP TABLE IF EXISTS `order_samples`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order_samples` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `order_id` bigint(20) NOT NULL COMMENT '订单ID',
  `sample_name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '样品名称',
  `sample_type` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '样品类型',
  `sample_desc` text COLLATE utf8mb4_unicode_ci COMMENT '样品描述',
  `quantity` int(11) DEFAULT NULL COMMENT '样品数量',
  `photos` json DEFAULT NULL COMMENT '样品照片',
  `test_params` json DEFAULT NULL COMMENT '检测参数',
  `special_requirements` text COLLATE utf8mb4_unicode_ci COMMENT '特殊要求',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  KEY `ix_order_samples_order_id` (`order_id`),
  KEY `ix_order_samples_id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_samples`
--

/*!40000 ALTER TABLE `order_samples` DISABLE KEYS */;
/*!40000 ALTER TABLE `order_samples` ENABLE KEYS */;

--
-- Table structure for table `order_status_history`
--

DROP TABLE IF EXISTS `order_status_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order_status_history` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `order_id` bigint(20) NOT NULL COMMENT '订单ID',
  `from_status` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '原状态',
  `to_status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '新状态',
  `operator_id` bigint DEFAULT NULL COMMENT '操作人ID',
  `operator_type` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '操作人类型',
  `remark` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '备注',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  KEY `ix_order_status_history_id` (`id`),
  KEY `ix_order_status_history_order_id` (`order_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_status_history`
--

/*!40000 ALTER TABLE `order_status_history` DISABLE KEYS */;
/*!40000 ALTER TABLE `order_status_history` ENABLE KEYS */;

--
-- Table structure for table `orders`
--

DROP TABLE IF EXISTS `orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orders` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `order_no` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '订单号',
  `user_id` bigint(20) NOT NULL COMMENT '用户ID',
  `project_id` bigint(20) NOT NULL COMMENT '项目ID',
  `project_name` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '项目名称',
  `lab_id` bigint(20) NOT NULL COMMENT '实验室ID',
  `lab_name` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '实验室名称',
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '订单状态',
  `project_fee` decimal(10,2) NOT NULL COMMENT '项目费用',
  `urgent_fee` decimal(10,2) DEFAULT NULL COMMENT '加急费用',
  `shipping_fee` decimal(10,2) DEFAULT NULL COMMENT '运费',
  `discount_amount` decimal(10,2) DEFAULT NULL COMMENT '优惠金额',
  `total_fee` decimal(10,2) NOT NULL COMMENT '总金额',
  `paid_fee` decimal(10,2) DEFAULT NULL COMMENT '已支付金额',
  `sample_count` int(11) DEFAULT NULL COMMENT '样品数量',
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
  PRIMARY KEY (`id`),
  UNIQUE KEY `order_no` (`order_no`),
  KEY `ix_orders_user_id` (`user_id`),
  KEY `ix_orders_lab_id` (`lab_id`),
  KEY `ix_orders_status` (`status`),
  KEY `ix_orders_id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders`
--

/*!40000 ALTER TABLE `orders` DISABLE KEYS */;
/*!40000 ALTER TABLE `orders` ENABLE KEYS */;

--
-- Table structure for table `payment_orders`
--

DROP TABLE IF EXISTS `payment_orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `payment_orders` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '订单ID',
  `user_id` int(11) NOT NULL COMMENT '用户ID',
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
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payment_orders`
--

/*!40000 ALTER TABLE `payment_orders` DISABLE KEYS */;
/*!40000 ALTER TABLE `payment_orders` ENABLE KEYS */;

--
-- Table structure for table `payments`
--

DROP TABLE IF EXISTS `payments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `payments` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `payment_no` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '支付单号',
  `order_id` bigint(20) NOT NULL COMMENT '订单ID',
  `order_no` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '订单号',
  `user_id` bigint(20) NOT NULL COMMENT '用户ID',
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payments`
--

/*!40000 ALTER TABLE `payments` DISABLE KEYS */;
/*!40000 ALTER TABLE `payments` ENABLE KEYS */;

--
-- Table structure for table `points_exchange_records`
--

DROP TABLE IF EXISTS `points_exchange_records`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `points_exchange_records` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '兑换ID',
  `user_id` int(11) NOT NULL COMMENT '用户ID',
  `goods_id` int(11) NOT NULL COMMENT '商品ID',
  `points` int(11) NOT NULL COMMENT '兑换消耗积分',
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
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `points_exchange_records`
--

/*!40000 ALTER TABLE `points_exchange_records` DISABLE KEYS */;
/*!40000 ALTER TABLE `points_exchange_records` ENABLE KEYS */;

--
-- Table structure for table `points_goods`
--

DROP TABLE IF EXISTS `points_goods`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `points_goods` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '商品ID',
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '商品名称',
  `points` int(11) NOT NULL COMMENT '所需积分',
  `category` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '商品分类',
  `image` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '商品图片',
  `description` text COLLATE utf8mb4_unicode_ci COMMENT '商品描述',
  `stock` int(11) DEFAULT NULL COMMENT '库存数量',
  `is_active` tinyint(1) DEFAULT NULL COMMENT '是否上架',
  `sort_order` int(11) DEFAULT NULL COMMENT '排序',
  `created_at` datetime DEFAULT NULL COMMENT '创建时间',
  `updated_at` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `ix_points_goods_id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `points_goods`
--

/*!40000 ALTER TABLE `points_goods` DISABLE KEYS */;
/*!40000 ALTER TABLE `points_goods` ENABLE KEYS */;

--
-- Table structure for table `points_records`
--

DROP TABLE IF EXISTS `points_records`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `points_records` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '记录ID',
  `user_id` int(11) NOT NULL COMMENT '用户ID',
  `points` int(11) NOT NULL COMMENT '积分变动（正数为增加，负数为减少）',
  `type` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '积分类型：order,exchange,signin,invite等',
  `related_id` int(11) DEFAULT NULL COMMENT '关联ID（订单ID、兑换ID等）',
  `description` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '积分描述',
  `created_at` datetime DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`),
  KEY `ix_points_records_id` (`id`),
  KEY `ix_points_records_user_id` (`user_id`),
  CONSTRAINT `points_records_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `points_records`
--

/*!40000 ALTER TABLE `points_records` DISABLE KEYS */;
/*!40000 ALTER TABLE `points_records` ENABLE KEYS */;

--
-- Table structure for table `project_categories`
--

DROP TABLE IF EXISTS `project_categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `project_categories` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `name` varchar(100) NOT NULL COMMENT '分类名称',
  `code` varchar(50) DEFAULT NULL COMMENT '分类代码',
  `parent_id` bigint DEFAULT NULL COMMENT '父分类ID',
  `level` int(11) DEFAULT '1' COMMENT '层级',
  `description` text COMMENT '分类描述',
  `is_hot` tinyint(1) DEFAULT '0' COMMENT '是否热门',
  `icon` varchar(200) DEFAULT NULL COMMENT '图标',
  `cover_image` varchar(500) DEFAULT NULL COMMENT '封面图',
  `sort_order` int(11) DEFAULT '0' COMMENT '排序',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `is_active` tinyint(1) DEFAULT '1' COMMENT '是否启用',
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`),
  KEY `idx_sort` (`sort_order`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='项目分类表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `project_categories`
--

/*!40000 ALTER TABLE `project_categories` DISABLE KEYS */;
INSERT INTO `project_categories` VALUES (1,'微观形貌',NULL,NULL,1,'扫描电镜、透射电镜等形貌观察',0,'🔬',NULL,1,'2025-10-18 18:16:06',1),(2,'成分分析',NULL,NULL,1,'XRD、FTIR、NMR等成分检测',0,'🧪',NULL,2,'2025-10-18 18:16:06',1),(3,'热学性能',NULL,NULL,1,'TGA、DSC等热性能测试',0,'🌡️',NULL,3,'2025-10-18 18:16:06',1),(4,'力学性能',NULL,NULL,1,'拉伸、压缩等力学测试',0,'💪',NULL,4,'2025-10-18 18:16:06',1);
/*!40000 ALTER TABLE `project_categories` ENABLE KEYS */;

--
-- Table structure for table `project_favorites`
--

DROP TABLE IF EXISTS `project_favorites`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `project_favorites` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL COMMENT '用户ID',
  `project_id` int(11) NOT NULL COMMENT '项目ID',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '收藏时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_user_project` (`user_id`,`project_id`),
  KEY `ix_project_favorites_user_id` (`user_id`),
  KEY `ix_project_favorites_id` (`id`),
  KEY `ix_project_favorites_project_id` (`project_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `project_favorites`
--

/*!40000 ALTER TABLE `project_favorites` DISABLE KEYS */;
/*!40000 ALTER TABLE `project_favorites` ENABLE KEYS */;

--
-- Table structure for table `project_reviews`
--

DROP TABLE IF EXISTS `project_reviews`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `project_reviews` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `project_id` bigint(20) NOT NULL COMMENT '项目ID',
  `user_id` bigint(20) NOT NULL COMMENT '用户ID',
  `order_id` bigint DEFAULT NULL COMMENT '订单ID',
  `rating` int(11) NOT NULL COMMENT '评分',
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
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `project_reviews`
--

/*!40000 ALTER TABLE `project_reviews` DISABLE KEYS */;
/*!40000 ALTER TABLE `project_reviews` ENABLE KEYS */;

--
-- Table structure for table `projects`
--

DROP TABLE IF EXISTS `projects`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `projects` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `project_no` varchar(32) NOT NULL COMMENT '项目编号',
  `name` varchar(200) NOT NULL COMMENT '项目名称',
  `category_id` bigint(20) NOT NULL COMMENT '分类ID',
  `lab_id` bigint(20) NOT NULL COMMENT '实验室ID',
  `original_price` decimal(10,2) NOT NULL COMMENT '原价',
  `current_price` decimal(10,2) NOT NULL COMMENT '现价',
  `unit` varchar(20) DEFAULT '样品' COMMENT '单位',
  `service_cycle_min` int(11) DEFAULT NULL COMMENT '最短服务周期',
  `service_cycle_max` int(11) DEFAULT NULL COMMENT '最长服务周期',
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
  `view_count` int(11) DEFAULT '0' COMMENT '浏览量',
  `order_count` int(11) DEFAULT '0' COMMENT '订单量',
  `booking_count` int(11) DEFAULT '0' COMMENT '预约量',
  `satisfaction` decimal(5,2) DEFAULT '100.00' COMMENT '满意度',
  `sort_order` int(11) DEFAULT '0' COMMENT '排序',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `project_no` (`project_no`),
  KEY `idx_category` (`category_id`),
  KEY `idx_lab` (`lab_id`),
  KEY `idx_status` (`status`),
  KEY `idx_hot` (`is_hot`),
  KEY `idx_recommended` (`is_recommended`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='项目表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `projects`
--

/*!40000 ALTER TABLE `projects` DISABLE KEYS */;
INSERT INTO `projects` VALUES (1,'PRJ001','扫描电镜（SEM）',1,1,200.00,180.00,'样品',3,5,'Zeiss Sigma 300',NULL,'扫描电子显微镜，观察样品表面形貌，分辨率可达纳米级别。适用于材料表面结构分析、断口分析等。','样品尺寸不超过50mm；样品需导电或喷金处理；干燥样品',NULL,NULL,NULL,'https://picsum.photos/400/300?random=1',NULL,'active',1,0,40,0,0,100.00,1,'2025-10-18 18:16:06','2025-12-01 15:22:25'),(2,'PRJ002','透射电镜（TEM）',1,1,300.00,280.00,'样品',5,7,'FEI Tecnai G2 F20',NULL,'透射电子显微镜，可观察样品内部结构，分辨率达到原子级别。适用于纳米材料结构分析、晶体结构研究等。','样品厚度小于100nm；样品需制备成薄片；导电样品',NULL,NULL,NULL,'https://picsum.photos/400/300?random=2',NULL,'active',1,0,16,0,0,100.00,2,'2025-10-18 18:16:06','2025-11-28 20:27:23'),(3,'PRJ003','X射线衍射（XRD）',2,1,150.00,130.00,'样品',2,3,'Bruker D8 Advance',NULL,'X射线衍射仪，用于物质晶体结构分析、相组成分析、晶粒大小测定等。','粉末样品或块状样品；样品量≥100mg；平整表面',NULL,NULL,NULL,'https://picsum.photos/400/300?random=3',NULL,'active',0,0,4,0,0,100.00,3,'2025-10-18 18:16:06','2025-11-23 18:52:41'),(4,'PRJ004','红外光谱（FTIR）',2,1,100.00,90.00,'样品',1,2,'Thermo Nicolet iS50',NULL,'傅里叶变换红外光谱仪，用于有机物、无机物的定性定量分析，官能团鉴定。','固体或液体样品；样品量≥10mg；避免强吸湿性',NULL,NULL,NULL,'https://picsum.photos/400/300?random=4',NULL,'active',0,0,6,0,0,100.00,4,'2025-10-18 18:16:06','2025-11-23 21:15:20'),(5,'PRJ005','热重分析（TGA）',3,1,180.00,160.00,'样品',2,3,'TA Instruments Q500',NULL,'热重分析仪，测量样品质量随温度变化关系，用于材料热稳定性、分解温度测定等。','样品量5-20mg；粉末或小块状；不挥发性溶剂',NULL,NULL,NULL,'https://picsum.photos/400/300?random=5',NULL,'active',0,0,7,0,0,100.00,5,'2025-10-18 18:16:06','2025-11-23 22:58:58'),(6,'PRJ006','万能材料试验机',4,1,250.00,230.00,'样品',3,5,'Instron 5969',NULL,'万能材料试验机，用于材料拉伸、压缩、弯曲、剪切等力学性能测试。','标准试样；尺寸符合国标；表面光滑',NULL,NULL,NULL,'https://picsum.photos/400/300?random=6',NULL,'active',1,0,5,0,0,100.00,6,'2025-10-18 18:16:06','2025-10-21 13:36:52'),(7,'PRJ007','核磁共振（NMR）',2,1,400.00,380.00,'样品',5,7,'Bruker Avance III 400',NULL,'核磁共振波谱仪，用于有机化合物结构鉴定、纯度分析、反应机理研究等。','样品量≥5mg；溶于氘代溶剂；高纯度样品',NULL,NULL,NULL,'https://picsum.photos/400/300?random=7',NULL,'active',0,0,11,0,0,100.00,7,'2025-10-18 18:16:06','2025-11-23 21:35:30'),(8,'PRJ008','气相色谱-质谱联用（GC-MS）',2,1,350.00,320.00,'样品',4,6,'Agilent 7890B-5977A',NULL,'气相色谱-质谱联用仪，用于复杂混合物分离鉴定、有机物定性定量分析。','液体或可挥发固体；样品量≥1ml；不含颗粒物',NULL,NULL,NULL,'https://picsum.photos/400/300?random=8',NULL,'active',1,0,2,0,0,100.00,8,'2025-10-18 18:16:06','2025-11-23 18:51:50');
/*!40000 ALTER TABLE `projects` ENABLE KEYS */;

--
-- Table structure for table `recharge_records`
--

DROP TABLE IF EXISTS `recharge_records`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `recharge_records` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '充值记录ID',
  `user_id` int(11) NOT NULL COMMENT '用户ID',
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
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `recharge_records`
--

/*!40000 ALTER TABLE `recharge_records` DISABLE KEYS */;
INSERT INTO `recharge_records` VALUES (1,11,'RC17609348422118441',100.00,105.00,5.00,'WECHAT',NULL,NULL,'PENDING',NULL,'2025-10-20 12:34:02',NULL,NULL),(2,11,'RC17609439414237508',100.00,105.00,5.00,'WECHAT',NULL,NULL,'PENDING',NULL,'2025-10-20 15:05:41',NULL,NULL),(3,11,'RC17609440438022540',100.00,105.00,5.00,'WECHAT',NULL,NULL,'PENDING',NULL,'2025-10-20 15:07:23',NULL,NULL),(4,11,'RC17609443089927783',100.00,105.00,5.00,'WECHAT',NULL,NULL,'PENDING',NULL,'2025-10-20 15:11:48',NULL,NULL),(5,11,'RC17609452670098000',100.00,105.00,5.00,'WECHAT',NULL,NULL,'PENDING',NULL,'2025-10-20 15:27:47',NULL,NULL),(6,11,'RC17609452772342864',100.00,105.00,5.00,'WECHAT',NULL,NULL,'PENDING',NULL,'2025-10-20 15:27:57',NULL,NULL),(7,11,'RC17609460270802158',100.00,105.00,5.00,'WECHAT',NULL,NULL,'PENDING',NULL,'2025-10-20 15:40:27',NULL,NULL),(8,11,'RC17609460375242424',100.00,105.00,5.00,'WECHAT',NULL,NULL,'PENDING',NULL,'2025-10-20 15:40:37',NULL,NULL),(9,11,'RC17609462951549213',100.00,105.00,5.00,'WECHAT',NULL,NULL,'PENDING',NULL,'2025-10-20 15:44:55',NULL,NULL),(10,11,'RC17609463073536225',100.00,105.00,5.00,'WECHAT',NULL,NULL,'PENDING',NULL,'2025-10-20 15:45:07',NULL,NULL),(11,11,'RC17609469277553915',100.00,105.00,5.00,'WECHAT',NULL,NULL,'PENDING',NULL,'2025-10-20 15:55:27',NULL,NULL),(12,11,'RC17609469497091495',100.00,105.00,5.00,'WECHAT',NULL,NULL,'PENDING',NULL,'2025-10-20 15:55:49',NULL,NULL),(13,11,'RC17609470453728072',100.00,105.00,5.00,'WECHAT',NULL,NULL,'PENDING',NULL,'2025-10-20 15:57:25',NULL,NULL),(14,11,'RC17609470741264859',1.00,1.00,0.00,'WECHAT',NULL,'4200002837202510206466406783','SUCCESS',NULL,'2025-10-20 15:57:54','2025-10-20 16:12:12','2025-10-20 16:12:12'),(15,11,'RC17609473870979138',1.00,1.00,0.00,'WECHAT',NULL,'4200002938202510205150536186','SUCCESS',NULL,'2025-10-20 16:03:07','2025-10-20 16:17:34','2025-10-20 16:17:34'),(16,11,'RC17609484342061416',1.00,1.00,0.00,'WECHAT',NULL,'4200002924202510203101186614','SUCCESS',NULL,'2025-10-20 16:20:34','2025-10-20 16:20:47','2025-10-20 16:20:47'),(17,11,'RC17639104465414523',100.00,105.00,5.00,'WECHAT',NULL,NULL,'PENDING',NULL,'2025-11-23 23:07:26',NULL,NULL);
/*!40000 ALTER TABLE `recharge_records` ENABLE KEYS */;

--
-- Table structure for table `recovery_tasks`
--

DROP TABLE IF EXISTS `recovery_tasks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `recovery_tasks` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '任务ID',
  `user_id` int(11) NOT NULL COMMENT '用户ID',
  `membership_id` int(11) DEFAULT NULL COMMENT '会员ID',
  `task_no` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '任务编号',
  `service_type` enum('SUPER_RECOVERY','IMAGE_RECOVERY','WECHAT_RECOVERY','VIDEO_RECOVERY','FILE_RECOVERY','AUDIO_RECOVERY') COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '服务类型',
  `status` enum('PENDING','SCANNING','SCANNED','RECOVERING','COMPLETED','FAILED','CANCELLED') COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '任务状态',
  `device_type` enum('ANDROID','IOS','WINDOWS','MAC','OTHER') COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '设备类型',
  `device_model` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '设备型号',
  `device_os_version` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '系统版本',
  `device_storage_size` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '存储容量',
  `recovery_types` text COLLATE utf8mb4_unicode_ci COMMENT '恢复类型列表，JSON格式',
  `scan_deep` tinyint(1) DEFAULT NULL COMMENT '是否深度扫描',
  `progress_percent` int(11) DEFAULT NULL COMMENT '进度百分比',
  `scanned_files_count` int(11) DEFAULT NULL COMMENT '已扫描文件数',
  `recoverable_files_count` int(11) DEFAULT NULL COMMENT '可恢复文件数',
  `recovered_files_count` int(11) DEFAULT NULL COMMENT '已恢复文件数',
  `result_summary` text COLLATE utf8mb4_unicode_ci COMMENT '恢复结果摘要',
  `result_files_url` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '恢复文件下载链接',
  `engineer_id` int(11) DEFAULT NULL COMMENT '负责工程师ID',
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
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `recovery_tasks`
--

/*!40000 ALTER TABLE `recovery_tasks` DISABLE KEYS */;
/*!40000 ALTER TABLE `recovery_tasks` ENABLE KEYS */;

--
-- Table structure for table `scan_results`
--

DROP TABLE IF EXISTS `scan_results`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `scan_results` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '结果ID',
  `task_id` int(11) NOT NULL COMMENT '任务ID',
  `file_type` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '文件类型',
  `file_name` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '文件名',
  `file_path` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '文件路径',
  `file_size` int(11) DEFAULT NULL COMMENT '文件大小（字节）',
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
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `scan_results`
--

/*!40000 ALTER TABLE `scan_results` DISABLE KEYS */;
/*!40000 ALTER TABLE `scan_results` ENABLE KEYS */;

--
-- Table structure for table `service_packages`
--

DROP TABLE IF EXISTS `service_packages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `service_packages` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '套餐ID',
  `service_type` enum('SUPER_RECOVERY','IMAGE_RECOVERY','WECHAT_RECOVERY','VIDEO_RECOVERY','FILE_RECOVERY','AUDIO_RECOVERY') COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '服务类型',
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '套餐名称',
  `description` text COLLATE utf8mb4_unicode_ci COMMENT '套餐描述',
  `price` decimal(10,2) NOT NULL COMMENT '现价',
  `original_price` decimal(10,2) DEFAULT NULL COMMENT '原价',
  `features` text COLLATE utf8mb4_unicode_ci COMMENT '功能特性列表，JSON格式',
  `max_recoveries` int(11) DEFAULT NULL COMMENT '最大恢复次数，0表示无限制',
  `is_active` tinyint(1) DEFAULT NULL COMMENT '是否启用',
  `sort_order` int(11) DEFAULT NULL COMMENT '排序',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `service_type` (`service_type`),
  KEY `ix_service_packages_id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `service_packages`
--

/*!40000 ALTER TABLE `service_packages` DISABLE KEYS */;
/*!40000 ALTER TABLE `service_packages` ENABLE KEYS */;

--
-- Table structure for table `sms_codes`
--

DROP TABLE IF EXISTS `sms_codes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sms_codes` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `phone` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '手机号',
  `code` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '验证码',
  `is_used` tinyint(1) DEFAULT NULL COMMENT '是否已使用',
  `scene` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '使用场景(register/login/reset_password)',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `expires_at` datetime NOT NULL COMMENT '过期时间',
  PRIMARY KEY (`id`),
  KEY `ix_sms_codes_phone` (`phone`),
  KEY `ix_sms_codes_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sms_codes`
--

/*!40000 ALTER TABLE `sms_codes` DISABLE KEYS */;
INSERT INTO `sms_codes` VALUES (1,'13800138000','517378',0,'register','2025-10-18 13:51:21','2025-10-18 05:56:22'),(6,'18663764585','293014',1,'login','2025-11-28 20:27:31','2025-11-28 12:32:32');
/*!40000 ALTER TABLE `sms_codes` ENABLE KEYS */;

--
-- Table structure for table `task_progress_logs`
--

DROP TABLE IF EXISTS `task_progress_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `task_progress_logs` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '日志ID',
  `task_id` int(11) NOT NULL COMMENT '任务ID',
  `progress_percent` int(11) DEFAULT NULL COMMENT '进度百分比',
  `current_step` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '当前步骤',
  `step_description` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '步骤描述',
  `files_scanned` int(11) DEFAULT NULL COMMENT '已扫描文件数',
  `files_found` int(11) DEFAULT NULL COMMENT '发现文件数',
  `files_recovered` int(11) DEFAULT NULL COMMENT '已恢复文件数',
  `log_level` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '日志级别',
  `message` text COLLATE utf8mb4_unicode_ci COMMENT '日志消息',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  KEY `ix_task_progress_logs_id` (`id`),
  KEY `ix_task_progress_logs_task_id` (`task_id`),
  CONSTRAINT `task_progress_logs_ibfk_1` FOREIGN KEY (`task_id`) REFERENCES `recovery_tasks` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `task_progress_logs`
--

/*!40000 ALTER TABLE `task_progress_logs` DISABLE KEYS */;
/*!40000 ALTER TABLE `task_progress_logs` ENABLE KEYS */;

--
-- Table structure for table `user_addresses`
--

DROP TABLE IF EXISTS `user_addresses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_addresses` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` bigint(20) NOT NULL COMMENT '用户ID',
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
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_addresses`
--

/*!40000 ALTER TABLE `user_addresses` DISABLE KEYS */;
INSERT INTO `user_addresses` VALUES (1,11,'11','13000000001','北京市','北京市','海淀区','1111',0,'2025-10-19 13:52:25',NULL),(2,13,'王泽华','15939409857','北京市','北京市','西城区','北京大学',1,'2025-10-20 00:03:49',NULL),(3,14,'刘','17302076676','广东省','广州市','天河区','海珠广场',1,'2025-10-20 11:16:53',NULL);
/*!40000 ALTER TABLE `user_addresses` ENABLE KEYS */;

--
-- Table structure for table `user_certification`
--

DROP TABLE IF EXISTS `user_certification`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_certification` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL COMMENT '用户ID',
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
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_certification`
--

/*!40000 ALTER TABLE `user_certification` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_certification` ENABLE KEYS */;

--
-- Table structure for table `user_coupons`
--

DROP TABLE IF EXISTS `user_coupons`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_coupons` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '用户优惠券ID',
  `user_id` int(11) NOT NULL COMMENT '用户ID',
  `coupon_id` int(11) NOT NULL COMMENT '优惠券ID',
  `coupon_name` varchar(100) DEFAULT NULL COMMENT '优惠券名称',
  `coupon_type` varchar(20) DEFAULT NULL COMMENT '优惠券类型',
  `discount_value` decimal(10,2) DEFAULT NULL COMMENT '优惠值',
  `status` enum('UNUSED','USED','EXPIRED') DEFAULT 'UNUSED',
  `order_id` int(11) DEFAULT NULL COMMENT '使用的订单ID',
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
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_coupons`
--

/*!40000 ALTER TABLE `user_coupons` DISABLE KEYS */;
INSERT INTO `user_coupons` VALUES (1,12,1,'新人专享券','cash',10.00,'UNUSED',NULL,NULL,'2025-11-23 22:36:39','2025-12-23 22:36:39','2025-11-23 22:36:39','2025-11-23 22:36:39');
/*!40000 ALTER TABLE `user_coupons` ENABLE KEYS */;

--
-- Table structure for table `user_groups`
--

DROP TABLE IF EXISTS `user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '团队ID',
  `name` varchar(100) NOT NULL COMMENT '团队名称',
  `avatar` varchar(255) DEFAULT NULL COMMENT '团队头像',
  `description` text COMMENT '团队描述',
  `owner_id` int(11) NOT NULL COMMENT '负责人用户ID',
  `owner_name` varchar(50) DEFAULT NULL COMMENT '负责人姓名',
  `owner_phone` varchar(20) DEFAULT NULL COMMENT '负责人手机号',
  `university` varchar(100) DEFAULT NULL COMMENT '所属高校',
  `department` varchar(100) DEFAULT NULL COMMENT '所属院系',
  `invite_code` varchar(20) DEFAULT NULL COMMENT '邀请码',
  `member_count` int(11) DEFAULT '1' COMMENT '成员数量',
  `total_orders` int(11) DEFAULT '0' COMMENT '累计订单数',
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
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_groups`
--

/*!40000 ALTER TABLE `user_groups` DISABLE KEYS */;
INSERT INTO `user_groups` VALUES (1,'测试团队','https://example.com/avatar.jpg','高校 - 北京市',12,'张三','admin','北京市','海淀区','MHX4KQOB',1,0,0.00,'ACTIVE',0,'2025-11-23 16:16:56','2025-11-23 16:16:56');
/*!40000 ALTER TABLE `user_groups` ENABLE KEYS */;

--
-- Table structure for table `user_memberships`
--

DROP TABLE IF EXISTS `user_memberships`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_memberships` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '会员ID',
  `user_id` int(11) NOT NULL COMMENT '用户ID',
  `service_type` enum('SUPER_RECOVERY','IMAGE_RECOVERY','WECHAT_RECOVERY','VIDEO_RECOVERY','FILE_RECOVERY','AUDIO_RECOVERY') COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '服务类型',
  `is_active` tinyint(1) DEFAULT NULL COMMENT '是否激活',
  `expires_at` datetime DEFAULT NULL COMMENT '过期时间',
  `max_recoveries` int(11) DEFAULT NULL COMMENT '最大恢复次数，0表示无限制',
  `used_recoveries` int(11) DEFAULT NULL COMMENT '已使用恢复次数',
  `purchase_price` decimal(10,2) DEFAULT NULL COMMENT '购买价格',
  `purchase_order_no` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '购买订单号',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `ix_user_memberships_user_id` (`user_id`),
  KEY `ix_user_memberships_id` (`id`),
  CONSTRAINT `user_memberships_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_memberships`
--

/*!40000 ALTER TABLE `user_memberships` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_memberships` ENABLE KEYS */;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '用户ID',
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
  `membership_level` enum('NORMAL','SILVER','GOLD','PLATINUM') COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '会员等级',
  `credit_limit` decimal(10,2) DEFAULT NULL COMMENT '信用额度',
  `used_credit` decimal(10,2) DEFAULT NULL COMMENT '已用信用额度',
  `prepaid_balance` decimal(10,2) DEFAULT NULL COMMENT '预付余额',
  `points_balance` int(11) DEFAULT NULL COMMENT '积分余额',
  `total_points_earned` int(11) DEFAULT NULL COMMENT '累计获得积分',
  `total_points_used` int(11) DEFAULT NULL COMMENT '累计使用积分',
  `total_spent` decimal(10,2) DEFAULT NULL COMMENT '累计消费金额',
  `total_orders` int(11) DEFAULT NULL COMMENT '累计订单数',
  `status` enum('ACTIVE','INACTIVE','BANNED') COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '用户状态',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  `last_login_at` datetime DEFAULT NULL COMMENT '最后登录时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_users_phone` (`phone`),
  UNIQUE KEY `idx_wechat_openid` (`wechat_openid`),
  KEY `ix_users_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'18663764585','$2b$12$lk5hUspm9pidavlm17J0I.UH8z4McvfAlR1tR/piFLBqzDzDOaJWW','用户4585',NULL,NULL,NULL,NULL,0,NULL,NULL,'NORMAL',3000.00,0.00,0.00,0,0,0,0.00,0,'ACTIVE','2025-10-18 13:54:57','2025-11-28 20:27:38','2025-11-28 12:27:39'),(11,NULL,NULL,'微信用户3rhTPY',NULL,NULL,'orB2m7V3L6LNKlpYO2mhaT3rhTPY',NULL,0,NULL,NULL,'NORMAL',3000.00,0.00,3.00,0,0,0,0.00,0,'ACTIVE','2025-10-18 17:20:51','2025-11-23 23:06:53','2025-11-23 15:06:54'),(12,'admin','$2b$12$/3JHrrhnE9T/jcZUaR9IruW6qvXOo65IijCEL3IAa6ER0s8dfbq6W','管理员','/static/uploads/20251018/d099536d2f5b4a4b88c2fbf3cd9b6315.png',NULL,NULL,NULL,1,NULL,NULL,'NORMAL',999999.00,0.00,0.00,0,0,0,0.00,0,'ACTIVE','2025-10-18 17:47:06','2025-11-28 19:13:49','2025-11-28 11:13:49'),(13,NULL,NULL,'微信用户0rmpgs',NULL,NULL,'orB2m7SVODCoFs6ECSfviQ0rmpgs',NULL,0,NULL,NULL,'NORMAL',3000.00,0.00,0.00,0,0,0,0.00,0,'ACTIVE','2025-10-19 23:58:31','2025-11-23 19:35:33','2025-11-23 11:35:33'),(14,NULL,NULL,'微信用户F4ENsU',NULL,NULL,'orB2m7TPBZc-HobpObc4IjF4ENsU',NULL,0,NULL,NULL,'NORMAL',3000.00,0.00,0.00,0,0,0,0.00,0,'ACTIVE','2025-10-20 11:15:59','2025-10-20 11:15:59','2025-10-20 03:15:59'),(15,'13800138000','$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzpLhJ632u','测试用户',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,1000.00,NULL,NULL,NULL,NULL,NULL,NULL,'2025-11-23 16:07:10','2025-11-23 16:07:10',NULL),(16,NULL,NULL,'微信用户GMohko',NULL,NULL,'orB2m7f85fTvYFRVt9RtmXGMohko',NULL,0,NULL,NULL,'NORMAL',3000.00,0.00,0.00,0,0,0,0.00,0,'ACTIVE','2025-11-23 23:13:19','2025-11-23 23:13:23','2025-11-23 15:13:24');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;

--
-- Table structure for table `withdraw_records`
--

DROP TABLE IF EXISTS `withdraw_records`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `withdraw_records` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '提现记录ID',
  `user_id` int(11) NOT NULL COMMENT '用户ID',
  `amount` decimal(10,2) NOT NULL COMMENT '提现金额',
  `withdraw_type` varchar(20) DEFAULT 'invite_reward' COMMENT '提现类型',
  `account_type` varchar(20) DEFAULT NULL COMMENT '账户类型：alipay/wechat/bank',
  `account_name` varchar(50) DEFAULT NULL COMMENT '账户名',
  `account_number` varchar(100) DEFAULT NULL COMMENT '账户号码',
  `status` enum('PENDING','APPROVED','REJECTED','COMPLETED') DEFAULT 'PENDING',
  `reject_reason` text COMMENT '拒绝原因',
  `reviewer_id` int(11) DEFAULT NULL COMMENT '审核人ID',
  `reviewed_at` datetime DEFAULT NULL COMMENT '审核时间',
  `transaction_no` varchar(100) DEFAULT NULL COMMENT '交易单号',
  `completed_at` datetime DEFAULT NULL COMMENT '完成时间',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='提现记录表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `withdraw_records`
--

/*!40000 ALTER TABLE `withdraw_records` DISABLE KEYS */;
/*!40000 ALTER TABLE `withdraw_records` ENABLE KEYS */;

--
-- Dumping routines for database 'eceshi'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-12-02 13:18:39

-- 重新启用外键检查
SET FOREIGN_KEY_CHECKS = 1;
SET UNIQUE_CHECKS = 1;
COMMIT;

-- 导入完成

-- 创建项目相关表
USE eceshi;

-- 项目分类表
CREATE TABLE IF NOT EXISTS project_categories (
    id BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT 'ID',
    name VARCHAR(100) NOT NULL COMMENT '分类名称',
    description TEXT COMMENT '分类描述',
    icon VARCHAR(200) COMMENT '图标',
    sort_order INT DEFAULT 0 COMMENT '排序',
    status VARCHAR(20) DEFAULT 'active' COMMENT '状态',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX idx_status (status),
    INDEX idx_sort (sort_order)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='项目分类表';

-- 项目表
CREATE TABLE IF NOT EXISTS projects (
    id BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT 'ID',
    project_no VARCHAR(32) UNIQUE NOT NULL COMMENT '项目编号',
    name VARCHAR(200) NOT NULL COMMENT '项目名称',
    category_id BIGINT NOT NULL COMMENT '分类ID',
    lab_id BIGINT NOT NULL COMMENT '实验室ID',
    original_price DECIMAL(10,2) NOT NULL COMMENT '原价',
    current_price DECIMAL(10,2) NOT NULL COMMENT '现价',
    unit VARCHAR(20) DEFAULT '样品' COMMENT '单位',
    service_cycle_min INT COMMENT '最短服务周期',
    service_cycle_max INT COMMENT '最长服务周期',
    equipment_name VARCHAR(200) COMMENT '仪器名称',
    equipment_model VARCHAR(200) COMMENT '仪器型号',
    introduction TEXT COMMENT '项目介绍',
    sample_requirements TEXT COMMENT '样品要求',
    test_parameters JSON COMMENT '检测参数',
    booking_notice TEXT COMMENT '预约须知',
    faq JSON COMMENT '常见问题',
    cover_image VARCHAR(500) COMMENT '封面图',
    detail_images JSON COMMENT '详情图',
    status VARCHAR(20) DEFAULT 'active' COMMENT '状态',
    is_hot BOOLEAN DEFAULT FALSE COMMENT '是否热门',
    is_recommended BOOLEAN DEFAULT FALSE COMMENT '是否推荐',
    view_count INT DEFAULT 0 COMMENT '浏览量',
    booking_count INT DEFAULT 0 COMMENT '预约量',
    satisfaction DECIMAL(5,2) DEFAULT 100.00 COMMENT '满意度',
    sort_order INT DEFAULT 0 COMMENT '排序',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_category (category_id),
    INDEX idx_lab (lab_id),
    INDEX idx_status (status),
    INDEX idx_hot (is_hot),
    INDEX idx_recommended (is_recommended)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='项目表';

-- 项目评价表
CREATE TABLE IF NOT EXISTS project_reviews (
    id BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT 'ID',
    project_id BIGINT NOT NULL COMMENT '项目ID',
    user_id BIGINT NOT NULL COMMENT '用户ID',
    order_id BIGINT COMMENT '订单ID',
    rating INT NOT NULL COMMENT '评分',
    content TEXT COMMENT '评价内容',
    images JSON COMMENT '评价图片',
    status VARCHAR(20) DEFAULT 'pending' COMMENT '状态',
    reply TEXT COMMENT '商家回复',
    reply_at DATETIME COMMENT '回复时间',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX idx_project (project_id),
    INDEX idx_user (user_id),
    INDEX idx_order (order_id),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='项目评价表';

SELECT '✅ 项目相关表创建完成！' as result;


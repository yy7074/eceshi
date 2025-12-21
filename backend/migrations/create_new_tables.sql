-- 创建新功能所需的数据库表
-- 执行方式: mysql -u username -p database_name < create_new_tables.sql

-- 1. 轮播图表
CREATE TABLE IF NOT EXISTS banners (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL COMMENT '标题',
    subtitle VARCHAR(500) COMMENT '副标题',
    image VARCHAR(500) NOT NULL COMMENT '图片URL',
    link_type VARCHAR(50) DEFAULT 'none' COMMENT '链接类型: none/project/url/page',
    link_value VARCHAR(500) COMMENT '链接值',
    button_text VARCHAR(50) COMMENT '按钮文字',
    sort_order INT DEFAULT 0 COMMENT '排序',
    is_active BOOLEAN DEFAULT TRUE COMMENT '是否启用',
    position VARCHAR(50) DEFAULT 'home' COMMENT '展示位置',
    start_time DATETIME COMMENT '开始时间',
    end_time DATETIME COMMENT '结束时间',
    click_count INT DEFAULT 0 COMMENT '点击次数',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_position_active (position, is_active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='轮播图';

-- 2. 公告表
CREATE TABLE IF NOT EXISTS announcements (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL COMMENT '标题',
    content TEXT NOT NULL COMMENT '内容',
    summary VARCHAR(500) COMMENT '摘要',
    category VARCHAR(50) DEFAULT 'system' COMMENT '分类',
    is_top BOOLEAN DEFAULT FALSE COMMENT '是否置顶',
    is_active BOOLEAN DEFAULT TRUE COMMENT '是否启用',
    view_count INT DEFAULT 0 COMMENT '查看次数',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_category_active (category, is_active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='公告';

-- 3. 用户通知表
CREATE TABLE IF NOT EXISTS user_notifications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL COMMENT '用户ID',
    title VARCHAR(200) NOT NULL COMMENT '标题',
    content TEXT COMMENT '内容',
    category VARCHAR(50) DEFAULT 'system' COMMENT '分类',
    is_read BOOLEAN DEFAULT FALSE COMMENT '是否已读',
    related_type VARCHAR(50) COMMENT '关联类型',
    related_id INT COMMENT '关联ID',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user_read (user_id, is_read)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户通知';

-- 4. 帮助分类表
CREATE TABLE IF NOT EXISTS help_categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL COMMENT '分类名称',
    icon VARCHAR(100) COMMENT '图标',
    sort_order INT DEFAULT 0 COMMENT '排序',
    is_active BOOLEAN DEFAULT TRUE COMMENT '是否启用',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='帮助分类';

-- 5. 帮助文章表
CREATE TABLE IF NOT EXISTS help_articles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    category_id INT NOT NULL COMMENT '分类ID',
    title VARCHAR(200) NOT NULL COMMENT '标题',
    content TEXT NOT NULL COMMENT '内容',
    is_hot BOOLEAN DEFAULT FALSE COMMENT '是否热门',
    view_count INT DEFAULT 0 COMMENT '查看次数',
    sort_order INT DEFAULT 0 COMMENT '排序',
    is_active BOOLEAN DEFAULT TRUE COMMENT '是否启用',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_category_active (category_id, is_active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='帮助文章';

-- 6. 聊天会话表
CREATE TABLE IF NOT EXISTS chat_sessions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL COMMENT '用户ID',
    staff_id INT COMMENT '客服ID',
    status VARCHAR(20) DEFAULT 'active' COMMENT '状态',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    closed_at DATETIME COMMENT '关闭时间',
    INDEX idx_user_status (user_id, status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='聊天会话';

-- 7. 聊天消息表
CREATE TABLE IF NOT EXISTS chat_messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    session_id INT NOT NULL COMMENT '会话ID',
    sender_type VARCHAR(20) NOT NULL COMMENT '发送者类型',
    sender_id INT COMMENT '发送者ID',
    content TEXT NOT NULL COMMENT '消息内容',
    message_type VARCHAR(20) DEFAULT 'text' COMMENT '消息类型',
    is_read BOOLEAN DEFAULT FALSE COMMENT '是否已读',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_session (session_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='聊天消息';

-- 8. 快捷回复表
CREATE TABLE IF NOT EXISTS quick_replies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    question VARCHAR(500) NOT NULL COMMENT '问题',
    answer TEXT NOT NULL COMMENT '回答',
    category VARCHAR(50) COMMENT '分类',
    sort_order INT DEFAULT 0 COMMENT '排序',
    is_active BOOLEAN DEFAULT TRUE COMMENT '是否启用',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='快捷回复';

-- 9. 合同表
CREATE TABLE IF NOT EXISTS contracts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    contract_no VARCHAR(50) UNIQUE NOT NULL COMMENT '合同编号',
    user_id INT NOT NULL COMMENT '用户ID',
    order_id INT COMMENT '关联订单ID',
    order_no VARCHAR(50) COMMENT '关联订单号',
    title VARCHAR(200) NOT NULL COMMENT '合同标题',
    content TEXT COMMENT '合同内容',
    amount DECIMAL(10,2) COMMENT '合同金额',
    status VARCHAR(20) DEFAULT 'active' COMMENT '状态',
    signed_at DATETIME COMMENT '签订日期',
    expired_at DATETIME COMMENT '到期日期',
    file_url VARCHAR(500) COMMENT '合同文件URL',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_user (user_id),
    INDEX idx_order (order_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='合同';

-- 10. 检测报告表
CREATE TABLE IF NOT EXISTS reports (
    id INT AUTO_INCREMENT PRIMARY KEY,
    report_no VARCHAR(50) UNIQUE NOT NULL COMMENT '报告编号',
    user_id INT NOT NULL COMMENT '用户ID',
    order_id INT NOT NULL COMMENT '订单ID',
    order_no VARCHAR(50) COMMENT '订单号',
    project_name VARCHAR(200) COMMENT '项目名称',
    sample_name VARCHAR(200) COMMENT '样品名称',
    status VARCHAR(20) DEFAULT 'pending' COMMENT '状态',
    file_url VARCHAR(500) COMMENT '报告文件URL',
    file_size INT COMMENT '文件大小',
    download_count INT DEFAULT 0 COMMENT '下载次数',
    completed_at DATETIME COMMENT '完成时间',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_user (user_id),
    INDEX idx_order (order_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='检测报告';

-- 11. 样品追踪记录表
CREATE TABLE IF NOT EXISTS sample_trackings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL COMMENT '订单ID',
    order_no VARCHAR(50) COMMENT '订单号',
    sample_name VARCHAR(200) COMMENT '样品名称',
    status VARCHAR(50) NOT NULL COMMENT '状态',
    status_text VARCHAR(100) COMMENT '状态描述',
    location VARCHAR(200) COMMENT '当前位置',
    operator VARCHAR(100) COMMENT '操作人',
    remark TEXT COMMENT '备注',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_order (order_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='样品追踪记录';

-- 12. 样品物流信息表
CREATE TABLE IF NOT EXISTS sample_logistics (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL COMMENT '订单ID',
    logistics_type VARCHAR(20) DEFAULT 'send' COMMENT '类型',
    company VARCHAR(100) COMMENT '快递公司',
    tracking_no VARCHAR(100) COMMENT '快递单号',
    sender_name VARCHAR(100) COMMENT '寄件人',
    sender_phone VARCHAR(20) COMMENT '寄件人电话',
    sender_address VARCHAR(500) COMMENT '寄件地址',
    receiver_name VARCHAR(100) COMMENT '收件人',
    receiver_phone VARCHAR(20) COMMENT '收件人电话',
    receiver_address VARCHAR(500) COMMENT '收件地址',
    status VARCHAR(20) DEFAULT 'pending' COMMENT '状态',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_order (order_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='样品物流信息';

-- 13. 加盟申请表
CREATE TABLE IF NOT EXISTS franchise_applications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    application_no VARCHAR(50) UNIQUE NOT NULL COMMENT '申请编号',
    name VARCHAR(100) NOT NULL COMMENT '联系人姓名',
    phone VARCHAR(20) NOT NULL COMMENT '联系电话',
    company VARCHAR(200) COMMENT '公司名称',
    city VARCHAR(100) COMMENT '所在城市',
    mode VARCHAR(50) DEFAULT 'agent' COMMENT '合作模式',
    intention TEXT COMMENT '合作意向',
    status VARCHAR(20) DEFAULT 'pending' COMMENT '状态',
    staff_id INT COMMENT '处理人ID',
    staff_remark TEXT COMMENT '处理备注',
    contacted_at DATETIME COMMENT '联系时间',
    user_id INT COMMENT '关联用户ID',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_phone (phone),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='加盟申请';

-- 插入示例数据

-- 轮播图示例数据
INSERT INTO banners (title, subtitle, image, link_type, link_value, button_text, sort_order, is_active, position) VALUES
('专业检测服务', '材料检测·分析测试·科研服务', 'https://picsum.photos/1200/400?random=1', 'page', 'projects', '立即预约', 1, TRUE, 'home'),
('新用户优惠', '首单立减100元', 'https://picsum.photos/1200/400?random=2', 'page', 'coupons', '领取优惠', 2, TRUE, 'home'),
('合作伙伴招募', '区域代理·项目合作·实验室入驻', 'https://picsum.photos/1200/400?random=3', 'page', 'franchise', '了解详情', 3, TRUE, 'home');

-- 公告示例数据
INSERT INTO announcements (title, content, summary, category, is_top, is_active) VALUES
('系统升级通知', '为了提供更好的服务体验，我们将于本周六凌晨2:00-6:00进行系统升级维护，届时部分功能可能暂时无法使用，请提前做好安排。给您带来的不便，敬请谅解！', '系统将于本周六凌晨进行升级维护', 'system', TRUE, TRUE),
('春节放假通知', '2025年春节放假时间为1月28日至2月4日，期间订单正常接收，检测服务将于2月5日恢复。祝大家新春快乐！', '春节期间服务安排', 'notice', FALSE, TRUE),
('新项目上线', '全新XRD高分辨检测服务已上线，欢迎体验！首周下单享8折优惠。', '新检测项目上线', 'activity', FALSE, TRUE);

-- 帮助分类示例数据
INSERT INTO help_categories (name, icon, sort_order, is_active) VALUES
('下单指南', '📦', 1, TRUE),
('支付问题', '💳', 2, TRUE),
('样品寄送', '📮', 3, TRUE),
('报告相关', '📄', 4, TRUE),
('发票问题', '🧾', 5, TRUE),
('账户问题', '👤', 6, TRUE);

-- 帮助文章示例数据
INSERT INTO help_articles (category_id, title, content, is_hot, sort_order, is_active) VALUES
(1, '如何下单预约检测服务？', '1. 登录账户后，在首页或分类页面选择需要的检测项目\n2. 进入项目详情页，查看检测内容、周期和价格\n3. 点击"立即预约"按钮，填写样品信息\n4. 选择收货地址和优惠券（如有）\n5. 确认订单信息后提交\n6. 完成支付即可', TRUE, 1, TRUE),
(1, '如何选择适合的检测项目？', '您可以通过以下方式选择检测项目：\n1. 在首页分类中浏览各类检测项目\n2. 使用搜索功能直接搜索项目名称\n3. 联系在线客服获取专业建议\n4. 查看项目详情了解检测内容和应用场景', FALSE, 2, TRUE),
(2, '支持哪些支付方式？', '目前支持以下支付方式：\n1. 微信支付\n2. 支付宝支付\n3. 余额支付（需先充值）\n4. 对公转账（企业用户）', TRUE, 1, TRUE),
(3, '样品如何寄送？', '1. 下单支付后，系统会显示实验室收件地址\n2. 将样品妥善包装，防止运输损坏\n3. 选择顺丰或其他快递寄出\n4. 在订单页面填写快递单号\n5. 实验室收到样品后会及时确认', TRUE, 1, TRUE),
(4, '如何下载检测报告？', '检测完成后，您可以通过以下方式获取报告：\n1. 在"我的订单"中找到已完成的订单\n2. 点击"下载报告"按钮获取电子版\n3. 纸质报告会邮寄到您预留的地址', TRUE, 1, TRUE);

-- 快捷回复示例数据
INSERT INTO quick_replies (question, answer, category, sort_order, is_active) VALUES
('检测需要多长时间？', '一般检测周期为3-7个工作日，具体时间取决于检测项目的复杂程度。加急服务可缩短至1-3个工作日，需额外支付加急费用。', '常见问题', 1, TRUE),
('如何查看检测进度？', '您可以在"我的订单"页面查看订单状态，或使用"样品追踪"功能实时了解检测进度。', '常见问题', 2, TRUE),
('报告可以加急吗？', '可以的，我们提供加急服务。下单时选择加急选项或联系客服说明需求，加急费用根据项目不同有所差异。', '常见问题', 3, TRUE),
('如何申请发票？', '订单完成后，在"我的发票"页面申请开具发票，支持增值税普通发票和专用发票。发票将在申请后3-5个工作日内开具。', '发票相关', 4, TRUE),
('样品会退还吗？', '根据检测类型不同：破坏性检测的样品不退还；非破坏性检测的样品可申请退还，需承担运费。', '样品相关', 5, TRUE);


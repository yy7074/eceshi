-- 信用系统数据库迁移脚本
-- 版本: v2
-- 日期: 2024
-- 描述: 添加信用系统相关表和字段

-- =====================================================
-- 1. 创建信用交易记录表
-- =====================================================
CREATE TABLE IF NOT EXISTS credit_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    transaction_type VARCHAR(20) NOT NULL COMMENT '交易类型: consume/repay/refund/grant/adjust',
    amount DECIMAL(10, 2) NOT NULL COMMENT '交易金额',
    balance_before DECIMAL(10, 2) COMMENT '交易前可用额度',
    balance_after DECIMAL(10, 2) COMMENT '交易后可用额度',
    order_id INTEGER COMMENT '关联订单ID',
    order_no VARCHAR(50) COMMENT '订单编号',
    repayment_id INTEGER COMMENT '关联还款记录ID',
    reference_type VARCHAR(50) COMMENT '关联类型',
    reference_id INTEGER COMMENT '关联ID',
    operator_id INTEGER COMMENT '操作人ID',
    status VARCHAR(20) DEFAULT 'success' COMMENT '交易状态',
    description VARCHAR(500) COMMENT '交易描述',
    remark VARCHAR(255) COMMENT '备注',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
CREATE INDEX IF NOT EXISTS idx_credit_records_user_id ON credit_records(user_id);
CREATE INDEX IF NOT EXISTS idx_credit_records_order_id ON credit_records(order_id);

-- =====================================================
-- 2. 创建信用欠款表
-- =====================================================
CREATE TABLE IF NOT EXISTS credit_debts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    order_id INTEGER NOT NULL COMMENT '订单ID',
    order_no VARCHAR(50) COMMENT '订单编号',
    original_amount DECIMAL(10, 2) NOT NULL COMMENT '原始欠款金额',
    paid_amount DECIMAL(10, 2) DEFAULT 0 COMMENT '已还金额',
    remaining_amount DECIMAL(10, 2) NOT NULL COMMENT '剩余欠款',
    status VARCHAR(20) DEFAULT 'unpaid' COMMENT '还款状态: unpaid/partial/paid',
    due_date DATETIME COMMENT '应还日期',
    paid_at DATETIME COMMENT '还清时间',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
CREATE INDEX IF NOT EXISTS idx_credit_debts_user_id ON credit_debts(user_id);
CREATE INDEX IF NOT EXISTS idx_credit_debts_order_id ON credit_debts(order_id);

-- =====================================================
-- 3. 创建还款记录表
-- =====================================================
CREATE TABLE IF NOT EXISTS repayments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    repayment_no VARCHAR(50) UNIQUE COMMENT '还款单号',
    amount DECIMAL(10, 2) NOT NULL COMMENT '还款金额',
    payment_method VARCHAR(20) COMMENT '支付方式',
    debt_ids TEXT COMMENT '关联的欠款ID列表',
    transaction_id VARCHAR(100) COMMENT '第三方支付交易号',
    status VARCHAR(20) DEFAULT 'pending' COMMENT '还款状态',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    paid_at DATETIME COMMENT '支付完成时间',
    FOREIGN KEY (user_id) REFERENCES users(id)
);
CREATE INDEX IF NOT EXISTS idx_repayments_user_id ON repayments(user_id);
CREATE UNIQUE INDEX IF NOT EXISTS idx_repayments_no ON repayments(repayment_no);

-- =====================================================
-- 4. 创建信用额度申请表
-- =====================================================
CREATE TABLE IF NOT EXISTS credit_limit_applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    current_limit DECIMAL(10, 2) COMMENT '当前额度',
    requested_limit DECIMAL(10, 2) COMMENT '申请额度',
    reason TEXT COMMENT '申请理由',
    status VARCHAR(20) DEFAULT 'pending' COMMENT '状态',
    approved_limit DECIMAL(10, 2) COMMENT '批准额度',
    reviewer_id INTEGER COMMENT '审核人ID',
    review_remark VARCHAR(255) COMMENT '审核备注',
    reject_reason VARCHAR(255) COMMENT '拒绝原因',
    reviewed_at DATETIME COMMENT '审核时间',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
CREATE INDEX IF NOT EXISTS idx_credit_limit_applications_user_id ON credit_limit_applications(user_id);

-- =====================================================
-- 5. 更新 user_certification 表（添加新字段）
-- =====================================================
-- 注意: SQLite 不支持 ALTER TABLE ADD COLUMN IF NOT EXISTS
-- 以下语句在 SQLite 中可能需要手动检查

-- 添加基本身份信息字段
ALTER TABLE user_certification ADD COLUMN real_name VARCHAR(50) COMMENT '真实姓名';
ALTER TABLE user_certification ADD COLUMN id_card VARCHAR(20) COMMENT '身份证号';

-- 添加企业/单位信息字段
ALTER TABLE user_certification ADD COLUMN company VARCHAR(100) COMMENT '公司/单位名称';
ALTER TABLE user_certification ADD COLUMN position VARCHAR(50) COMMENT '职位';

-- 添加导师字段（别名）
ALTER TABLE user_certification ADD COLUMN supervisor VARCHAR(50) COMMENT '导师姓名';

-- 添加证件照片字段（别名）
ALTER TABLE user_certification ADD COLUMN student_card VARCHAR(255) COMMENT '学生证/工作证照片';

-- 添加审核人信息
ALTER TABLE user_certification ADD COLUMN reviewer_id INTEGER COMMENT '审核人ID';
ALTER TABLE user_certification ADD COLUMN reviewed_at DATETIME COMMENT '审核时间';

-- =====================================================
-- 6. 确保 users 表有信用相关字段
-- =====================================================
-- 如果不存在则添加
ALTER TABLE users ADD COLUMN credit_limit DECIMAL(10, 2) DEFAULT 0 COMMENT '信用额度';
ALTER TABLE users ADD COLUMN used_credit DECIMAL(10, 2) DEFAULT 0 COMMENT '已用额度';

-- =====================================================
-- 7. 更新 orders 表（添加新字段）
-- =====================================================

-- 添加草稿和开票状态字段
ALTER TABLE orders ADD COLUMN is_draft BOOLEAN DEFAULT 0 COMMENT '是否为草稿';
ALTER TABLE orders ADD COLUMN invoice_status VARCHAR(20) DEFAULT 'none' COMMENT '开票状态';
ALTER TABLE orders ADD COLUMN invoice_id BIGINT COMMENT '关联发票ID';
ALTER TABLE orders ADD COLUMN payment_status VARCHAR(20) DEFAULT 'unpaid' COMMENT '支付状态';
ALTER TABLE orders ADD COLUMN credit_amount DECIMAL(10, 2) DEFAULT 0 COMMENT '信用支付金额';

-- 添加指派信息字段
ALTER TABLE orders ADD COLUMN assigned_lab_id BIGINT COMMENT '指派实验室ID';
ALTER TABLE orders ADD COLUMN assigned_user_id BIGINT COMMENT '指派操作员ID';
ALTER TABLE orders ADD COLUMN assigned_at DATETIME COMMENT '指派时间';

-- 添加索引
CREATE INDEX IF NOT EXISTS idx_orders_is_draft ON orders(is_draft);
CREATE INDEX IF NOT EXISTS idx_orders_invoice_status ON orders(invoice_status);
CREATE INDEX IF NOT EXISTS idx_orders_payment_status ON orders(payment_status);

-- =====================================================
-- 8. 创建实验室表
-- =====================================================
CREATE TABLE IF NOT EXISTS laboratories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL COMMENT '实验室名称',
    code VARCHAR(50) UNIQUE COMMENT '实验室编号',
    lab_type VARCHAR(20) DEFAULT 'third_party' COMMENT '实验室类型: platform/third_party/university',
    status VARCHAR(20) DEFAULT 'pending' COMMENT '状态: pending/approved/rejected/active/suspended/closed',
    institution VARCHAR(200) COMMENT '所属机构',
    address VARCHAR(500) COMMENT '实验室地址',
    province VARCHAR(50) COMMENT '省份',
    city VARCHAR(50) COMMENT '城市',
    district VARCHAR(50) COMMENT '区县',
    contact_name VARCHAR(50) COMMENT '联系人姓名',
    contact_phone VARCHAR(20) COMMENT '联系电话',
    contact_email VARCHAR(100) COMMENT '联系邮箱',
    description TEXT COMMENT '实验室简介',
    qualification_cert VARCHAR(500) COMMENT '资质证书',
    business_license VARCHAR(500) COMMENT '营业执照',
    capabilities TEXT COMMENT '检测能力(JSON)',
    equipment_list TEXT COMMENT '设备清单(JSON)',
    service_areas TEXT COMMENT '服务范围(JSON)',
    commission_rate DECIMAL(5, 2) DEFAULT 15.00 COMMENT '平台佣金比例(%)',
    balance DECIMAL(10, 2) DEFAULT 0 COMMENT '账户余额',
    total_orders INTEGER DEFAULT 0 COMMENT '总订单数',
    completed_orders INTEGER DEFAULT 0 COMMENT '完成订单数',
    average_rating DECIMAL(3, 2) DEFAULT 5.00 COMMENT '平均评分',
    admin_user_id INTEGER COMMENT '管理员用户ID',
    approved_at DATETIME COMMENT '审核通过时间',
    approved_by INTEGER COMMENT '审核人ID',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (admin_user_id) REFERENCES users(id)
);
CREATE INDEX IF NOT EXISTS idx_laboratories_code ON laboratories(code);
CREATE INDEX IF NOT EXISTS idx_laboratories_status ON laboratories(status);
CREATE INDEX IF NOT EXISTS idx_laboratories_lab_type ON laboratories(lab_type);
CREATE INDEX IF NOT EXISTS idx_laboratories_admin_user_id ON laboratories(admin_user_id);

-- =====================================================
-- 9. 创建实验室入驻申请表
-- =====================================================
CREATE TABLE IF NOT EXISTS lab_applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    applicant_id INTEGER NOT NULL COMMENT '申请人用户ID',
    lab_name VARCHAR(100) NOT NULL COMMENT '实验室名称',
    lab_type VARCHAR(20) DEFAULT 'third_party' COMMENT '实验室类型',
    institution VARCHAR(200) COMMENT '所属机构',
    address VARCHAR(500) COMMENT '实验室地址',
    province VARCHAR(50) COMMENT '省份',
    city VARCHAR(50) COMMENT '城市',
    district VARCHAR(50) COMMENT '区县',
    contact_name VARCHAR(50) COMMENT '联系人',
    contact_phone VARCHAR(20) COMMENT '联系电话',
    contact_email VARCHAR(100) COMMENT '联系邮箱',
    description TEXT COMMENT '实验室简介',
    qualification_cert VARCHAR(500) COMMENT '资质证书',
    business_license VARCHAR(500) COMMENT '营业执照',
    capabilities TEXT COMMENT '检测能力(JSON)',
    equipment_list TEXT COMMENT '设备清单(JSON)',
    status VARCHAR(20) DEFAULT 'pending' COMMENT '状态: pending/reviewing/approved/rejected',
    reviewer_id INTEGER COMMENT '审核人ID',
    review_comment VARCHAR(500) COMMENT '审核意见',
    reviewed_at DATETIME COMMENT '审核时间',
    laboratory_id INTEGER COMMENT '创建的实验室ID',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (applicant_id) REFERENCES users(id),
    FOREIGN KEY (laboratory_id) REFERENCES laboratories(id)
);
CREATE INDEX IF NOT EXISTS idx_lab_applications_applicant_id ON lab_applications(applicant_id);
CREATE INDEX IF NOT EXISTS idx_lab_applications_status ON lab_applications(status);

-- =====================================================
-- 10. 创建实验室设备表
-- =====================================================
CREATE TABLE IF NOT EXISTS lab_equipment (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    laboratory_id INTEGER NOT NULL COMMENT '实验室ID',
    name VARCHAR(100) NOT NULL COMMENT '设备名称',
    model VARCHAR(100) COMMENT '设备型号',
    brand VARCHAR(100) COMMENT '品牌厂商',
    serial_number VARCHAR(100) COMMENT '设备序列号',
    category VARCHAR(50) COMMENT '设备类别',
    specifications TEXT COMMENT '技术规格',
    purchase_date DATE COMMENT '购置日期',
    calibration_date DATE COMMENT '最近校准日期',
    next_calibration_date DATE COMMENT '下次校准日期',
    status VARCHAR(20) DEFAULT 'normal' COMMENT '设备状态: normal/maintenance/fault/retired',
    images TEXT COMMENT '设备图片(JSON)',
    remark VARCHAR(500) COMMENT '备注',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (laboratory_id) REFERENCES laboratories(id)
);
CREATE INDEX IF NOT EXISTS idx_lab_equipment_laboratory_id ON lab_equipment(laboratory_id);
CREATE INDEX IF NOT EXISTS idx_lab_equipment_status ON lab_equipment(status);

-- =====================================================
-- 11. 创建实验室人员表
-- =====================================================
CREATE TABLE IF NOT EXISTS lab_staff (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    laboratory_id INTEGER NOT NULL COMMENT '实验室ID',
    user_id INTEGER COMMENT '关联用户ID',
    name VARCHAR(50) NOT NULL COMMENT '姓名',
    phone VARCHAR(20) COMMENT '联系电话',
    email VARCHAR(100) COMMENT '邮箱',
    position VARCHAR(50) COMMENT '职位',
    title VARCHAR(50) COMMENT '职称',
    role VARCHAR(20) DEFAULT 'technician' COMMENT '角色: admin/technician/assistant',
    specialties TEXT COMMENT '专业特长',
    certifications TEXT COMMENT '资质证书(JSON)',
    status VARCHAR(20) DEFAULT 'active' COMMENT '状态: active/inactive',
    joined_at DATE COMMENT '入职日期',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (laboratory_id) REFERENCES laboratories(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
CREATE INDEX IF NOT EXISTS idx_lab_staff_laboratory_id ON lab_staff(laboratory_id);
CREATE INDEX IF NOT EXISTS idx_lab_staff_user_id ON lab_staff(user_id);

-- =====================================================
-- 12. 更新报告表（添加新字段）
-- =====================================================
ALTER TABLE reports ADD COLUMN laboratory_id BIGINT COMMENT '实验室ID';
ALTER TABLE reports ADD COLUMN report_type VARCHAR(50) DEFAULT 'test_report' COMMENT '报告类型';
ALTER TABLE reports ADD COLUMN file_name VARCHAR(200) COMMENT '文件名称';
ALTER TABLE reports ADD COLUMN file_format VARCHAR(20) COMMENT '文件格式';
ALTER TABLE reports ADD COLUMN uploader_id INTEGER COMMENT '上传人ID';
ALTER TABLE reports ADD COLUMN verifier_id INTEGER COMMENT '审核人ID';
ALTER TABLE reports ADD COLUMN verified_at DATETIME COMMENT '审核时间';
ALTER TABLE reports ADD COLUMN remark TEXT COMMENT '备注';

CREATE INDEX IF NOT EXISTS idx_reports_laboratory_id ON reports(laboratory_id);
CREATE INDEX IF NOT EXISTS idx_reports_report_type ON reports(report_type);

-- =====================================================
-- 13. 创建角色表
-- =====================================================
CREATE TABLE IF NOT EXISTS roles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) NOT NULL UNIQUE COMMENT '角色名称',
    code VARCHAR(50) NOT NULL UNIQUE COMMENT '角色编码',
    description VARCHAR(255) COMMENT '角色描述',
    is_system BOOLEAN DEFAULT 0 COMMENT '是否系统内置角色',
    is_active BOOLEAN DEFAULT 1 COMMENT '是否启用',
    sort_order INTEGER DEFAULT 0 COMMENT '排序',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_roles_code ON roles(code);

-- =====================================================
-- 14. 创建权限表
-- =====================================================
CREATE TABLE IF NOT EXISTS permissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL COMMENT '权限名称',
    code VARCHAR(100) NOT NULL UNIQUE COMMENT '权限编码',
    module VARCHAR(50) COMMENT '所属模块',
    description VARCHAR(255) COMMENT '权限描述',
    is_active BOOLEAN DEFAULT 1 COMMENT '是否启用',
    sort_order INTEGER DEFAULT 0 COMMENT '排序',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_permissions_code ON permissions(code);
CREATE INDEX IF NOT EXISTS idx_permissions_module ON permissions(module);

-- =====================================================
-- 15. 创建角色-权限关联表
-- =====================================================
CREATE TABLE IF NOT EXISTS role_permissions (
    role_id INTEGER NOT NULL,
    permission_id INTEGER NOT NULL,
    PRIMARY KEY (role_id, permission_id),
    FOREIGN KEY (role_id) REFERENCES roles(id),
    FOREIGN KEY (permission_id) REFERENCES permissions(id)
);

-- =====================================================
-- 16. 创建用户-角色关联表
-- =====================================================
CREATE TABLE IF NOT EXISTS user_roles (
    user_id INTEGER NOT NULL,
    role_id INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, role_id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (role_id) REFERENCES roles(id)
);

-- =====================================================
-- 17. 更新用户表（添加is_admin字段）
-- =====================================================
ALTER TABLE users ADD COLUMN is_admin BOOLEAN DEFAULT 0 COMMENT '是否管理员';

-- =====================================================
-- 说明
-- =====================================================
-- 1. 此脚本适用于 SQLite 数据库
-- 2. 对于 MySQL，请将 AUTOINCREMENT 改为 AUTO_INCREMENT
-- 3. 对于 PostgreSQL，请使用 SERIAL 代替 INTEGER PRIMARY KEY AUTOINCREMENT
-- 4. ALTER TABLE 语句在字段已存在时会报错，可以忽略这些错误
-- 5. 建议在执行前备份数据库

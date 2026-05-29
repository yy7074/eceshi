"""
订单相关模型
"""
from sqlalchemy import Column, BigInteger, String, Integer, DateTime, Boolean, Text, JSON, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Order(Base):
    """订单主表"""
    __tablename__ = "orders"
    
    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    order_no = Column(String(32), unique=True, nullable=False, comment="订单号")
    user_id = Column(BigInteger, nullable=False, index=True, comment="用户ID")
    project_id = Column(BigInteger, nullable=False, comment="项目ID")
    project_name = Column(String(200), nullable=False, comment="项目名称")
    lab_id = Column(BigInteger, nullable=False, index=True, comment="实验室ID")
    lab_name = Column(String(200), nullable=False, comment="实验室名称")
    
    # 订单状态
    status = Column(String(20), nullable=False, index=True, default="pending_payment", comment="订单状态")
    is_draft = Column(Boolean, default=False, index=True, comment="是否为草稿")

    # 开票状态
    invoice_status = Column(String(20), default="none", index=True, comment="开票状态: none/requested/processing/issued/rejected")
    invoice_id = Column(BigInteger, comment="关联发票ID")

    # 支付状态（独立于订单状态）
    payment_status = Column(String(20), default="unpaid", index=True, comment="支付状态: unpaid/partial/paid")
    credit_amount = Column(Numeric(10, 2), default=0, comment="信用支付金额")
    payment_source = Column(String(30), comment="资金来源: prepaid/credit/mixed/wechat/alipay")
    repayment_status = Column(String(20), default="not_required", index=True, comment="还款状态: not_required/pending/partial/paid")
    repayment_method = Column(String(30), comment="还款方式: wechat/alipay/transfer/prepaid/other")
    repayment_amount = Column(Numeric(10, 2), default=0, comment="已登记还款金额")
    repayment_time = Column(DateTime, comment="最近还款登记时间")
    repayment_records = Column(JSON, comment="还款记录明细")

    # 对接销售/老师
    sales_id = Column(BigInteger, comment="对接销售/老师ID")
    sales_name = Column(String(50), comment="对接销售/老师姓名")
    sales_phone = Column(String(20), comment="对接销售/老师电话")

    # 指派信息
    assigned_lab_id = Column(BigInteger, comment="指派实验室ID")
    assigned_user_id = Column(BigInteger, comment="指派操作员ID")
    assigned_at = Column(DateTime, comment="指派时间")
    assigned_staff_id = Column(BigInteger, comment="指派实验人员ID")
    assigned_staff_name = Column(String(50), comment="指派实验人员姓名")

    # 费用信息
    project_fee = Column(Numeric(10, 2), nullable=False, comment="项目费用")
    urgent_fee = Column(Numeric(10, 2), default=0, comment="加急费用")
    shipping_fee = Column(Numeric(10, 2), default=0, comment="运费")
    discount_amount = Column(Numeric(10, 2), default=0, comment="优惠金额")
    total_fee = Column(Numeric(10, 2), nullable=False, comment="总金额")
    paid_fee = Column(Numeric(10, 2), default=0, comment="已支付金额")
    
    # 样品数量
    sample_count = Column(Integer, default=1, comment="样品数量")
    
    # 配送信息
    shipping_method = Column(String(20), comment="配送方式")
    receiver_name = Column(String(50), comment="收件人")
    receiver_phone = Column(String(20), comment="收件人电话")
    receiver_address = Column(String(500), comment="收件地址")
    
    # 支付信息
    payment_method = Column(String(20), comment="支付方式")
    payment_time = Column(DateTime, comment="支付时间")

    # 订单相关文件
    report_url = Column(String(500), comment="测试报告文件链接")
    checklist_url = Column(String(500), comment="测试清单文件链接")
    invoice_file_url = Column(String(500), comment="订单发票文件链接")
    
    # 时间信息
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    paid_at = Column(DateTime, comment="支付时间")
    confirmed_at = Column(DateTime, comment="确认时间")
    started_at = Column(DateTime, comment="开始实验时间")
    completed_at = Column(DateTime, comment="完成时间")
    cancelled_at = Column(DateTime, comment="取消时间")
    
    # 备注
    remark = Column(Text, comment="用户备注")
    admin_test_requirements = Column(Text, comment="后台修改后的测试条件/要求")
    admin_notes_to_lab = Column(Text, comment="后台给实验室的备注事项")
    cancel_reason = Column(String(200), comment="取消原因")
    
    # 是否加急
    is_urgent = Column(Boolean, default=False, comment="是否加急")
    
    # 预计完成时间
    estimated_completion_time = Column(DateTime, comment="预计完成时间")
    
    # 关系
    user = relationship("User", foreign_keys=[user_id], primaryjoin="Order.user_id == User.id")
    project = relationship("Project", foreign_keys=[project_id], primaryjoin="Order.project_id == Project.id")


class OrderSample(Base):
    """订单样品表"""
    __tablename__ = "order_samples"
    
    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    order_id = Column(BigInteger, nullable=False, index=True, comment="订单ID")
    
    # 样品信息
    sample_name = Column(String(100), nullable=False, comment="样品名称")
    sample_type = Column(String(50), comment="样品类型")
    sample_desc = Column(Text, comment="样品描述")
    quantity = Column(Integer, default=1, comment="样品数量")
    photos = Column(JSON, comment="样品照片")
    
    # 检测参数
    test_params = Column(JSON, comment="检测参数")
    special_requirements = Column(Text, comment="特殊要求")
    
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")


class OrderFee(Base):
    """订单费用明细表"""
    __tablename__ = "order_fees"
    
    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    order_id = Column(BigInteger, nullable=False, index=True, comment="订单ID")
    
    fee_type = Column(String(20), nullable=False, comment="费用类型")
    fee_name = Column(String(50), nullable=False, comment="费用名称")
    amount = Column(Numeric(10, 2), nullable=False, comment="金额")
    remark = Column(String(200), comment="备注")
    
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")


class OrderStatusHistory(Base):
    """订单状态流转表"""
    __tablename__ = "order_status_history"
    
    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    order_id = Column(BigInteger, nullable=False, index=True, comment="订单ID")
    
    from_status = Column(String(20), comment="原状态")
    to_status = Column(String(20), nullable=False, comment="新状态")
    
    operator_id = Column(BigInteger, comment="操作人ID")
    operator_type = Column(String(20), comment="操作人类型")
    remark = Column(String(200), comment="备注")
    
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")


class Payment(Base):
    """支付记录表"""
    __tablename__ = "payments"
    
    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    payment_no = Column(String(32), unique=True, nullable=False, comment="支付单号")
    order_id = Column(BigInteger, nullable=False, index=True, comment="订单ID")
    order_no = Column(String(32), nullable=False, comment="订单号")
    user_id = Column(BigInteger, nullable=False, index=True, comment="用户ID")
    
    # 支付信息
    payment_method = Column(String(20), nullable=False, comment="支付方式")
    payment_channel = Column(String(20), comment="支付渠道")
    amount = Column(Numeric(10, 2), nullable=False, comment="支付金额")
    
    # 状态
    status = Column(String(20), nullable=False, default="pending", comment="支付状态")
    trade_no = Column(String(64), index=True, comment="第三方交易号")
    
    # 时间
    paid_at = Column(DateTime, comment="支付时间")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")


class UserAddress(Base):
    """用户地址表"""
    __tablename__ = "user_addresses"
    
    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    user_id = Column(BigInteger, nullable=False, index=True, comment="用户ID")
    
    # 收货信息
    receiver_name = Column(String(50), nullable=False, comment="收件人")
    phone = Column(String(20), nullable=False, comment="手机号")
    province = Column(String(50), nullable=False, comment="省")
    city = Column(String(50), nullable=False, comment="市")
    district = Column(String(50), comment="区")
    detail_address = Column(String(200), nullable=False, comment="详细地址")
    
    # 是否默认
    is_default = Column(Boolean, default=False, comment="是否默认")
    
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, onupdate=func.now(), comment="更新时间")

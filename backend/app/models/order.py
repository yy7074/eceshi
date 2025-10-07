"""
订单相关模型
"""
from sqlalchemy import Column, BigInteger, String, Integer, DateTime, Boolean, Text, JSON, Numeric
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
    
    # 时间信息
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    paid_at = Column(DateTime, comment="支付时间")
    confirmed_at = Column(DateTime, comment="确认时间")
    started_at = Column(DateTime, comment="开始实验时间")
    completed_at = Column(DateTime, comment="完成时间")
    cancelled_at = Column(DateTime, comment="取消时间")
    
    # 备注
    remark = Column(Text, comment="用户备注")
    cancel_reason = Column(String(200), comment="取消原因")
    
    # 是否加急
    is_urgent = Column(Boolean, default=False, comment="是否加急")
    
    # 预计完成时间
    estimated_completion_time = Column(DateTime, comment="预计完成时间")


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


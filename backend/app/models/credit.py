"""
信用系统模型
信用记录、欠款管理
"""
from sqlalchemy import Column, Integer, String, DateTime, Enum, Numeric, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum

from app.core.database import Base


class CreditTransactionType(enum.Enum):
    """信用交易类型"""
    CONSUME = "consume"  # 信用消费（下单）
    REPAY = "repay"  # 还款
    REFUND = "refund"  # 退款（订单取消退回额度）
    GRANT = "grant"  # 授予额度（认证通过）
    ADJUST = "adjust"  # 额度调整（管理员调整）


class CreditTransactionStatus(enum.Enum):
    """交易状态"""
    PENDING = "pending"  # 待处理
    SUCCESS = "success"  # 成功
    FAILED = "failed"  # 失败


class RepaymentStatus(enum.Enum):
    """还款状态"""
    UNPAID = "unpaid"  # 未还款
    PARTIAL = "partial"  # 部分还款
    PAID = "paid"  # 已还清


class CreditRecord(Base):
    """信用交易记录表"""
    __tablename__ = "credit_records"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True, comment="用户ID")

    # 交易信息
    transaction_type = Column(
        Enum(CreditTransactionType),
        nullable=False,
        comment="交易类型"
    )
    amount = Column(Numeric(10, 2), nullable=False, comment="交易金额")
    balance_before = Column(Numeric(10, 2), comment="交易前可用额度")
    balance_after = Column(Numeric(10, 2), comment="交易后可用额度")

    # 关联信息
    order_id = Column(Integer, index=True, comment="关联订单ID")
    order_no = Column(String(50), comment="订单编号")
    repayment_id = Column(Integer, index=True, comment="关联还款记录ID")
    reference_type = Column(String(50), comment="关联类型: certification/limit_application/admin_adjustment")
    reference_id = Column(Integer, comment="关联ID")
    operator_id = Column(Integer, comment="操作人ID（管理员）")

    # 状态
    status = Column(
        Enum(CreditTransactionStatus),
        default=CreditTransactionStatus.SUCCESS,
        comment="交易状态"
    )

    # 描述和备注
    description = Column(String(500), comment="交易描述")
    remark = Column(String(255), comment="备注")

    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class CreditDebt(Base):
    """信用欠款表（记录每笔信用消费的欠款）"""
    __tablename__ = "credit_debts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True, comment="用户ID")

    # 关系
    user = relationship("User", backref="credit_debts")

    # 欠款信息
    order_id = Column(Integer, nullable=False, index=True, comment="订单ID")
    order_no = Column(String(50), comment="订单编号")
    original_amount = Column(Numeric(10, 2), nullable=False, comment="原始欠款金额")
    paid_amount = Column(Numeric(10, 2), default=0, comment="已还金额")
    remaining_amount = Column(Numeric(10, 2), nullable=False, comment="剩余欠款")

    # 状态
    status = Column(
        Enum(RepaymentStatus),
        default=RepaymentStatus.UNPAID,
        comment="还款状态"
    )

    # 时间
    due_date = Column(DateTime(timezone=True), comment="应还日期")
    paid_at = Column(DateTime(timezone=True), comment="还清时间")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class Repayment(Base):
    """还款记录表"""
    __tablename__ = "repayments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True, comment="用户ID")

    # 还款信息
    repayment_no = Column(String(50), unique=True, index=True, comment="还款单号")
    amount = Column(Numeric(10, 2), nullable=False, comment="还款金额")
    payment_method = Column(String(20), comment="支付方式: wechat/alipay/balance/transfer")

    # 关联的欠款
    debt_ids = Column(Text, comment="关联的欠款ID列表，JSON格式")

    # 支付信息
    transaction_id = Column(String(100), comment="第三方支付交易号")

    # 状态
    status = Column(
        Enum(CreditTransactionStatus),
        default=CreditTransactionStatus.PENDING,
        comment="还款状态"
    )

    # 时间
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    paid_at = Column(DateTime(timezone=True), comment="支付完成时间")


class CreditLimitApplication(Base):
    """信用额度提升申请表"""
    __tablename__ = "credit_limit_applications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True, comment="用户ID")

    # 关系
    user = relationship("User", backref="credit_limit_applications")

    # 申请信息
    current_limit = Column(Numeric(10, 2), comment="当前额度")
    requested_limit = Column(Numeric(10, 2), comment="申请额度")
    reason = Column(Text, comment="申请理由")

    # 审核信息
    status = Column(String(20), default="pending", comment="状态: pending/approved/rejected")
    approved_limit = Column(Numeric(10, 2), comment="批准额度")
    reviewer_id = Column(Integer, comment="审核人ID")
    review_remark = Column(String(255), comment="审核备注")
    reject_reason = Column(String(255), comment="拒绝原因")
    reviewed_at = Column(DateTime(timezone=True), comment="审核时间")

    # 时间
    created_at = Column(DateTime(timezone=True), server_default=func.now())

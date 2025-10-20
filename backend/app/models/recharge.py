"""
钱包充值模型
"""
from sqlalchemy import Column, Integer, String, DateTime, Numeric, Enum
from sqlalchemy.sql import func
import enum

from app.core.database import Base


class RechargeStatus(enum.Enum):
    """充值状态"""
    PENDING = "pending"  # 待支付
    SUCCESS = "success"  # 充值成功
    FAILED = "failed"  # 充值失败
    REFUNDED = "refunded"  # 已退款


class RechargeMethod(enum.Enum):
    """充值方式"""
    WECHAT = "wechat"  # 微信支付
    ALIPAY = "alipay"  # 支付宝


class RechargeRecord(Base):
    """充值记录表"""
    __tablename__ = "recharge_records"
    
    id = Column(Integer, primary_key=True, index=True, comment="充值记录ID")
    user_id = Column(Integer, nullable=False, index=True, comment="用户ID")
    
    # 充值信息
    recharge_no = Column(String(64), unique=True, index=True, comment="充值单号")
    amount = Column(Numeric(10, 2), nullable=False, comment="充值金额")
    actual_amount = Column(Numeric(10, 2), comment="实际到账金额（含赠送）")
    bonus_amount = Column(Numeric(10, 2), default=0, comment="赠送金额")
    
    # 支付信息
    payment_method = Column(Enum(RechargeMethod), nullable=False, comment="支付方式")
    payment_no = Column(String(64), comment="支付单号")
    transaction_id = Column(String(128), comment="第三方交易号")
    
    # 状态
    status = Column(
        Enum(RechargeStatus),
        default=RechargeStatus.PENDING,
        comment="充值状态"
    )
    
    # 备注
    remark = Column(String(255), comment="备注")
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    paid_at = Column(DateTime(timezone=True), comment="支付时间")
    completed_at = Column(DateTime(timezone=True), comment="完成时间")
    
    def __repr__(self):
        return f"<RechargeRecord {self.recharge_no}>"


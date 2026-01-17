"""
佣金设置相关模型
支持根据不同客户设置佣金比例
"""
from sqlalchemy import Column, BigInteger, String, Date, DateTime, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class UserCommissionSetting(Base):
    """
    客户佣金设置表
    用于为不同客户设置不同的佣金比例
    """
    __tablename__ = "user_commission_settings"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)

    # 用户关联
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False, unique=True, index=True, comment="用户ID")

    # 佣金配置
    commission_rate = Column(Numeric(5, 2), default=0, comment="佣金比例（%）")
    max_rate = Column(Numeric(5, 2), default=12.00, comment="最大比例（%）")

    # 生效时间
    effective_from = Column(Date, comment="生效日期")
    effective_to = Column(Date, comment="失效日期")

    # 审核信息
    created_by = Column(BigInteger, ForeignKey("users.id"), comment="设置人")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, onupdate=func.now(), comment="更新时间")

    # 关系
    user = relationship("User", foreign_keys=[user_id], backref="commission_setting")
    creator = relationship("User", foreign_keys=[created_by])


class CommissionRecord(Base):
    """
    佣金记录表
    记录每笔订单产生的佣金
    """
    __tablename__ = "commission_records"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)

    # 关联
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False, index=True, comment="获得佣金的用户ID")
    order_id = Column(BigInteger, ForeignKey("orders.id"), nullable=False, index=True, comment="订单ID")
    from_user_id = Column(BigInteger, ForeignKey("users.id"), comment="下单用户ID（被邀请人）")

    # 金额信息
    order_amount = Column(Numeric(10, 2), comment="订单金额")
    commission_rate = Column(Numeric(5, 2), comment="佣金比例")
    commission_amount = Column(Numeric(10, 2), comment="佣金金额")

    # 状态: pending-待结算, settled-已结算, cancelled-已取消
    status = Column(String(20), default="pending", comment="状态")
    settled_at = Column(DateTime, comment="结算时间")

    # 时间戳
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")

    # 关系
    user = relationship("User", foreign_keys=[user_id], backref="commission_records")
    order = relationship("Order", backref="commission_record")
    from_user = relationship("User", foreign_keys=[from_user_id])

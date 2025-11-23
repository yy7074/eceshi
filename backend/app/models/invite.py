"""
邀请返利模型
"""
from sqlalchemy import Column, Integer, String, DateTime, Enum, Numeric, Text
from sqlalchemy.sql import func
import enum

from app.core.database import Base


class InviteStatus(enum.Enum):
    """邀请状态"""
    PENDING = "pending"  # 待完成（被邀请人未消费）
    COMPLETED = "completed"  # 已完成（奖励已发放）
    WITHDRAWN = "withdrawn"  # 已提现


class WithdrawStatus(enum.Enum):
    """提现状态"""
    PENDING = "pending"  # 待审核
    APPROVED = "approved"  # 已通过
    REJECTED = "rejected"  # 已拒绝
    COMPLETED = "completed"  # 已完成


class InviteRecord(Base):
    """邀请记录表"""
    __tablename__ = "invite_records"
    
    id = Column(Integer, primary_key=True, index=True, comment="邀请记录ID")
    inviter_id = Column(Integer, nullable=False, index=True, comment="邀请人用户ID")
    invitee_id = Column(Integer, nullable=False, index=True, comment="被邀请人用户ID")
    
    # 邀请人信息
    inviter_name = Column(String(50), comment="邀请人昵称")
    inviter_phone = Column(String(20), comment="邀请人手机号")
    
    # 被邀请人信息
    invitee_name = Column(String(50), comment="被邀请人昵称")
    invitee_phone = Column(String(20), comment="被邀请人手机号")
    
    # 奖励信息
    reward_amount = Column(Numeric(10, 2), default=0, comment="奖励金额")
    reward_type = Column(String(20), default="balance", comment="奖励类型：balance/points")
    
    # 状态
    status = Column(Enum(InviteStatus), default=InviteStatus.PENDING, comment="邀请状态")
    
    # 完成信息
    first_order_id = Column(Integer, comment="被邀请人首单ID")
    first_order_amount = Column(Numeric(10, 2), comment="首单金额")
    completed_at = Column(DateTime(timezone=True), comment="完成时间")
    
    # 时间
    invited_at = Column(DateTime(timezone=True), server_default=func.now(), comment="邀请时间")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")
    
    def __repr__(self):
        return f"<InviteRecord inviter_id={self.inviter_id} invitee_id={self.invitee_id}>"


class WithdrawRecord(Base):
    """提现记录表"""
    __tablename__ = "withdraw_records"
    
    id = Column(Integer, primary_key=True, index=True, comment="提现记录ID")
    user_id = Column(Integer, nullable=False, index=True, comment="用户ID")
    
    # 提现信息
    amount = Column(Numeric(10, 2), nullable=False, comment="提现金额")
    withdraw_type = Column(String(20), default="invite_reward", comment="提现类型")
    
    # 账户信息
    account_type = Column(String(20), comment="账户类型：alipay/wechat/bank")
    account_name = Column(String(50), comment="账户名")
    account_number = Column(String(100), comment="账户号码")
    
    # 状态
    status = Column(Enum(WithdrawStatus), default=WithdrawStatus.PENDING, comment="提现状态")
    reject_reason = Column(Text, comment="拒绝原因")
    
    # 审核信息
    reviewer_id = Column(Integer, comment="审核人ID")
    reviewed_at = Column(DateTime(timezone=True), comment="审核时间")
    
    # 完成信息
    transaction_no = Column(String(100), comment="交易单号")
    completed_at = Column(DateTime(timezone=True), comment="完成时间")
    
    # 时间
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")
    
    def __repr__(self):
        return f"<WithdrawRecord user_id={self.user_id} amount={self.amount}>"


class InviteConfig(Base):
    """邀请配置表"""
    __tablename__ = "invite_config"
    
    id = Column(Integer, primary_key=True, index=True, comment="配置ID")
    
    # 奖励配置
    inviter_reward = Column(Numeric(10, 2), default=10, comment="邀请人奖励金额")
    invitee_reward = Column(Numeric(10, 2), default=5, comment="被邀请人奖励金额")
    reward_type = Column(String(20), default="balance", comment="奖励类型")
    
    # 条件配置
    min_order_amount = Column(Numeric(10, 2), default=0, comment="最低订单金额要求")
    reward_delay_days = Column(Integer, default=0, comment="奖励延迟天数")
    
    # 提现配置
    min_withdraw_amount = Column(Numeric(10, 2), default=10, comment="最低提现金额")
    withdraw_fee_rate = Column(Numeric(5, 4), default=0, comment="提现手续费率")
    
    # 状态
    is_active = Column(Integer, default=1, comment="是否启用")
    
    # 时间
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")
    
    def __repr__(self):
        return f"<InviteConfig id={self.id}>"

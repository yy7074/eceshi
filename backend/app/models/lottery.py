"""
抽奖系统模型
"""
from sqlalchemy import Column, Integer, String, DateTime, Enum, Numeric, Text, BigInteger, Boolean
from sqlalchemy.sql import func
import enum

from app.core.database import Base


class PrizeType(enum.Enum):
    """奖品类型"""
    COUPON = "coupon"  # 优惠券
    CASH = "cash"  # 现金红包
    POINTS = "points"  # 积分
    GIFT = "gift"  # 实物礼品
    EMPTY = "empty"  # 谢谢参与


class PrizeStatus(enum.Enum):
    """奖品领取状态"""
    UNCLAIMED = "unclaimed"  # 未领取
    CLAIMED = "claimed"  # 已领取
    EXPIRED = "expired"  # 已过期


class LotteryPrize(Base):
    """抽奖奖品配置表"""
    __tablename__ = "lottery_prizes"
    
    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    
    # 奖品信息
    name = Column(String(100), nullable=False, comment="奖品名称")
    prize_type = Column(Enum(PrizeType), nullable=False, comment="奖品类型")
    icon = Column(String(50), default="🎁", comment="奖品图标")
    
    # 奖品价值
    value = Column(Numeric(10, 2), default=0, comment="奖品价值")
    coupon_id = Column(BigInteger, comment="关联优惠券ID")
    points_amount = Column(Integer, comment="积分数量")
    
    # 概率配置
    probability = Column(Integer, default=0, comment="中奖概率（万分比）")
    daily_limit = Column(Integer, default=0, comment="每日限量（0表示不限）")
    total_limit = Column(Integer, default=0, comment="总限量（0表示不限）")
    issued_count = Column(Integer, default=0, comment="已发放数量")
    
    # 状态
    is_active = Column(Boolean, default=True, comment="是否启用")
    sort_order = Column(Integer, default=0, comment="排序")
    
    # 时间
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")
    
    def __repr__(self):
        return f"<LotteryPrize {self.name}>"


class LotteryRecord(Base):
    """抽奖记录表"""
    __tablename__ = "lottery_records"
    
    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    user_id = Column(BigInteger, nullable=False, index=True, comment="用户ID")
    prize_id = Column(BigInteger, nullable=False, comment="奖品ID")
    
    # 奖品信息快照
    prize_name = Column(String(100), comment="奖品名称")
    prize_type = Column(String(20), comment="奖品类型")
    prize_value = Column(Numeric(10, 2), comment="奖品价值")
    prize_icon = Column(String(50), comment="奖品图标")
    
    # 领取状态
    status = Column(Enum(PrizeStatus), default=PrizeStatus.UNCLAIMED, comment="领取状态")
    claimed_at = Column(DateTime(timezone=True), comment="领取时间")
    expire_at = Column(DateTime(timezone=True), comment="过期时间")
    
    # 关联信息
    coupon_id = Column(BigInteger, comment="发放的优惠券ID")
    order_id = Column(BigInteger, comment="关联的订单ID（获得抽奖机会的订单）")
    
    # 时间
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="中奖时间")
    
    def __repr__(self):
        return f"<LotteryRecord user_id={self.user_id} prize={self.prize_name}>"


class LotteryChance(Base):
    """抽奖机会表"""
    __tablename__ = "lottery_chances"
    
    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    user_id = Column(BigInteger, nullable=False, index=True, comment="用户ID")
    
    # 机会来源
    source_type = Column(String(20), nullable=False, comment="来源类型: order/signin/invite/activity")
    source_id = Column(BigInteger, comment="来源ID（订单ID等）")
    
    # 状态
    is_used = Column(Boolean, default=False, comment="是否已使用")
    used_at = Column(DateTime(timezone=True), comment="使用时间")
    record_id = Column(BigInteger, comment="使用后的抽奖记录ID")
    
    # 有效期
    expire_at = Column(DateTime(timezone=True), comment="过期时间")
    
    # 时间
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="获得时间")
    
    def __repr__(self):
        return f"<LotteryChance user_id={self.user_id}>"


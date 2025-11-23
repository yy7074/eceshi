"""
优惠券模型
"""
from sqlalchemy import Column, Integer, String, DateTime, Enum, Numeric, Boolean, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum

from app.core.database import Base


class CouponType(enum.Enum):
    """优惠券类型"""
    DISCOUNT = "discount"  # 折扣券
    CASH = "cash"  # 代金券
    FULL_REDUCTION = "full_reduction"  # 满减券


class CouponStatus(enum.Enum):
    """优惠券状态"""
    ACTIVE = "active"  # 可领取
    INACTIVE = "inactive"  # 已下架
    EXPIRED = "expired"  # 已过期


class UserCouponStatus(enum.Enum):
    """用户优惠券状态"""
    UNUSED = "unused"  # 未使用
    USED = "used"  # 已使用
    EXPIRED = "expired"  # 已过期


class Coupon(Base):
    """优惠券模板表"""
    __tablename__ = "coupons"
    
    id = Column(Integer, primary_key=True, index=True, comment="优惠券ID")
    name = Column(String(100), nullable=False, comment="优惠券名称")
    description = Column(Text, comment="优惠券描述")
    
    # 优惠券类型和金额
    type = Column(Enum(CouponType), nullable=False, comment="优惠券类型")
    discount_rate = Column(Numeric(5, 2), comment="折扣率（如0.9表示9折）")
    cash_amount = Column(Numeric(10, 2), comment="代金券金额")
    full_amount = Column(Numeric(10, 2), comment="满减门槛金额")
    reduction_amount = Column(Numeric(10, 2), comment="满减优惠金额")
    
    # 使用限制
    min_order_amount = Column(Numeric(10, 2), default=0, comment="最低订单金额")
    max_discount_amount = Column(Numeric(10, 2), comment="最大优惠金额")
    
    # 发放和有效期
    total_quantity = Column(Integer, default=0, comment="发行总量（0表示不限量）")
    received_quantity = Column(Integer, default=0, comment="已领取数量")
    valid_days = Column(Integer, default=30, comment="有效天数")
    
    # 适用范围
    applicable_projects = Column(Text, comment="适用项目ID列表（JSON格式）")
    applicable_categories = Column(Text, comment="适用分类ID列表（JSON格式）")
    
    # 状态
    status = Column(Enum(CouponStatus), default=CouponStatus.ACTIVE, comment="优惠券状态")
    
    # 时间
    start_time = Column(DateTime(timezone=True), comment="开始时间")
    end_time = Column(DateTime(timezone=True), comment="结束时间")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")
    
    def __repr__(self):
        return f"<Coupon {self.name}>"


class UserCoupon(Base):
    """用户优惠券表"""
    __tablename__ = "user_coupons"
    
    id = Column(Integer, primary_key=True, index=True, comment="用户优惠券ID")
    user_id = Column(Integer, nullable=False, index=True, comment="用户ID")
    coupon_id = Column(Integer, nullable=False, index=True, comment="优惠券ID")
    
    # 优惠券信息快照
    coupon_name = Column(String(100), comment="优惠券名称")
    coupon_type = Column(String(20), comment="优惠券类型")
    discount_value = Column(Numeric(10, 2), comment="优惠值")
    
    # 使用情况
    status = Column(Enum(UserCouponStatus), default=UserCouponStatus.UNUSED, comment="使用状态")
    order_id = Column(Integer, comment="使用的订单ID")
    used_at = Column(DateTime(timezone=True), comment="使用时间")
    
    # 有效期
    received_at = Column(DateTime(timezone=True), server_default=func.now(), comment="领取时间")
    expire_at = Column(DateTime(timezone=True), nullable=False, comment="过期时间")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")
    
    def __repr__(self):
        return f"<UserCoupon user_id={self.user_id} coupon_id={self.coupon_id}>"

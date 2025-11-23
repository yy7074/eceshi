"""
优惠券相关Schema
"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from decimal import Decimal


class CouponBase(BaseModel):
    """优惠券基础信息"""
    name: str
    description: Optional[str] = None
    type: str  # discount/cash/full_reduction
    discount_rate: Optional[Decimal] = None
    cash_amount: Optional[Decimal] = None
    full_amount: Optional[Decimal] = None
    reduction_amount: Optional[Decimal] = None
    min_order_amount: Decimal = Decimal("0")
    max_discount_amount: Optional[Decimal] = None


class CouponInDB(CouponBase):
    """数据库中的优惠券"""
    id: int
    total_quantity: int
    received_quantity: int
    valid_days: int
    status: str
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class UserCouponItem(BaseModel):
    """用户优惠券列表项"""
    id: int
    coupon_id: int
    coupon_name: str
    coupon_type: str
    discount_value: Decimal
    status: str
    received_at: datetime
    expire_at: datetime
    order_id: Optional[int] = None
    used_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class CouponReceiveRequest(BaseModel):
    """领取优惠券请求"""
    coupon_id: int


class CouponListResponse(BaseModel):
    """优惠券列表响应"""
    items: List[CouponInDB]
    total: int


class UserCouponListResponse(BaseModel):
    """用户优惠券列表响应"""
    items: List[UserCouponItem]
    total: int

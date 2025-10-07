"""
订单相关Schema
"""
from typing import Optional, List, Any
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field


# ==================== 订单样品 ====================

class OrderSampleCreate(BaseModel):
    """创建订单样品"""
    sample_name: str = Field(..., description="样品名称")
    sample_type: Optional[str] = Field(None, description="样品类型")
    sample_desc: Optional[str] = Field(None, description="样品描述")
    quantity: int = Field(1, description="样品数量")
    photos: Optional[List[str]] = Field(None, description="样品照片")
    test_params: Optional[dict] = Field(None, description="检测参数")
    special_requirements: Optional[str] = Field(None, description="特殊要求")


class OrderSampleInDB(OrderSampleCreate):
    """数据库中的订单样品"""
    id: int
    order_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# ==================== 订单创建 ====================

class OrderCreate(BaseModel):
    """创建订单"""
    project_id: int = Field(..., description="项目ID")
    samples: List[OrderSampleCreate] = Field(..., description="样品列表")
    
    # 配送信息
    shipping_method: str = Field(..., description="配送方式: self|express|platform")
    address_id: Optional[int] = Field(None, description="地址ID（快递寄送时必填）")
    
    # 优惠信息
    coupon_id: Optional[int] = Field(None, description="优惠券ID")
    use_points: int = Field(0, description="使用积分")
    
    # 其他
    is_urgent: bool = Field(False, description="是否加急")
    remark: Optional[str] = Field(None, description="备注")


class OrderCalculate(BaseModel):
    """计算订单费用"""
    project_id: int = Field(..., description="项目ID")
    sample_count: int = Field(1, description="样品数量")
    is_urgent: bool = Field(False, description="是否加急")
    shipping_method: str = Field(..., description="配送方式")
    coupon_id: Optional[int] = Field(None, description="优惠券ID")
    use_points: int = Field(0, description="使用积分")


class OrderFeeDetail(BaseModel):
    """费用明细"""
    fee_type: str = Field(..., description="费用类型")
    fee_name: str = Field(..., description="费用名称")
    amount: Decimal = Field(..., description="金额")


class OrderCalculateResponse(BaseModel):
    """订单费用计算结果"""
    project_fee: Decimal = Field(..., description="项目费用")
    urgent_fee: Decimal = Field(0, description="加急费用")
    shipping_fee: Decimal = Field(0, description="运费")
    discount_amount: Decimal = Field(0, description="优惠金额")
    total_fee: Decimal = Field(..., description="总金额")
    fee_details: List[OrderFeeDetail] = Field([], description="费用明细")


# ==================== 订单信息 ====================

class OrderInDB(BaseModel):
    """数据库中的订单"""
    id: int
    order_no: str
    user_id: int
    project_id: int
    project_name: str
    lab_id: int
    lab_name: str
    status: str
    
    # 费用
    project_fee: Decimal
    urgent_fee: Decimal
    shipping_fee: Decimal
    discount_amount: Decimal
    total_fee: Decimal
    paid_fee: Decimal
    
    # 样品
    sample_count: int
    
    # 配送
    shipping_method: Optional[str]
    receiver_name: Optional[str]
    receiver_phone: Optional[str]
    receiver_address: Optional[str]
    
    # 支付
    payment_method: Optional[str]
    payment_time: Optional[datetime]
    
    # 时间
    created_at: datetime
    paid_at: Optional[datetime]
    confirmed_at: Optional[datetime]
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    cancelled_at: Optional[datetime]
    
    # 其他
    remark: Optional[str]
    cancel_reason: Optional[str]
    is_urgent: bool
    estimated_completion_time: Optional[datetime]
    
    class Config:
        from_attributes = True


class OrderDetail(OrderInDB):
    """订单详情（包含样品）"""
    samples: List[OrderSampleInDB] = Field([], description="样品列表")


class OrderListItem(BaseModel):
    """订单列表项"""
    id: int
    order_no: str
    project_name: str
    lab_name: str
    status: str
    total_fee: Decimal
    sample_count: int
    created_at: datetime
    project_image: Optional[str] = None
    
    class Config:
        from_attributes = True


class OrderListResponse(BaseModel):
    """订单列表响应"""
    total: int = Field(..., description="总数")
    list: List[OrderListItem] = Field(..., description="订单列表")


# ==================== 订单操作 ====================

class OrderCancel(BaseModel):
    """取消订单"""
    reason: str = Field(..., description="取消原因")


class OrderEvaluate(BaseModel):
    """订单评价"""
    rating: int = Field(..., ge=1, le=5, description="评分1-5")
    content: str = Field(..., description="评价内容")
    tags: Optional[List[str]] = Field(None, description="评价标签")
    images: Optional[List[str]] = Field(None, description="评价图片")


# ==================== 地址 ====================

class AddressCreate(BaseModel):
    """创建地址"""
    receiver_name: str = Field(..., description="收件人")
    phone: str = Field(..., description="手机号")
    province: str = Field(..., description="省")
    city: str = Field(..., description="市")
    district: Optional[str] = Field(None, description="区")
    detail_address: str = Field(..., description="详细地址")
    is_default: bool = Field(False, description="是否默认")


class AddressUpdate(BaseModel):
    """更新地址"""
    receiver_name: Optional[str] = None
    phone: Optional[str] = None
    province: Optional[str] = None
    city: Optional[str] = None
    district: Optional[str] = None
    detail_address: Optional[str] = None
    is_default: Optional[bool] = None


class AddressInDB(BaseModel):
    """数据库中的地址"""
    id: int
    user_id: int
    receiver_name: str
    phone: str
    province: str
    city: str
    district: Optional[str]
    detail_address: str
    is_default: bool
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


# ==================== 支付 ====================

class PaymentCreate(BaseModel):
    """创建支付"""
    order_id: int = Field(..., description="订单ID")
    payment_method: str = Field(..., description="支付方式: balance|alipay|wechat")
    payment_password: Optional[str] = Field(None, description="支付密码（余额支付时必填）")


class PaymentInDB(BaseModel):
    """数据库中的支付记录"""
    id: int
    payment_no: str
    order_id: int
    order_no: str
    user_id: int
    payment_method: str
    payment_channel: Optional[str]
    amount: Decimal
    status: str
    trade_no: Optional[str]
    paid_at: Optional[datetime]
    created_at: datetime
    
    class Config:
        from_attributes = True


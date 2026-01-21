"""
样品组管理相关的Pydantic模型
"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Any
from datetime import datetime
from decimal import Decimal
import re


# ==================== 样品明细 ====================

class SampleItemBase(BaseModel):
    """样品明细基础模型"""
    sample_no: Optional[str] = Field(None, max_length=100, description="样品编号")
    sample_name: Optional[str] = Field(None, max_length=200, description="样品名称")
    sample_composition: Optional[str] = Field(None, description="样品成分")
    sample_state: Optional[str] = Field(None, max_length=50, description="样品状态")
    danger_type: Optional[str] = Field(None, max_length=50, description="危险性")
    storage_requirement: Optional[str] = Field(None, max_length=100, description="存放要求")
    quantity: int = Field(default=1, ge=1, description="数量")
    remark: Optional[str] = Field(None, description="备注")
    photos: Optional[List[str]] = Field(None, description="样品照片")

    @field_validator('sample_no')
    @classmethod
    def validate_sample_no(cls, v):
        """验证样品编号只能包含英文、数字、下划线"""
        if v is not None and v != '':
            if not re.match(r'^[a-zA-Z0-9_]+$', v):
                raise ValueError('样品编号只能包含英文字母、数字和下划线')
        return v


class SampleItemCreate(SampleItemBase):
    """创建样品明细"""
    pass


class SampleItemUpdate(BaseModel):
    """更新样品明细"""
    sample_no: Optional[str] = Field(None, max_length=100)
    sample_name: Optional[str] = Field(None, max_length=200)
    sample_composition: Optional[str] = None
    sample_state: Optional[str] = Field(None, max_length=50)
    danger_type: Optional[str] = Field(None, max_length=50)
    storage_requirement: Optional[str] = Field(None, max_length=100)
    quantity: Optional[int] = Field(None, ge=1)
    remark: Optional[str] = None
    photos: Optional[List[str]] = None

    @field_validator('sample_no')
    @classmethod
    def validate_sample_no(cls, v):
        if v is not None and v != '':
            if not re.match(r'^[a-zA-Z0-9_]+$', v):
                raise ValueError('样品编号只能包含英文字母、数字和下划线')
        return v


class SampleItemResponse(SampleItemBase):
    """样品明细响应"""
    id: int
    group_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ==================== 样品组 ====================

class SampleGroupBase(BaseModel):
    """样品组基础模型"""
    project_id: int = Field(..., description="项目ID")
    group_name: Optional[str] = Field(None, max_length=100, description="分组名称/测试目的")
    option_selections: Optional[List[dict]] = Field(None, description="选项选择")


class SampleGroupCreate(SampleGroupBase):
    """创建样品组"""
    items: Optional[List[SampleItemCreate]] = Field(None, description="初始样品列表")


class SampleGroupUpdate(BaseModel):
    """更新样品组"""
    group_name: Optional[str] = Field(None, max_length=100)
    option_selections: Optional[List[dict]] = None
    is_collapsed: Optional[bool] = None


class SampleGroupResponse(BaseModel):
    """样品组响应"""
    id: int
    user_id: int
    project_id: int
    order_id: Optional[int] = None
    group_name: Optional[str] = None
    group_index: int
    option_selections: Optional[List[dict]] = None
    options_fee: Decimal = Decimal("0")
    is_collapsed: bool = False
    status: str
    items: List[SampleItemResponse] = []
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class SampleGroupListResponse(BaseModel):
    """样品组列表响应"""
    id: int
    project_id: int
    group_name: Optional[str] = None
    group_index: int
    options_fee: Decimal = Decimal("0")
    is_collapsed: bool = False
    status: str
    sample_count: int = 0
    created_at: datetime

    class Config:
        from_attributes = True


# ==================== 批量操作 ====================

class BatchAddSamplesRequest(BaseModel):
    """批量添加样品请求"""
    count: int = Field(..., ge=1, le=100, description="添加数量")
    prefix: Optional[str] = Field(None, max_length=50, description="编号前缀")
    start_number: int = Field(default=1, ge=1, description="起始编号")

    @field_validator('prefix')
    @classmethod
    def validate_prefix(cls, v):
        """验证编号前缀只能包含英文、数字、下划线"""
        if v is not None and v != '':
            if not re.match(r'^[a-zA-Z0-9_]*$', v):
                raise ValueError('编号前缀只能包含英文字母、数字和下划线')
        return v


class BatchAddSamplesResponse(BaseModel):
    """批量添加样品响应"""
    added_count: int
    items: List[SampleItemResponse]


# ==================== 提交相关 ====================

class SubmitGroupsRequest(BaseModel):
    """批量提交样品组请求"""
    group_ids: List[int] = Field(..., min_length=1, description="要提交的样品组ID列表")
    merge_order: bool = Field(default=False, description="是否合并为一个订单")
    address_id: Optional[int] = Field(None, description="收货地址ID")
    coupon_id: Optional[int] = Field(None, description="优惠券ID")
    remark: Optional[str] = Field(None, description="订单备注")


class SubmitGroupsResponse(BaseModel):
    """批量提交样品组响应"""
    order_ids: List[int]
    total_amount: Decimal
    message: str


# ==================== 价格计算 ====================

class CalculateGroupsPriceRequest(BaseModel):
    """计算多组价格请求"""
    group_ids: List[int] = Field(..., min_length=1, description="样品组ID列表")
    merge: bool = Field(default=False, description="是否合并计算")


class GroupPriceDetail(BaseModel):
    """单组价格详情"""
    group_id: int
    group_name: Optional[str] = None
    sample_count: int
    base_price: Decimal
    options_fee: Decimal
    subtotal: Decimal


class CalculateGroupsPriceResponse(BaseModel):
    """计算多组价格响应"""
    groups: List[GroupPriceDetail]
    total_sample_count: int
    total_base_price: Decimal
    total_options_fee: Decimal
    total_amount: Decimal


# ==================== 复制 ====================

class CopyGroupResponse(BaseModel):
    """复制样品组响应"""
    new_group: SampleGroupResponse
    message: str

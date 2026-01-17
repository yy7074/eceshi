"""
佣金设置相关的Pydantic模型
"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime, date
from decimal import Decimal


# ==================== 用户佣金设置 ====================

class CommissionSettingBase(BaseModel):
    """佣金设置基础模型"""
    commission_rate: Decimal = Field(..., ge=0, le=12, description="佣金比例（%），最大12%")
    effective_from: Optional[date] = Field(None, description="生效日期")
    effective_to: Optional[date] = Field(None, description="失效日期")

    @field_validator('commission_rate')
    @classmethod
    def validate_rate(cls, v):
        if v > Decimal("12"):
            raise ValueError('佣金比例不能超过12%')
        return v


class CommissionSettingCreate(CommissionSettingBase):
    """创建佣金设置"""
    user_id: int = Field(..., description="用户ID")


class CommissionSettingUpdate(BaseModel):
    """更新佣金设置"""
    commission_rate: Optional[Decimal] = Field(None, ge=0, le=12)
    effective_from: Optional[date] = None
    effective_to: Optional[date] = None

    @field_validator('commission_rate')
    @classmethod
    def validate_rate(cls, v):
        if v is not None and v > Decimal("12"):
            raise ValueError('佣金比例不能超过12%')
        return v


class CommissionSettingResponse(BaseModel):
    """佣金设置响应"""
    id: int
    user_id: int
    commission_rate: Decimal
    max_rate: Decimal
    effective_from: Optional[date] = None
    effective_to: Optional[date] = None
    created_by: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    # 用户信息
    user_name: Optional[str] = None
    user_phone: Optional[str] = None

    class Config:
        from_attributes = True


class CommissionSettingListResponse(BaseModel):
    """佣金设置列表响应"""
    items: List[CommissionSettingResponse]
    total: int
    page: int
    page_size: int


# ==================== 佣金记录 ====================

class CommissionRecordResponse(BaseModel):
    """佣金记录响应"""
    id: int
    user_id: int
    order_id: int
    from_user_id: Optional[int] = None
    order_amount: Decimal
    commission_rate: Decimal
    commission_amount: Decimal
    status: str
    settled_at: Optional[datetime] = None
    created_at: datetime

    # 关联信息
    order_no: Optional[str] = None
    from_user_name: Optional[str] = None

    class Config:
        from_attributes = True


class CommissionRecordListResponse(BaseModel):
    """佣金记录列表响应"""
    items: List[CommissionRecordResponse]
    total: int
    page: int
    page_size: int


# ==================== 佣金统计 ====================

class CommissionStatsResponse(BaseModel):
    """佣金统计响应"""
    total_commission: Decimal = Decimal("0")
    pending_commission: Decimal = Decimal("0")
    settled_commission: Decimal = Decimal("0")
    total_orders: int = 0
    current_rate: Decimal = Decimal("0")


# ==================== 批量操作 ====================

class BatchSetCommissionRequest(BaseModel):
    """批量设置佣金请求"""
    user_ids: List[int] = Field(..., min_length=1, description="用户ID列表")
    commission_rate: Decimal = Field(..., ge=0, le=12, description="佣金比例")
    effective_from: Optional[date] = None
    effective_to: Optional[date] = None


class SettleCommissionRequest(BaseModel):
    """结算佣金请求"""
    record_ids: List[int] = Field(..., min_length=1, description="佣金记录ID列表")


class SettleCommissionResponse(BaseModel):
    """结算佣金响应"""
    settled_count: int
    total_amount: Decimal
    message: str

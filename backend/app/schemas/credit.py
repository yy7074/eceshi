"""
信用系统Schema
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from decimal import Decimal


# ========== 信用额度 ==========

class CreditInfoResponse(BaseModel):
    """信用额度信息响应"""
    credit_limit: Decimal = Field(..., description="信用额度")
    used_credit: Decimal = Field(..., description="已用额度")
    available_credit: Decimal = Field(..., description="可用额度")
    total_debt: Decimal = Field(..., description="总欠款")
    is_certified: bool = Field(..., description="是否已认证")


# ========== 信用消费 ==========

class CreditPayRequest(BaseModel):
    """信用支付请求"""
    order_id: int = Field(..., description="订单ID")
    amount: Decimal = Field(..., description="支付金额")


class CreditPayResponse(BaseModel):
    """信用支付响应"""
    success: bool
    message: str
    debt_id: Optional[int] = None
    remaining_credit: Optional[Decimal] = None


# ========== 欠款管理 ==========

class DebtItem(BaseModel):
    """欠款项"""
    id: int
    order_id: int
    order_no: str
    original_amount: Decimal
    paid_amount: Decimal
    remaining_amount: Decimal
    status: str
    due_date: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


class DebtListResponse(BaseModel):
    """欠款列表响应"""
    total_debt: Decimal
    debt_count: int
    debts: List[DebtItem]


# ========== 还款 ==========

class RepaymentRequest(BaseModel):
    """还款请求"""
    amount: Decimal = Field(..., gt=0, description="还款金额")
    payment_method: str = Field(..., description="支付方式: wechat/alipay/balance")
    debt_ids: Optional[List[int]] = Field(None, description="指定还款的欠款ID列表，不填则按时间顺序还款")


class RepaymentResponse(BaseModel):
    """还款响应"""
    repayment_no: str
    amount: Decimal
    status: str
    payment_url: Optional[str] = None  # 第三方支付链接


class RepaymentRecord(BaseModel):
    """还款记录"""
    id: int
    repayment_no: str
    amount: Decimal
    payment_method: str
    status: str
    created_at: datetime
    paid_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ========== 交易记录 ==========

class CreditRecordItem(BaseModel):
    """信用交易记录项"""
    id: int
    transaction_type: str
    amount: Decimal
    balance_before: Optional[Decimal] = None
    balance_after: Optional[Decimal] = None
    order_no: Optional[str] = None
    status: str
    remark: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class CreditRecordListResponse(BaseModel):
    """交易记录列表响应"""
    total: int
    page: int
    page_size: int
    records: List[CreditRecordItem]


# ========== 额度申请 ==========

class CreditLimitApplicationRequest(BaseModel):
    """额度提升申请请求"""
    requested_limit: Decimal = Field(..., gt=0, description="申请额度")
    reason: Optional[str] = Field(None, description="申请理由")


class CreditLimitApplicationResponse(BaseModel):
    """额度申请响应"""
    id: int
    current_limit: Decimal
    requested_limit: Decimal
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

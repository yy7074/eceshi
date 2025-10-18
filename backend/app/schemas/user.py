"""
用户相关的Pydantic模型（请求/响应）
"""
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime
from decimal import Decimal


# ========== 用户注册/登录 ==========

class UserRegister(BaseModel):
    """用户注册请求"""
    phone: str = Field(..., min_length=11, max_length=11, description="手机号")
    password: str = Field(..., min_length=6, description="密码")
    sms_code: str = Field(..., min_length=6, max_length=6, description="短信验证码")
    
    @validator('phone')
    def validate_phone(cls, v):
        if not v.isdigit():
            raise ValueError('手机号必须是数字')
        return v


class UserLogin(BaseModel):
    """用户登录请求"""
    phone: str = Field(..., description="手机号")
    password: str = Field(..., description="密码")


class SMSCodeRequest(BaseModel):
    """发送短信验证码请求"""
    phone: str = Field(..., min_length=11, max_length=11, description="手机号")
    scene: str = Field(..., description="场景: register/login/reset_password")
    
    @validator('phone')
    def validate_phone(cls, v):
        if not v.isdigit():
            raise ValueError('手机号必须是数字')
        return v


class SMSLoginRequest(BaseModel):
    """短信验证码登录请求"""
    phone: str = Field(..., min_length=11, max_length=11, description="手机号")
    sms_code: str = Field(..., min_length=6, max_length=6, description="短信验证码")
    
    @validator('phone')
    def validate_phone(cls, v):
        if not v.isdigit():
            raise ValueError('手机号必须是数字')
        return v


class WechatLoginRequest(BaseModel):
    """微信登录请求"""
    code: str = Field(..., description="微信登录code")


class TokenResponse(BaseModel):
    """登录响应（JWT令牌）"""
    access_token: str
    token_type: str = "bearer"
    user_id: int
    phone: Optional[str] = None  # 微信登录用户可能没有手机号
    nickname: Optional[str] = None


# ========== 用户信息 ==========

class UserBase(BaseModel):
    """用户基础信息"""
    phone: Optional[str] = None  # 微信登录用户可能没有手机号
    nickname: Optional[str] = None
    avatar: Optional[str] = None
    email: Optional[EmailStr] = None


class UserInfo(UserBase):
    """用户详细信息（响应）"""
    id: int
    is_certified: bool
    membership_level: int
    credit_limit: Decimal
    used_credit: Decimal
    prepaid_balance: Decimal
    points_balance: int
    total_spent: Decimal
    total_orders: int
    status: str
    created_at: datetime
    last_login_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    """更新用户信息"""
    nickname: Optional[str] = Field(None, max_length=50)
    avatar: Optional[str] = None
    email: Optional[EmailStr] = None


# ========== 实名认证 ==========

class CertificationRequest(BaseModel):
    """实名认证请求"""
    real_name: str = Field(..., max_length=50, description="真实姓名")
    id_card: str = Field(..., min_length=18, max_length=18, description="身份证号")
    enrollment_year: Optional[str] = Field(None, description="入学年份")
    graduation_year: Optional[str] = Field(None, description="毕业年份")
    province: str = Field(..., description="省份")
    city: str = Field(..., description="城市")
    university: str = Field(..., description="高校")
    department: str = Field(..., description="院系")
    supervisor_name: Optional[str] = Field(None, description="导师姓名")
    supervisor_title: Optional[str] = Field(None, description="导师职称")
    student_card_photo: Optional[str] = Field(None, description="学生证照片URL")
    id_card_front: Optional[str] = Field(None, description="身份证正面URL")
    id_card_back: Optional[str] = Field(None, description="身份证反面URL")


class CertificationResponse(BaseModel):
    """实名认证响应"""
    id: int
    user_id: int
    status: str
    real_name: str
    university: str
    department: str
    created_at: datetime
    certified_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


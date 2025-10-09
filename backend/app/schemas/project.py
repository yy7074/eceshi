"""
项目相关Schema
"""
from typing import Optional, List
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field


# ==================== 项目分类 ====================

class CategoryBase(BaseModel):
    """分类基础"""
    name: str = Field(..., description="分类名称")
    code: Optional[str] = Field(None, description="分类代码")
    parent_id: Optional[int] = Field(None, description="父分类ID")
    icon: Optional[str] = Field(None, description="图标")
    description: Optional[str] = Field(None, description="描述")


class CategoryInDB(CategoryBase):
    """数据库中的分类"""
    id: int
    level: int
    sort_order: int
    is_hot: bool
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# ==================== 实验室 ====================

class LaboratoryBase(BaseModel):
    """实验室基础"""
    name: str = Field(..., description="实验室名称")
    short_name: Optional[str] = Field(None, description="简称")
    institution: Optional[str] = Field(None, description="所属机构")
    province: Optional[str] = Field(None, description="省份")
    city: Optional[str] = Field(None, description="城市")


class LaboratoryInDB(LaboratoryBase):
    """数据库中的实验室"""
    id: int
    lab_no: str
    rating: Decimal
    order_count: int
    is_verified: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# ==================== 项目 ====================

class ProjectBase(BaseModel):
    """项目基础"""
    name: str = Field(..., description="项目名称")
    category_id: int = Field(..., description="分类ID")
    original_price: Decimal = Field(..., description="原价")
    current_price: Decimal = Field(..., description="现价")


class ProjectCreate(ProjectBase):
    """创建项目"""
    lab_id: int = Field(..., description="实验室ID")
    service_cycle_min: Optional[int] = Field(None, description="最短服务周期")
    service_cycle_max: Optional[int] = Field(None, description="最长服务周期")
    equipment_name: Optional[str] = Field(None, description="仪器名称")
    equipment_model: Optional[str] = Field(None, description="仪器型号")
    introduction: Optional[str] = Field(None, description="项目介绍")
    sample_requirements: Optional[str] = Field(None, description="样品要求")


class ProjectUpdate(BaseModel):
    """更新项目"""
    name: Optional[str] = None
    original_price: Optional[Decimal] = None
    current_price: Optional[Decimal] = None
    introduction: Optional[str] = None
    status: Optional[str] = None


class ProjectInDB(ProjectBase):
    """数据库中的项目"""
    id: int
    project_no: str
    lab_id: int
    service_cycle_min: Optional[int]
    service_cycle_max: Optional[int]
    equipment_name: Optional[str]
    equipment_model: Optional[str]
    cover_image: Optional[str]
    status: str
    is_hot: bool
    view_count: int
    booking_count: int
    satisfaction: Decimal
    created_at: datetime
    
    class Config:
        from_attributes = True


class ProjectDetail(ProjectInDB):
    """项目详情"""
    lab_name: Optional[str] = None
    category_name: Optional[str] = None
    introduction: Optional[str] = None
    sample_requirements: Optional[str] = None
    booking_notice: Optional[str] = None
    detail_images: Optional[List[str]] = None
    faq: Optional[List[dict]] = None


class ProjectListItem(BaseModel):
    """项目列表项"""
    id: int
    name: str
    lab_name: str
    original_price: Decimal
    current_price: Decimal
    cover_image: Optional[str]
    satisfaction: Decimal
    booking_count: int
    is_hot: bool
    
    class Config:
        from_attributes = True


# ==================== 评价 ====================

class ReviewCreate(BaseModel):
    """创建评价"""
    order_id: int = Field(..., description="订单ID")
    rating: int = Field(..., ge=1, le=5, description="评分1-5")
    content: str = Field(..., description="评价内容")
    tags: Optional[List[str]] = Field(None, description="评价标签")
    images: Optional[List[str]] = Field(None, description="评价图片")
    is_anonymous: bool = Field(False, description="是否匿名")


class ReviewInDB(BaseModel):
    """数据库中的评价"""
    id: int
    project_id: int
    order_id: int
    user_id: int
    rating: int
    content: str
    tags: Optional[List[str]]
    images: Optional[List[str]]
    is_anonymous: bool
    reply_content: Optional[str]
    reply_time: Optional[datetime]
    created_at: datetime
    
    class Config:
        from_attributes = True


class ReviewDetail(ReviewInDB):
    """评价详情"""
    user_nickname: Optional[str] = None
    user_avatar: Optional[str] = None
    project_name: Optional[str] = None


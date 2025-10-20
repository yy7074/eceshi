"""
评价功能API
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

from app.core.database import get_db
from app.core.response import Response
from app.api.v1.deps import get_current_user
from app.models.user import User


router = APIRouter()


# 创建评价表模型
from sqlalchemy import Column, Integer, String, Text, DateTime, Numeric, Boolean, func
from app.core.database import Base

class OrderReview(Base):
    """订单评价表"""
    __tablename__ = "order_reviews"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, nullable=False, index=True, comment="订单ID")
    user_id = Column(Integer, nullable=False, index=True, comment="用户ID")
    project_id = Column(Integer, nullable=False, index=True, comment="项目ID")
    
    # 评分（1-5星）
    service_rating = Column(Integer, default=5, comment="服务质量评分")
    quality_rating = Column(Integer, default=5, comment="检测效果评分")
    logistics_rating = Column(Integer, default=5, comment="物流配送评分")
    
    # 评价内容
    content = Column(Text, comment="评价内容")
    images = Column(Text, comment="评价图片（JSON数组）")
    tags = Column(String(500), comment="评价标签（逗号分隔）")
    
    # 其他信息
    is_anonymous = Column(Boolean, default=False, comment="是否匿名")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="评价时间")


# Pydantic模型
class ReviewCreate(BaseModel):
    """创建评价"""
    order_id: int = Field(..., description="订单ID")
    service_rating: int = Field(5, ge=1, le=5, description="服务质量评分")
    quality_rating: int = Field(5, ge=1, le=5, description="检测效果评分")
    logistics_rating: int = Field(5, ge=1, le=5, description="物流配送评分")
    content: Optional[str] = Field(None, description="评价内容")
    images: Optional[List[str]] = Field([], description="评价图片URL列表")
    tags: Optional[List[str]] = Field([], description="评价标签")
    is_anonymous: bool = Field(False, description="是否匿名")


@router.post("/create", summary="创建评价")
async def create_review(
    data: ReviewCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """创建订单评价"""
    from app.models.order import Order
    import json
    
    # 检查订单是否存在且属于当前用户
    order = db.query(Order).filter(
        Order.id == data.order_id,
        Order.user_id == current_user.id
    ).first()
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="订单不存在或无权评价"
        )
    
    # 检查订单是否已完成
    if order.status != "completed":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="只有已完成的订单才能评价"
        )
    
    # 检查是否已评价
    existing = db.query(OrderReview).filter(
        OrderReview.order_id == data.order_id
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该订单已评价"
        )
    
    # 创建评价
    review = OrderReview(
        order_id=data.order_id,
        user_id=current_user.id,
        project_id=order.project_id,
        service_rating=data.service_rating,
        quality_rating=data.quality_rating,
        logistics_rating=data.logistics_rating,
        content=data.content,
        images=json.dumps(data.images) if data.images else None,
        tags=','.join(data.tags) if data.tags else None,
        is_anonymous=data.is_anonymous
    )
    
    db.add(review)
    db.commit()
    db.refresh(review)
    
    return Response.success(data={"id": review.id}, message="评价成功")


@router.get("/my", summary="获取我的评价列表")
async def get_my_reviews(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取当前用户的评价列表"""
    import json
    
    query = db.query(OrderReview).filter(OrderReview.user_id == current_user.id)
    total = query.count()
    
    reviews = query.order_by(OrderReview.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
    
    items = []
    for review in reviews:
        items.append({
            "id": review.id,
            "order_id": review.order_id,
            "project_id": review.project_id,
            "service_rating": review.service_rating,
            "quality_rating": review.quality_rating,
            "logistics_rating": review.logistics_rating,
            "content": review.content,
            "images": json.loads(review.images) if review.images else [],
            "tags": review.tags.split(',') if review.tags else [],
            "is_anonymous": review.is_anonymous,
            "created_at": review.created_at.isoformat() if review.created_at else None
        })
    
    return Response.success(data={
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size
    })


@router.get("/project/{project_id}", summary="获取项目的评价列表")
async def get_project_reviews(
    project_id: int,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """获取项目的评价列表（公开）"""
    import json
    from sqlalchemy.orm import joinedload
    
    query = db.query(OrderReview).filter(OrderReview.project_id == project_id)
    total = query.count()
    
    reviews = query.order_by(OrderReview.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
    
    # 获取用户信息
    items = []
    for review in reviews:
        user = db.query(User).filter(User.id == review.user_id).first()
        
        items.append({
            "id": review.id,
            "user_nickname": "匿名用户" if review.is_anonymous else (user.nickname if user else "用户"),
            "user_avatar": None if review.is_anonymous else (user.avatar if user else None),
            "service_rating": review.service_rating,
            "quality_rating": review.quality_rating,
            "logistics_rating": review.logistics_rating,
            "avg_rating": (review.service_rating + review.quality_rating + review.logistics_rating) / 3,
            "content": review.content,
            "images": json.loads(review.images) if review.images else [],
            "tags": review.tags.split(',') if review.tags else [],
            "created_at": review.created_at.isoformat() if review.created_at else None
        })
    
    return Response.success(data={
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size
    })


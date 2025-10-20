"""
收藏功能API
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime

from app.core.database import get_db
from app.core.response import Response
from app.api.v1.deps import get_current_user
from app.models.user import User
from app.models.project import Project


router = APIRouter()


# 创建收藏表模型（如果不存在）
from sqlalchemy import Column, Integer, DateTime, func, UniqueConstraint
from app.core.database import Base

class ProjectFavorite(Base):
    """项目收藏表"""
    __tablename__ = "project_favorites"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True, comment="用户ID")
    project_id = Column(Integer, nullable=False, index=True, comment="项目ID")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="收藏时间")
    
    __table_args__ = (
        UniqueConstraint('user_id', 'project_id', name='uk_user_project'),
    )


@router.post("/add", summary="收藏项目")
async def add_favorite(
    project_id: int = Query(..., description="项目ID"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """添加项目到收藏"""
    # 检查项目是否存在
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="项目不存在"
        )
    
    # 检查是否已收藏
    existing = db.query(ProjectFavorite).filter(
        ProjectFavorite.user_id == current_user.id,
        ProjectFavorite.project_id == project_id
    ).first()
    
    if existing:
        return Response.success(message="已经收藏过该项目")
    
    # 创建收藏记录
    favorite = ProjectFavorite(
        user_id=current_user.id,
        project_id=project_id
    )
    db.add(favorite)
    db.commit()
    
    return Response.success(message="收藏成功")


@router.delete("/remove", summary="取消收藏")
async def remove_favorite(
    project_id: int = Query(..., description="项目ID"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """取消收藏项目"""
    favorite = db.query(ProjectFavorite).filter(
        ProjectFavorite.user_id == current_user.id,
        ProjectFavorite.project_id == project_id
    ).first()
    
    if not favorite:
        return Response.success(message="未收藏该项目")
    
    db.delete(favorite)
    db.commit()
    
    return Response.success(message="取消收藏成功")


@router.get("/list", summary="获取收藏列表")
async def get_favorite_list(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取用户的收藏列表"""
    from sqlalchemy.orm import joinedload
    
    # 查询收藏记录
    query = db.query(ProjectFavorite).filter(
        ProjectFavorite.user_id == current_user.id
    )
    
    total = query.count()
    
    favorites = query.order_by(ProjectFavorite.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
    
    # 获取项目详情
    project_ids = [f.project_id for f in favorites]
    projects = db.query(Project).options(
        joinedload(Project.category),
        joinedload(Project.laboratory)
    ).filter(Project.id.in_(project_ids)).all()
    
    # 构建返回数据
    project_map = {p.id: p for p in projects}
    items = []
    
    for favorite in favorites:
        project = project_map.get(favorite.project_id)
        if project:
            items.append({
                "id": project.id,
                "name": project.name,
                "project_no": project.project_no,
                "cover_image": project.cover_image,
                "current_price": float(project.current_price) if project.current_price else 0,
                "original_price": float(project.original_price) if project.original_price else 0,
                "satisfaction": float(project.satisfaction) if project.satisfaction else 100.0,
                "order_count": project.order_count or 0,
                "lab_name": project.laboratory.name if project.laboratory else None,
                "category_name": project.category.name if project.category else None,
                "favorited_at": favorite.created_at.isoformat() if favorite.created_at else None
            })
    
    return Response.success(data={
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size
    })


@router.get("/check", summary="检查是否已收藏")
async def check_favorite(
    project_id: int = Query(..., description="项目ID"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """检查项目是否已收藏"""
    favorite = db.query(ProjectFavorite).filter(
        ProjectFavorite.user_id == current_user.id,
        ProjectFavorite.project_id == project_id
    ).first()
    
    return Response.success(data={
        "is_favorited": favorite is not None
    })


"""帮助中心API"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.response import success_response, error_response
from app.models.help import HelpCategory, HelpArticle

router = APIRouter()


@router.get("/categories")
async def get_help_categories(
    db: Session = Depends(get_db)
):
    """获取帮助分类列表"""
    categories = db.query(HelpCategory).filter(
        HelpCategory.is_active == True
    ).order_by(HelpCategory.sort_order.asc()).all()
    
    return success_response(data={
        "items": [
            {
                "id": c.id,
                "name": c.name,
                "icon": c.icon
            }
            for c in categories
        ]
    })


@router.get("/articles")
async def get_help_articles(
    category_id: Optional[int] = Query(None, description="分类ID"),
    is_hot: Optional[bool] = Query(None, description="是否热门"),
    keyword: Optional[str] = Query(None, description="搜索关键词"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """获取帮助文章列表"""
    query = db.query(HelpArticle).filter(HelpArticle.is_active == True)
    
    if category_id:
        query = query.filter(HelpArticle.category_id == category_id)
    if is_hot:
        query = query.filter(HelpArticle.is_hot == True)
    if keyword:
        query = query.filter(HelpArticle.title.contains(keyword))
    
    query = query.order_by(HelpArticle.sort_order.asc(), HelpArticle.id.desc())
    
    total = query.count()
    items = query.offset((page - 1) * page_size).limit(page_size).all()
    
    return success_response(data={
        "items": [
            {
                "id": a.id,
                "category_id": a.category_id,
                "title": a.title,
                "is_hot": a.is_hot,
                "view_count": a.view_count
            }
            for a in items
        ],
        "total": total,
        "page": page,
        "page_size": page_size
    })


@router.get("/articles/{article_id}")
async def get_article_detail(
    article_id: int,
    db: Session = Depends(get_db)
):
    """获取文章详情"""
    article = db.query(HelpArticle).filter(
        HelpArticle.id == article_id,
        HelpArticle.is_active == True
    ).first()
    
    if not article:
        return error_response(message="文章不存在")
    
    # 增加浏览量
    article.view_count = (article.view_count or 0) + 1
    db.commit()
    
    # 获取分类信息
    category = db.query(HelpCategory).filter(HelpCategory.id == article.category_id).first()
    
    return success_response(data={
        "id": article.id,
        "category_id": article.category_id,
        "category_name": category.name if category else None,
        "title": article.title,
        "content": article.content,
        "is_hot": article.is_hot,
        "view_count": article.view_count,
        "created_at": article.created_at.strftime("%Y-%m-%d %H:%M:%S") if article.created_at else None
    })


@router.get("/hot")
async def get_hot_articles(
    limit: int = Query(10, ge=1, le=20),
    db: Session = Depends(get_db)
):
    """获取热门问题"""
    articles = db.query(HelpArticle).filter(
        HelpArticle.is_active == True,
        HelpArticle.is_hot == True
    ).order_by(HelpArticle.view_count.desc()).limit(limit).all()
    
    return success_response(data={
        "items": [
            {
                "id": a.id,
                "title": a.title,
                "view_count": a.view_count
            }
            for a in articles
        ]
    })


@router.get("/search")
async def search_help(
    keyword: str = Query(..., min_length=1, description="搜索关键词"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """搜索帮助文章"""
    query = db.query(HelpArticle).filter(
        HelpArticle.is_active == True,
        (HelpArticle.title.contains(keyword) | HelpArticle.content.contains(keyword))
    )
    
    total = query.count()
    items = query.order_by(HelpArticle.view_count.desc()).offset((page - 1) * page_size).limit(page_size).all()
    
    return success_response(data={
        "items": [
            {
                "id": a.id,
                "title": a.title,
                "content": a.content[:200] + "..." if len(a.content) > 200 else a.content
            }
            for a in items
        ],
        "total": total,
        "page": page,
        "page_size": page_size
    })


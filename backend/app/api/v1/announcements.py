"""公告管理API"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.response import success_response, error_response
from app.models.announcement import Announcement, UserNotification
from app.models.user import User
from app.api.v1.deps import get_current_user, get_current_user_optional

router = APIRouter()


@router.get("/list")
async def get_announcements(
    category: Optional[str] = Query(None, description="分类"),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """获取公告列表"""
    query = db.query(Announcement).filter(Announcement.is_active == True)
    
    if category:
        query = query.filter(Announcement.category == category)
    
    # 置顶排序
    query = query.order_by(Announcement.is_top.desc(), Announcement.created_at.desc())
    
    total = query.count()
    items = query.offset((page - 1) * page_size).limit(page_size).all()
    
    return success_response(data={
        "items": [
            {
                "id": a.id,
                "title": a.title,
                "summary": a.summary or (a.content[:100] + "..." if len(a.content) > 100 else a.content),
                "category": a.category,
                "is_top": a.is_top,
                "view_count": a.view_count,
                "created_at": a.created_at.strftime("%Y-%m-%d %H:%M:%S") if a.created_at else None
            }
            for a in items
        ],
        "total": total,
        "page": page,
        "page_size": page_size
    })


@router.get("/notifications/list")
async def get_user_notifications_before_detail(
    category: Optional[str] = Query(None, description="分类"),
    is_read: Optional[bool] = Query(None, description="是否已读"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=50),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取用户通知列表。静态路由需放在公告详情动态路由之前。"""
    query = db.query(UserNotification).filter(UserNotification.user_id == current_user.id)
    if category:
        query = query.filter(UserNotification.category == category)
    if is_read is not None:
        query = query.filter(UserNotification.is_read == is_read)

    total = query.count()
    unread_count = db.query(UserNotification).filter(
        UserNotification.user_id == current_user.id,
        UserNotification.is_read == False
    ).count()
    items = query.order_by(UserNotification.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()

    return success_response(data={
        "items": [
            {
                "id": n.id,
                "title": n.title,
                "content": n.content,
                "category": n.category,
                "is_read": n.is_read,
                "related_type": n.related_type,
                "related_id": n.related_id,
                "created_at": n.created_at.strftime("%Y-%m-%d %H:%M:%S") if n.created_at else None
            }
            for n in items
        ],
        "total": total,
        "unread_count": unread_count,
        "page": page,
        "page_size": page_size
    })


@router.post("/notifications/{notification_id}/read")
async def mark_notification_read_before_detail(
    notification_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    notification = db.query(UserNotification).filter(
        UserNotification.id == notification_id,
        UserNotification.user_id == current_user.id
    ).first()
    if notification:
        notification.is_read = True
        db.commit()
    return success_response(message="ok")


@router.post("/notifications/read-all")
async def mark_all_notifications_read_before_detail(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db.query(UserNotification).filter(
        UserNotification.user_id == current_user.id,
        UserNotification.is_read == False
    ).update({"is_read": True})
    db.commit()
    return success_response(message="ok")


@router.get("/{announcement_id}")
async def get_announcement_detail(
    announcement_id: int,
    db: Session = Depends(get_db)
):
    """获取公告详情"""
    announcement = db.query(Announcement).filter(
        Announcement.id == announcement_id,
        Announcement.is_active == True
    ).first()
    
    if not announcement:
        return error_response(message="公告不存在")
    
    # 增加浏览量
    announcement.view_count = (announcement.view_count or 0) + 1
    db.commit()
    
    return success_response(data={
        "id": announcement.id,
        "title": announcement.title,
        "content": announcement.content,
        "category": announcement.category,
        "view_count": announcement.view_count,
        "created_at": announcement.created_at.strftime("%Y-%m-%d %H:%M:%S") if announcement.created_at else None
    })


# ============ 用户通知 ============

@router.get("/notifications/list")
async def get_user_notifications(
    category: Optional[str] = Query(None, description="分类"),
    is_read: Optional[bool] = Query(None, description="是否已读"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=50),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取用户通知列表"""
    query = db.query(UserNotification).filter(UserNotification.user_id == current_user.id)
    
    if category:
        query = query.filter(UserNotification.category == category)
    if is_read is not None:
        query = query.filter(UserNotification.is_read == is_read)
    
    query = query.order_by(UserNotification.created_at.desc())
    
    total = query.count()
    unread_count = db.query(UserNotification).filter(
        UserNotification.user_id == current_user.id,
        UserNotification.is_read == False
    ).count()
    
    items = query.offset((page - 1) * page_size).limit(page_size).all()
    
    return success_response(data={
        "items": [
            {
                "id": n.id,
                "title": n.title,
                "content": n.content,
                "category": n.category,
                "is_read": n.is_read,
                "related_type": n.related_type,
                "related_id": n.related_id,
                "created_at": n.created_at.strftime("%Y-%m-%d %H:%M:%S") if n.created_at else None
            }
            for n in items
        ],
        "total": total,
        "unread_count": unread_count,
        "page": page,
        "page_size": page_size
    })


@router.post("/notifications/{notification_id}/read")
async def mark_notification_read(
    notification_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """标记通知已读"""
    notification = db.query(UserNotification).filter(
        UserNotification.id == notification_id,
        UserNotification.user_id == current_user.id
    ).first()
    
    if notification:
        notification.is_read = True
        db.commit()
    
    return success_response(message="ok")


@router.post("/notifications/read-all")
async def mark_all_notifications_read(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """标记所有通知已读"""
    db.query(UserNotification).filter(
        UserNotification.user_id == current_user.id,
        UserNotification.is_read == False
    ).update({"is_read": True})
    db.commit()
    
    return success_response(message="ok")

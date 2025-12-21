"""Banner/轮播图API"""
from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.core.database import get_db
from app.core.response import success_response, error_response
from app.models.banner import Banner
from app.api.v1.deps import get_current_user_optional

router = APIRouter()


@router.get("/list")
async def get_banners(
    position: str = Query("home", description="展示位置"),
    db: Session = Depends(get_db)
):
    """获取轮播图列表"""
    now = datetime.now()
    
    query = db.query(Banner).filter(
        Banner.is_active == True,
        Banner.position == position
    )
    
    # 过滤时间范围
    query = query.filter(
        and_(
            (Banner.start_time == None) | (Banner.start_time <= now),
            (Banner.end_time == None) | (Banner.end_time >= now)
        )
    )
    
    banners = query.order_by(Banner.sort_order.asc(), Banner.id.desc()).all()
    
    return success_response(data={
        "items": [
            {
                "id": b.id,
                "title": b.title,
                "subtitle": b.subtitle,
                "image": b.image,
                "link_type": b.link_type,
                "link_value": b.link_value,
                "button_text": b.button_text
            }
            for b in banners
        ]
    })


@router.get("/{banner_id}")
async def get_banner_detail(
    banner_id: int,
    db: Session = Depends(get_db)
):
    """获取轮播图详情"""
    banner = db.query(Banner).filter(Banner.id == banner_id).first()
    if not banner:
        return error_response(message="轮播图不存在")
    
    return success_response(data={
        "id": banner.id,
        "title": banner.title,
        "subtitle": banner.subtitle,
        "image": banner.image,
        "link_type": banner.link_type,
        "link_value": banner.link_value,
        "button_text": banner.button_text
    })


@router.post("/{banner_id}/click")
async def record_banner_click(
    banner_id: int,
    db: Session = Depends(get_db)
):
    """记录轮播图点击"""
    banner = db.query(Banner).filter(Banner.id == banner_id).first()
    if banner:
        banner.click_count = (banner.click_count or 0) + 1
        db.commit()
    
    return success_response(message="ok")


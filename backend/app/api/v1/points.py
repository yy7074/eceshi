"""
积分系统API
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional

from app.core.database import get_db
from app.core.response import Response
from app.api.v1.deps import get_current_user
from app.models.user import User
from app.models.points import PointsGoods, PointsRecord, PointsExchangeRecord


router = APIRouter()


@router.get("/balance", summary="获取用户积分余额")
async def get_points_balance(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取当前用户的积分余额
    """
    # 计算用户积分余额
    total_points = db.query(func.sum(PointsRecord.points)).filter(
        PointsRecord.user_id == current_user.id
    ).scalar() or 0
    
    # 获取积分明细统计  
    earned = db.query(func.sum(PointsRecord.points)).filter(
        PointsRecord.user_id == current_user.id,
        PointsRecord.points > 0
    ).scalar() or 0
    
    spent = db.query(func.sum(PointsRecord.points)).filter(
        PointsRecord.user_id == current_user.id,
        PointsRecord.points < 0
    ).scalar() or 0
    
    return Response.success(data={
        "balance": int(total_points),
        "earned": int(earned),
        "spent": abs(int(spent))
    })


@router.get("/goods", summary="获取积分商品列表")
async def get_points_goods(
    category: Optional[str] = Query(None, description="商品分类"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    db: Session = Depends(get_db)
):
    """
    获取积分商品列表
    """
    # 构建查询
    query = db.query(PointsGoods).filter(PointsGoods.is_active == True)
    
    # 分类筛选
    if category:
        query = query.filter(PointsGoods.category == category)
    
    # 总数
    total = query.count()
    
    # 分页查询
    goods_list = query.order_by(
        PointsGoods.sort_order,
        PointsGoods.created_at.desc()
    ).offset((page - 1) * page_size).limit(page_size).all()
    
    # 格式化返回
    goods = []
    for g in goods_list:
        goods.append({
            "id": g.id,
            "name": g.name,
            "points": g.points,
            "category": g.category,
            "image": g.image,
            "description": g.description,
            "stock": g.stock
        })
    
    return Response.success(data={
        "items": goods,
        "total": total,
        "page": page,
        "page_size": page_size
    })


@router.post("/exchange", summary="兑换积分商品")
async def exchange_points_goods(
    goods_id: int = Query(..., description="商品ID"),
    address_id: int = Query(..., description="收货地址ID"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    兑换积分商品
    """
    # 查询商品
    goods = db.query(PointsGoods).filter(
        PointsGoods.id == goods_id,
        PointsGoods.is_active == True
    ).first()
    
    if not goods:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="商品不存在或已下架"
        )
    
    # 检查库存
    if goods.stock <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="商品库存不足"
        )
    
    # 计算用户积分余额
    from sqlalchemy import func
    total_points = db.query(func.sum(PointsRecord.points)).filter(
        PointsRecord.user_id == current_user.id
    ).scalar() or 0
    
    # 检查积分是否足够
    if total_points < goods.points:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="积分不足"
        )
    
    # 查询收货地址
    from app.models.user import UserAddress
    address = db.query(UserAddress).filter(
        UserAddress.id == address_id,
        UserAddress.user_id == current_user.id
    ).first()
    
    if not address:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="收货地址不存在"
        )
    
    # 创建兑换记录
    import json
    exchange_record = PointsExchangeRecord(
        user_id=current_user.id,
        goods_id=goods.id,
        points=goods.points,
        status="pending",
        address_snapshot=json.dumps({
            "name": address.name,
            "phone": address.phone,
            "province": address.province,
            "city": address.city,
            "district": address.district,
            "address": address.address
        }, ensure_ascii=False)
    )
    db.add(exchange_record)
    
    # 扣减积分
    points_record = PointsRecord(
        user_id=current_user.id,
        points=-goods.points,
        type="exchange",
        related_id=exchange_record.id,
        description=f"兑换商品：{goods.name}"
    )
    db.add(points_record)
    
    # 扣减库存
    goods.stock -= 1
    
    db.commit()
    db.refresh(exchange_record)
    
    return Response.success(
        data={"exchange_id": exchange_record.id},
        message="兑换成功"
    )


@router.get("/records", summary="获取积分记录")
async def get_points_records(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取用户的积分记录
    """
    # 总数
    total = db.query(PointsRecord).filter(
        PointsRecord.user_id == current_user.id
    ).count()
    
    # 分页查询
    records = db.query(PointsRecord).filter(
        PointsRecord.user_id == current_user.id
    ).order_by(
        PointsRecord.created_at.desc()
    ).offset((page - 1) * page_size).limit(page_size).all()
    
    # 格式化返回
    items = []
    for r in records:
        items.append({
            "id": r.id,
            "points": r.points,
            "type": r.type,
            "description": r.description,
            "created_at": r.created_at.isoformat() if r.created_at else None
        })
    
    return Response.success(data={
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size
    })


@router.get("/exchanges", summary="获取兑换记录")
async def get_exchange_records(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取用户的兑换记录
    """
    from sqlalchemy.orm import joinedload
    
    # 总数
    total = db.query(PointsExchangeRecord).filter(
        PointsExchangeRecord.user_id == current_user.id
    ).count()
    
    # 分页查询
    records = db.query(PointsExchangeRecord).options(
        joinedload(PointsExchangeRecord.goods)
    ).filter(
        PointsExchangeRecord.user_id == current_user.id
    ).order_by(
        PointsExchangeRecord.created_at.desc()
    ).offset((page - 1) * page_size).limit(page_size).all()
    
    # 格式化返回
    items = []
    for r in records:
        items.append({
            "id": r.id,
            "goods_name": r.goods.name if r.goods else None,
            "goods_image": r.goods.image if r.goods else None,
            "points": r.points,
            "status": r.status,
            "express_company": r.express_company,
            "express_no": r.express_no,
            "created_at": r.created_at.isoformat() if r.created_at else None
        })
    
    return Response.success(data={
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size
    })


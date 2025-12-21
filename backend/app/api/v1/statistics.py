"""数据统计API"""
from typing import List, Optional
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_

from app.core.database import get_db
from app.core.response import success_response, error_response
from app.models.order import Order
from app.models.user import User
from app.models.coupon import UserCoupon
from app.models.points import PointsRecord
from app.api.v1.deps import get_current_user

router = APIRouter()


@router.get("/overview")
async def get_user_overview(
    time_range: str = Query("month", description="时间范围: week/month/year/all"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取用户数据概览"""
    # 计算时间范围
    now = datetime.now()
    start_date = None
    
    if time_range == "week":
        start_date = now - timedelta(days=7)
    elif time_range == "month":
        start_date = now - timedelta(days=30)
    elif time_range == "year":
        start_date = now - timedelta(days=365)
    
    # 构建查询条件
    query_filter = [Order.user_id == current_user.id]
    if start_date:
        query_filter.append(Order.created_at >= start_date)
    
    # 订单统计
    total_orders = db.query(func.count(Order.id)).filter(*query_filter).scalar() or 0
    total_amount = db.query(func.sum(Order.total_amount)).filter(
        *query_filter,
        Order.status.in_(["paid", "confirmed", "testing", "completed"])
    ).scalar() or 0
    
    # 积分统计
    total_points = db.query(func.sum(PointsRecord.points)).filter(
        PointsRecord.user_id == current_user.id,
        PointsRecord.points > 0
    ).scalar() or 0
    
    # 优惠券统计
    total_coupons = db.query(func.count(UserCoupon.id)).filter(
        UserCoupon.user_id == current_user.id,
        UserCoupon.status == "unused"
    ).scalar() or 0
    
    return success_response(data={
        "total_orders": total_orders,
        "total_amount": float(total_amount),
        "total_points": int(total_points),
        "total_coupons": total_coupons,
        "time_range": time_range
    })


@router.get("/order-stats")
async def get_order_stats(
    time_range: str = Query("month", description="时间范围"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取订单状态统计"""
    # 计算时间范围
    now = datetime.now()
    start_date = None
    
    if time_range == "week":
        start_date = now - timedelta(days=7)
    elif time_range == "month":
        start_date = now - timedelta(days=30)
    elif time_range == "year":
        start_date = now - timedelta(days=365)
    
    query_filter = [Order.user_id == current_user.id]
    if start_date:
        query_filter.append(Order.created_at >= start_date)
    
    # 各状态订单数
    status_counts = db.query(
        Order.status,
        func.count(Order.id).label("count")
    ).filter(*query_filter).group_by(Order.status).all()
    
    stats = {
        "unpaid": 0,
        "paid": 0,
        "confirmed": 0,
        "testing": 0,
        "completed": 0,
        "cancelled": 0
    }
    
    for status, count in status_counts:
        if status in stats:
            stats[status] = count
    
    return success_response(data=stats)


@router.get("/project-stats")
async def get_project_stats(
    time_range: str = Query("month", description="时间范围"),
    limit: int = Query(5, ge=1, le=20),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取检测项目分布统计"""
    # 计算时间范围
    now = datetime.now()
    start_date = None
    
    if time_range == "week":
        start_date = now - timedelta(days=7)
    elif time_range == "month":
        start_date = now - timedelta(days=30)
    elif time_range == "year":
        start_date = now - timedelta(days=365)
    
    query_filter = [Order.user_id == current_user.id]
    if start_date:
        query_filter.append(Order.created_at >= start_date)
    
    # 项目使用统计
    project_stats = db.query(
        Order.project_name,
        func.count(Order.id).label("count")
    ).filter(*query_filter).group_by(Order.project_name).order_by(
        func.count(Order.id).desc()
    ).limit(limit).all()
    
    if not project_stats:
        return success_response(data={"items": []})
    
    max_count = max(p[1] for p in project_stats)
    colors = ["#1890ff", "#52c41a", "#faad14", "#f5222d", "#722ed1", "#13c2c2", "#eb2f96"]
    
    items = [
        {
            "name": name or "未知项目",
            "count": count,
            "percent": round(count / max_count * 100) if max_count > 0 else 0,
            "color": colors[i % len(colors)]
        }
        for i, (name, count) in enumerate(project_stats)
    ]
    
    return success_response(data={"items": items})


@router.get("/trend")
async def get_consumption_trend(
    time_range: str = Query("month", description="时间范围"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取消费趋势"""
    now = datetime.now()
    
    if time_range == "week":
        # 最近7天
        dates = [(now - timedelta(days=i)).strftime("%m-%d") for i in range(6, -1, -1)]
        start_date = now - timedelta(days=7)
        date_format = "%Y-%m-%d"
    elif time_range == "month":
        # 最近6个月
        dates = []
        for i in range(5, -1, -1):
            d = now - timedelta(days=30*i)
            dates.append(d.strftime("%m月"))
        start_date = now - timedelta(days=180)
        date_format = "%Y-%m"
    else:
        # 最近12个月
        dates = []
        for i in range(11, -1, -1):
            d = now - timedelta(days=30*i)
            dates.append(d.strftime("%m月"))
        start_date = now - timedelta(days=365)
        date_format = "%Y-%m"
    
    # 查询消费数据
    orders = db.query(Order).filter(
        Order.user_id == current_user.id,
        Order.created_at >= start_date,
        Order.status.in_(["paid", "confirmed", "testing", "completed"])
    ).all()
    
    # 按日期聚合
    amount_by_date = {}
    for order in orders:
        if time_range == "week":
            key = order.created_at.strftime("%m-%d")
        else:
            key = order.created_at.strftime("%m月")
        amount_by_date[key] = amount_by_date.get(key, 0) + float(order.total_amount or 0)
    
    # 生成趋势数据
    max_amount = max(amount_by_date.values()) if amount_by_date else 1
    trend_data = [
        {
            "label": date,
            "amount": amount_by_date.get(date, 0),
            "height": round(amount_by_date.get(date, 0) / max_amount * 100) if max_amount > 0 else 0
        }
        for date in dates
    ]
    
    return success_response(data={"items": trend_data})


@router.get("/frequent-projects")
async def get_frequent_projects(
    limit: int = Query(5, ge=1, le=10),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取常用检测项目"""
    project_stats = db.query(
        Order.project_id,
        Order.project_name,
        func.count(Order.id).label("count")
    ).filter(
        Order.user_id == current_user.id
    ).group_by(
        Order.project_id, Order.project_name
    ).order_by(
        func.count(Order.id).desc()
    ).limit(limit).all()
    
    return success_response(data={
        "items": [
            {
                "id": project_id,
                "name": name or "未知项目",
                "count": count
            }
            for project_id, name, count in project_stats
        ]
    })


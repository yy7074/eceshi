"""积分发放服务。"""
from decimal import Decimal
from sqlalchemy.orm import Session

from app.models.points import PointsRecord
from app.models.user import User


def grant_order_points(db: Session, user: User, order_id: int, order_no: str, amount) -> int:
    """按订单实付金额发放积分，避免同一订单重复发放。"""
    paid_amount = Decimal(str(amount or 0))
    points = int(paid_amount)
    if points <= 0:
        return 0

    existing = db.query(PointsRecord).filter(
        PointsRecord.user_id == user.id,
        PointsRecord.type == "order",
        PointsRecord.related_id == order_id,
    ).first()
    if existing:
        return 0

    db.add(PointsRecord(
        user_id=user.id,
        points=points,
        type="order",
        related_id=order_id,
        description=f"订单{order_no}返积分"
    ))
    user.points_balance = (user.points_balance or 0) + points
    user.total_points_earned = (user.total_points_earned or 0) + points
    return points

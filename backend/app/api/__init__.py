"""
API路由汇总
"""
from fastapi import APIRouter

from app.api.v1 import auth, users, projects, orders, addresses, payments, upload, admin, favorites, reviews, points, coupons, invites, groups, recharge


# 创建主路由
router = APIRouter()

# 注册各模块路由
router.include_router(auth.router, prefix="/auth", tags=["认证"])
router.include_router(users.router, prefix="/users", tags=["用户"])
router.include_router(projects.router, prefix="/projects", tags=["检测项目"])
router.include_router(orders.router, prefix="/orders", tags=["订单"])
router.include_router(addresses.router, prefix="/addresses", tags=["地址管理"])
router.include_router(payments.router, prefix="/payments", tags=["支付"])
router.include_router(upload.router, prefix="/upload", tags=["文件上传"])
router.include_router(favorites.router, prefix="/favorites", tags=["收藏"])
router.include_router(reviews.router, prefix="/reviews", tags=["评价"])
router.include_router(points.router, prefix="/points", tags=["积分系统"])
router.include_router(coupons.router, prefix="/coupons", tags=["优惠券"])
router.include_router(invites.router, prefix="/invites", tags=["邀请好友"])
router.include_router(groups.router, prefix="/groups", tags=["团队功能"])
router.include_router(recharge.router, prefix="/recharge", tags=["钱包充值"])
router.include_router(admin.router, prefix="/admin", tags=["后台管理"])

"""
API路由汇总
"""
from fastapi import APIRouter

from app.api.v1 import auth, users, projects, orders, addresses, payments, upload, admin


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
router.include_router(admin.router, prefix="/admin", tags=["后台管理"])

"""
科研检测服务平台 - 后端主入口
FastAPI Application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.database import engine, Base
from app.api import router


# 应用生命周期管理
@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用启动和关闭时的生命周期管理"""
    # 启动时
    print("🚀 科研检测服务平台启动中...")
    print(f"📝 环境: {'开发' if settings.DEBUG else '生产'}")
    print(f"🔗 数据库: {settings.DATABASE_URL.split('@')[-1]}")
    
    # 创建数据库表（生产环境使用Alembic迁移）
    if settings.DEBUG:
        Base.metadata.create_all(bind=engine)
        print("✅ 数据库表创建完成")
    
    yield
    
    # 关闭时
    print("👋 科研检测服务平台关闭")


# 创建FastAPI应用
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="科研检测服务平台API - 对标eceshi.com",
    lifespan=lifespan,
    docs_url="/api/docs" if settings.DEBUG else None,
    redoc_url="/api/redoc" if settings.DEBUG else None,
)


# CORS中间件配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 全局异常处理
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """全局异常处理器"""
    return JSONResponse(
        status_code=500,
        content={
            "code": 500,
            "message": "服务器内部错误" if not settings.DEBUG else str(exc),
            "data": None
        }
    )


# 根路由
@app.get("/")
async def root():
    """根路由 - API欢迎信息"""
    return {
        "message": "欢迎使用科研检测服务平台API",
        "version": settings.APP_VERSION,
        "docs": "/api/docs",
        "status": "running"
    }


# 健康检查
@app.get("/health")
async def health_check():
    """健康检查接口"""
    return {
        "status": "healthy",
        "version": settings.APP_VERSION
    }


# 注册API路由
app.include_router(router, prefix="/api/v1")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )


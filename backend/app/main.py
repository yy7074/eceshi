"""
科研检测服务平台 - 后端主入口
FastAPI Application
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from pathlib import Path
from starlette.middleware.base import BaseHTTPMiddleware

from sqlalchemy.exc import OperationalError

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
    
    # 导入所有模型（确保SQLAlchemy能创建所有表）
    import app.models  # noqa: F401
    
    # 创建数据库表（生产环境使用Alembic迁移）
    if settings.DEBUG:
        try:
            Base.metadata.create_all(bind=engine)
            print("✅ 数据库表创建完成")
        except OperationalError as e:
            err_msg = str(getattr(e, "orig", e))
            # errno 13 = 权限不足，MySQL 无法在数据目录创建表文件；1005 = Can't create table
            if "errno: 13" in err_msg or "1005" in err_msg or "Can't create table" in err_msg:
                print("⚠️ 数据库表创建失败(可能权限不足 errno 13)，应用继续启动。")
                print("   请任选其一：1) 服务器执行 chown -R mysql:mysql <MySQL数据目录>")
                print("   2) 用 root 执行 migrations/create_lab_applications.sql 创建缺失表后重启。")
            else:
                raise
    
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


# 处理 X-Forwarded-Host 的中间件
class ProxyFixMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 如果存在 X-Forwarded-Host，使用它来修复重定向
        if "x-forwarded-host" in request.headers:
            request.scope["headers"] = [
                (k, v) if k != b"host" else (b"host", request.headers["x-forwarded-host"].encode())
                for k, v in request.scope["headers"]
            ]
        response = await call_next(request)
        return response

app.add_middleware(ProxyFixMiddleware)

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


# 挂载静态文件目录（必须在API路由之前）
static_dir = Path("static")
static_dir.mkdir(exist_ok=True)

# 挂载Web端用户网站（html=True 会自动处理 index.html）
web_dir = Path("static/web")
if web_dir.exists():
    # 添加 /web 路由，直接返回 index.html（避免重定向到 127.0.0.1）
    @app.get("/web")
    async def web_index():
        """直接返回 web/index.html"""
        index_file = web_dir / "index.html"
        if index_file.exists():
            return FileResponse(index_file)
        return {"error": "Web page not found"}
    
    # 挂载 /web/ 路径下的静态文件
    app.mount("/web/", StaticFiles(directory="static/web", html=True), name="web")

# 挂载后台管理页面（html=True 会自动处理 index.html）
admin_dir = Path("admin")
if admin_dir.exists():
    # 添加 /admin 路由，直接返回 index.html（避免重定向到 127.0.0.1）
    @app.get("/admin")
    async def admin_index():
        """直接返回 admin/index.html"""
        index_file = admin_dir / "index.html"
        if index_file.exists():
            return FileResponse(index_file)
        return {"error": "Admin page not found"}
    
    # 挂载 /admin/ 路径下的静态文件
    app.mount("/admin/", StaticFiles(directory="admin", html=True), name="admin")

# 挂载静态文件
app.mount("/static", StaticFiles(directory="static"), name="static")

# 注册API路由（放在最后）
app.include_router(router, prefix="/api/v1")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )


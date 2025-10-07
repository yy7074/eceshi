"""
数据库配置
SQLAlchemy配置和会话管理
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Generator

from app.core.config import settings


# 创建数据库引擎
engine = create_engine(
    settings.DATABASE_URL,
    pool_size=settings.DATABASE_POOL_SIZE,
    max_overflow=settings.DATABASE_MAX_OVERFLOW,
    pool_pre_ping=True,  # 连接池预检查
    pool_recycle=3600,   # 连接回收时间
    echo=settings.DEBUG,  # SQL日志
)

# 创建会话工厂
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# 创建基类
Base = declarative_base()


# 数据库会话依赖
def get_db() -> Generator:
    """
    获取数据库会话
    使用依赖注入，自动管理会话生命周期
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


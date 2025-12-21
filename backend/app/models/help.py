"""帮助中心模型"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.sql import func
from app.core.database import Base


class HelpCategory(Base):
    """帮助分类"""
    __tablename__ = "help_categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, comment="分类名称")
    icon = Column(String(100), comment="图标")
    sort_order = Column(Integer, default=0, comment="排序")
    is_active = Column(Boolean, default=True, comment="是否启用")
    created_at = Column(DateTime, server_default=func.now())


class HelpArticle(Base):
    """帮助文章"""
    __tablename__ = "help_articles"
    
    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, nullable=False, index=True, comment="分类ID")
    title = Column(String(200), nullable=False, comment="标题")
    content = Column(Text, nullable=False, comment="内容")
    is_hot = Column(Boolean, default=False, comment="是否热门")
    view_count = Column(Integer, default=0, comment="查看次数")
    sort_order = Column(Integer, default=0, comment="排序")
    is_active = Column(Boolean, default=True, comment="是否启用")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


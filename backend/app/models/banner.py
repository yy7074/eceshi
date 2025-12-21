"""Banner/轮播图模型"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.sql import func
from app.core.database import Base


class Banner(Base):
    """轮播图"""
    __tablename__ = "banners"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, comment="标题")
    subtitle = Column(String(500), comment="副标题")
    image = Column(String(500), nullable=False, comment="图片URL")
    link_type = Column(String(50), default="none", comment="链接类型: none/project/url/page")
    link_value = Column(String(500), comment="链接值")
    button_text = Column(String(50), comment="按钮文字")
    sort_order = Column(Integer, default=0, comment="排序")
    is_active = Column(Boolean, default=True, comment="是否启用")
    position = Column(String(50), default="home", comment="展示位置: home/category/other")
    start_time = Column(DateTime, comment="开始时间")
    end_time = Column(DateTime, comment="结束时间")
    click_count = Column(Integer, default=0, comment="点击次数")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


"""
检测项目相关API
项目列表、详情、分类等
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.core.database import get_db
from app.core.response import Response


router = APIRouter()


@router.get("/categories", summary="获取项目分类")
async def get_project_categories(
    db: Session = Depends(get_db)
):
    """
    获取检测项目分类
    对标eceshi: 电镜专场、材料测试、生物医学、环境检测等
    """
    # TODO: 从数据库查询分类
    categories = [
        {
            "id": 1,
            "name": "电镜专场",
            "icon": "https://example.com/icon1.png",
            "description": "SEM、TEM、EPMA、AFM、EBSD系列",
            "hot": True
        },
        {
            "id": 2,
            "name": "材料测试",
            "icon": "https://example.com/icon2.png",
            "description": "组织形貌、成分含量、化学结构、物理性能",
            "hot": True
        },
        {
            "id": 3,
            "name": "生物医学",
            "icon": "https://example.com/icon3.png",
            "description": "细胞检测、蛋白质分析、基因检测",
            "hot": False
        },
        {
            "id": 4,
            "name": "环境检测",
            "icon": "https://example.com/icon4.png",
            "description": "水质、土壤、气体、固废检测",
            "hot": False
        }
    ]
    
    return Response.success(data=categories)


@router.get("/list", summary="获取项目列表")
async def get_projects(
    category_id: Optional[int] = Query(None, description="分类ID"),
    keyword: Optional[str] = Query(None, description="搜索关键词"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    db: Session = Depends(get_db)
):
    """
    获取检测项目列表
    支持分类筛选、关键词搜索、分页
    """
    # TODO: 从数据库查询项目列表
    projects = [
        {
            "id": 1,
            "name": "场发射扫描电镜（SEM）",
            "category": "电镜专场",
            "original_price": 400.00,
            "current_price": 312.00,
            "satisfaction": 99,
            "booking_count": 10987,
            "service_cycle_min": 2.5,
            "service_cycle_max": 6.0,
            "equipment_model": "日本 JEOL JSM-7800F",
            "lab_name": "某985高校材料实验室",
            "cover_image": "https://example.com/project1.jpg"
        },
        {
            "id": 2,
            "name": "凝胶渗透色谱（GPC）",
            "category": "材料测试",
            "original_price": 350.00,
            "current_price": 280.00,
            "satisfaction": 98,
            "booking_count": 8765,
            "service_cycle_min": 3.0,
            "service_cycle_max": 7.0,
            "equipment_model": "美国 Agilent-1260 Infinity II",
            "lab_name": "某211高校化学实验室",
            "cover_image": "https://example.com/project2.jpg"
        }
    ]
    
    return Response.success(data={
        "list": projects,
        "total": len(projects),
        "page": page,
        "page_size": page_size
    })


@router.get("/{project_id}", summary="获取项目详情")
async def get_project_detail(
    project_id: int,
    db: Session = Depends(get_db)
):
    """
    获取检测项目详情
    包含项目介绍、预约须知、样品要求、常见问题、结果展示等
    """
    # TODO: 从数据库查询项目详情
    project = {
        "id": project_id,
        "name": "场发射扫描电镜（SEM）",
        "category": "电镜专场",
        "original_price": 400.00,
        "current_price": 312.00,
        "satisfaction": 99,
        "booking_count": 10987,
        "service_cycle_min": 2.5,
        "service_cycle_max": 6.0,
        "equipment_model": "日本 JEOL JSM-7800F",
        "lab_name": "某985高校材料实验室",
        "lab_id": 1,
        "cover_image": "https://example.com/project1.jpg",
        "images": [
            "https://example.com/project1-1.jpg",
            "https://example.com/project1-2.jpg"
        ],
        "introduction": "扫描电子显微镜（SEM）是一种高分辨率的显微镜...",
        "booking_notice": "1. 请提前预约\n2. 样品需要满足要求\n3. ...",
        "sample_requirements": "样品类型：固体、粉末、薄膜\n样品尺寸：不超过20mm...",
        "faq": [
            {
                "question": "样品需要喷金吗？",
                "answer": "不导电样品需要喷金处理"
            },
            {
                "question": "多久能拿到数据？",
                "answer": "正常3-5个工作日"
            }
        ],
        "result_samples": [
            {
                "title": "样品案例1",
                "image": "https://example.com/result1.jpg"
            }
        ]
    }
    
    return Response.success(data=project)


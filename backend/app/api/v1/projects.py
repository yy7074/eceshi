"""
检测项目相关API
项目列表、详情、分类等
"""
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel
from decimal import Decimal

from app.core.database import get_db
from app.core.response import Response
from app.models.project import ProjectCategory, Project
from app.api.v1.deps import get_current_user
from app.models.user import User


router = APIRouter()


class ProjectCreate(BaseModel):
    """创建项目请求"""
    project_no: str
    name: str
    category_id: int
    lab_id: int = 1  # 默认实验室ID
    original_price: Decimal
    current_price: Decimal
    unit: str = "样品"
    service_cycle_min: Optional[int] = None
    service_cycle_max: Optional[int] = None
    equipment_name: Optional[str] = None
    equipment_model: Optional[str] = None
    introduction: Optional[str] = None
    sample_requirements: Optional[str] = None
    cover_image: Optional[str] = None
    is_hot: bool = False
    is_recommended: bool = False
    sort_order: int = 0


class ProjectUpdate(BaseModel):
    """更新项目请求"""
    name: Optional[str] = None
    category_id: Optional[int] = None
    original_price: Optional[Decimal] = None
    current_price: Optional[Decimal] = None
    unit: Optional[str] = None
    service_cycle_min: Optional[int] = None
    service_cycle_max: Optional[int] = None
    equipment_name: Optional[str] = None
    equipment_model: Optional[str] = None
    introduction: Optional[str] = None
    sample_requirements: Optional[str] = None
    cover_image: Optional[str] = None
    is_hot: Optional[bool] = None
    is_recommended: Optional[bool] = None
    sort_order: Optional[int] = None
    status: Optional[str] = None


@router.get("/categories", summary="获取项目分类")
async def get_project_categories(
    db: Session = Depends(get_db)
):
    """获取检测项目分类"""
    categories = db.query(ProjectCategory).filter(
        ProjectCategory.is_active == True
    ).order_by(ProjectCategory.sort_order).all()
    
    return Response.success(data=[{
        "id": cat.id,
        "name": cat.name,
        "description": cat.description,
        "icon": cat.icon,
        "sort_order": cat.sort_order
    } for cat in categories])


@router.get("/admin/list", summary="获取项目列表（管理员）")
async def get_admin_projects_list(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    category_id: Optional[int] = None,
    status: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取项目列表（管理员）
    - 支持分页、搜索、筛选
    """
    query = db.query(Project)
    
    # 搜索
    if search:
        query = query.filter(
            (Project.name.like(f"%{search}%")) |
            (Project.project_no.like(f"%{search}%"))
        )
    
    # 按分类筛选
    if category_id:
        query = query.filter(Project.category_id == category_id)
    
    # 按状态筛选
    if status:
        query = query.filter(Project.status == status)
    
    # 总数
    total = query.count()
    
    # 分页
    offset = (page - 1) * page_size
    projects = query.order_by(Project.sort_order, Project.created_at.desc()).offset(offset).limit(page_size).all()
    
    # 获取分类信息
    category_map = {cat.id: cat.name for cat in db.query(ProjectCategory).all()}
    
    return Response.success(data={
        "list": [{
            "id": p.id,
            "project_no": p.project_no,
            "name": p.name,
            "category_id": p.category_id,
            "category_name": category_map.get(p.category_id, "未知"),
            "original_price": float(p.original_price),
            "current_price": float(p.current_price),
            "unit": p.unit,
            "cover_image": p.cover_image,
            "status": p.status,
            "is_hot": p.is_hot,
            "is_recommended": p.is_recommended,
            "view_count": p.view_count,
            "booking_count": p.booking_count,
            "sort_order": p.sort_order,
            "created_at": p.created_at.isoformat() if p.created_at else None
        } for p in projects],
        "total": total,
        "page": page,
        "page_size": page_size
    })


@router.get("/admin/{project_id}", summary="获取项目详情（管理员）")
async def get_admin_project_detail(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取项目详情"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")
    
    return Response.success(data={
        "id": project.id,
        "project_no": project.project_no,
        "name": project.name,
        "category_id": project.category_id,
        "lab_id": project.lab_id,
        "original_price": float(project.original_price),
        "current_price": float(project.current_price),
        "unit": project.unit,
        "service_cycle_min": project.service_cycle_min,
        "service_cycle_max": project.service_cycle_max,
        "equipment_name": project.equipment_name,
        "equipment_model": project.equipment_model,
        "introduction": project.introduction,
        "sample_requirements": project.sample_requirements,
        "cover_image": project.cover_image,
        "status": project.status,
        "is_hot": project.is_hot,
        "is_recommended": project.is_recommended,
        "view_count": project.view_count,
        "booking_count": project.booking_count,
        "satisfaction": float(project.satisfaction) if project.satisfaction else 100.0,
        "sort_order": project.sort_order,
        "created_at": project.created_at.isoformat() if project.created_at else None,
        "updated_at": project.updated_at.isoformat() if project.updated_at else None
    })


@router.post("/admin/create", summary="创建项目（管理员）")
async def create_project(
    request: ProjectCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """创建新项目"""
    # 检查项目编号是否已存在
    existing = db.query(Project).filter(Project.project_no == request.project_no).first()
    if existing:
        raise HTTPException(status_code=400, detail="项目编号已存在")
    
    # 创建项目
    project = Project(
        project_no=request.project_no,
        name=request.name,
        category_id=request.category_id,
        lab_id=request.lab_id,
        original_price=request.original_price,
        current_price=request.current_price,
        unit=request.unit,
        service_cycle_min=request.service_cycle_min,
        service_cycle_max=request.service_cycle_max,
        equipment_name=request.equipment_name,
        equipment_model=request.equipment_model,
        introduction=request.introduction,
        sample_requirements=request.sample_requirements,
        cover_image=request.cover_image,
        is_hot=request.is_hot,
        is_recommended=request.is_recommended,
        sort_order=request.sort_order,
        status="active"
    )
    
    db.add(project)
    db.commit()
    db.refresh(project)
    
    return Response.success(data={"id": project.id}, message="项目创建成功")


@router.put("/admin/{project_id}", summary="更新项目（管理员）")
async def update_project(
    project_id: int,
    request: ProjectUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新项目信息"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")
    
    # 更新字段
    update_data = request.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(project, field, value)
    
    db.commit()
    return Response.success(message="项目更新成功")


@router.delete("/admin/{project_id}", summary="删除项目（管理员）")
async def delete_project(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """删除项目"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")
    
    db.delete(project)
    db.commit()
    
    return Response.success(message="项目删除成功")


@router.put("/admin/{project_id}/status", summary="更新项目状态（管理员）")
async def update_project_status(
    project_id: int,
    status: str = Query(..., description="状态: active/inactive"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新项目状态"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")
    
    project.status = status
    db.commit()
    
    return Response.success(message="状态更新成功")


# 前端用户接口
@router.get("/old-categories", summary="获取项目分类(OLD)")
async def get_old_project_categories(
    db: Session = Depends(get_db)
):
    """
    获取检测项目分类（旧接口，保留兼容性）
    对标eceshi: 电镜专场、材料测试、生物医学、环境检测等
    """
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


"""
文件上传API
"""
from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
import os
import uuid
from datetime import datetime
from pathlib import Path

from app.core.database import get_db
from app.core.response import Response
from app.core.config import settings
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter()

# 上传目录
UPLOAD_DIR = Path("static/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# 允许的文件类型
ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB


def allowed_file(filename: str) -> bool:
    """检查文件类型是否允许"""
    return Path(filename).suffix.lower() in ALLOWED_EXTENSIONS


@router.post("/image", summary="上传图片")
async def upload_image(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    上传图片
    
    - 支持格式：jpg, jpeg, png, gif, webp, svg
    - 最大大小：10MB
    - 返回图片URL
    """
    # 检查文件类型
    if not allowed_file(file.filename):
        raise HTTPException(
            status_code=400,
            detail=f"不支持的文件类型。允许的类型: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    # 读取文件内容
    contents = await file.read()
    
    # 检查文件大小
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"文件过大。最大允许: {MAX_FILE_SIZE / 1024 / 1024}MB"
        )
    
    # 生成唯一文件名
    ext = Path(file.filename).suffix
    filename = f"{uuid.uuid4().hex}{ext}"
    
    # 按日期组织目录
    date_dir = UPLOAD_DIR / datetime.now().strftime("%Y%m%d")
    date_dir.mkdir(parents=True, exist_ok=True)
    
    # 保存文件
    file_path = date_dir / filename
    with open(file_path, "wb") as f:
        f.write(contents)
    
    # 生成访问URL
    url = f"/static/uploads/{datetime.now().strftime('%Y%m%d')}/{filename}"
    
    return Response.success(
        data={
            "url": url,
            "filename": file.filename,
            "size": len(contents),
            "content_type": file.content_type
        },
        message="上传成功"
    )


@router.post("/images", summary="批量上传图片")
async def upload_images(
    files: List[UploadFile] = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    批量上传图片
    
    - 最多同时上传10张
    - 支持格式：jpg, jpeg, png, gif, webp, svg
    - 单个文件最大：10MB
    """
    if len(files) > 10:
        raise HTTPException(status_code=400, detail="最多同时上传10个文件")
    
    results = []
    errors = []
    
    for file in files:
        try:
            # 检查文件类型
            if not allowed_file(file.filename):
                errors.append({
                    "filename": file.filename,
                    "error": "不支持的文件类型"
                })
                continue
            
            # 读取文件内容
            contents = await file.read()
            
            # 检查文件大小
            if len(contents) > MAX_FILE_SIZE:
                errors.append({
                    "filename": file.filename,
                    "error": "文件过大"
                })
                continue
            
            # 生成唯一文件名
            ext = Path(file.filename).suffix
            filename = f"{uuid.uuid4().hex}{ext}"
            
            # 按日期组织目录
            date_dir = UPLOAD_DIR / datetime.now().strftime("%Y%m%d")
            date_dir.mkdir(parents=True, exist_ok=True)
            
            # 保存文件
            file_path = date_dir / filename
            with open(file_path, "wb") as f:
                f.write(contents)
            
            # 生成访问URL
            url = f"/static/uploads/{datetime.now().strftime('%Y%m%d')}/{filename}"
            
            results.append({
                "url": url,
                "filename": file.filename,
                "size": len(contents)
            })
            
        except Exception as e:
            errors.append({
                "filename": file.filename,
                "error": str(e)
            })
    
    return Response.success(
        data={
            "success": results,
            "errors": errors,
            "total": len(files),
            "success_count": len(results),
            "error_count": len(errors)
        },
        message=f"上传完成：成功{len(results)}个，失败{len(errors)}个"
    )


@router.delete("/image", summary="删除图片")
async def delete_image(
    url: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    删除图片
    
    - 需要管理员权限
    - 传入图片URL
    """
    try:
        # 从URL提取文件路径
        if not url.startswith("/static/uploads/"):
            raise HTTPException(status_code=400, detail="无效的图片URL")
        
        file_path = Path(url.replace("/static/uploads/", "static/uploads/"))
        
        # 检查文件是否存在
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="文件不存在")
        
        # 删除文件
        file_path.unlink()
        
        return Response.success(message="删除成功")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除失败: {str(e)}")


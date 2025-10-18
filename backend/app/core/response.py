"""
统一响应格式
"""
from typing import Any, Optional
from fastapi.responses import JSONResponse


class Response:
    """统一响应格式"""
    
    @staticmethod
    def success(data: Any = None, message: str = "操作成功", code: int = 200) -> dict:
        """成功响应"""
        return {
            "code": code,
            "message": message,
            "data": data
        }
    
    @staticmethod
    def error(message: str = "操作失败", code: int = 400, data: Any = None) -> dict:
        """错误响应"""
        return {
            "code": code,
            "message": message,
            "data": data
        }
    
    @staticmethod
    def unauthorized(message: str = "未授权") -> dict:
        """未授权响应"""
        return {
            "code": 401,
            "message": message,
            "data": None
        }
    
    @staticmethod
    def forbidden(message: str = "禁止访问") -> dict:
        """禁止访问响应"""
        return {
            "code": 403,
            "message": message,
            "data": None
        }
    
    @staticmethod
    def not_found(message: str = "资源不存在") -> dict:
        """资源不存在响应"""
        return {
            "code": 404,
            "message": message,
            "data": None
        }


# 兼容性：为旧代码提供别名
class SuccessResponse(dict):
    """成功响应（兼容性）"""
    def __init__(self, data: Any = None, message: str = "操作成功", code: int = 200):
        super().__init__(code=code, message=message, data=data)


class ErrorResponse(dict):
    """错误响应（兼容性）"""
    def __init__(self, message: str = "操作失败", code: int = 400, data: Any = None):
        super().__init__(code=code, message=message, data=data)


"""
配置管理
使用pydantic-settings管理环境变量
"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """应用配置"""
    
    # 应用配置
    APP_NAME: str = "科研检测服务平台"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    SECRET_KEY: str = "dev-secret-key-change-in-production"
    
    # 服务器配置
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # 数据库配置
    DATABASE_URL: str = "mysql+pymysql://root:password@localhost:3306/eceshi?charset=utf8mb4"
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20
    
    # Redis配置
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: str = ""
    
    # JWT配置
    JWT_SECRET_KEY: str = "jwt-secret-key"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24小时
    
    # 阿里云OSS配置
    ALIYUN_OSS_ACCESS_KEY_ID: str = ""
    ALIYUN_OSS_ACCESS_KEY_SECRET: str = ""
    ALIYUN_OSS_ENDPOINT: str = "oss-cn-hangzhou.aliyuncs.com"
    ALIYUN_OSS_BUCKET: str = "eceshi-files"
    
    # 微信小程序配置
    WECHAT_APPID: str = ""
    WECHAT_SECRET: str = ""
    
    # 支付宝配置
    ALIPAY_APPID: str = ""
    ALIPAY_PRIVATE_KEY_PATH: str = "./keys/alipay_private_key.pem"
    ALIPAY_PUBLIC_KEY_PATH: str = "./keys/alipay_public_key.pem"
    ALIPAY_GATEWAY: str = "https://openapi.alipay.com/gateway.do"
    
    # CORS配置
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8080"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# 创建全局配置实例
settings = Settings()


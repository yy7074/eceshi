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
    VERSION: str = "1.0.0"  # 兼容性
    DEBUG: bool = True
    SECRET_KEY: str = "dev-secret-key-change-in-production"
    ALLOWED_HOSTS: List[str] = ["*"]
    
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
    REDIS_URL: str = "redis://localhost:6379/0"  # 兼容性
    
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
    
    # 微信支付配置
    WECHAT_MCH_ID: str = ""  # 微信商户号
    WECHAT_PAY_KEY: str = ""  # API密钥
    WECHAT_PAY_NOTIFY_URL: str = "https://catdog.dachaonet.com/api/v1/payments/wechat/notify"
    
    # 阿里云短信配置
    SMS_ACCESS_KEY: str = ""
    SMS_SECRET_KEY: str = ""
    SMS_SIGN_NAME: str = "科研检测"
    SMS_TEMPLATE_ID: str = ""  # 验证码短信模板ID
    SMS_REGION: str = "cn-hangzhou"
    
    # 支付宝配置
    ALIPAY_APP_ID: str = ""
    ALIPAY_PRIVATE_KEY: str = ""  # 应用私钥字符串
    ALIPAY_PUBLIC_KEY: str = ""  # 支付宝公钥字符串
    ALIPAY_GATEWAY: str = "https://openapi.alipay.com/gateway.do"  # 正式环境
    # ALIPAY_GATEWAY: str = "https://openapi.alipaydev.com/gateway.do"  # 沙箱环境
    
    # 文件上传配置（兼容性）
    UPLOAD_DIR: str = "static/uploads"
    MAX_FILE_SIZE: int = 10485760  # 10MB
    ALLOWED_EXTENSIONS: str = ".jpg,.jpeg,.png,.gif,.webp"
    
    # CORS配置
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8080"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # 忽略额外的配置项，避免验证错误


# 创建全局配置实例
settings = Settings()


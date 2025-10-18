"""
阿里云短信服务
"""
from alibabacloud_dysmsapi20170525.client import Client as Dysmsapi20170525Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_dysmsapi20170525 import models as dysmsapi_20170525_models
from alibabacloud_tea_util import models as util_models
import random
import asyncio
from typing import Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.sms_code import SMSCode
import logging

logger = logging.getLogger(__name__)


class SMSService:
    """阿里云短信服务"""
    
    def __init__(self):
        """初始化短信客户端"""
        self.client = self._create_client()
    
    def _create_client(self) -> Optional[Dysmsapi20170525Client]:
        """创建阿里云短信客户端"""
        if not settings.SMS_ACCESS_KEY or not settings.SMS_SECRET_KEY:
            logger.warning("短信服务配置不完整，将使用开发模式")
            return None
            
        config = open_api_models.Config(
            access_key_id=settings.SMS_ACCESS_KEY,
            access_key_secret=settings.SMS_SECRET_KEY,
            endpoint=f"dysmsapi.aliyuncs.com"
        )
        return Dysmsapi20170525Client(config)
    
    async def send_verification_code(
        self, 
        phone: str, 
        db: Session,
        scene: str = "login"
    ) -> dict:
        """
        发送验证码短信
        
        Args:
            phone: 手机号
            db: 数据库会话
            scene: 使用场景(register/login/reset_password)
        
        Returns:
            dict: 发送结果
        """
        try:
            # 生成6位数字验证码
            code = str(random.randint(100000, 999999))
            
            # 如果是开发环境或未配置短信服务，使用固定验证码
            if settings.DEBUG or not self.client:
                logger.info(f"开发模式：手机号 {phone} 的验证码是 {code}")
                # 存储验证码到数据库
                await self._store_verification_code(phone, code, db, scene)
                return {
                    "success": True,
                    "message": "验证码发送成功（开发模式）",
                    "code": code  # 开发环境返回验证码，生产环境应删除此字段
                }
            
            # 生产环境：调用阿里云短信API
            send_sms_request = dysmsapi_20170525_models.SendSmsRequest(
                phone_numbers=phone,
                sign_name=settings.SMS_SIGN_NAME,
                template_code=settings.SMS_TEMPLATE_ID,
                template_param=f'{{"code":"{code}"}}'
            )
            
            runtime = util_models.RuntimeOptions()
            
            # 发送短信（需要在事件循环中执行）
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None, 
                self.client.send_sms_with_options,
                send_sms_request, 
                runtime
            )
            
            # 存储验证码到数据库
            await self._store_verification_code(phone, code, db, scene)
            
            logger.info(f"短信发送成功：手机号 {phone}, BizId: {response.body.biz_id}")
            
            return {
                "success": True,
                "message": "验证码发送成功",
                "biz_id": response.body.biz_id
            }
            
        except Exception as e:
            logger.error(f"发送短信验证码失败: {str(e)}")
            return {
                "success": False,
                "message": f"发送失败: {str(e)}"
            }
    
    async def verify_code(
        self, 
        phone: str, 
        code: str, 
        db: Session,
        scene: str = None
    ) -> bool:
        """
        验证验证码
        
        Args:
            phone: 手机号
            code: 验证码
            db: 数据库会话
            scene: 使用场景(可选)
        
        Returns:
            bool: 验证是否成功
        """
        try:
            # 查询条件
            query = db.query(SMSCode).filter(
                SMSCode.phone == phone,
                SMSCode.code == code,
                SMSCode.is_used == False,
                SMSCode.expires_at > datetime.utcnow()
            )
            
            # 如果指定了场景，添加场景过滤
            if scene:
                query = query.filter(SMSCode.scene == scene)
            
            sms_code = query.first()
            
            if not sms_code:
                logger.warning(f"验证码验证失败：手机号 {phone}, 验证码 {code}")
                return False
            
            # 标记为已使用
            sms_code.is_used = True
            db.commit()
            
            logger.info(f"验证码验证成功：手机号 {phone}")
            return True
            
        except Exception as e:
            logger.error(f"验证短信验证码失败: {str(e)}")
            db.rollback()
            return False
    
    async def _store_verification_code(
        self, 
        phone: str, 
        code: str, 
        db: Session,
        scene: str = "login"
    ):
        """
        存储验证码到数据库
        
        Args:
            phone: 手机号
            code: 验证码
            db: 数据库会话
            scene: 使用场景
        """
        try:
            # 先删除该手机号的旧验证码
            db.query(SMSCode).filter(
                SMSCode.phone == phone,
                SMSCode.scene == scene
            ).delete()
            
            # 创建新的验证码记录，5分钟后过期
            expires_at = datetime.utcnow() + timedelta(minutes=5)
            sms_code = SMSCode(
                phone=phone,
                code=code,
                scene=scene,
                expires_at=expires_at
            )
            
            db.add(sms_code)
            db.commit()
            
            logger.info(f"验证码已存储：手机号 {phone}, 场景 {scene}")
            
        except Exception as e:
            logger.error(f"存储验证码失败: {str(e)}")
            db.rollback()
            raise


# 创建全局实例
sms_service = SMSService()


"""
微信小程序登录服务
"""
import httpx
import logging
from typing import Optional, Dict
from app.core.config import settings

logger = logging.getLogger(__name__)


class WechatService:
    """微信小程序服务"""
    
    def __init__(self):
        self.appid = settings.WECHAT_APPID
        self.secret = settings.WECHAT_SECRET
        self.code2session_url = "https://api.weixin.qq.com/sns/jscode2session"
    
    async def code_to_session(self, code: str) -> Dict:
        """
        使用code换取openid和session_key
        
        Args:
            code: 微信登录code
            
        Returns:
            {
                "openid": "用户唯一标识",
                "session_key": "会话密钥",
                "unionid": "用户在开放平台的唯一标识（如果有）",
                "errcode": 0,
                "errmsg": ""
            }
        """
        try:
            # 开发环境返回模拟数据
            if settings.DEBUG and not self.appid:
                logger.info(f"开发模式：微信登录code={code}")
                return {
                    "openid": f"test_openid_{code[-6:]}",
                    "session_key": "test_session_key",
                    "unionid": None,
                    "errcode": 0,
                    "errmsg": "ok"
                }
            
            # 调用微信API
            params = {
                "appid": self.appid,
                "secret": self.secret,
                "js_code": code,
                "grant_type": "authorization_code"
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get(self.code2session_url, params=params)
                result = response.json()
                
                if "errcode" in result and result["errcode"] != 0:
                    logger.error(f"微信code2session失败: {result}")
                    return result
                
                logger.info(f"微信code2session成功: openid={result.get('openid')}")
                return result
                
        except Exception as e:
            logger.error(f"微信code2session异常: {str(e)}")
            return {
                "errcode": -1,
                "errmsg": f"请求失败: {str(e)}"
            }


# 创建全局实例
wechat_service = WechatService()


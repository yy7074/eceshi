"""
微信小程序登录服务
"""
import httpx
import logging
from typing import Optional, Dict
from app.core.config import settings
from app.core.redis_client import get_redis

logger = logging.getLogger(__name__)

ACCESS_TOKEN_REDIS_KEY = "wechat:access_token"


class WechatService:
    """微信小程序服务"""

    def __init__(self):
        self.appid = settings.WECHAT_APPID
        self.secret = settings.WECHAT_SECRET
        self.code2session_url = "https://api.weixin.qq.com/sns/jscode2session"
        self.token_url = "https://api.weixin.qq.com/cgi-bin/token"
        self.qrcode_unlimited_url = "https://api.weixin.qq.com/wxa/getwxacodeunlimit"
    
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

    async def get_access_token(self) -> str:
        """
        获取小程序 access_token。Redis 缓存，过期前 5 分钟刷新。
        """
        r = get_redis()
        cached = r.get(ACCESS_TOKEN_REDIS_KEY)
        if cached:
            return cached

        params = {
            "grant_type": "client_credential",
            "appid": self.appid,
            "secret": self.secret,
        }
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(self.token_url, params=params)
            data = resp.json()

        if "access_token" not in data:
            logger.error(f"获取 access_token 失败: {data}")
            raise RuntimeError(f"获取 access_token 失败: {data.get('errmsg', data)}")

        token = data["access_token"]
        expires_in = int(data.get("expires_in", 7200))
        r.set(ACCESS_TOKEN_REDIS_KEY, token, ex=max(expires_in - 300, 60))
        return token

    async def get_unlimited_qrcode(
        self,
        scene: str,
        page: str = "pages/login/login",
        env_version: str = "release",
    ) -> bytes:
        """
        调用 wxacode.getUnlimited 生成带参二维码（PNG 二进制）。

        scene: 最多 32 字符，限 a-zA-Z0-9!#$&'()*+,/:;=?@-._~
        page: 扫码打开的小程序页面路径
        env_version: release | trial | develop
        """
        access_token = await self.get_access_token()
        payload = {
            "scene": scene,
            "page": page,
            "check_path": False,
            "env_version": env_version,
            "width": 280,
        }
        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.post(
                self.qrcode_unlimited_url,
                params={"access_token": access_token},
                json=payload,
            )
            content_type = resp.headers.get("content-type", "")
            # 错误时微信返回 JSON
            if content_type.startswith("application/json") or content_type.startswith("text/plain"):
                data = resp.json()
                logger.error(f"生成小程序二维码失败: {data}")
                # 40001: access_token 过期/无效 - 清缓存重试一次
                if data.get("errcode") == 40001:
                    get_redis().delete(ACCESS_TOKEN_REDIS_KEY)
                raise RuntimeError(
                    f"生成小程序二维码失败: errcode={data.get('errcode')} {data.get('errmsg', '')}"
                )
            return resp.content


# 创建全局实例
wechat_service = WechatService()


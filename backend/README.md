# 后端 API 文档

## 启动项目

```bash
# 安装依赖
pip install -r requirements.txt

# 启动开发服务器
python -m app.main

# 或使用uvicorn
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API 文档

启动后访问:
- Swagger UI: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc

## API 接口列表

### 认证模块 (`/api/v1/auth`)

| 接口 | 方法 | 说明 |
|------|------|------|
| `/auth/send-sms` | POST | 发送短信验证码 |
| `/auth/register` | POST | 用户注册 |
| `/auth/login` | POST | 用户登录 |
| `/auth/wechat-login` | POST | 微信小程序登录 |

### 用户模块 (`/api/v1/users`)

| 接口 | 方法 | 说明 | 需要认证 |
|------|------|------|---------|
| `/users/me` | GET | 获取当前用户信息 | ✅ |
| `/users/me` | PUT | 更新用户信息 | ✅ |
| `/users/certification` | POST | 提交实名认证 | ✅ |
| `/users/certification` | GET | 获取认证信息 | ✅ |
| `/users/balance` | GET | 获取账户余额 | ✅ |

### 检测项目模块 (`/api/v1/projects`)

| 接口 | 方法 | 说明 |
|------|------|------|
| `/projects/categories` | GET | 获取项目分类 |
| `/projects/list` | GET | 获取项目列表 |
| `/projects/{id}` | GET | 获取项目详情 |

## 响应格式

### 成功响应
```json
{
  "code": 200,
  "message": "操作成功",
  "data": { ... }
}
```

### 错误响应
```json
{
  "code": 400,
  "message": "错误信息",
  "data": null
}
```

## 认证

使用 JWT Bearer Token 认证:

```
Authorization: Bearer <access_token>
```

登录/注册成功后会返回 `access_token`，将其添加到请求头即可。

## 环境变量

复制 `.env.example` 为 `.env` 并配置:

```bash
# 数据库
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/eceshi?charset=utf8mb4

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379

# JWT
JWT_SECRET_KEY=your-secret-key

# 阿里云OSS
ALIYUN_OSS_ACCESS_KEY_ID=xxx
ALIYUN_OSS_ACCESS_KEY_SECRET=xxx
```


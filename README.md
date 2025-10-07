# 科研检测服务平台

> 对标 eceshi.com 的一站式科研检测服务平台

## 📋 项目简介

科研检测服务平台是一个连接实验室资源与科研用户需求的在线服务平台，提供检测项目预约、云现场服务、实验室加盟、会员权益等功能。

### 核心功能

- ✅ 用户注册登录、实名认证
- ✅ 检测项目浏览、预约下单
- ⭐ 云现场服务（按小时预约设备）
- ⭐ 发布需求（用户主动发布，实验室竞标）
- ⭐ 实验室加盟合作生态
- ⭐ 会员权益体系（预付有礼）
- ⭐ 专属顾问1v1服务

## 🏗️ 技术栈

### 后端
- **框架**: Python 3.10+ / FastAPI
- **数据库**: MySQL 8.0 + Redis
- **ORM**: SQLAlchemy
- **认证**: JWT
- **文档**: Swagger/OpenAPI

### 前端
- **框架**: uni-app
- **支持平台**: 
  - 微信小程序
  - 支付宝小程序
  - H5网站（PC + 移动端）
  - App（iOS + Android）

## 📁 项目结构

```
eceshi/
├── backend/              # Python后端
│   ├── app/
│   │   ├── api/         # API路由
│   │   │   └── v1/      # v1版本API
│   │   ├── core/        # 核心配置
│   │   ├── models/      # 数据库模型
│   │   ├── schemas/     # Pydantic模型
│   │   ├── services/    # 业务逻辑
│   │   └── utils/       # 工具函数
│   ├── tests/           # 测试
│   ├── requirements.txt # 依赖包
│   └── .env            # 环境变量
│
├── frontend/            # uni-app前端
│   ├── pages/          # 页面
│   ├── components/     # 组件
│   ├── static/         # 静态资源
│   ├── store/          # 状态管理
│   ├── utils/          # 工具函数
│   ├── manifest.json   # 应用配置
│   └── pages.json      # 页面配置
│
└── docs/               # 文档
    └── 开发计划.md      # 详细开发计划
```

## 🚀 快速开始

### 后端启动

1. **安装依赖**
```bash
cd backend
pip install -r requirements.txt
```

2. **配置环境变量**
```bash
cp .env.example .env
# 编辑.env文件，配置数据库、Redis等
```

3. **启动开发服务器**
```bash
# 方式1: 直接运行
python -m app.main

# 方式2: 使用uvicorn
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

4. **访问API文档**
- Swagger UI: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc

### 前端启动

1. **使用HBuilderX**
   - 打开HBuilderX
   - 文件 → 导入 → 从本地目录导入
   - 选择 `frontend` 目录
   - 运行 → 运行到浏览器/小程序

2. **使用CLI（可选）**
```bash
cd frontend
npm install
npm run dev:h5          # H5
npm run dev:mp-weixin   # 微信小程序
npm run dev:mp-alipay   # 支付宝小程序
```

## 📊 数据库

### 创建数据库
```sql
CREATE DATABASE eceshi CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 运行迁移（开发中自动创建表）
开发模式下会自动创建数据库表。生产环境使用Alembic迁移。

## 🔑 API接口示例

### 1. 用户注册
```bash
POST /api/v1/auth/register
Content-Type: application/json

{
  "phone": "13800138000",
  "password": "123456",
  "sms_code": "123456"
}
```

### 2. 用户登录
```bash
POST /api/v1/auth/login
Content-Type: application/json

{
  "phone": "13800138000",
  "password": "123456"
}
```

### 3. 获取用户信息（需要认证）
```bash
GET /api/v1/users/me
Authorization: Bearer <access_token>
```

### 4. 获取项目列表
```bash
GET /api/v1/projects/list?page=1&page_size=10
```

## 🔧 开发规范

### 代码风格
- Python: PEP 8
- 使用类型注解
- 函数和类添加文档字符串

### Git提交规范
```
feat: 新功能
fix: 修复bug
docs: 文档更新
style: 代码格式调整
refactor: 重构
test: 测试
chore: 构建/工具链
```

## 📝 开发计划

详见 [开发计划.md](./开发计划.md) (2600+行详细规划)

**开发周期**: 24-28周（6-7个月）
**团队规模**: 17-22人

### 开发阶段
- ✅ 阶段一: 需求分析与设计 (2-3周)
- 🚧 阶段二: 核心功能开发 (12-14周)
  - 迭代1: 用户基础功能 ✅
  - 迭代2: 下单与支付功能
  - 迭代3: 实验室管理端
  - 迭代4: 发票与预付功能
  - 迭代5: 会员与预付功能
  - 迭代6: 云现场服务
  - 迭代7: 发布需求功能
  - 迭代8: 实验室加盟
  - 迭代9: 营销与积分功能
  - 迭代10: 专属顾问与客服
- ⏳ 阶段三: 集成测试与优化 (4周)
- ⏳ 阶段四: 用户验收与试运行 (3周)
- ⏳ 阶段五: 正式上线与运维

## 🤝 贡献指南

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'feat: Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

[MIT License](LICENSE)

## 📞 联系方式

- 项目主页: https://github.com/yourusername/eceshi
- 问题反馈: [Issues](https://github.com/yourusername/eceshi/issues)

---

**让科研检测更简单！** 🚀


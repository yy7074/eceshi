# 后台管理API错误修复指南

## 问题分析

根据错误日志，发现以下两个问题：

### 问题1: 分类接口404错误
**错误信息**: `GET /api/v1/categories HTTP/1.1" 404 Not Found`

**原因**: 访问路径错误
- ❌ 错误路径: `/api/v1/categories`
- ✅ 正确路径: `/api/v1/admin/categories`

**解决方法**:
前端代码中修改API调用路径：
```javascript
// 错误
api.get('/api/v1/categories')

// 正确
api.get('/api/v1/admin/categories')
```

### 问题2: 订单分配接口422错误
**错误信息**: `GET /api/v1/admin/orders/pending-assign?page=1&page_size=20 HTTP/1.1" 422 Unprocessable Entity`

**原因**: 可能是以下几种情况之一：
1. 认证token无效或过期
2. 数据库表结构问题
3. 参数验证问题

**解决方法**:

#### 方法1: 重新登录获取新token
```bash
# 使用管理员账号登录
curl -X POST http://localhost:3001/api/v1/auth/admin-login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "123456"
  }'
```

获取返回的 `access_token`，然后在后续请求中使用：
```bash
curl -X GET "http://localhost:3001/api/v1/admin/orders/pending-assign?page=1&page_size=20" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

#### 方法2: 检查数据库表结构
确保数据库中存在所有必要的表：
```sql
-- 检查orders表
DESCRIBE orders;

-- 检查是否有assigned_lab_id字段
SHOW COLUMNS FROM orders LIKE 'assigned_lab_id';
```

如果缺少字段，需要添加：
```sql
ALTER TABLE orders ADD COLUMN assigned_lab_id BIGINT COMMENT '指派实验室ID';
ALTER TABLE orders ADD COLUMN assigned_user_id BIGINT COMMENT '指派操作员ID';
ALTER TABLE orders ADD COLUMN assigned_at DATETIME COMMENT '指派时间';
```

#### 方法3: 检查订单数据
确保数据库中有待分配的订单：
```sql
-- 查看待分配的订单
SELECT id, order_no, status, assigned_lab_id 
FROM orders 
WHERE is_draft = 0 
  AND status IN ('paid', 'pending_assign') 
  AND assigned_lab_id IS NULL;
```

如果没有数据，需要先插入测试数据：
```bash
python backend/insert_admin_test_data.py
```

## 完整的API测试流程

### 1. 登录获取token
```bash
curl -X POST http://localhost:3001/api/v1/auth/admin-login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "123456"
  }'
```

**预期响应**:
```json
{
  "code": 200,
  "message": "登录成功",
  "data": {
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "token_type": "bearer",
    "user_id": 1,
    "phone": "admin",
    "nickname": "管理员",
    "is_admin": true
  }
}
```

### 2. 使用token访问分类接口
```bash
# 替换 YOUR_ACCESS_TOKEN 为实际的token
curl -X GET "http://localhost:3001/api/v1/admin/categories?page=1&page_size=20" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**预期响应**:
```json
{
  "code": 200,
  "message": "操作成功",
  "data": {
    "items": [...],
    "total": 6,
    "page": 1,
    "page_size": 20
  }
}
```

### 3. 使用token访问订单分配统计接口
```bash
curl -X GET "http://localhost:3001/api/v1/admin/orders/assignment-stats" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**预期响应**:
```json
{
  "code": 200,
  "message": "操作成功",
  "data": {
    "pending_count": 5,
    "assigned_count": 3,
    "rejected_count": 0,
    "testing_count": 2,
    "today_assigned": 2,
    "lab_distribution": [...]
  }
}
```

### 4. 使用token访问待分配订单列表
```bash
curl -X GET "http://localhost:3001/api/v1/admin/orders/pending-assign?page=1&page_size=20" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**预期响应**:
```json
{
  "code": 200,
  "message": "操作成功",
  "data": {
    "items": [...],
    "total": 5,
    "page": 1,
    "page_size": 20
  }
}
```

## 常见错误及解决方案

### 错误: 401 Unauthorized
**原因**: Token无效或未提供
**解决**: 
1. 重新登录获取新token
2. 检查请求头格式：`Authorization: Bearer YOUR_TOKEN`
3. 检查token是否过期

### 错误: 403 Forbidden
**原因**: 权限不足
**解决**:
1. 确保使用管理员账号登录
2. 检查用户是否有管理员权限
3. 检查`is_admin`字段是否为True

### 错误: 404 Not Found
**原因**: API路径错误
**解决**:
1. 检查URL路径是否正确
2. 确认是否使用了`/admin`前缀
3. 查看API文档确认正确路径

### 错误: 422 Unprocessable Entity
**原因**: 参数验证失败
**解决**:
1. 检查请求参数格式是否正确
2. 检查参数类型是否匹配
3. 查看API文档确认参数要求

### 错误: 500 Internal Server Error
**原因**: 服务器内部错误
**解决**:
1. 查看后端日志：`tail -f backend/app.log`
2. 检查数据库连接是否正常
3. 检查是否有SQL错误

## 数据库检查清单

### 检查表是否存在
```sql
SHOW TABLES;
```

确保以下表都存在：
- users
- orders
- order_samples
- order_fees
- order_status_history
- payments
- user_addresses
- projects
- project_categories
- laboratories
- user_certification
- coupons
- user_coupons
- points_records
- recharge_records
- invite_records
- user_groups
- group_members
- banners
- announcements
- help_docs
- chat_messages
- reports
- samples
- contracts
- franchises

### 检查orders表结构
```sql
DESCRIBE orders;
```

确保orders表包含以下字段：
- id
- order_no
- user_id
- project_id
- project_name
- lab_id
- lab_name
- status
- is_draft
- invoice_status
- payment_status
- credit_amount
- assigned_lab_id
- assigned_user_id
- assigned_at
- project_fee
- urgent_fee
- shipping_fee
- discount_amount
- total_fee
- paid_fee
- sample_count
- shipping_method
- receiver_name
- receiver_phone
- receiver_address
- payment_method
- payment_time
- created_at
- paid_at
- confirmed_at
- started_at
- completed_at
- cancelled_at
- remark
- cancel_reason
- is_urgent
- estimated_completion_time

### 如果缺少字段，添加它们
```sql
ALTER TABLE orders ADD COLUMN assigned_lab_id BIGINT COMMENT '指派实验室ID';
ALTER TABLE orders ADD COLUMN assigned_user_id BIGINT COMMENT '指派操作员ID';
ALTER TABLE orders ADD COLUMN assigned_at DATETIME COMMENT '指派时间';
ALTER TABLE orders ADD COLUMN credit_amount DECIMAL(10,2) DEFAULT 0 COMMENT '信用支付金额';
ALTER TABLE orders ADD COLUMN invoice_status VARCHAR(20) DEFAULT 'none' COMMENT '开票状态';
```

## 后端服务重启

### 重启后端服务
```bash
# 停止当前服务
pkill -f "uvicorn app.main:app"

# 重新启动
cd backend
python -m app.main
```

或者使用uvicorn：
```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 3001
```

## 测试步骤

### 完整测试流程

1. **启动后端服务**
```bash
cd backend
python -m app.main
```

2. **登录获取token**
```bash
curl -X POST http://localhost:3001/api/v1/auth/admin-login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "123456"}'
```

3. **测试分类接口**
```bash
# 使用步骤2获取的token
curl -X GET "http://localhost:3001/api/v1/admin/categories" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

4. **测试订单分配统计**
```bash
curl -X GET "http://localhost:3001/api/v1/admin/orders/assignment-stats" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

5. **测试待分配订单列表**
```bash
curl -X GET "http://localhost:3001/api/v1/admin/orders/pending-assign" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

6. **测试指派订单**
```bash
curl -X POST "http://localhost:3001/api/v1/admin/orders/1/assign" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"laboratory_id": 1, "remark": "测试指派"}'
```

## 调试技巧

### 查看后端日志
```bash
# 实时查看日志
tail -f backend/app.log

# 查看最近的错误
grep ERROR backend/app.log | tail -20
```

### 启用SQLAlchemy日志
在`backend/app/core/config.py`中设置：
```python
DEBUG = True  # 这会启用SQL日志
```

### 测试数据库连接
```bash
# 测试MySQL连接
mysql -u root -p -e "USE eceshi; SELECT COUNT(*) FROM users;"
```

## 前端对接注意事项

### 正确的API路径
所有后台管理API都需要添加`/admin`前缀：

```javascript
// 正确的API路径示例
const API_BASE = 'http://localhost:3001/api/v1/admin'

export const adminAPI = {
  // 用户管理
  users: `${API_BASE}/users`,
  
  // 项目管理
  projects: `${API_BASE}/projects`,
  
  // 订单管理
  orders: `${API_BASE}/orders`,
  
  // 订单分配
  pendingAssign: `${API_BASE}/orders/pending-assign`,
  assignmentStats: `${API_BASE}/orders/assignment-stats`,
  
  // 分类管理
  categories: `${API_BASE}/categories`,
  
  // 实验室管理
  laboratories: `${API_BASE}/laboratories`,
  
  // 优惠券管理
  coupons: `${API_BASE}/coupons`,
  
  // 充值管理
  recharges: `${API_BASE}/recharges`,
  
  // 积分商品
  pointsGoods: `${API_BASE}/points-goods`,
  
  // 评价管理
  reviews: `${API_BASE}/reviews`,
  
  // 团队管理
  groups: `${API_BASE}/groups`,
  
  // 邀请管理
  invites: `${API_BASE}/invites`,
  
  // 实名认证
  certifications: `${API_BASE}/certifications`,
  
  // 信用管理
  creditDebts: `${API_BASE}/credit/debts`,
  limitApplications: `${API_BASE}/credit/limit-applications`,
  
  // 实验室申请
  labApplications: `${API_BASE}/lab-applications`,
  
  // 角色管理
  roles: `${API_BASE}/roles`,
  permissions: `${API_BASE}/permissions`,
  
  // 数据分析
  analytics: `${API_BASE}/analytics`,
  
  // 财务管理
  financeStats: `${API_BASE}/finance/stats`,
  financeIncome: `${API_BASE}/finance/income`,
  financeExpense: `${API_BASE}/finance/expense`,
  
  // 报表统计
  reportsOverview: `${API_BASE}/reports/overview`,
  orderTrend: `${API_BASE}/reports/order-trend`,
  projectRanking: `${API_BASE}/reports/project-ranking`,
  labPerformance: `${API_BASE}/reports/lab-performance`,
  financeSummary: `${API_BASE}/reports/finance-summary`,
  
  // 员工管理
  staff: `${API_BASE}/staff`,
  
  // 数据导出
  exportOrders: `${API_BASE}/export/orders`,
  exportUsers: `${API_BASE}/export/users`
}
```

### 请求拦截器
确保所有请求都携带token：
```javascript
import axios from 'axios'

const request = axios.create({
  baseURL: 'http://localhost:3001/api/v1',
  timeout: 10000
})

// 请求拦截器
request.interceptors.request.use(
  config => {
    // 添加token
    const token = localStorage.getItem('admin_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
request.interceptors.response.use(
  response => {
    const res = response.data
    if (res.code !== 200) {
      // 处理错误
      console.error('API Error:', res.message)
      return Promise.reject(new Error(res.message))
    }
    return res
  },
  error => {
    // 处理网络错误
    console.error('Network Error:', error)
    return Promise.reject(error)
  }
)

export default request
```

## 总结

1. **确保数据库表结构完整**：运行`insert_admin_test_data.py`插入测试数据
2. **使用正确的API路径**：所有后台管理API都需要`/admin`前缀
3. **获取有效的token**：使用管理员账号登录获取token
4. **在请求头中携带token**：`Authorization: Bearer YOUR_TOKEN`
5. **检查后端日志**：遇到问题时查看详细错误信息
6. **重启后端服务**：修改代码后重启服务

按照以上步骤操作，应该能够正常访问后台管理系统的所有功能。

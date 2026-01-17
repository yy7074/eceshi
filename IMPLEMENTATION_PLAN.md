# 网站及小程序完善修改 - 实施计划

## 总体进度

| 模块 | 状态 | 预计文件数 |
|------|------|-----------|
| 一、选项及定价功能 | ✅ 已完成 | 8 |
| 二、样品组管理功能 | ✅ 已完成 | 6 |
| 三、充值赠送+开票充值 | ✅ 已完成 | 4 |
| 四、佣金设置功能 | ✅ 已完成 | 4 |

---

## 一、选项及定价功能优化 ✅ 已完成

### 已实现功能
- [x] 无限层级选项树结构
- [x] 单选/多选/输入三种选项类型
- [x] 三种价格类型（固定/按样品数/百分比）
- [x] 红色提示文字
- [x] 后台选项管理 CRUD
- [x] 前端动态选项组件
- [x] 实时价格计算

### 已创建文件
- `backend/app/models/project_option.py`
- `backend/app/schemas/project_option.py`
- `backend/app/api/v1/project_options.py`
- `frontend/components/DynamicOptionsForm.vue`
- `frontend/components/OptionNode.vue`

---

## 二、样品组管理功能 ✅ 已完成

### 需求分析
1. 同一测试项目支持按测试目的增加分组
2. 多个订单可同时提交，价格分开或叠加计算
3. 分组序列支持收起/展开、复制、新增、删除
4. 样品组内包含：
   - 样品数量（支持批量添加）
   - 样品编号（仅支持英文、数字、下划线）
   - 样品名称、成分、状态等信息

### 数据库设计

```sql
-- 样品组表
CREATE TABLE sample_groups (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    order_id BIGINT,                    -- 关联订单（提交后）
    user_id BIGINT NOT NULL,            -- 用户ID
    project_id BIGINT NOT NULL,         -- 项目ID

    group_name VARCHAR(100),            -- 分组名称/测试目的
    group_index INT DEFAULT 1,          -- 分组序号

    -- 选项快照
    option_selections JSON,             -- 该组选择的选项
    options_fee DECIMAL(10,2) DEFAULT 0,

    is_collapsed BOOLEAN DEFAULT FALSE, -- 是否收起
    status VARCHAR(20) DEFAULT 'draft', -- draft/submitted

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME
);

-- 样品明细表（组内样品）
CREATE TABLE sample_items (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    group_id BIGINT NOT NULL,           -- 关联样品组

    sample_no VARCHAR(100),             -- 样品编号（英文+数字+下划线）
    sample_name VARCHAR(200),           -- 样品名称
    sample_composition TEXT,            -- 样品成分
    sample_state VARCHAR(50),           -- 样品状态
    danger_type VARCHAR(50),            -- 危险性
    storage_requirement VARCHAR(100),   -- 存放要求
    quantity INT DEFAULT 1,             -- 数量

    remark TEXT,                        -- 备注
    photos JSON,                        -- 样品照片

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### 后端实现

#### 新建文件
| 文件 | 说明 |
|------|------|
| `backend/app/models/sample_group.py` | 样品组和样品明细模型 |
| `backend/app/schemas/sample_group.py` | Pydantic schemas |
| `backend/app/api/v1/sample_groups.py` | 样品组 API |

#### API 设计
| 端点 | 方法 | 说明 |
|------|------|------|
| `/sample-groups` | GET | 获取用户的样品组列表 |
| `/sample-groups` | POST | 创建样品组 |
| `/sample-groups/{id}` | PUT | 更新样品组 |
| `/sample-groups/{id}` | DELETE | 删除样品组 |
| `/sample-groups/{id}/copy` | POST | 复制样品组 |
| `/sample-groups/{id}/items` | GET | 获取组内样品 |
| `/sample-groups/{id}/items` | POST | 添加样品 |
| `/sample-groups/{id}/items/batch` | POST | 批量添加样品 |
| `/sample-groups/submit` | POST | 批量提交样品组生成订单 |
| `/sample-groups/calculate` | POST | 计算多组价格 |

### 前端实现

#### 新建文件
| 文件 | 说明 |
|------|------|
| `frontend/components/SampleGroupList.vue` | 样品组列表组件 |
| `frontend/components/SampleGroupCard.vue` | 单个样品组卡片 |
| `frontend/components/SampleItemForm.vue` | 样品明细表单 |
| `frontend/components/BatchAddSamples.vue` | 批量添加样品弹窗 |

#### 修改文件
| 文件 | 变更 |
|------|------|
| `frontend/pagesA/booking/booking.vue` | 集成样品组管理 |
| `frontend/utils/api.js` | 添加样品组 API |

---

## 三、充值赠送+开票充值 ✅ 已完成

### 需求分析
1. 充值页面明确展示赠送示例（如充10000送500）
2. 增加开票充值入口
3. 开票充值由后台输入金额，前端展示

### 数据库设计

```sql
-- 充值赠送规则表（已有，需确认）
-- 开票充值记录表
CREATE TABLE invoice_recharge_records (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,

    amount DECIMAL(10,2) NOT NULL,      -- 充值金额
    bonus_amount DECIMAL(10,2) DEFAULT 0, -- 赠送金额

    invoice_title VARCHAR(200),         -- 发票抬头
    invoice_tax_no VARCHAR(50),         -- 税号
    invoice_type VARCHAR(20),           -- 发票类型

    status VARCHAR(20) DEFAULT 'pending', -- pending/confirmed/rejected

    admin_id BIGINT,                    -- 确认的管理员
    confirmed_at DATETIME,              -- 确认时间
    remark TEXT,                        -- 备注

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### 后端实现

#### 修改文件
| 文件 | 变更 |
|------|------|
| `backend/app/api/v1/recharge.py` | 添加开票充值接口 |
| `backend/app/api/v1/admin.py` | 添加确认开票充值接口 |

### 前端实现

#### 修改文件
| 文件 | 变更 |
|------|------|
| `frontend/pagesA/recharge/recharge.vue` | 添加赠送示例展示、开票充值入口 |

---

## 四、佣金设置功能 ✅ 已完成

### 需求分析
1. 去除 "T+7 工作日结算佣金" 表述
2. 支持根据不同客户设置佣金比例（≤12%）

### 数据库设计

```sql
-- 客户佣金设置表
CREATE TABLE user_commission_settings (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL UNIQUE,     -- 用户ID

    commission_rate DECIMAL(5,2) DEFAULT 0, -- 佣金比例（%）
    max_rate DECIMAL(5,2) DEFAULT 12.00,    -- 最大比例

    effective_from DATE,                -- 生效日期
    effective_to DATE,                  -- 失效日期

    created_by BIGINT,                  -- 设置人
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME
);

-- 佣金记录表
CREATE TABLE commission_records (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    order_id BIGINT NOT NULL,

    order_amount DECIMAL(10,2),         -- 订单金额
    commission_rate DECIMAL(5,2),       -- 佣金比例
    commission_amount DECIMAL(10,2),    -- 佣金金额

    status VARCHAR(20) DEFAULT 'pending', -- pending/settled/cancelled
    settled_at DATETIME,

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### 后端实现

#### 新建文件
| 文件 | 说明 |
|------|------|
| `backend/app/models/commission.py` | 佣金模型 |
| `backend/app/schemas/commission.py` | Pydantic schemas |

#### 修改文件
| 文件 | 变更 |
|------|------|
| `backend/app/api/v1/admin.py` | 添加佣金设置管理接口 |
| `backend/app/api/v1/invites.py` | 修改佣金计算逻辑 |

### 前端实现

#### 修改文件
| 文件 | 变更 |
|------|------|
| 后台管理页面 | 添加客户佣金设置功能 |
| `frontend/pagesA/invite/invite.vue` | 去除 T+7 表述 |

---

## 实施顺序

### 第一阶段：样品组管理（核心功能）
1. 创建数据库模型
2. 实现后端 API
3. 创建前端组件
4. 集成到预约页面
5. 测试多组提交

### 第二阶段：佣金设置
1. 创建佣金模型
2. 实现管理端接口
3. 修改佣金计算逻辑
4. 更新前端展示

### 第三阶段：充值功能优化
1. 添加开票充值模型
2. 实现相关接口
3. 更新充值页面
4. 添加赠送示例展示

---

## 注意事项

1. **样品编号校验**：仅允许英文、数字、下划线
   ```javascript
   const sampleNoRegex = /^[a-zA-Z0-9_]+$/
   ```

2. **价格计算**：
   - 分开计算：各组独立计算
   - 叠加计算：合并为一个订单

3. **佣金比例限制**：最大不超过 12%

4. **开票充值流程**：
   - 用户提交申请 → 后台确认到账 → 充值到账户

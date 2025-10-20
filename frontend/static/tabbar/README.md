# TabBar图标说明

## 📌 需要的图标文件

由于微信小程序tabBar需要PNG格式图标，请准备以下8个图标文件：

### 尺寸要求
- 建议尺寸：81px × 81px
- 格式：PNG
- 背景：透明

### 图标列表

#### 1. 首页
- `home.png` - 灰色（#8c8c8c）房子图标
- `home-active.png` - 蓝色（#1890ff）房子图标

#### 2. 分类
- `category.png` - 灰色（#8c8c8c）四格图标
- `category-active.png` - 蓝色（#1890ff）四格图标

#### 3. 订单
- `order.png` - 灰色（#8c8c8c）订单/文档图标
- `order-active.png` - 蓝色（#1890ff）订单/文档图标

#### 4. 我的
- `user.png` - 灰色（#8c8c8c）人像图标
- `user-active.png` - 蓝色（#1890ff）人像图标

## 🎨 临时方案

如果暂时没有图标，可以：

### 方案1：使用在线工具生成
访问：https://www.iconfont.cn/
1. 搜索对应图标
2. 下载PNG格式
3. 调整颜色和尺寸

### 方案2：使用emoji
修改pages.json，暂时不使用iconPath

### 方案3：使用纯色方块（测试用）
创建纯色PNG文件作为占位

## 📝 当前状态

已在pages.json中配置图标路径，但图标文件需要手动添加。

图标未添加前，tabBar会显示文字但没有图标。

# TabBar页面跳转修复说明

## 问题描述
出现错误：`navigateTo:fail can not navigateTo a tabbar page`

## 原因
在小程序中，tabBar页面（首页、分类、订单、个人中心）不能使用 `uni.navigateTo` 跳转，必须使用 `uni.switchTab`。

## 已修复的问题

### 1. 首页跳转到分类页
**文件**: `pages/index/index.vue`

**修改前**:
```javascript
goCategory(item) {
    uni.navigateTo({
        url: `/pages/category/category?id=${item.id}&name=${item.name}`
    })
}
```

**修改后**:
```javascript
goCategory(item) {
    // 跳转到分类页（tabBar页面使用switchTab）
    uni.switchTab({
        url: `/pages/category/category`
    })
}
```

### 2. 个人中心跳转到订单页
**文件**: `pages/user/user.vue`

**修改前**:
```javascript
goOrders(status) {
    uni.navigateTo({
        url: `/pages/order/order?status=${status}`
    })
}
```

**修改后**:
```javascript
goOrders(status) {
    // 存储状态到本地，订单页面会读取
    uni.setStorageSync('order_status_filter', status)
    uni.switchTab({
        url: '/pages/order/order'
    })
}
```

### 3. 订单页读取状态参数
**文件**: `pages/order/order.vue`

**增加**:
```javascript
onShow() {
    // 检查是否有状态筛选参数（从个人中心跳转过来）
    const statusFilter = uni.getStorageSync('order_status_filter')
    if (statusFilter) {
        this.currentTab = statusFilter
        uni.removeStorageSync('order_status_filter') // 使用后删除
    }
    
    // 每次显示页面时刷新
    const token = uni.getStorageSync('token')
    if (token) {
        this.loadOrders(true)
    }
}
```

## 跳转方法对比

### uni.navigateTo
- 用于跳转到**非tabBar页面**
- 可以传递参数
- 可以返回上一页
- 示例：项目详情、预约页面、订单详情等

### uni.switchTab
- 用于跳转到**tabBar页面**
- **不能传递参数**（需要用本地存储传递）
- 不能返回，直接切换
- 示例：首页、分类、订单、个人中心

### uni.redirectTo
- 关闭当前页面，跳转到应用内的某个页面
- 不能跳转到tabBar页面
- 示例：登录成功后跳转

### uni.reLaunch
- 关闭所有页面，打开到应用内的某个页面
- 可以跳转到tabBar页面
- 示例：退出登录后跳转

## tabBar页面列表

根据 `pages.json` 配置，以下是tabBar页面：
1. `pages/index/index` - 首页
2. `pages/category/category` - 分类
3. `pages/order/order` - 订单
4. `pages/user/user` - 个人中心

**所有跳转到这些页面的地方都必须使用 `uni.switchTab`！**

## 测试清单

- [x] 首页点击分类导航
- [x] 个人中心点击订单状态入口
- [x] 个人中心点击"全部订单"
- [ ] 其他可能的跳转

## 注意事项

1. **tabBar页面不能传参数**：
   - 需要传参时，使用本地存储（如 `uni.setStorageSync`）
   - 在目标页面的 `onShow` 中读取并清除

2. **避免使用 `navigateTo` 跳转tabBar**：
   - 编译时不会报错
   - 运行时会报错

3. **底部tabBar自动切换**：
   - 使用 `uni.switchTab` 时，底部tabBar会自动高亮对应的页面

## 解决方案模板

如果需要在跳转tabBar页面时传递参数：

```javascript
// 发起页面
goToTabBarPage(param) {
    // 1. 保存参数到本地
    uni.setStorageSync('tab_param', param)
    
    // 2. 跳转
    uni.switchTab({
        url: '/pages/xxx/xxx'
    })
}

// 目标tabBar页面
onShow() {
    // 3. 读取参数
    const param = uni.getStorageSync('tab_param')
    if (param) {
        // 使用参数
        this.handleParam(param)
        // 4. 清除参数（避免重复使用）
        uni.removeStorageSync('tab_param')
    }
}
```

---

**最后更新**: 2025年10月19日
**状态**: 已修复

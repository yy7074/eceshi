/**
 * API接口定义
 */
import request from './request.js'

export default {
	// ========== 认证相关 ==========
	
	// 发送短信验证码
	sendSms(data) {
		return request.post('/api/v1/auth/send-sms', data)
	},
	
	// 用户注册
	register(data) {
		return request.post('/api/v1/auth/register', data)
	},
	
	// 用户登录
	login(data) {
		return request.post('/api/v1/auth/login', data)
	},
	
	// 短信验证码登录
	smsLogin(data) {
		return request.post('/api/v1/auth/sms-login', data)
	},
	
	// 微信登录
	wechatLogin(code) {
		return request.post('/api/v1/auth/wechat-login', { code })
	},
	
	// ========== 用户相关 ==========
	
	// 获取当前用户信息
	getUserInfo() {
		return request.get('/api/v1/users/me')
	},
	
	// 更新用户信息
	updateUserInfo(data) {
		return request.put('/api/v1/users/me', data)
	},
	
	// 提交实名认证
	submitCertification(data) {
		return request.post('/api/v1/users/certification', data)
	},
	
	// 获取认证信息
	getCertification() {
		return request.get('/api/v1/users/certification')
	},
	
	// 获取账户余额
	getBalance() {
		return request.get('/api/v1/users/balance')
	},
	
	// ========== 检测项目相关 ==========
	
	// 获取项目分类
	getCategories() {
		return request.get('/api/v1/projects/categories')
	},
	
	// 获取项目列表
	getProjects(params) {
		return request.get('/api/v1/projects/list', params)
	},
	
	// 获取项目详情
	getProjectDetail(id) {
		return request.get(`/api/v1/projects/${id}`)
	},
	
	// ========== 项目选项相关 ==========

	// 获取项目选项树
	getProjectOptions(projectId) {
		return request.get(`/api/v1/project-options/project/${projectId}/options`)
	},

	// 获取分类选项树
	getCategoryOptions(categoryId) {
		return request.get(`/api/v1/project-options/category/${categoryId}/options`)
	},

	// 计算选项价格
	calculateOptionsPrice(data) {
		return request.post('/api/v1/project-options/options/calculate', data)
	},

	// ========== 样品组管理相关 ==========

	// 获取样品组列表
	getSampleGroups(params) {
		return request.get('/api/v1/sample-groups', params)
	},

	// 获取样品组详情
	getSampleGroupDetail(groupId) {
		return request.get(`/api/v1/sample-groups/${groupId}`)
	},

	// 创建样品组
	createSampleGroup(data) {
		return request.post('/api/v1/sample-groups', data)
	},

	// 更新样品组
	updateSampleGroup(groupId, data) {
		return request.put(`/api/v1/sample-groups/${groupId}`, data)
	},

	// 删除样品组
	deleteSampleGroup(groupId) {
		return request.delete(`/api/v1/sample-groups/${groupId}`)
	},

	// 复制样品组
	copySampleGroup(groupId) {
		return request.post(`/api/v1/sample-groups/${groupId}/copy`)
	},

	// 获取组内样品列表
	getSampleItems(groupId) {
		return request.get(`/api/v1/sample-groups/${groupId}/items`)
	},

	// 添加样品
	addSampleItem(groupId, data) {
		return request.post(`/api/v1/sample-groups/${groupId}/items`, data)
	},

	// 批量添加样品
	batchAddSampleItems(groupId, data) {
		return request.post(`/api/v1/sample-groups/${groupId}/items/batch`, data)
	},

	// 更新样品
	updateSampleItem(groupId, itemId, data) {
		return request.put(`/api/v1/sample-groups/${groupId}/items/${itemId}`, data)
	},

	// 删除样品
	deleteSampleItem(groupId, itemId) {
		return request.delete(`/api/v1/sample-groups/${groupId}/items/${itemId}`)
	},

	// 计算多组价格
	calculateGroupsPrice(data) {
		return request.post('/api/v1/sample-groups/calculate', data)
	},

	// 批量提交样品组生成订单
	submitSampleGroups(data) {
		return request.post('/api/v1/sample-groups/submit', data)
	},

	// ========== 订单相关 ==========

	// 计算订单费用（支持选项）
	calculateOrder(data) {
		return request.post('/api/v1/orders/calculate', data)
	},
	
	// 创建订单
	createOrder(data) {
		return request.post('/api/v1/orders/create', data)
	},
	
	// 获取订单列表
	getOrders(params) {
		return request.get('/api/v1/orders/list', params)
	},
	
	// 获取订单详情
	getOrderDetail(id) {
		return request.get(`/api/v1/orders/${id}`)
	},
	
	// 取消订单
	cancelOrder(id, data) {
		return request.post(`/api/v1/orders/${id}/cancel`, data)
	},

	// ========== 草稿订单相关 ==========

	// 获取草稿订单列表
	getDraftOrders(params) {
		return request.get('/api/v1/orders/drafts', params)
	},

	// 保存草稿订单
	saveDraftOrder(data) {
		return request.post('/api/v1/orders/draft', data)
	},

	// 更新草稿订单
	updateDraftOrder(id, data) {
		return request.put(`/api/v1/orders/draft/${id}`, data)
	},

	// 提交草稿订单
	submitDraftOrder(id) {
		return request.post(`/api/v1/orders/draft/${id}/submit`)
	},

	// 删除草稿订单
	deleteDraftOrder(id) {
		return request.delete(`/api/v1/orders/draft/${id}`)
	},

	// ========== 地址相关 ==========
	
	// 获取地址列表
	getAddresses() {
		return request.get('/api/v1/addresses/list')
	},
	
	// 添加地址
	addAddress(data) {
		return request.post('/api/v1/addresses/add', data)
	},
	
	// 更新地址
	updateAddress(id, data) {
		return request.put(`/api/v1/addresses/${id}`, data)
	},
	
	// 删除地址
	deleteAddress(id) {
		return request.delete(`/api/v1/addresses/${id}`)
	},
	
	// 设置默认地址
	setDefaultAddress(id) {
		return request.post(`/api/v1/addresses/${id}/set-default`)
	},
	
	// ========== 支付相关 ==========
	
	// 创建支付
	createPayment(data) {
		return request.post('/api/v1/payments/create', data)
	},
	
	// 查询支付状态
	getPaymentStatus(id) {
		return request.get(`/api/v1/payments/${id}/status`)
	},
	
	// ========== 收藏相关 ==========
	
	// 收藏项目
	addFavorite(projectId) {
		return request.post('/api/v1/favorites/add', null, {
			params: { project_id: projectId }
		})
	},
	
	// 取消收藏
	removeFavorite(projectId) {
		return request.delete('/api/v1/favorites/remove', null, {
			params: { project_id: projectId }
		})
	},
	
	// 获取收藏列表
	getFavorites(params) {
		return request.get('/api/v1/favorites/list', params)
	},
	
	// 检查是否已收藏
	checkFavorite(projectId) {
		return request.get('/api/v1/favorites/check', { project_id: projectId })
	},
	
	// ========== 评价相关 ==========
	
	// 创建评价
	createReview(data) {
		return request.post('/api/v1/reviews/create', data)
	},
	
	// 获取我的评价
	getMyReviews(params) {
		return request.get('/api/v1/reviews/my', params)
	},
	
	// 获取项目评价列表
	getProjectReviews(projectId, params) {
		return request.get(`/api/v1/reviews/project/${projectId}`, params)
	},
	
	// ========== 积分相关 ==========
	
	// 获取积分余额
	getPointsBalance() {
		return request.get('/api/v1/points/balance')
	},
	
	// 获取积分商品列表
	getPointsGoods(params) {
		return request.get('/api/v1/points/goods', params)
	},
	
	// 兑换积分商品
	exchangePoints(goodsId, addressId) {
		return request.post('/api/v1/points/exchange', null, {
			params: { goods_id: goodsId, address_id: addressId }
		})
	},
	
	// 获取积分记录
	getPointsRecords(params) {
		return request.get('/api/v1/points/records', params)
	},
	
	// 获取兑换记录
	getExchangeRecords(params) {
		return request.get('/api/v1/points/exchanges', params)
	},
	
	// ========== 优惠券相关 ==========
	
	// 获取我的优惠券
	getMyCoupons(params) {
		return request.get('/api/v1/coupons/my', params)
	},
	
	// 获取可领取优惠券
	getAvailableCoupons(params) {
		return request.get('/api/v1/coupons/available', params)
	},
	
	// 领取优惠券
	receiveCoupon(couponId) {
		return request.post('/api/v1/coupons/receive', null, {
			params: { coupon_id: couponId }
		})
	},
	
	// ========== 邀请好友相关 ==========
	
	// 获取邀请统计
	getInviteStats() {
		return request.get('/api/v1/invites/stats')
	},
	
	// 获取邀请记录
	getInviteRecords(params) {
		return request.get('/api/v1/invites/records', params)
	},
	
	// 申请提现
	withdrawRewards(amount) {
		return request.post('/api/v1/invites/withdraw', null, {
			params: { amount }
		})
	},
	
	// ========== 团队功能相关 ==========
	
	// 创建团队
	createGroup(data) {
		return request.post('/api/v1/groups/create', data)
	},
	
	// 获取我的团队
	getMyGroups() {
		return request.get('/api/v1/groups/my')
	},
	
	// 获取团队详情
	getGroupDetail(groupId) {
		return request.get(`/api/v1/groups/${groupId}`)
	},
	
	// 加入团队
	joinGroup(groupCode) {
		return request.post('/api/v1/groups/join', null, {
			params: { group_code: groupCode }
		})
	},
	
	// 通过手机号加入团队
	joinGroupByPhone(phone) {
		return request.post('/api/v1/groups/join-by-phone', { phone })
	},
	
	// ========== 钱包充值相关 ==========
	
	// 创建充值订单
	createRecharge(data) {
		return request.post('/api/v1/recharge/create', data)
	},
	
	// 获取充值记录
	getRechargeRecords(params) {
		return request.get('/api/v1/recharge/records', params)
	},
	
	// 获取充值详情
	getRechargeDetail(rechargeId) {
		return request.get(`/api/v1/recharge/${rechargeId}`)
	},
	
	// 获取充值赠送规则
	getBonusRules() {
		return request.get('/api/v1/recharge/bonus/rules')
	},
	
	// ========== 发票相关 ==========
	
	// 申请开票
	applyInvoice(data) {
		return request.post('/api/v1/invoices/apply', data)
	},
	
	// 获取发票列表
	getInvoices(params) {
		return request.get('/api/v1/invoices/list', params)
	},
	
	// 获取发票详情
	getInvoiceDetail(invoiceId) {
		return request.get(`/api/v1/invoices/${invoiceId}`)
	},
	
	// 获取可开票订单
	getInvoiceableOrders() {
		return request.get('/api/v1/invoices/invoiceable/orders')
	},
	
	// ========== 抽奖相关 ==========
	
	// 获取抽奖次数
	getLotteryChances() {
		return request.get('/api/v1/lottery/chances')
	},
	
	// 进行抽奖
	doLottery() {
		return request.post('/api/v1/lottery/draw')
	},
	
	// 获取奖品列表
	getLotteryPrizes() {
		return request.get('/api/v1/lottery/prizes')
	},
	
	// 获取中奖记录
	getLotteryRecords(params) {
		return request.get('/api/v1/lottery/records', params)
	},
	
	// 领取奖品
	claimPrize(recordId) {
		return request.post(`/api/v1/lottery/claim/${recordId}`)
	},
	
	// 获取最近中奖记录
	getRecentLotteryRecords(limit = 10) {
		return request.get('/api/v1/lottery/recent', { limit })
	},
	
	// ========== 预付记录相关 ==========
	
	// 获取预付统计
	getPrepayStats() {
		return request.get('/api/v1/prepay/stats')
	},
	
	// 获取预付记录
	getPrepayRecords(params) {
		return request.get('/api/v1/prepay/records', params)
	},
	
	// ========== 帮助中心相关 ==========
	
	// 获取帮助分类
	getHelpCategories() {
		return request.get('/api/v1/help/categories')
	},
	
	// 获取帮助文章
	getHelpArticles(params) {
		return request.get('/api/v1/help/articles', params)
	},
	
	// ========== 公告相关 ==========
	
	// 获取公告列表
	getAnnouncements(params) {
		return request.get('/api/v1/announcements/list', params)
	},
	
	// 获取公告详情
	getAnnouncementDetail(id) {
		return request.get(`/api/v1/announcements/${id}`)
	},
	
	// ========== 客服相关 ==========
	
	// 获取聊天历史
	getChatHistory() {
		return request.get('/api/v1/chat/history')
	},
	
	// 发送消息
	sendChatMessage(data) {
		return request.post('/api/v1/chat/send', data)
	},
	
	// ========== 报告相关 ==========
	
	// 获取报告列表
	getReports(params) {
		return request.get('/api/v1/reports/list', params)
	},
	
	// 下载报告
	downloadReport(orderId) {
		return request.get(`/api/v1/reports/${orderId}/download`)
	},
	
	// ========== 样品追踪相关 ==========
	
	// 获取样品状态
	getSampleStatus(orderId) {
		return request.get(`/api/v1/samples/${orderId}/status`)
	},
	
	// 提交快递单号
	submitExpressNo(orderId, data) {
		return request.post(`/api/v1/samples/${orderId}/express`, data)
	},
	
	// ========== 合同相关 ==========
	
	// 获取合同列表
	getContracts(params) {
		return request.get('/api/v1/contracts/list', params)
	},
	
	// 获取合同详情
	getContractDetail(id) {
		return request.get(`/api/v1/contracts/${id}`)
	},
	
	// 下载合同
	downloadContract(id) {
		return request.post(`/api/v1/contracts/${id}/download`)
	},
	
	// ========== 轮播图相关 ==========
	
	// 获取轮播图列表
	getBanners(position = 'home') {
		return request.get('/api/v1/banners/list', { position })
	},
	
	// 记录轮播图点击
	recordBannerClick(bannerId) {
		return request.post(`/api/v1/banners/${bannerId}/click`)
	},
	
	// ========== 用户通知相关 ==========
	
	// 获取用户通知列表
	getNotifications(params) {
		return request.get('/api/v1/announcements/notifications/list', params)
	},
	
	// 标记通知已读
	markNotificationRead(id) {
		return request.post(`/api/v1/announcements/notifications/${id}/read`)
	},
	
	// 标记所有通知已读
	markAllNotificationsRead() {
		return request.post('/api/v1/announcements/notifications/read-all')
	},
	
	// ========== 快捷回复相关 ==========
	
	// 获取快捷问题
	getQuickReplies() {
		return request.get('/api/v1/chat/quick-replies')
	},
	
	// 获取或创建聊天会话
	getChatSession() {
		return request.get('/api/v1/chat/session')
	},
	
	// ========== 加盟申请相关 ==========
	
	// 提交加盟申请
	submitFranchise(data) {
		return request.post('/api/v1/franchise/apply', data)
	},
	
	// 获取我的加盟申请
	getMyFranchiseApplications() {
		return request.get('/api/v1/franchise/my-applications')
	},
	
	// 查询申请状态
	checkFranchiseStatus(phone) {
		return request.get('/api/v1/franchise/check', { phone })
	},
	
	// 获取合作模式
	getFranchiseModes() {
		return request.get('/api/v1/franchise/modes')
	},
	
	// ========== 数据统计相关 ==========
	
	// 获取数据概览
	getStatsOverview(timeRange = 'month') {
		return request.get('/api/v1/statistics/overview', { time_range: timeRange })
	},
	
	// 获取订单统计
	getOrderStats(timeRange = 'month') {
		return request.get('/api/v1/statistics/order-stats', { time_range: timeRange })
	},
	
	// 获取项目统计
	getProjectStats(timeRange = 'month', limit = 5) {
		return request.get('/api/v1/statistics/project-stats', { time_range: timeRange, limit })
	},
	
	// 获取消费趋势
	getConsumptionTrend(timeRange = 'month') {
		return request.get('/api/v1/statistics/trend', { time_range: timeRange })
	},
	
	// 获取常用项目
	getFrequentProjects(limit = 5) {
		return request.get('/api/v1/statistics/frequent-projects', { limit })
	},
	
	// ========== 样品追踪增强 ==========
	
	// 获取样品时间线
	getSampleTimeline(orderId) {
		return request.get(`/api/v1/samples/order/${orderId}/timeline`)
	},
	
	// 提交物流信息
	submitLogistics(orderId, data) {
		return request.post(`/api/v1/samples/order/${orderId}/logistics`, data)
	},

	// ========== 信用系统相关 ==========

	// 获取信用额度信息
	getCreditInfo() {
		return request.get('/api/v1/credit/info')
	},

	// 获取欠款列表
	getDebtList(params) {
		return request.get('/api/v1/credit/debts', params)
	},

	// 信用支付
	creditPay(data) {
		return request.post('/api/v1/credit/pay', data)
	},

	// 还款
	repayDebt(data) {
		return request.post('/api/v1/credit/repay', data)
	},

	// 获取信用交易记录
	getCreditRecords(params) {
		return request.get('/api/v1/credit/records', params)
	},

	// 获取还款记录
	getRepaymentRecords(params) {
		return request.get('/api/v1/credit/repayments', params)
	},

	// 申请提升额度
	applyLimitIncrease(data) {
		return request.post('/api/v1/credit/limit/apply', data)
	},

	// 获取额度申请记录
	getLimitApplications() {
		return request.get('/api/v1/credit/limit/applications')
	},

	// ========== 实验室相关 ==========

	// 获取实验室列表
	getLaboratories(params) {
		return request.get('/api/v1/laboratories/list', params)
	},

	// 获取实验室详情
	getLaboratoryDetail(id) {
		return request.get(`/api/v1/laboratories/${id}`)
	},

	// 提交实验室入驻申请
	submitLabApplication(data) {
		return request.post('/api/v1/laboratories/apply', data)
	},

	// 获取我的入驻申请状态
	getMyLabApplicationStatus() {
		return request.get('/api/v1/laboratories/apply/status')
	},

	// 获取我的实验室信息
	getMyLaboratory() {
		return request.get('/api/v1/laboratories/my/info')
	},

	// 获取我的实验室设备列表
	getMyLabEquipments(params) {
		return request.get('/api/v1/laboratories/my/equipments', params)
	},

	// 添加设备
	addLabEquipment(data) {
		return request.post('/api/v1/laboratories/my/equipments', data)
	},

	// 更新设备信息
	updateLabEquipment(id, data) {
		return request.put(`/api/v1/laboratories/my/equipments/${id}`, data)
	},

	// 删除设备
	deleteLabEquipment(id) {
		return request.delete(`/api/v1/laboratories/my/equipments/${id}`)
	},

	// 获取我的实验室技术人员
	getMyLabStaff() {
		return request.get('/api/v1/laboratories/my/staff')
	},

	// 添加技术人员
	addLabStaff(data) {
		return request.post('/api/v1/laboratories/my/staff', data)
	},

	// ========== 实验室订单管理 ==========

	// 获取实验室订单列表
	getLabOrders(params) {
		return request.get('/api/v1/laboratories/my/orders', params)
	},

	// 获取实验室订单详情
	getLabOrderDetail(orderId) {
		return request.get(`/api/v1/laboratories/my/orders/${orderId}`)
	},

	// 接受订单
	acceptLabOrder(orderId, data = {}) {
		return request.post(`/api/v1/laboratories/my/orders/${orderId}/accept`, data)
	},

	// 拒绝订单
	rejectLabOrder(orderId, data) {
		return request.post(`/api/v1/laboratories/my/orders/${orderId}/reject`, data)
	},

	// 开始检测
	startLabTesting(orderId, data = {}) {
		return request.post(`/api/v1/laboratories/my/orders/${orderId}/start`, data)
	},

	// 上传检测报告
	uploadLabReport(orderId, data) {
		return request.post(`/api/v1/laboratories/my/orders/${orderId}/upload-report`, data)
	},

	// 完成检测
	completeLabTesting(orderId, data = {}) {
		return request.post(`/api/v1/laboratories/my/orders/${orderId}/complete`, data)
	},

	// 获取实验室统计数据
	getLabStatistics() {
		return request.get('/api/v1/laboratories/my/statistics')
	},

	// ========== 管理端：订单指派 ==========

	// 获取待指派订单列表
	getPendingAssignOrders(params) {
		return request.get('/api/v1/admin/orders/pending-assign', params)
	},

	// 获取适合的实验室列表
	getSuitableLabsForOrder(orderId) {
		return request.get(`/api/v1/admin/orders/${orderId}/suitable-labs`)
	},

	// 指派订单到实验室
	assignOrderToLab(orderId, data) {
		return request.post(`/api/v1/admin/orders/${orderId}/assign`, data)
	},

	// 批量指派订单
	batchAssignOrders(data) {
		return request.post('/api/v1/admin/orders/batch-assign', data)
	},

	// 重新指派订单
	reassignOrder(orderId, data) {
		return request.post(`/api/v1/admin/orders/${orderId}/reassign`, data)
	},

	// 获取订单指派统计
	getAssignmentStats() {
		return request.get('/api/v1/admin/orders/assignment-stats')
	},

	// ========== 管理端：角色权限管理 ==========

	// 获取角色列表
	getRoles(params) {
		return request.get('/api/v1/admin/roles', params)
	},

	// 获取角色详情
	getRoleDetail(roleId) {
		return request.get(`/api/v1/admin/roles/${roleId}`)
	},

	// 创建角色
	createRole(data) {
		return request.post('/api/v1/admin/roles', data)
	},

	// 更新角色
	updateRole(roleId, data) {
		return request.put(`/api/v1/admin/roles/${roleId}`, data)
	},

	// 删除角色
	deleteRole(roleId) {
		return request.delete(`/api/v1/admin/roles/${roleId}`)
	},

	// 获取所有权限
	getPermissions(params) {
		return request.get('/api/v1/admin/permissions', params)
	},

	// 分配用户角色
	assignUserRoles(userId, roleIds) {
		return request.post(`/api/v1/admin/users/${userId}/roles`, { role_ids: roleIds })
	},

	// 获取用户角色
	getUserRoles(userId) {
		return request.get(`/api/v1/admin/users/${userId}/roles`)
	},

	// 获取用户权限
	getUserPermissions(userId) {
		return request.get(`/api/v1/admin/users/${userId}/permissions`)
	},

	// 初始化角色和权限
	initRolesAndPermissions() {
		return request.post('/api/v1/admin/roles/init')
	},

	// ========== 管理端：数据导出与报表 ==========

	// 导出订单数据
	exportOrders(params) {
		return request.get('/api/v1/admin/export/orders', params)
	},

	// 导出用户数据
	exportUsers(params) {
		return request.get('/api/v1/admin/export/users', params)
	},

	// 获取报表概览
	getReportsOverview(timeRange = 'month') {
		return request.get('/api/v1/admin/reports/overview', { time_range: timeRange })
	},

	// 获取订单趋势
	getOrderTrend(timeRange = 'month') {
		return request.get('/api/v1/admin/reports/order-trend', { time_range: timeRange })
	},

	// 获取项目排行
	getProjectRanking(params) {
		return request.get('/api/v1/admin/reports/project-ranking', params)
	},

	// 获取实验室业绩
	getLabPerformance(timeRange = 'month') {
		return request.get('/api/v1/admin/reports/lab-performance', { time_range: timeRange })
	},

	// 获取财务汇总
	getFinanceSummary(year, month) {
		return request.get('/api/v1/admin/reports/finance-summary', { year, month })
	}
}


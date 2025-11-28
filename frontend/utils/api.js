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
	
	// ========== 订单相关 ==========
	
	// 计算订单费用
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
	}
}


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
	}
}


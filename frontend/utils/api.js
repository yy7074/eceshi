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
	}
}


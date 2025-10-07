/**
 * API请求封装
 */

// 开发环境API地址
const DEV_BASE_URL = 'http://localhost:8000'
// 生产环境API地址
const PROD_BASE_URL = 'https://api.yourdomain.com'

// 根据环境选择API地址
const BASE_URL = process.env.NODE_ENV === 'development' ? DEV_BASE_URL : PROD_BASE_URL

/**
 * 请求封装
 * @param {Object} options 请求配置
 */
function request(options) {
	return new Promise((resolve, reject) => {
		// 获取token
		const token = uni.getStorageSync('token')
		
		uni.request({
			url: BASE_URL + options.url,
			method: options.method || 'GET',
			data: options.data || {},
			header: {
				'Content-Type': 'application/json',
				'Authorization': token ? `Bearer ${token}` : '',
				...options.header
			},
			success: (res) => {
				if (res.statusCode === 200) {
					// 业务逻辑处理
					if (res.data.code === 200) {
						resolve(res.data)
					} else {
						// 业务错误
						uni.showToast({
							title: res.data.message || '请求失败',
							icon: 'none'
						})
						reject(res.data)
					}
				} else if (res.statusCode === 401) {
					// 未授权，跳转登录
					uni.showToast({
						title: '请先登录',
						icon: 'none'
					})
					setTimeout(() => {
						uni.navigateTo({
							url: '/pages/login/login'
						})
					}, 1500)
					reject(res.data)
				} else {
					// HTTP错误
					uni.showToast({
						title: '网络错误',
						icon: 'none'
					})
					reject(res.data)
				}
			},
			fail: (err) => {
				uni.showToast({
					title: '网络请求失败',
					icon: 'none'
				})
				reject(err)
			}
		})
	})
}

// 导出请求方法
export default {
	get(url, data, options = {}) {
		return request({
			url,
			method: 'GET',
			data,
			...options
		})
	},
	post(url, data, options = {}) {
		return request({
			url,
			method: 'POST',
			data,
			...options
		})
	},
	put(url, data, options = {}) {
		return request({
			url,
			method: 'PUT',
			data,
			...options
		})
	},
	delete(url, data, options = {}) {
		return request({
			url,
			method: 'DELETE',
			data,
			...options
		})
	}
}


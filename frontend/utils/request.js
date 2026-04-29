/**
 * API请求封装
 */

// 开发环境API地址
// const DEV_BASE_URL = 'http://8.148.188.85:3000'
const DEV_BASE_URL = 'https://www.keyanbaice.com'

// 生产环境API地址
// const PROD_BASE_URL = 'http://8.148.188.85:3000'
const PROD_BASE_URL = 'https://www.keyanbaice.com'
// 根据环境选择API地址
const BASE_URL = process.env.NODE_ENV === 'development' ? DEV_BASE_URL : PROD_BASE_URL
let isRedirectingToLogin = false

function clearLoginState() {
	uni.removeStorageSync('token')
	uni.removeStorageSync('userInfo')
}

function redirectToLogin() {
	if (isRedirectingToLogin) {
		return
	}
	const pages = getCurrentPages()
	const currentPage = pages[pages.length - 1]
	const currentRoute = currentPage ? `/${currentPage.route}` : ''
	if (currentRoute === '/pages/login/login') {
		return
	}

	isRedirectingToLogin = true
	setTimeout(() => {
		uni.reLaunch({
			url: '/pages/login/login?force=1',
			complete: () => {
				setTimeout(() => {
					isRedirectingToLogin = false
				}, 500)
			}
		})
	}, 600)
}

function buildUrl(url, params) {
	if (!params || typeof params !== 'object') {
		return url
	}
	const queryItems = []
	Object.entries(params).forEach(([key, value]) => {
		if (value === undefined || value === null || value === '') {
			return
		}
		if (Array.isArray(value)) {
			value.forEach(item => {
				queryItems.push(`${encodeURIComponent(key)}=${encodeURIComponent(item)}`)
			})
			return
		}
		queryItems.push(`${encodeURIComponent(key)}=${encodeURIComponent(value)}`)
	})
	const queryString = queryItems.join('&')
	if (!queryString) {
		return url
	}
	return `${url}${url.includes('?') ? '&' : '?'}${queryString}`
}

/**
 * 请求封装
 * @param {Object} options 请求配置
 */
function request(options) {
	return new Promise((resolve, reject) => {
		// 获取token
		const token = uni.getStorageSync('token')
		
		// 构建请求头：只有 token 存在时才加 Authorization
		const headers = {
			'Content-Type': 'application/json',
			...options.header
		}
		if (token) {
			headers['Authorization'] = `Bearer ${token}`
		}
		
		uni.request({
			url: BASE_URL + buildUrl(options.url, options.params),
			method: options.method || 'GET',
			data: options.data || {},
			header: headers,
			success: (res) => {
				if (res.statusCode === 200) {
					// 业务逻辑处理
					if (res.data.code === 200 || res.data.code === 0) {
						resolve(res.data)
					} else {
						// 业务错误
						uni.showToast({
							title: res.data.message || '请求失败',
							icon: 'none'
						})
						reject(res.data)
					}
				} else if (res.statusCode === 401 || (res.statusCode === 403 && res.data && res.data.detail === 'Not authenticated')) {
					// 未授权或未登录，跳转登录
					clearLoginState()
					uni.showToast({
						title: '请先登录',
						icon: 'none'
					})
					redirectToLogin()
					reject(res.data)
				} else {
					// HTTP错误
					uni.showToast({
						title: res.data.message || res.data.detail || '网络错误',
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
	baseUrl: BASE_URL,
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

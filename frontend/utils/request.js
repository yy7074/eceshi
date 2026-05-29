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
let lastLoginPromptAt = 0

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

	const now = Date.now()
	if (now - lastLoginPromptAt < 3000) {
		return
	}
	lastLoginPromptAt = now
	isRedirectingToLogin = true
	uni.showModal({
		title: '需要登录',
		content: '登录后可继续使用该功能，也可以先返回首页浏览。',
		confirmText: '去登录',
		cancelText: '先逛逛',
		success: (res) => {
			if (res.confirm) {
				uni.navigateTo({
					url: '/pages/login/login?force=1',
					fail: () => {
						uni.reLaunch({ url: '/pages/login/login?force=1' })
					}
				})
				return
			}
			uni.switchTab({
				url: '/pages/index/index'
			})
		},
		complete: () => {
			setTimeout(() => {
				isRedirectingToLogin = false
			}, 500)
		}
	})
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
		
		const requestUrl = BASE_URL + buildUrl(options.url, options.params)
		uni.request({
			url: requestUrl,
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
				const rawMessage = err && err.errMsg ? err.errMsg : '网络请求失败'
				const toastMessage = rawMessage.replace(/^request:fail\s*/, '') || '网络请求失败'
				console.error('网络请求失败', {
					url: requestUrl,
					method: options.method || 'GET',
					err
				})
				uni.showToast({
					title: toastMessage.length > 28 ? toastMessage.slice(0, 28) : toastMessage,
					icon: 'none',
					duration: 3000
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
			params: options.params || data,
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

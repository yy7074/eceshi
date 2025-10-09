import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const store = new Vuex.Store({
	state: {
		token: '',
		userInfo: null,
		hasLogin: false
	},
	mutations: {
		SET_TOKEN(state, token) {
			state.token = token
			state.hasLogin = !!token
			uni.setStorageSync('token', token)
		},
		SET_USER_INFO(state, userInfo) {
			state.userInfo = userInfo
			uni.setStorageSync('userInfo', JSON.stringify(userInfo))
		},
		LOGOUT(state) {
			state.token = ''
			state.userInfo = null
			state.hasLogin = false
			uni.removeStorageSync('token')
			uni.removeStorageSync('userInfo')
		}
	},
	actions: {
		// 登录
		login({ commit }, { token, userInfo }) {
			commit('SET_TOKEN', token)
			commit('SET_USER_INFO', userInfo)
		},
		// 登出
		logout({ commit }) {
			commit('LOGOUT')
			// 跳转到登录页
			uni.reLaunch({
				url: '/pages/login/login'
			})
		}
	}
})

export default store


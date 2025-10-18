<template>
	<view class="login-container">
		<!-- 顶部装饰 -->
		<view class="header">
			<view class="logo">🔬</view>
			<text class="title">科研检测服务平台</text>
			<text class="subtitle">一站式科研检测服务</text>
		</view>
		
		<!-- 登录表单 -->
		<view class="form-container">
			<!-- Tab切换 -->
			<view class="tabs">
				<view 
					class="tab-item" 
					:class="{ active: currentTab === 'password' }"
					@click="switchTab('password')"
				>
					<text>密码登录</text>
				</view>
				<view 
					class="tab-item" 
					:class="{ active: currentTab === 'sms' }"
					@click="switchTab('sms')"
				>
					<text>验证码登录</text>
				</view>
			</view>
			
			<!-- 密码登录 -->
			<view v-if="currentTab === 'password'" class="form">
				<view class="form-item">
					<text class="label">手机号</text>
					<input 
						v-model="passwordForm.phone" 
						type="number"
						maxlength="11"
						placeholder="请输入手机号"
						class="input"
					/>
				</view>
				
				<view class="form-item">
					<text class="label">密码</text>
					<input 
						v-model="passwordForm.password"
						:password="!showPassword"
						placeholder="请输入密码"
						class="input"
					/>
					<text 
						class="icon-eye" 
						@click="showPassword = !showPassword"
					>
						{{ showPassword ? '👁️' : '👁️‍🗨️' }}
					</text>
				</view>
				
				<button 
					class="btn-primary btn-login" 
					:loading="loading"
					@click="handlePasswordLogin"
				>
					登录
				</button>
			</view>
			
			<!-- 验证码登录 -->
			<view v-if="currentTab === 'sms'" class="form">
				<view class="form-item">
					<text class="label">手机号</text>
					<input 
						v-model="smsForm.phone" 
						type="number"
						maxlength="11"
						placeholder="请输入手机号"
						class="input"
					/>
				</view>
				
				<view class="form-item">
					<text class="label">验证码</text>
					<input 
						v-model="smsForm.sms_code"
						type="number"
						maxlength="6"
						placeholder="请输入验证码"
						class="input"
					/>
					<button 
						class="btn-sms" 
						:disabled="countdown > 0"
						@click="sendSmsCode"
					>
						{{ countdown > 0 ? `${countdown}秒后重试` : '获取验证码' }}
					</button>
				</view>
				
				<button 
					class="btn-primary btn-login" 
					:loading="loading"
					@click="handleSmsLogin"
				>
					登录
				</button>
			</view>
			
			<!-- 底部链接 -->
			<view class="footer-links">
				<text @click="goRegister" class="link">立即注册</text>
				<text class="divider">|</text>
				<text @click="goForgetPassword" class="link">忘记密码</text>
			</view>
			
			<!-- 协议 -->
			<view class="agreement">
				<checkbox-group @change="onAgreeChange">
					<label>
						<checkbox value="agree" :checked="agreed" color="#007AFF" />
						<text class="agreement-text">
							我已阅读并同意
							<text class="link" @click.stop="showAgreement('user')">《用户协议》</text>
							和
							<text class="link" @click.stop="showAgreement('privacy')">《隐私政策》</text>
						</text>
					</label>
				</checkbox-group>
			</view>
		</view>
		
		<!-- 其他登录方式 -->
		<!-- #ifdef MP-WEIXIN -->
		<view class="other-login">
			<view class="divider-line">
				<text class="divider-text">其他登录方式</text>
			</view>
			<view class="login-icons">
				<view class="icon-item" @click="wechatLogin">
					<view class="icon">💬</view>
					<text class="icon-text">微信</text>
				</view>
			</view>
		</view>
		<!-- #endif -->
	</view>
</template>

<script>
	import api from '@/utils/api.js'
	
	export default {
		data() {
			return {
				currentTab: 'password', // password | sms
				passwordForm: {
					phone: '',
					password: ''
				},
				smsForm: {
					phone: '',
					sms_code: ''
				},
				showPassword: false,
				loading: false,
				countdown: 0,
				agreed: false
			}
		},
		onLoad() {
			// 检查是否已登录
			const token = uni.getStorageSync('token')
			if (token) {
				uni.switchTab({
					url: '/pages/index/index'
				})
			}
		},
		methods: {
			// 切换Tab
			switchTab(tab) {
				this.currentTab = tab
			},
			
			// 密码登录
			async handlePasswordLogin() {
				// 验证
				if (!this.passwordForm.phone) {
					return uni.showToast({ title: '请输入手机号', icon: 'none' })
				}
				if (!/^1[3-9]\d{9}$/.test(this.passwordForm.phone)) {
					return uni.showToast({ title: '手机号格式不正确', icon: 'none' })
				}
				if (!this.passwordForm.password) {
					return uni.showToast({ title: '请输入密码', icon: 'none' })
				}
				if (!this.agreed) {
					return uni.showToast({ title: '请先阅读并同意用户协议', icon: 'none' })
				}
				
				this.loading = true
				try {
					const res = await api.login(this.passwordForm)
					
					// 保存登录信息
					this.$store.dispatch('login', {
						token: res.data.access_token,
						userInfo: {
							id: res.data.user_id,
							phone: res.data.phone,
							nickname: res.data.nickname
						}
					})
					
					uni.showToast({
						title: '登录成功',
						icon: 'success'
					})
					
					// 跳转到首页
					setTimeout(() => {
						uni.switchTab({
							url: '/pages/index/index'
						})
					}, 1500)
					
				} catch (error) {
					console.error('登录失败', error)
				} finally {
					this.loading = false
				}
			},
			
			// 验证码登录
			async handleSmsLogin() {
				// 验证
				if (!this.smsForm.phone) {
					return uni.showToast({ title: '请输入手机号', icon: 'none' })
				}
				if (!/^1[3-9]\d{9}$/.test(this.smsForm.phone)) {
					return uni.showToast({ title: '手机号格式不正确', icon: 'none' })
				}
				if (!this.smsForm.sms_code) {
					return uni.showToast({ title: '请输入验证码', icon: 'none' })
				}
				if (!this.agreed) {
					return uni.showToast({ title: '请先阅读并同意用户协议', icon: 'none' })
				}
				
				this.loading = true
				try {
					const res = await api.smsLogin(this.smsForm)
					
					// 保存登录信息
					this.$store.dispatch('login', {
						token: res.data.access_token,
						userInfo: {
							id: res.data.user_id,
							phone: res.data.phone,
							nickname: res.data.nickname
						}
					})
					
					uni.showToast({
						title: '登录成功',
						icon: 'success'
					})
					
					// 跳转到首页
					setTimeout(() => {
						uni.switchTab({
							url: '/pages/index/index'
						})
					}, 1500)
					
				} catch (error) {
					console.error('登录失败', error)
				} finally {
					this.loading = false
				}
			},
			
			// 发送验证码
			async sendSmsCode() {
				if (!this.smsForm.phone) {
					return uni.showToast({ title: '请输入手机号', icon: 'none' })
				}
				if (!/^1[3-9]\d{9}$/.test(this.smsForm.phone)) {
					return uni.showToast({ title: '手机号格式不正确', icon: 'none' })
				}
				
				try {
					await api.sendSms({
						phone: this.smsForm.phone,
						scene: 'login'
					})
					
					uni.showToast({
						title: '验证码已发送',
						icon: 'success'
					})
					
					// 倒计时
					this.countdown = 60
					const timer = setInterval(() => {
						this.countdown--
						if (this.countdown <= 0) {
							clearInterval(timer)
						}
					}, 1000)
					
				} catch (error) {
					console.error('发送验证码失败', error)
				}
			},
			
			// 微信登录
			wechatLogin() {
				// #ifdef MP-WEIXIN
				uni.login({
					provider: 'weixin',
					success: async (loginRes) => {
						try {
							const res = await api.wechatLogin(loginRes.code)
							
							// 保存登录信息
							this.$store.dispatch('login', {
								token: res.data.access_token,
								userInfo: {
									id: res.data.user_id,
									phone: res.data.phone,
									nickname: res.data.nickname
								}
							})
							
							uni.showToast({
								title: '登录成功',
								icon: 'success'
							})
							
							// 跳转到首页
							setTimeout(() => {
								uni.switchTab({
									url: '/pages/index/index'
								})
							}, 1500)
							
						} catch (error) {
							console.error('微信登录失败', error)
							uni.showToast({
								title: '微信登录失败',
								icon: 'none'
							})
						}
					},
					fail: (error) => {
						console.error('微信授权失败', error)
						uni.showToast({
							title: '微信授权失败',
							icon: 'none'
						})
					}
				})
				// #endif
			},
			
			// 跳转注册
			goRegister() {
				uni.navigateTo({
					url: '/pages/register/register'
				})
			},
			
			// 忘记密码
			goForgetPassword() {
				uni.navigateTo({
					url: '/pages/forget-password/forget-password'
				})
			},
			
			// 协议变更
			onAgreeChange(e) {
				this.agreed = e.detail.value.length > 0
			},
			
			// 显示协议
			showAgreement(type) {
				uni.showModal({
					title: type === 'user' ? '用户协议' : '隐私政策',
					content: '协议内容...',
					showCancel: false
				})
			}
		}
	}
</script>

<style lang="scss" scoped>
	.login-container {
		min-height: 100vh;
		background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
		padding: 80rpx 60rpx;
	}
	
	.header {
		text-align: center;
		margin-bottom: 80rpx;
		
		.logo {
			font-size: 120rpx;
			margin-bottom: 30rpx;
			text-align: center;
		}
		
		.title {
			display: block;
			font-size: 48rpx;
			font-weight: bold;
			color: #ffffff;
			margin-bottom: 16rpx;
		}
		
		.subtitle {
			display: block;
			font-size: 28rpx;
			color: rgba(255, 255, 255, 0.8);
		}
	}
	
	.form-container {
		background-color: #ffffff;
		border-radius: 24rpx;
		padding: 60rpx 40rpx;
		box-shadow: 0 8rpx 32rpx rgba(0, 0, 0, 0.1);
	}
	
	.tabs {
		display: flex;
		margin-bottom: 50rpx;
		
		.tab-item {
			flex: 1;
			text-align: center;
			padding-bottom: 20rpx;
			font-size: 32rpx;
			color: #666;
			border-bottom: 4rpx solid transparent;
			transition: all 0.3s;
			
			&.active {
				color: #007AFF;
				border-bottom-color: #007AFF;
				font-weight: bold;
			}
		}
	}
	
	.form {
		.form-item {
			position: relative;
			margin-bottom: 40rpx;
			
			.label {
				display: block;
				font-size: 28rpx;
				color: #333;
				margin-bottom: 16rpx;
			}
			
			.input {
				width: 100%;
				height: 88rpx;
				padding: 0 24rpx;
				border: 2rpx solid #e0e0e0;
				border-radius: 12rpx;
				font-size: 30rpx;
				
				&:focus {
					border-color: #007AFF;
				}
			}
			
			.icon-eye {
				position: absolute;
				right: 24rpx;
				bottom: 24rpx;
				font-size: 40rpx;
			}
			
			.btn-sms {
				position: absolute;
				right: 12rpx;
				bottom: 12rpx;
				padding: 12rpx 24rpx;
				background-color: #007AFF;
				color: #ffffff;
				border: none;
				border-radius: 8rpx;
				font-size: 24rpx;
				
				&:disabled {
					background-color: #cccccc;
				}
			}
		}
		
		.btn-login {
			width: 100%;
			margin-top: 30rpx;
			height: 88rpx;
			line-height: 88rpx;
			font-size: 32rpx;
		}
	}
	
	.footer-links {
		display: flex;
		justify-content: center;
		align-items: center;
		margin-top: 40rpx;
		font-size: 26rpx;
		
		.link {
			color: #007AFF;
		}
		
		.divider {
			margin: 0 20rpx;
			color: #ccc;
		}
	}
	
	.agreement {
		margin-top: 40rpx;
		font-size: 24rpx;
		color: #666;
		
		.agreement-text {
			margin-left: 12rpx;
		}
		
		.link {
			color: #007AFF;
		}
	}
	
	.other-login {
		margin-top: 80rpx;
		
		.divider-line {
			text-align: center;
			margin-bottom: 40rpx;
			
			.divider-text {
				position: relative;
				padding: 0 20rpx;
				color: rgba(255, 255, 255, 0.8);
				font-size: 26rpx;
				
				&::before,
				&::after {
					content: '';
					position: absolute;
					top: 50%;
					width: 100rpx;
					height: 2rpx;
					background-color: rgba(255, 255, 255, 0.3);
				}
				
				&::before {
					right: 100%;
					margin-right: 20rpx;
				}
				
				&::after {
					left: 100%;
					margin-left: 20rpx;
				}
			}
		}
		
		.login-icons {
			display: flex;
			justify-content: center;
			
			.icon-item {
				display: flex;
				flex-direction: column;
				align-items: center;
				
				.icon {
					font-size: 80rpx;
					margin-bottom: 12rpx;
				}
				
				.icon-text {
					font-size: 24rpx;
					color: rgba(255, 255, 255, 0.8);
				}
			}
		}
	}
</style>


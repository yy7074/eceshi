<template>
	<view class="register-container">
		<view class="header">
			<text class="title">用户注册</text>
			<text class="subtitle">欢迎加入博才科研百测</text>
		</view>
		
		<view class="form-container">
			<view class="form-item">
				<text class="label">手机号</text>
				<input 
					v-model="form.phone" 
					type="number"
					maxlength="11"
					placeholder="请输入手机号"
					class="input"
				/>
			</view>
			
			<view class="form-item">
				<text class="label">验证码</text>
				<input 
					v-model="form.sms_code"
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
					{{ countdown > 0 ? `${countdown}秒` : '获取验证码' }}
				</button>
			</view>
			
			<view class="form-item">
				<text class="label">设置密码</text>
				<input 
					v-model="form.password"
					:password="!showPassword"
					placeholder="请设置6位以上密码"
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
				class="btn-primary btn-register" 
				:loading="loading"
				@click="handleRegister"
			>
				立即注册
			</button>
			
			<view class="footer-link">
				<text>已有账号？</text>
				<text class="link" @click="goLogin">立即登录</text>
			</view>
		</view>
	</view>
</template>

<script>
	import api from '@/utils/api.js'
	
	export default {
		data() {
			return {
				form: {
					phone: '',
					password: '',
					sms_code: ''
				},
				showPassword: false,
				loading: false,
				countdown: 0
			}
		},
		methods: {
			// 发送验证码
			async sendSmsCode() {
				if (!this.form.phone) {
					return uni.showToast({ title: '请输入手机号', icon: 'none' })
				}
				if (!/^1[3-9]\d{9}$/.test(this.form.phone)) {
					return uni.showToast({ title: '手机号格式不正确', icon: 'none' })
				}
				
				try {
					const res = await api.sendSms({
						phone: this.form.phone,
						scene: 'register'
					})
					
					uni.showToast({
						title: '验证码已发送',
						icon: 'success'
					})
					
					// 开发模式显示验证码
					if (res.data && res.data.code) {
						uni.showModal({
							title: '验证码（开发模式）',
							content: `验证码：${res.data.code}`,
							showCancel: false
						})
					}
					
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
			
			// 注册
			async handleRegister() {
				// 验证
				if (!this.form.phone) {
					return uni.showToast({ title: '请输入手机号', icon: 'none' })
				}
				if (!/^1[3-9]\d{9}$/.test(this.form.phone)) {
					return uni.showToast({ title: '手机号格式不正确', icon: 'none' })
				}
				if (!this.form.sms_code) {
					return uni.showToast({ title: '请输入验证码', icon: 'none' })
				}
				if (!this.form.password) {
					return uni.showToast({ title: '请设置密码', icon: 'none' })
				}
				if (this.form.password.length < 6) {
					return uni.showToast({ title: '密码至少6位', icon: 'none' })
				}
				
					this.loading = true
					try {
						const res = await api.register({
							...this.form,
							...this.getPendingInvitePayload()
						})
						
						// 保存登录信息
						this.$store.dispatch('login', {
						token: res.data.access_token,
						userInfo: {
							id: res.data.user_id,
							phone: res.data.phone,
								nickname: res.data.nickname
							}
						})
						this.clearPendingInvite()
					
					uni.showToast({
						title: '注册成功',
						icon: 'success'
					})
					
					// 跳转到首页
					setTimeout(() => {
						uni.switchTab({
							url: '/pages/index/index'
						})
					}, 1500)
					
				} catch (error) {
					console.error('注册失败', error)
				} finally {
					this.loading = false
				}
			},
			
				// 返回登录
				goLogin() {
					uni.navigateBack()
				},

				getPendingInvitePayload() {
					const stored = uni.getStorageSync('pendingInvite')
					if (!stored) {
						return {}
					}
					if (typeof stored === 'string') {
						try {
							return JSON.parse(stored)
						} catch (error) {
							return {}
						}
					}
					return stored
				},

				clearPendingInvite() {
					uni.removeStorageSync('pendingInvite')
				}
			}
		}
</script>

<style lang="scss" scoped>
	.register-container {
		min-height: 100vh;
		background: #1890ff;
		padding: 80rpx 60rpx;
	}
	
	.header {
		text-align: center;
		margin-bottom: 80rpx;
		
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
		
		.btn-register {
			width: 100%;
			margin-top: 30rpx;
			height: 88rpx;
			line-height: 88rpx;
			font-size: 32rpx;
		}
		
		.footer-link {
			text-align: center;
			margin-top: 40rpx;
			font-size: 26rpx;
			color: #666;
			
			.link {
				color: #007AFF;
				margin-left: 12rpx;
			}
		}
	}
</style>

<template>
	<view class="user-container">
		<!-- 用户信息卡片 -->
		<view class="user-card">
			<view v-if="hasLogin" class="user-info">
				<view v-if="userInfo.avatar" class="avatar">
					<image :src="userInfo.avatar" mode="aspectFill" class="avatar-img"></image>
				</view>
				<view v-else class="avatar avatar-placeholder">👤</view>
				<view class="info">
					<text class="nickname">{{ userInfo.nickname || '未设置昵称' }}</text>
					<text class="phone">{{ userInfo.phone }}</text>
				</view>
				<view v-if="userInfo.membership_level > 0" class="vip-badge">
					{{ membershipText }}
				</view>
			</view>
			<view v-else class="user-info" @click="goLogin">
				<view class="avatar avatar-placeholder">👤</view>
				<view class="info">
					<text class="nickname">点击登录/注册</text>
					<text class="phone">登录后享受更多服务</text>
				</view>
			</view>
		</view>
		
		<!-- 账户信息 -->
		<view v-if="hasLogin" class="account-info card">
			<view class="info-item" @click="goBalance">
				<view class="value">¥{{ balance.prepaid_balance }}</view>
				<view class="label">预付余额</view>
			</view>
			<view class="divider"></view>
			<view class="info-item" @click="goBalance">
				<view class="value">¥{{ balance.available_credit }}</view>
				<view class="label">可用额度</view>
			</view>
			<view class="divider"></view>
			<view class="info-item" @click="goPoints">
				<view class="value">{{ balance.points_balance }}</view>
				<view class="label">我的积分</view>
			</view>
		</view>
		
		<!-- 菜单列表 -->
		<view class="menu-list">
			<!-- 我的服务 -->
			<view class="menu-section card">
				<view class="section-title">我的服务</view>
				<view class="menu-item" @click="goPage('/pagesA/certification/certification')">
					<text class="icon">📝</text>
					<text class="title">实名认证</text>
					<view class="badge" v-if="!userInfo.is_certified">未认证</view>
					<text class="arrow">></text>
				</view>
				<view class="menu-item" @click="goPage('/pagesA/member/member')">
					<text class="icon">👑</text>
					<text class="title">会员中心</text>
					<text class="arrow">></text>
				</view>
				<view class="menu-item" @click="goPage('/pages/order/order')">
					<text class="icon">📋</text>
					<text class="title">我的订单</text>
					<text class="arrow">></text>
				</view>
			</view>
			
			<!-- 账户管理 -->
			<view class="menu-section card">
				<view class="section-title">账户管理</view>
				<view class="menu-item" @click="goPage('/pagesA/balance/balance')">
					<text class="icon">💰</text>
					<text class="title">账户余额</text>
					<text class="arrow">></text>
				</view>
				<view class="menu-item" @click="goPage('/pagesA/invoice/invoice')">
					<text class="icon">🧾</text>
					<text class="title">发票管理</text>
					<text class="arrow">></text>
				</view>
				<view class="menu-item" @click="goPage('/pagesA/coupon/coupon')">
					<text class="icon">🎫</text>
					<text class="title">优惠券</text>
					<text class="arrow">></text>
				</view>
			</view>
			
			<!-- 设置 -->
			<view class="menu-section card">
				<view class="section-title">设置</view>
				<view class="menu-item" @click="goPage('/pagesA/settings/settings')">
					<text class="icon">⚙️</text>
					<text class="title">设置</text>
					<text class="arrow">></text>
				</view>
				<view class="menu-item" @click="goPage('/pagesA/about/about')">
					<text class="icon">ℹ️</text>
					<text class="title">关于我们</text>
					<text class="arrow">></text>
				</view>
			</view>
		</view>
		
		<!-- 退出登录 -->
		<view v-if="hasLogin" class="logout-btn">
			<button class="btn" @click="handleLogout">退出登录</button>
		</view>
	</view>
</template>

<script>
	import api from '@/utils/api.js'
	
	export default {
		data() {
			return {
				userInfo: {},
				balance: {
					prepaid_balance: 0,
					available_credit: 0,
					points_balance: 0
				}
			}
		},
		computed: {
			hasLogin() {
				return this.$store.state.hasLogin
			},
			membershipText() {
				const level = this.userInfo.membership_level
				const map = { 1: '银卡会员', 2: '金卡会员', 3: '白金卡会员' }
				return map[level] || ''
			}
		},
		onShow() {
			if (this.hasLogin) {
				this.loadUserInfo()
				this.loadBalance()
			}
		},
		methods: {
			// 加载用户信息
			async loadUserInfo() {
				try {
					const res = await api.getUserInfo()
					this.userInfo = res.data
					this.$store.commit('SET_USER_INFO', res.data)
				} catch (error) {
					console.error('加载用户信息失败', error)
				}
			},
			
			// 加载余额
			async loadBalance() {
				try {
					const res = await api.getBalance()
					this.balance = res.data
				} catch (error) {
					console.error('加载余额失败', error)
				}
			},
			
			// 跳转登录
			goLogin() {
				uni.navigateTo({
					url: '/pages/login/login'
				})
			},
			
			// 跳转页面
			goPage(url) {
				if (!this.hasLogin) {
					return this.goLogin()
				}
				uni.navigateTo({ url })
			},
			
			// 跳转余额页
			goBalance() {
				this.goPage('/pagesA/balance/balance')
			},
			
			// 跳转积分页
			goPoints() {
				this.goPage('/pagesA/points/points')
			},
			
			// 退出登录
			handleLogout() {
				uni.showModal({
					title: '提示',
					content: '确定要退出登录吗？',
					success: (res) => {
						if (res.confirm) {
							this.$store.dispatch('logout')
							this.userInfo = {}
							this.balance = {
								prepaid_balance: 0,
								available_credit: 0,
								points_balance: 0
							}
						}
					}
				})
			}
		}
	}
</script>

<style lang="scss" scoped>
	.user-container {
		min-height: 100vh;
		background-color: #f8f8f8;
		padding-bottom: 40rpx;
	}
	
	.user-card {
		background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
		padding: 60rpx 30rpx 40rpx;
		
		.user-info {
			display: flex;
			align-items: center;
			
			.avatar {
				width: 120rpx;
				height: 120rpx;
				border-radius: 60rpx;
				border: 4rpx solid rgba(255, 255, 255, 0.3);
				overflow: hidden;
				display: flex;
				align-items: center;
				justify-content: center;
				background-color: rgba(255, 255, 255, 0.2);
				
				&-placeholder {
					font-size: 60rpx;
					line-height: 1;
				}
				
				&-img {
					width: 100%;
					height: 100%;
				}
			}
			
			.info {
				flex: 1;
				margin-left: 24rpx;
				
				.nickname {
					display: block;
					font-size: 36rpx;
					font-weight: bold;
					color: #ffffff;
					margin-bottom: 12rpx;
				}
				
				.phone {
					display: block;
					font-size: 26rpx;
					color: rgba(255, 255, 255, 0.8);
				}
			}
			
			.vip-badge {
				padding: 8rpx 20rpx;
				background: linear-gradient(135deg, #FFD700, #FFA500);
				border-radius: 30rpx;
				font-size: 22rpx;
				color: #ffffff;
				font-weight: bold;
			}
		}
	}
	
	.account-info {
		display: flex;
		margin: -40rpx 30rpx 20rpx;
		padding: 30rpx 0;
		background-color: #ffffff;
		box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.08);
		
		.info-item {
			flex: 1;
			text-align: center;
			
			.value {
				font-size: 36rpx;
				font-weight: bold;
				color: #333;
				margin-bottom: 12rpx;
			}
			
			.label {
				font-size: 24rpx;
				color: #999;
			}
		}
		
		.divider {
			width: 2rpx;
			background-color: #f0f0f0;
		}
	}
	
	.menu-list {
		padding: 0 30rpx;
		
		.menu-section {
			margin-bottom: 20rpx;
			
			.section-title {
				padding: 24rpx;
				font-size: 28rpx;
				color: #666;
				font-weight: bold;
			}
			
			.menu-item {
				display: flex;
				align-items: center;
				padding: 30rpx 24rpx;
				border-bottom: 2rpx solid #f5f5f5;
				
				&:last-child {
					border-bottom: none;
				}
				
				.icon {
					font-size: 40rpx;
					margin-right: 20rpx;
				}
				
				.title {
					flex: 1;
					font-size: 30rpx;
					color: #333;
				}
				
				.badge {
					padding: 4rpx 12rpx;
					background-color: #ff4d4f;
					color: #ffffff;
					font-size: 20rpx;
					border-radius: 20rpx;
					margin-right: 12rpx;
				}
				
				.arrow {
					font-size: 28rpx;
					color: #ccc;
				}
			}
		}
	}
	
	.logout-btn {
		padding: 0 30rpx;
		margin-top: 40rpx;
		
		.btn {
			width: 100%;
			height: 88rpx;
			line-height: 88rpx;
			background-color: #ffffff;
			color: #ff4d4f;
			border-radius: 12rpx;
			font-size: 32rpx;
			border: 2rpx solid #ff4d4f;
		}
	}
</style>


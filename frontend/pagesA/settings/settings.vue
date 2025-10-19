<template>
	<view class="settings-page">
		<!-- 账号与安全 -->
		<view class="settings-section">
			<view class="section-title">账号与安全</view>
			<view class="settings-list">
				<view class="setting-item" @click="goPage('/pagesA/profile/profile')">
					<view class="item-left">
						<text class="item-icon">👤</text>
						<text class="item-label">个人资料</text>
					</view>
					<view class="item-right">
						<text class="item-arrow">›</text>
					</view>
				</view>
				<view class="setting-item" @click="goPage('/pagesA/certification/certification')">
					<view class="item-left">
						<text class="item-icon">🆔</text>
						<text class="item-label">实名认证</text>
					</view>
					<view class="item-right">
						<text v-if="userInfo.is_certified" class="certified-badge">已认证</text>
						<text class="item-arrow">›</text>
					</view>
				</view>
				<view class="setting-item" @click="showToast('修改手机号')">
					<view class="item-left">
						<text class="item-icon">📱</text>
						<text class="item-label">手机号</text>
					</view>
					<view class="item-right">
						<text class="item-value">{{ userInfo.phone || '未绑定' }}</text>
						<text class="item-arrow">›</text>
					</view>
				</view>
				<view class="setting-item" @click="showToast('修改密码')">
					<view class="item-left">
						<text class="item-icon">🔐</text>
						<text class="item-label">修改密码</text>
					</view>
					<view class="item-right">
						<text class="item-arrow">›</text>
					</view>
				</view>
			</view>
		</view>
		
		<!-- 通知设置 -->
		<view class="settings-section">
			<view class="section-title">通知设置</view>
			<view class="settings-list">
				<view class="setting-item">
					<view class="item-left">
						<text class="item-icon">🔔</text>
						<text class="item-label">订单通知</text>
					</view>
					<view class="item-right">
						<switch :checked="notifications.order" @change="toggleNotification('order')" color="#667eea" />
					</view>
				</view>
				<view class="setting-item">
					<view class="item-left">
						<text class="item-icon">💬</text>
						<text class="item-label">消息通知</text>
					</view>
					<view class="item-right">
						<switch :checked="notifications.message" @change="toggleNotification('message')" color="#667eea" />
					</view>
				</view>
				<view class="setting-item">
					<view class="item-left">
						<text class="item-icon">🎯</text>
						<text class="item-label">活动通知</text>
					</view>
					<view class="item-right">
						<switch :checked="notifications.activity" @change="toggleNotification('activity')" color="#667eea" />
					</view>
				</view>
			</view>
		</view>
		
		<!-- 通用设置 -->
		<view class="settings-section">
			<view class="section-title">通用设置</view>
			<view class="settings-list">
				<view class="setting-item" @click="showToast('清除缓存')">
					<view class="item-left">
						<text class="item-icon">🗑️</text>
						<text class="item-label">清除缓存</text>
					</view>
					<view class="item-right">
						<text class="item-value">{{ cacheSize }}</text>
						<text class="item-arrow">›</text>
					</view>
				</view>
				<view class="setting-item" @click="checkUpdate">
					<view class="item-left">
						<text class="item-icon">🔄</text>
						<text class="item-label">检查更新</text>
					</view>
					<view class="item-right">
						<text class="item-value">{{ version }}</text>
						<text class="item-arrow">›</text>
					</view>
				</view>
			</view>
		</view>
		
		<!-- 关于 -->
		<view class="settings-section">
			<view class="section-title">关于</view>
			<view class="settings-list">
				<view class="setting-item" @click="showToast('用户协议')">
					<view class="item-left">
						<text class="item-icon">📄</text>
						<text class="item-label">用户协议</text>
					</view>
					<view class="item-right">
						<text class="item-arrow">›</text>
					</view>
				</view>
				<view class="setting-item" @click="showToast('隐私政策')">
					<view class="item-left">
						<text class="item-icon">🔒</text>
						<text class="item-label">隐私政策</text>
					</view>
					<view class="item-right">
						<text class="item-arrow">›</text>
					</view>
				</view>
				<view class="setting-item" @click="contactService">
					<view class="item-left">
						<text class="item-icon">☎️</text>
						<text class="item-label">联系客服</text>
					</view>
					<view class="item-right">
						<text class="item-arrow">›</text>
					</view>
				</view>
			</view>
		</view>
		
		<!-- 退出登录 -->
		<view class="logout-btn-wrapper">
			<button class="logout-btn" @click="handleLogout">退出登录</button>
		</view>
	</view>
</template>

<script>
import api from '@/utils/api.js'

export default {
	data() {
		return {
			userInfo: {},
			notifications: {
				order: true,
				message: true,
				activity: false
			},
			cacheSize: '0 MB',
			version: 'v1.0.0'
		}
	},
	
	onLoad() {
		this.loadUserInfo()
		this.calculateCacheSize()
	},
	
	methods: {
		// 加载用户信息
		async loadUserInfo() {
			try {
				const res = await api.getUserInfo()
				this.userInfo = res
			} catch (error) {
				console.error('加载用户信息失败', error)
			}
		},
		
		// 计算缓存大小
		calculateCacheSize() {
			// TODO: 实际计算缓存大小
			this.cacheSize = '0 MB'
		},
		
		// 跳转页面
		goPage(url) {
			uni.navigateTo({ url })
		},
		
		// 切换通知开关
		toggleNotification(type) {
			this.notifications[type] = !this.notifications[type]
			// TODO: 保存到本地或服务器
		},
		
		// 检查更新
		checkUpdate() {
			uni.showToast({
				title: '已是最新版本',
				icon: 'success'
			})
		},
		
		// 联系客服
		contactService() {
			uni.makePhoneCall({
				phoneNumber: '400-123-4567'
			})
		},
		
		// 退出登录
		handleLogout() {
			uni.showModal({
				title: '提示',
				content: '确定要退出登录吗？',
				success: (res) => {
					if (res.confirm) {
						// 清除本地数据
						uni.removeStorageSync('token')
						uni.removeStorageSync('userInfo')
						
						uni.showToast({
							title: '已退出登录',
							icon: 'success'
						})
						
						// 延迟跳转到登录页
						setTimeout(() => {
							uni.reLaunch({
								url: '/pages/login/login'
							})
						}, 1500)
					}
				}
			})
		},
		
		// 提示
		showToast(msg) {
			uni.showToast({
				title: msg + '功能开发中',
				icon: 'none'
			})
		}
	}
}
</script>

<style lang="scss" scoped>
.settings-page {
	min-height: 100vh;
	background: #f5f5f5;
	padding-bottom: 40rpx;
}

.settings-section {
	margin-bottom: 20rpx;
	
	.section-title {
		padding: 30rpx 30rpx 20rpx;
		font-size: 26rpx;
		color: #999;
	}
	
	.settings-list {
		background: white;
		
		.setting-item {
			display: flex;
			justify-content: space-between;
			align-items: center;
			padding: 30rpx;
			border-bottom: 1rpx solid #f5f5f5;
			
			&:last-child {
				border-bottom: none;
			}
			
			.item-left {
				display: flex;
				align-items: center;
				
				.item-icon {
					font-size: 36rpx;
					margin-right: 20rpx;
				}
				
				.item-label {
					font-size: 28rpx;
					color: #333;
				}
			}
			
			.item-right {
				display: flex;
				align-items: center;
				
				.item-value {
					font-size: 26rpx;
					color: #999;
					margin-right: 10rpx;
				}
				
				.certified-badge {
					font-size: 24rpx;
					padding: 5rpx 15rpx;
					background: #e8f5e9;
					color: #4caf50;
					border-radius: 8rpx;
					margin-right: 10rpx;
				}
				
				.item-arrow {
					font-size: 36rpx;
					color: #ccc;
				}
			}
		}
	}
}

.logout-btn-wrapper {
	padding: 40rpx 30rpx;
	
	.logout-btn {
		width: 100%;
		background: white;
		color: #ff4444;
		border: 1rpx solid #ff4444;
		border-radius: 50rpx;
		padding: 30rpx;
		font-size: 32rpx;
	}
}
</style>


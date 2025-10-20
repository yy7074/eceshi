<template>
	<view class="user-page">
		<!-- 用户信息卡片 -->
		<view class="user-header">
			<view class="user-info-card">
				<image 
					:src="userInfo.avatar || 'https://ui-avatars.com/api/?name=' + (userInfo.nickname || 'User')" 
					mode="aspectFill" 
					class="avatar"
				></image>
				<view class="user-text">
					<text class="member-id">会员{{ userInfo.member_no || 'ihC12T' }}</text>
					<text class="advisor">专属顾问{{ userInfo.advisor_name || '孙老师' }}：{{ userInfo.advisor_phone || '13385319048' }}</text>
				</view>
				<view class="edit-btn" @click="goEditProfile">
					<text class="edit-icon">✏️</text>
				</view>
			</view>
		</view>
		
		<!-- 账户金额信息 -->
		<view class="account-cards">
			<view class="account-item" @click="goAccountDetail('credit')">
				<text class="amount">{{ balance.available_credit || '0.00' }}</text>
				<text class="label">可用信用</text>
			</view>
			<view class="account-item" @click="goAccountDetail('prepaid')">
				<text class="amount">{{ balance.prepaid_balance || '0.00' }}</text>
				<view class="label-with-icon">
					<text>个人预付</text>
					<text class="info-icon" @click.stop="showPrepaidInfo">ⓘ</text>
				</view>
			</view>
			<view class="account-item" @click="goAccountDetail('invoice')">
				<text class="amount">{{ balance.invoice_amount || '0.00' }}</text>
				<text class="label">可开票</text>
			</view>
			<view class="account-item" @click="goAccountDetail('debt')">
				<text class="amount">{{ balance.debt_amount || '0.00' }}</text>
				<text class="label">个人欠款</text>
			</view>
		</view>
		
		<!-- 我的订单 -->
		<view class="order-section">
			<view class="section-header">
				<text class="title">我的订单</text>
				<view class="more" @click="goAllOrders">
					<text>全部订单</text>
					<text class="arrow">›</text>
				</view>
			</view>
			<view class="order-status-list">
				<view class="status-item" @click="goOrders('unpaid')">
					<view class="status-icon">
						<text class="icon-emoji">💳</text>
					</view>
					<text class="status-text">待支付</text>
				</view>
				<view class="status-item" @click="goOrders('paid')">
					<view class="status-icon">
						<text class="icon-emoji">⏰</text>
					</view>
					<text class="status-text">待确认</text>
				</view>
				<view class="status-item" @click="goOrders('confirmed')">
					<view class="status-icon">
						<text class="icon-emoji">📝</text>
					</view>
					<text class="status-text">待实验</text>
				</view>
				<view class="status-item" @click="goOrders('testing')">
					<view class="status-icon">
						<text class="icon-emoji">🔬</text>
					</view>
					<text class="status-text">实验中</text>
				</view>
				<view class="status-item" @click="goOrders('completed')">
					<view class="status-icon">
						<text class="icon-emoji">✅</text>
					</view>
					<text class="status-text">已完成</text>
				</view>
			</view>
		</view>
		
		<!-- 服务与工具 -->
		<view class="service-section">
			<view class="section-title">服务与工具</view>
			<view class="service-grid">
				<!-- 第一行 -->
				<view class="service-item" @click="goPage('/pagesA/certification/certification')">
					<view class="icon-wrap">
						<text class="service-icon">👤</text>
						<text class="badge new">NEW</text>
					</view>
					<text class="service-text">实名认证</text>
				</view>
				<view class="service-item" @click="goPage('/pagesA/group/group')">
					<text class="service-icon">👥</text>
					<text class="service-text">我的团体</text>
				</view>
				<view class="service-item" @click="goPage('/pagesA/invite/invite')">
					<view class="icon-wrap">
						<text class="service-icon">👥</text>
						<text class="badge rebate">返利</text>
					</view>
					<text class="service-text">邀请好友</text>
				</view>
				<view class="service-item" @click="goPage('/pagesA/points/points')">
					<view class="icon-wrap">
						<text class="service-icon">⭐</text>
						<text class="badge newest">上新</text>
					</view>
					<text class="service-text">我的积分</text>
				</view>
				
				<!-- 第二行 -->
				<view class="service-item" @click="goPage('/pagesA/wallet/wallet')">
					<text class="service-icon">💰</text>
					<text class="service-text">我的钱包</text>
				</view>
				<view class="service-item" @click="goPage('/pagesA/invoice/invoice')">
					<text class="service-icon">🧾</text>
					<text class="service-text">我的发票</text>
				</view>
				<view class="service-item" @click="goPage('/pagesA/coupon/coupon')">
					<view class="icon-wrap">
						<text class="service-icon">🎫</text>
						<text class="badge coupon">领券</text>
					</view>
					<text class="service-text">优惠券</text>
				</view>
				<view class="service-item" @click="goPage('/pagesA/prepaid/prepaid')">
					<text class="service-icon">📊</text>
					<text class="service-text">预付记录</text>
				</view>
				
				<!-- 第三行 -->
				<view class="service-item" @click="goPage('/pagesA/prize/prize')">
					<text class="service-icon">🎁</text>
					<text class="service-text">中奖记录</text>
				</view>
				<view class="service-item" @click="goPage('/pagesA/lottery/lottery')">
					<text class="service-icon">🎯</text>
					<text class="service-text">下单抽奖</text>
				</view>
				<view class="service-item" @click="goPage('/pagesA/feedback/feedback')">
					<text class="service-icon">💬</text>
					<text class="service-text">建议/投诉</text>
				</view>
				<view class="service-item" @click="goPage('/pagesA/settings/settings')">
					<text class="service-icon">⚙️</text>
					<text class="service-text">设置</text>
				</view>
			</view>
		</view>
		
		<!-- 底部占位 -->
		<view class="bottom-placeholder"></view>
	</view>
</template>

<script>
import api from '@/utils/api.js'

export default {
	data() {
		return {
			userInfo: {
				avatar: '',
				nickname: '',
				member_no: '',
				advisor_name: '',
				advisor_phone: ''
			},
			balance: {
				available_credit: 0,
				prepaid_balance: 0,
				invoice_amount: 0,
				debt_amount: 0
			}
		}
	},
	onLoad() {
		this.loadUserInfo()
		this.loadBalance()
	},
	onShow() {
		// 每次显示页面时刷新数据
		this.loadBalance()
	},
	methods: {
		// 加载用户信息
		async loadUserInfo() {
			try {
				const token = uni.getStorageSync('token')
				if (!token) {
					this.goLogin()
					return
				}
				
				const res = await api.getUserInfo()
				// res已经是后端返回的完整对象 {code, message, data}
				// res.data才是用户信息
				this.userInfo = res.data || {}
				console.log('用户信息加载成功', this.userInfo)
			} catch (e) {
				console.error('加载用户信息失败', e)
				// 即使加载失败也显示登录按钮而不是跳转
			}
		},
		
		// 加载余额信息
		async loadBalance() {
			try {
				const res = await api.getBalance()
				this.balance = res.data || {}
			} catch (e) {
				console.error('加载余额失败', e)
			}
		},
		
		// 编辑个人资料
		goEditProfile() {
			uni.navigateTo({
				url: '/pagesA/profile/profile'
			})
		},
		
	// 账户详情
	goAccountDetail(type) {
		// 根据类型跳转到对应页面
		switch(type) {
			case 'credit':
				// 可用信用 - 暂无页面，显示提示
				uni.showToast({
					title: '功能开发中',
					icon: 'none'
				})
				break
			case 'prepaid':
				// 个人预付 - 跳转到充值页面
				uni.navigateTo({
					url: '/pagesA/recharge/recharge'
				})
				break
			case 'invoice':
				// 可开票 - 跳转到发票页面
				uni.navigateTo({
					url: '/pagesA/invoice/invoice'
				})
				break
			case 'debt':
				// 个人欠款 - 暂无页面，显示提示
				uni.showToast({
					title: '功能开发中',
					icon: 'none'
				})
				break
			default:
				uni.showToast({
					title: '功能开发中',
					icon: 'none'
				})
		}
	},
		
		// 显示预付说明
		showPrepaidInfo() {
			uni.showModal({
				title: '个人预付说明',
				content: '个人预付是指您预先充值到账户的金额，可用于支付订单费用',
				showCancel: false
			})
		},
		
		// 全部订单
		goAllOrders() {
			uni.switchTab({
				url: '/pages/order/order'
			})
		},
		
	// 订单列表（按状态）
	goOrders(status) {
		// 存储状态到本地，订单页面会读取
		uni.setStorageSync('order_status_filter', status)
		uni.switchTab({
			url: '/pages/order/order'
		})
	},
		
	// 跳转页面
	goPage(url) {
		// 检查是否登录
		const token = uni.getStorageSync('token')
		if (!token) {
			this.goLogin()
			return
		}
		
		// 跳转页面
		uni.navigateTo({ url })
	},
		
		// 登录
		goLogin() {
			uni.navigateTo({
				url: '/pages/login/login'
			})
		}
	}
}
</script>

<style lang="scss" scoped>
.user-page {
	min-height: 100vh;
	background: #f5f5f5;
	padding-bottom: 20rpx;
}

/* 用户信息头部 */
.user-header {
	background: #1890ff;
	padding: 32rpx 24rpx 64rpx;
	
	.user-info-card {
		display: flex;
		align-items: center;
		background: rgba(255, 255, 255, 0.95);
		padding: 24rpx;
		border-radius: 12rpx;
		box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.1);
		
		.avatar {
			width: 120rpx;
			height: 120rpx;
			border-radius: 60rpx;
			margin-right: 25rpx;
			border: 4rpx solid white;
		}
		
		.user-text {
			flex: 1;
			
			.member-id {
				display: block;
				font-size: 32rpx;
				font-weight: bold;
				color: #333;
				margin-bottom: 10rpx;
			}
			
			.advisor {
				display: block;
				font-size: 24rpx;
				color: #666;
			}
		}
		
		.edit-btn {
			padding: 15rpx;
			
			.edit-icon {
				font-size: 36rpx;
			}
		}
	}
}

/* 账户金额卡片 */
.account-cards {
	display: flex;
	margin: -40rpx 24rpx 16rpx;
	background: white;
	border-radius: 12rpx;
	padding: 24rpx 0;
	box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.04);
	
	.account-item {
		flex: 1;
		display: flex;
		flex-direction: column;
		align-items: center;
		border-right: 1rpx solid #f0f0f0;
		
		&:last-child {
			border-right: none;
		}
		
		.amount {
			font-size: 36rpx;
			font-weight: bold;
			color: #333;
			margin-bottom: 10rpx;
		}
		
		.label {
			font-size: 24rpx;
			color: #999;
		}
		
		.label-with-icon {
			display: flex;
			align-items: center;
			font-size: 24rpx;
			color: #999;
			
			.info-icon {
				margin-left: 5rpx;
				color: #4facfe;
				font-size: 28rpx;
			}
		}
	}
}

/* 我的订单 */
.order-section {
	background: white;
	margin: 0 24rpx 16rpx;
	padding: 24rpx;
	border-radius: 12rpx;
	
	.section-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 30rpx;
		
		.title {
			font-size: 32rpx;
			font-weight: bold;
			color: #333;
		}
		
		.more {
			display: flex;
			align-items: center;
			font-size: 26rpx;
			color: #999;
			
			.arrow {
				margin-left: 5rpx;
				font-size: 32rpx;
			}
		}
	}
	
	.order-status-list {
		display: flex;
		justify-content: space-between;
		
		.status-item {
			display: flex;
			flex-direction: column;
			align-items: center;
			
			.status-icon {
				width: 80rpx;
				height: 80rpx;
				background: #f5f8ff;
				border-radius: 16rpx;
				display: flex;
				align-items: center;
				justify-content: center;
				margin-bottom: 15rpx;
				
				.icon-emoji {
					font-size: 40rpx;
					line-height: 1;
				}
			}
			
			.status-text {
				font-size: 24rpx;
				color: #666;
			}
		}
	}
}

/* 服务与工具 */
.service-section {
	background: white;
	margin: 0 24rpx 16rpx;
	padding: 24rpx;
	border-radius: 12rpx;
	
	.section-title {
		font-size: 28rpx;
		font-weight: 600;
		color: #262626;
		margin-bottom: 24rpx;
	}
	
	.service-grid {
		display: grid;
		grid-template-columns: repeat(4, 1fr);
		gap: 40rpx 20rpx;
		
		.service-item {
			display: flex;
			flex-direction: column;
			align-items: center;
			
			.icon-wrap {
				position: relative;
				margin-bottom: 15rpx;
				
				.badge {
					position: absolute;
					top: -10rpx;
					right: -15rpx;
					padding: 4rpx 10rpx;
					border-radius: 10rpx;
					font-size: 18rpx;
					color: white;
					font-weight: bold;
					
					&.new {
						background: #ff6b6b;
					}
					
					&.rebate {
						background: #ff9500;
					}
					
					&.newest {
						background: #ff6b6b;
					}
					
					&.coupon {
						background: #ff9500;
					}
				}
			}
			
			.service-icon {
				font-size: 60rpx;
				margin-bottom: 15rpx;
			}
			
			.service-text {
				font-size: 24rpx;
				color: #666;
				text-align: center;
			}
		}
	}
}

/* 底部占位 */
.bottom-placeholder {
	height: 20rpx;
}
</style>

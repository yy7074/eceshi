<template>
	<view class="invite-page">
		<!-- 头部Banner -->
		<view class="header-banner">
			<text class="banner-title">邀请好友</text>
			<text class="banner-subtitle">送好礼 享返利</text>
			<view class="invite-code-card">
				<text class="code-label">我的邀请码</text>
				<text class="code-value">{{ inviteCode }}</text>
				<button class="copy-btn" @click="copyInviteCode">复制邀请码</button>
			</view>
		</view>
		
		<!-- 返利规则 -->
		<view class="rules-section">
			<view class="section-title">
				<text class="title-icon">💰</text>
				<text class="title-text">返利规则</text>
			</view>
			<view class="rules-list">
				<view class="rule-item">
					<text class="rule-number">1</text>
					<view class="rule-content">
						<text class="rule-title">好友注册</text>
						<text class="rule-desc">好友通过您的邀请码注册，您可获得10积分</text>
					</view>
				</view>
				<view class="rule-item">
					<text class="rule-number">2</text>
					<view class="rule-content">
						<text class="rule-title">好友下单</text>
						<text class="rule-desc">好友首次下单，您可获得订单金额5%的返利</text>
					</view>
				</view>
				<view class="rule-item">
					<text class="rule-number">3</text>
					<view class="rule-content">
						<text class="rule-title">持续返利</text>
						<text class="rule-desc">好友后续消费，您可持续获得3%的返利</text>
					</view>
				</view>
			</view>
		</view>
		
		<!-- 我的收益 -->
		<view class="earnings-section">
			<view class="section-title">
				<text class="title-icon">📊</text>
				<text class="title-text">我的收益</text>
			</view>
			<view class="earnings-stats">
				<view class="stat-item">
					<text class="stat-value">{{ totalInvites }}</text>
					<text class="stat-label">累计邀请</text>
				</view>
				<view class="stat-divider"></view>
				<view class="stat-item">
					<text class="stat-value">¥{{ totalEarnings.toFixed(2) }}</text>
					<text class="stat-label">累计收益</text>
				</view>
				<view class="stat-divider"></view>
				<view class="stat-item">
					<text class="stat-value">¥{{ availableEarnings.toFixed(2) }}</text>
					<text class="stat-label">可提现收益</text>
				</view>
			</view>
			<button v-if="availableEarnings > 0" class="withdraw-btn" @click="handleWithdraw">
				立即提现
			</button>
		</view>
		
		<!-- 邀请记录 -->
		<view class="records-section">
			<view class="section-header">
				<view class="section-title">
					<text class="title-icon">👥</text>
					<text class="title-text">邀请记录</text>
				</view>
				<view class="tabs">
					<view 
						v-for="(tab, index) in tabs" 
						:key="index"
						:class="['tab-item', currentTab === index ? 'active' : '']"
						@click="switchTab(index)"
					>
						{{ tab }}
					</view>
				</view>
			</view>
			
			<!-- 邀请列表 -->
			<view v-if="records.length > 0" class="records-list">
				<view v-for="(item, index) in records" :key="index" class="record-item">
					<view class="record-avatar">
						<image v-if="item.avatar" :src="item.avatar" mode="aspectFill"></image>
						<text v-else class="avatar-text">{{ item.nickname.substring(0, 1) }}</text>
					</view>
					<view class="record-info">
						<text class="record-name">{{ item.nickname }}</text>
						<text class="record-time">{{ item.time }}</text>
					</view>
					<view class="record-reward">
						<text v-if="currentTab === 0" class="reward-amount">+{{ item.points }}积分</text>
						<text v-else class="reward-amount">+¥{{ item.amount.toFixed(2) }}</text>
					</view>
				</view>
			</view>
			
			<!-- 空状态 -->
			<view v-else class="empty-state">
				<text class="empty-icon">👥</text>
				<text class="empty-text">{{ currentTab === 0 ? '还没有邀请记录' : '还没有返利记录' }}</text>
			</view>
		</view>
		
		<!-- 分享按钮 -->
		<view class="footer-btns">
			<button class="share-btn wechat" open-type="share">
				<text class="btn-icon">💬</text>
				<text class="btn-text">分享给好友</text>
			</button>
			<button class="share-btn moments" @click="shareMoments">
				<text class="btn-icon">📱</text>
				<text class="btn-text">生成海报</text>
			</button>
		</view>
	</view>
</template>

<script>
export default {
	data() {
		return {
			inviteCode: '',
			totalInvites: 0,
			totalEarnings: 0,
			availableEarnings: 0,
			currentTab: 0,
			tabs: ['邀请记录', '返利记录'],
			records: []
		}
	},
	
	onLoad() {
		this.generateInviteCode()
		this.loadInviteData()
	},
	
	// 分享配置
	onShareAppMessage() {
		return {
			title: `我在科研检测服务平台发现了超好用的检测服务！输入我的邀请码 ${this.inviteCode} 立享优惠！`,
			path: `/pages/index/index?inviteCode=${this.inviteCode}`
		}
	},
	
	methods: {
		// 生成邀请码
		generateInviteCode() {
			// TODO: 从后端获取邀请码
			const userId = uni.getStorageSync('userInfo')?.id || '000000'
			this.inviteCode = `INV${userId.toString().padStart(6, '0')}`
		},
		
		// 加载邀请数据
		async loadInviteData() {
			try {
				// TODO: 调用API获取邀请数据
				this.totalInvites = 0
				this.totalEarnings = 0
				this.availableEarnings = 0
				this.loadRecords()
			} catch (error) {
				console.error('加载邀请数据失败', error)
			}
		},
		
		// 加载记录
		async loadRecords() {
			try {
				// TODO: 调用API获取邀请/返利记录
				this.records = []
			} catch (error) {
				console.error('加载记录失败', error)
			}
		},
		
		// 复制邀请码
		copyInviteCode() {
			uni.setClipboardData({
				data: this.inviteCode,
				success: () => {
					uni.showToast({
						title: '邀请码已复制',
						icon: 'success'
					})
				}
			})
		},
		
		// 切换Tab
		switchTab(index) {
			this.currentTab = index
			this.loadRecords()
		},
		
		// 提现
		handleWithdraw() {
			uni.showModal({
				title: '提现',
				content: `确认提现 ¥${this.availableEarnings.toFixed(2)} 到钱包吗？`,
				success: (res) => {
					if (res.confirm) {
						uni.showToast({
							title: '提现功能开发中',
							icon: 'none'
						})
					}
				}
			})
		},
		
		// 生成海报
		shareMoments() {
			uni.showToast({
				title: '海报生成功能开发中',
				icon: 'none',
				duration: 2000
			})
		}
	}
}
</script>

<style lang="scss" scoped>
.invite-page {
	min-height: 100vh;
	background: #f5f5f5;
	padding-bottom: 180rpx;
}

.header-banner {
	background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
	padding: 60rpx 30rpx 80rpx;
	display: flex;
	flex-direction: column;
	align-items: center;
	
	.banner-title {
		font-size: 48rpx;
		font-weight: bold;
		color: white;
		margin-bottom: 10rpx;
	}
	
	.banner-subtitle {
		font-size: 28rpx;
		color: white;
		opacity: 0.9;
		margin-bottom: 40rpx;
	}
	
	.invite-code-card {
		background: white;
		border-radius: 16rpx;
		padding: 40rpx;
		width: 600rpx;
		display: flex;
		flex-direction: column;
		align-items: center;
		box-shadow: 0 8rpx 30rpx rgba(0, 0, 0, 0.1);
		
		.code-label {
			font-size: 26rpx;
			color: #999;
			margin-bottom: 20rpx;
		}
		
		.code-value {
			font-size: 56rpx;
			font-weight: bold;
			color: #ff9a9e;
			letter-spacing: 8rpx;
			margin-bottom: 30rpx;
		}
		
		.copy-btn {
			background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
			color: white;
			border: none;
			border-radius: 50rpx;
			padding: 20rpx 60rpx;
			font-size: 28rpx;
		}
	}
}

.rules-section,
.earnings-section,
.records-section {
	background: white;
	margin: 20rpx 30rpx;
	border-radius: 16rpx;
	padding: 30rpx;
}

.section-title {
	display: flex;
	align-items: center;
	margin-bottom: 30rpx;
	
	.title-icon {
		font-size: 36rpx;
		margin-right: 15rpx;
	}
	
	.title-text {
		font-size: 32rpx;
		font-weight: bold;
		color: #333;
	}
}

.rules-list {
	.rule-item {
		display: flex;
		padding: 30rpx 0;
		border-bottom: 1rpx solid #f5f5f5;
		
		&:last-child {
			border-bottom: none;
		}
		
		.rule-number {
			width: 60rpx;
			height: 60rpx;
			background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
			color: white;
			border-radius: 50%;
			display: flex;
			align-items: center;
			justify-content: center;
			font-size: 28rpx;
			font-weight: bold;
			margin-right: 20rpx;
			flex-shrink: 0;
		}
		
		.rule-content {
			flex: 1;
			display: flex;
			flex-direction: column;
			
			.rule-title {
				font-size: 28rpx;
				font-weight: bold;
				color: #333;
				margin-bottom: 10rpx;
			}
			
			.rule-desc {
				font-size: 26rpx;
				color: #666;
				line-height: 1.6;
			}
		}
	}
}

.earnings-stats {
	display: flex;
	justify-content: space-around;
	padding: 30rpx 0;
	margin-bottom: 20rpx;
	
	.stat-item {
		display: flex;
		flex-direction: column;
		align-items: center;
		
		.stat-value {
			font-size: 40rpx;
			font-weight: bold;
			color: #ff9a9e;
			margin-bottom: 10rpx;
		}
		
		.stat-label {
			font-size: 24rpx;
			color: #999;
		}
	}
	
	.stat-divider {
		width: 1rpx;
		background: #eee;
	}
}

.withdraw-btn {
	width: 100%;
	background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
	color: white;
	border: none;
	border-radius: 50rpx;
	padding: 25rpx;
	font-size: 28rpx;
	font-weight: bold;
}

.records-section {
	.section-header {
		display: flex;
		flex-direction: column;
		margin-bottom: 30rpx;
		
		.tabs {
			display: flex;
			margin-top: 20rpx;
			border-bottom: 1rpx solid #eee;
			
			.tab-item {
				flex: 1;
				text-align: center;
				padding: 20rpx 0;
				font-size: 28rpx;
				color: #666;
				position: relative;
				
				&.active {
					color: #ff9a9e;
					font-weight: bold;
					
					&::after {
						content: '';
						position: absolute;
						bottom: 0;
						left: 50%;
						transform: translateX(-50%);
						width: 60rpx;
						height: 4rpx;
						background: #ff9a9e;
						border-radius: 2rpx;
					}
				}
			}
		}
	}
	
	.records-list {
		.record-item {
			display: flex;
			align-items: center;
			padding: 30rpx 0;
			border-bottom: 1rpx solid #f5f5f5;
			
			&:last-child {
				border-bottom: none;
			}
			
			.record-avatar {
				width: 80rpx;
				height: 80rpx;
				border-radius: 50%;
				background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
				overflow: hidden;
				margin-right: 20rpx;
				display: flex;
				align-items: center;
				justify-content: center;
				
				image {
					width: 100%;
					height: 100%;
				}
				
				.avatar-text {
					font-size: 32rpx;
					color: white;
					font-weight: bold;
				}
			}
			
			.record-info {
				flex: 1;
				display: flex;
				flex-direction: column;
				
				.record-name {
					font-size: 28rpx;
					color: #333;
					margin-bottom: 10rpx;
				}
				
				.record-time {
					font-size: 24rpx;
					color: #999;
				}
			}
			
			.record-reward {
				.reward-amount {
					font-size: 28rpx;
					font-weight: bold;
					color: #ff9a9e;
				}
			}
		}
	}
}

.empty-state {
	display: flex;
	flex-direction: column;
	align-items: center;
	padding: 100rpx 0;
	
	.empty-icon {
		font-size: 120rpx;
		margin-bottom: 30rpx;
		opacity: 0.5;
	}
	
	.empty-text {
		font-size: 28rpx;
		color: #999;
	}
}

.footer-btns {
	position: fixed;
	bottom: 0;
	left: 0;
	right: 0;
	padding: 20rpx 30rpx;
	background: white;
	display: flex;
	gap: 20rpx;
	box-shadow: 0 -2rpx 10rpx rgba(0, 0, 0, 0.05);
	
	.share-btn {
		flex: 1;
		border: none;
		border-radius: 50rpx;
		padding: 30rpx;
		font-size: 28rpx;
		font-weight: bold;
		display: flex;
		align-items: center;
		justify-content: center;
		
		&.wechat {
			background: linear-gradient(135deg, #1aad19 0%, #2cc562 100%);
			color: white;
		}
		
		&.moments {
			background: white;
			color: #ff9a9e;
			border: 2rpx solid #ff9a9e;
		}
		
		.btn-icon {
			font-size: 32rpx;
			margin-right: 10rpx;
		}
	}
}
</style>


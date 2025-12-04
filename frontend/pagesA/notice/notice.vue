<template>
	<view class="notice-page">
		<!-- 消息类型切换 -->
		<view class="tabs">
			<view class="tab-item" :class="{ active: activeTab === 'all' }" @click="activeTab = 'all'">
				全部
			</view>
			<view class="tab-item" :class="{ active: activeTab === 'system' }" @click="activeTab = 'system'">
				系统公告
			</view>
			<view class="tab-item" :class="{ active: activeTab === 'order' }" @click="activeTab = 'order'">
				订单通知
			</view>
			<view class="tab-item" :class="{ active: activeTab === 'activity' }" @click="activeTab = 'activity'">
				活动消息
			</view>
		</view>
		
		<!-- 消息列表 -->
		<view class="notice-list" v-if="filteredNotices.length > 0">
			<view class="notice-item" v-for="notice in filteredNotices" :key="notice.id" @click="showDetail(notice)">
				<view class="notice-icon" :style="{ background: getIconBg(notice.type) }">
					<text>{{ getIcon(notice.type) }}</text>
				</view>
				<view class="notice-content">
					<view class="notice-header">
						<text class="notice-title">{{ notice.title }}</text>
						<text class="notice-time">{{ notice.time }}</text>
					</view>
					<text class="notice-summary">{{ notice.summary }}</text>
					<view class="notice-tag" v-if="!notice.read">
						<text class="unread-dot"></text>
					</view>
				</view>
			</view>
		</view>
		
		<!-- 空状态 -->
		<view class="empty-state" v-else>
			<text class="empty-icon">📭</text>
			<text class="empty-text">暂无消息</text>
		</view>
		
		<!-- 清除已读按钮 -->
		<view class="action-bar" v-if="notices.length > 0">
			<view class="action-btn" @click="markAllRead">
				<text>全部标为已读</text>
			</view>
		</view>
	</view>
</template>

<script>
export default {
	data() {
		return {
			activeTab: 'all',
			notices: [
				{
					id: 1,
					type: 'system',
					title: '平台服务升级通知',
					summary: '为提供更好的服务体验，我们将于12月10日进行系统升级维护...',
					content: '尊敬的用户：\n\n为提供更好的服务体验，我们将于2025年12月10日00:00-06:00进行系统升级维护，届时部分功能可能暂时无法使用，给您带来的不便敬请谅解。\n\n科研检测服务平台',
					time: '12-01',
					read: false
				},
				{
					id: 2,
					type: 'order',
					title: '订单状态更新',
					summary: '您的订单ORD2025120100001已完成检测，报告已生成...',
					content: '您的订单ORD2025120100001（X射线衍射分析）已完成检测，报告已生成，请前往订单详情页下载。',
					time: '11-30',
					read: false
				},
				{
					id: 3,
					type: 'activity',
					title: '12月优惠活动',
					summary: '金秋检测季，多项热门检测项目6折起，优惠券限时领取...',
					content: '金秋检测季活动火热进行中！\n\n活动时间：12月1日-12月31日\n\n优惠内容：\n1. XPS、SEM、FT-IR等热门检测项目6折起\n2. 新用户首单立减50元\n3. 老客户回馈：充值满1000送100\n\n快来参与吧！',
					time: '12-01',
					read: true
				},
				{
					id: 4,
					type: 'system',
					title: '新增检测项目上线',
					summary: '新增材料表征、生物科学等多个检测类目，欢迎体验...',
					content: '平台新增多个检测项目类目：\n\n1. 材料表征\n2. 高端测试\n3. 组织成分\n4. 生物科学\n5. 环境检测\n\n更多优质检测服务，敬请期待！',
					time: '11-28',
					read: true
				},
				{
					id: 5,
					type: 'order',
					title: '样品已签收',
					summary: '您的样品已被实验室签收，正在安排检测...',
					content: '您好，您寄送的样品已被实验室签收，订单ORD2025112800002正在安排检测，预计3-5个工作日完成。',
					time: '11-28',
					read: true
				}
			]
		}
	},
	computed: {
		filteredNotices() {
			if (this.activeTab === 'all') return this.notices
			return this.notices.filter(n => n.type === this.activeTab)
		}
	},
	methods: {
		getIcon(type) {
			const icons = {
				system: '📢',
				order: '📦',
				activity: '🎁'
			}
			return icons[type] || '📌'
		},
		getIconBg(type) {
			const colors = {
				system: '#e6f7ff',
				order: '#f6ffed',
				activity: '#fff7e6'
			}
			return colors[type] || '#f5f5f5'
		},
		showDetail(notice) {
			notice.read = true
			uni.showModal({
				title: notice.title,
				content: notice.content,
				showCancel: false,
				confirmText: '我知道了'
			})
		},
		markAllRead() {
			this.notices.forEach(n => n.read = true)
			uni.showToast({ title: '已全部标为已读', icon: 'success' })
		}
	}
}
</script>

<style lang="scss" scoped>
.notice-page {
	min-height: 100vh;
	background: #f5f5f5;
}

.tabs {
	display: flex;
	background: #fff;
	padding: 0 24rpx;
	border-bottom: 1rpx solid #f0f0f0;
	
	.tab-item {
		flex: 1;
		text-align: center;
		padding: 28rpx 0;
		font-size: 28rpx;
		color: #666;
		position: relative;
		
		&.active {
			color: #1890ff;
			font-weight: 500;
			
			&::after {
				content: '';
				position: absolute;
				bottom: 0;
				left: 50%;
				transform: translateX(-50%);
				width: 48rpx;
				height: 4rpx;
				background: #1890ff;
				border-radius: 2rpx;
			}
		}
	}
}

.notice-list {
	padding: 16rpx 24rpx;
	
	.notice-item {
		display: flex;
		background: #fff;
		padding: 24rpx;
		border-radius: 12rpx;
		margin-bottom: 16rpx;
		
		.notice-icon {
			width: 80rpx;
			height: 80rpx;
			border-radius: 16rpx;
			display: flex;
			align-items: center;
			justify-content: center;
			font-size: 36rpx;
			margin-right: 20rpx;
			flex-shrink: 0;
		}
		
		.notice-content {
			flex: 1;
			position: relative;
			
			.notice-header {
				display: flex;
				justify-content: space-between;
				align-items: center;
				margin-bottom: 8rpx;
			}
			
			.notice-title {
				font-size: 30rpx;
				font-weight: 500;
				color: #333;
			}
			
			.notice-time {
				font-size: 24rpx;
				color: #999;
			}
			
			.notice-summary {
				font-size: 26rpx;
				color: #666;
				display: -webkit-box;
				-webkit-line-clamp: 2;
				-webkit-box-orient: vertical;
				overflow: hidden;
			}
			
			.notice-tag {
				position: absolute;
				top: 0;
				right: 0;
				
				.unread-dot {
					display: block;
					width: 16rpx;
					height: 16rpx;
					background: #ff4d4f;
					border-radius: 50%;
				}
			}
		}
	}
}

.empty-state {
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	padding: 120rpx 0;
	
	.empty-icon {
		font-size: 80rpx;
		margin-bottom: 24rpx;
	}
	
	.empty-text {
		font-size: 28rpx;
		color: #999;
	}
}

.action-bar {
	padding: 24rpx;
	
	.action-btn {
		background: #fff;
		padding: 24rpx;
		border-radius: 12rpx;
		text-align: center;
		
		text {
			font-size: 28rpx;
			color: #1890ff;
		}
	}
}
</style>


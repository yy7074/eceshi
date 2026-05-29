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
					<text class="notice-corner">{{ getTypeText(notice.type) }}</text>
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
import api from '@/utils/api.js'

export default {
	data() {
		return {
			activeTab: 'all',
			notices: [],
			loading: false
		}
	},
	onLoad() {
		this.loadNotices()
	},
	onPullDownRefresh() {
		this.loadNotices().finally(() => uni.stopPullDownRefresh())
	},
	computed: {
		filteredNotices() {
			if (this.activeTab === 'all') return this.notices
			return this.notices.filter(n => n.type === this.activeTab)
		}
	},
	methods: {
		getReadAnnouncementIds() {
			const stored = uni.getStorageSync('readAnnouncementIds')
			if (!stored) return []
			try {
				return typeof stored === 'string' ? JSON.parse(stored) : stored
			} catch (e) {
				return []
			}
		},
		setReadAnnouncement(id) {
			const ids = new Set(this.getReadAnnouncementIds())
			ids.add(id)
			uni.setStorageSync('readAnnouncementIds', JSON.stringify([...ids]))
		},
		async loadNotices() {
			this.loading = true
			try {
				const [noticeRes, annRes] = await Promise.all([
					api.getNotifications({ page: 1, page_size: 50 }).catch(() => ({ data: { items: [] } })),
					api.getAnnouncements({ page: 1, page_size: 50 }).catch(() => ({ data: { items: [] } }))
				])
				const readAnnouncementIds = this.getReadAnnouncementIds()
				const notifications = (noticeRes.data?.items || []).map(item => ({
					id: `n-${item.id}`,
					rawId: item.id,
					source: 'notification',
					type: item.category || 'system',
					title: item.title,
					summary: item.content || '',
					content: item.content || '',
					time: this.formatTime(item.created_at),
					read: !!item.is_read
				}))
				const announcements = (annRes.data?.items || []).map(item => ({
					id: `a-${item.id}`,
					rawId: item.id,
					source: 'announcement',
					type: item.category || 'system',
					title: item.title,
					summary: item.summary || '',
					content: item.summary || '',
					time: this.formatTime(item.created_at),
					read: readAnnouncementIds.includes(item.id)
				}))
				this.notices = [...notifications, ...announcements]
			} finally {
				this.loading = false
			}
		},
		formatTime(value) {
			if (!value) return ''
			return String(value).replace('T', ' ').slice(5, 16)
		},
		getIcon(type) {
			const icons = {
				system: '📢',
				order: '📦',
				activity: '🎁'
			}
			return icons[type] || '📌'
		},
		getTypeText(type) {
			const map = {
				system: '系统',
				order: '订单',
				activity: '活动',
				notice: '公告'
			}
			return map[type] || '消息'
		},
		getIconBg(type) {
			const colors = {
				system: '#e6f7ff',
				order: '#f6ffed',
				activity: '#fff7e6'
			}
			return colors[type] || '#f5f5f5'
		},
		async showDetail(notice) {
			if (notice.source === 'notification') {
				await api.markNotificationRead(notice.rawId).catch(() => {})
			} else {
				const res = await api.getAnnouncementDetail(notice.rawId).catch(() => null)
				notice.content = res?.data?.content || notice.content || notice.summary
				this.setReadAnnouncement(notice.rawId)
			}
			notice.read = true
			uni.showModal({
				title: notice.title,
				content: notice.content,
				showCancel: false,
				confirmText: '我知道了'
			})
		},
		async markAllRead() {
			await api.markAllNotificationsRead().catch(() => {})
			const announcementIds = this.notices.filter(n => n.source === 'announcement').map(n => n.rawId)
			uni.setStorageSync('readAnnouncementIds', JSON.stringify(announcementIds))
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
		border-radius: 18rpx;
		margin-bottom: 18rpx;
		box-shadow: 0 6rpx 18rpx rgba(23, 37, 84, 0.06);
		
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
			background: #f8fafc;
			border-radius: 16rpx;
			padding: 18rpx 18rpx 44rpx;
			
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

			.notice-corner {
				position: absolute;
				right: 16rpx;
				bottom: 12rpx;
				padding: 4rpx 14rpx;
				border-radius: 999rpx;
				background: #e8f3ff;
				color: #1677ff;
				font-size: 22rpx;
			}
			
			.notice-tag {
				position: absolute;
				top: -4rpx;
				right: -4rpx;
				
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

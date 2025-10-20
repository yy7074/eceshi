<template>
	<view class="group-detail-page">
		<view v-if="loading" class="loading">加载中...</view>
		
		<view v-else-if="group.id" class="content">
			<!-- 项目信息 -->
			<view class="project-section">
				<image :src="group.project_image || 'https://picsum.photos/600/400'" mode="aspectFill" class="project-banner"></image>
				<view class="project-info">
					<text class="project-name">{{ group.project_name }}</text>
					<text class="project-desc">{{ group.project_desc }}</text>
				</view>
			</view>
			
			<!-- 团购信息 -->
			<view class="group-info-card">
				<view class="info-row">
					<text class="label">团购价：</text>
					<view class="price-group">
						<text class="group-price">¥{{ group.group_price }}</text>
						<text class="original-price">原价¥{{ group.original_price }}</text>
						<text class="save-tag">省¥{{ (group.original_price - group.group_price).toFixed(2) }}</text>
					</view>
				</view>
				<view class="info-row">
					<text class="label">成团人数：</text>
					<text class="value">{{ group.required_members }}人</text>
				</view>
				<view class="info-row">
					<text class="label">有效期：</text>
					<text class="value">{{ group.expire_time }}</text>
				</view>
				<view class="info-row">
					<text class="label">团长：</text>
					<text class="value">{{ group.leader_name }}</text>
				</view>
			</view>
			
			<!-- 进度 -->
			<view class="progress-card">
				<view class="progress-header">
					<text class="progress-title">拼团进度</text>
					<text :class="['status-badge', 'status-' + group.status]">{{ getStatusText(group.status) }}</text>
				</view>
				<view class="progress-bar-wrapper">
					<view class="progress-bar">
						<view class="progress-fill" :style="{ width: progressPercent + '%' }"></view>
					</view>
					<text class="progress-text">{{ group.current_members }}/{{ group.required_members }}人</text>
				</view>
				<text class="progress-tip">还差{{ group.required_members - group.current_members }}人成团</text>
			</view>
			
			<!-- 成员列表 -->
			<view class="members-card">
				<view class="members-header">
					<text class="members-title">参团成员（{{ group.members.length }}）</text>
				</view>
				<view class="members-list">
					<view v-for="(member, index) in group.members" :key="index" class="member-item">
						<image :src="member.avatar || generateAvatar(member.nickname)" mode="aspectFill" class="member-avatar"></image>
						<view class="member-info">
							<text class="member-name">{{ member.nickname }}</text>
							<text class="member-time">{{ member.join_time }}</text>
						</view>
						<text v-if="member.is_leader" class="leader-badge">团长</text>
					</view>
				</view>
			</view>
			
			<!-- 底部操作 -->
			<view class="footer-actions">
				<button v-if="!isMember && group.status === 'active'" class="btn-join" @click="joinGroup">立即参团</button>
				<button v-if="isLeader" class="btn-share" open-type="share">邀请好友参团</button>
				<button v-if="isMember && group.status === 'full'" class="btn-pay" @click="goPay">立即支付</button>
			</view>
		</view>
	</view>
</template>

<script>
export default {
	data() {
		return {
			groupId: '',
			loading: true,
			group: {},
			isMember: false,
			isLeader: false
		}
	},
	
	computed: {
		progressPercent() {
			if (!this.group.required_members) return 0
			return Math.min(100, (this.group.current_members / this.group.required_members * 100))
		}
	},
	
	onLoad(options) {
		if (options.id) {
			this.groupId = options.id
			this.loadGroupDetail()
		}
	},
	
	// 分享配置
	onShareAppMessage() {
		return {
			title: `【团购】${this.group.project_name} 仅需¥${this.group.group_price}，快来参团！`,
			path: `/pagesA/group-detail/group-detail?id=${this.groupId}`
		}
	},
	
	methods: {
	// 加载团体详情
	async loadGroupDetail() {
		try {
			this.loading = true
			
			// 调用API获取团体详情
			const res = await api.getGroupDetail(this.groupId)
			this.group = res.data
			
			// 如果API返回空数据，使用展示数据
			if (!this.group || !this.group.id) {
				// 展示数据（用于UI演示）
				const userInfo = uni.getStorageSync('userInfo') || {}
				this.group = {
					id: this.groupId,
					project_name: 'XRD物相分析',
					project_desc: '快速准确的物相鉴定',
					project_image: 'https://picsum.photos/600/400',
					group_price: 680,
					original_price: 850,
					required_members: 5,
					current_members: 2,
					status: 'active',
					expire_time: '2025-10-22 23:59',
					leader_name: '用户123',
					leader_id: 1,
					members: [
						{ id: 1, nickname: '用户123', avatar: '', join_time: '2025-10-19 10:00', is_leader: true },
						{ id: 2, nickname: '用户456', avatar: '', join_time: '2025-10-19 15:30', is_leader: false }
					]
				}
			}
			
			const userInfo = uni.getStorageSync('userInfo') || {}
			this.isLeader = this.group.leader_id === userInfo.id
			this.isMember = this.group.members && this.group.members.some(m => m.id === userInfo.id)
			
			this.loading = false
		} catch (error) {
			this.loading = false
			console.error('加载团体详情失败', error)
			uni.showToast({
				title: '加载失败',
				icon: 'none'
			})
		}
	},
		
		// 加入团体
		joinGroup() {
			uni.showModal({
				title: '确认参团',
				content: `确定要加入此团购吗？团购价¥${this.group.group_price}`,
				success: (res) => {
					if (res.confirm) {
						this.doJoinGroup()
					}
				}
			})
		},
		
	// 执行加入
	async doJoinGroup() {
		try {
			uni.showLoading({ title: '加入中...' })
			
			// 调用API加入团体（使用邀请码方式）
			await api.joinGroup(this.groupId.toString())
			
			uni.hideLoading()
			uni.showToast({
				title: '加入成功',
				icon: 'success'
			})
			
			// 刷新详情
			this.loadGroupDetail()
		} catch (error) {
				uni.hideLoading()
				console.error('加入失败', error)
				uni.showToast({
					title: error.message || '加入失败',
					icon: 'none'
				})
			}
		},
		
		// 去支付
		goPay() {
			uni.showToast({
				title: '支付功能开发中',
				icon: 'none'
			})
		},
		
		// 生成头像
		generateAvatar(name) {
			return `https://ui-avatars.com/api/?name=${encodeURIComponent(name)}&background=random&size=100`
		},
		
		// 获取状态文本
		getStatusText(status) {
			const statusMap = {
				'active': '进行中',
				'full': '已成团',
				'expired': '已过期',
				'cancelled': '已取消'
			}
			return statusMap[status] || '未知'
		}
	}
}
</script>

<style lang="scss" scoped>
.group-detail-page {
	min-height: 100vh;
	background: #f5f5f5;
	padding-bottom: 120rpx;
}

.loading {
	text-align: center;
	padding: 200rpx 0;
	color: #999;
}

/* 项目区域 */
.project-section {
	background: white;
	margin-bottom: 20rpx;
}

.project-banner {
	width: 100%;
	height: 400rpx;
}

.project-info {
	padding: 30rpx;
}

.project-name {
	font-size: 32rpx;
	font-weight: bold;
	color: #333;
	margin-bottom: 10rpx;
	display: block;
}

.project-desc {
	font-size: 26rpx;
	color: #666;
	display: block;
}

/* 团购信息卡片 */
.group-info-card {
	background: white;
	margin-bottom: 20rpx;
	padding: 30rpx;
}

.info-row {
	display: flex;
	align-items: center;
	margin-bottom: 20rpx;
	
	&:last-child {
		margin-bottom: 0;
	}
}

.label {
	font-size: 26rpx;
	color: #666;
	width: 140rpx;
}

.value {
	font-size: 26rpx;
	color: #333;
}

.price-group {
	display: flex;
	align-items: baseline;
	gap: 10rpx;
}

.group-price {
	font-size: 36rpx;
	font-weight: bold;
	color: #ff4444;
}

.original-price {
	font-size: 24rpx;
	color: #999;
	text-decoration: line-through;
}

.save-tag {
	font-size: 22rpx;
	color: #ff4444;
	background: #ffebee;
	padding: 4rpx 12rpx;
	border-radius: 8rpx;
}

/* 进度卡片 */
.progress-card {
	background: white;
	margin-bottom: 20rpx;
	padding: 30rpx;
}

.progress-header {
	display: flex;
	justify-content: space-between;
	align-items: center;
	margin-bottom: 20rpx;
}

.progress-title {
	font-size: 28rpx;
	font-weight: bold;
	color: #333;
}

.status-badge {
	font-size: 22rpx;
	padding: 6rpx 16rpx;
	border-radius: 8rpx;
}

.status-badge.status-active {
	background: #e8f5e9;
	color: #4caf50;
}

.status-badge.status-full {
	background: #e3f2fd;
	color: #2196f3;
}

.progress-bar-wrapper {
	display: flex;
	align-items: center;
	gap: 15rpx;
	margin-bottom: 15rpx;
}

.progress-bar {
	flex: 1;
	height: 16rpx;
	background: #f5f5f5;
	border-radius: 8rpx;
	overflow: hidden;
}

.progress-fill {
	height: 100%;
	background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
	border-radius: 8rpx;
}

.progress-text {
	font-size: 26rpx;
	color: #667eea;
	font-weight: bold;
}

.progress-tip {
	font-size: 24rpx;
	color: #ff9800;
	display: block;
}

/* 成员卡片 */
.members-card {
	background: white;
	margin-bottom: 20rpx;
	padding: 30rpx;
}

.members-header {
	margin-bottom: 20rpx;
}

.members-title {
	font-size: 28rpx;
	font-weight: bold;
	color: #333;
}

.members-list {
}

.member-item {
	display: flex;
	align-items: center;
	padding: 20rpx 0;
	border-bottom: 1rpx solid #f5f5f5;
	
	&:last-child {
		border-bottom: none;
	}
}

.member-avatar {
	width: 80rpx;
	height: 80rpx;
	border-radius: 50%;
	margin-right: 20rpx;
}

.member-info {
	flex: 1;
	display: flex;
	flex-direction: column;
}

.member-name {
	font-size: 28rpx;
	color: #333;
	margin-bottom: 8rpx;
}

.member-time {
	font-size: 24rpx;
	color: #999;
}

.leader-badge {
	font-size: 22rpx;
	color: #ff9800;
	background: #fff3e0;
	padding: 6rpx 16rpx;
	border-radius: 8rpx;
}

/* 底部操作 */
.footer-actions {
	position: fixed;
	bottom: 0;
	left: 0;
	right: 0;
	padding: 20rpx 30rpx;
	background: white;
	box-shadow: 0 -2rpx 10rpx rgba(0, 0, 0, 0.05);
}

.btn-join,
.btn-share,
.btn-pay {
	width: 100%;
	background: #1890ff;
	color: white;
	border: none;
	border-radius: 50rpx;
	padding: 30rpx;
	font-size: 32rpx;
	font-weight: bold;
}
</style>


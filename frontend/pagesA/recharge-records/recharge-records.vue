<template>
	<view class="records-page">
		<!-- 记录列表 -->
		<view v-if="records.length > 0" class="records-list">
			<view 
				v-for="record in records" 
				:key="record.id"
				class="record-item"
				@click="viewDetail(record)"
			>
				<view class="record-header">
					<view class="record-title">钱包充值</view>
					<view class="record-status" :class="'status-' + record.status">
						{{ statusText[record.status] }}
					</view>
				</view>
				
				<view class="record-amount">
					<text class="amount-symbol">+</text>
					<text class="amount-value">{{ record.actual_amount }}</text>
					<text class="amount-unit">元</text>
				</view>
				
				<view class="record-detail">
					<view class="detail-item">
						<text class="label">充值金额：</text>
						<text class="value">¥{{ record.amount }}</text>
					</view>
					<view v-if="record.bonus_amount > 0" class="detail-item">
						<text class="label">赠送金额：</text>
						<text class="value bonus">+¥{{ record.bonus_amount }}</text>
					</view>
				</view>
				
				<view class="record-footer">
					<text class="record-no">{{ record.recharge_no }}</text>
					<text class="record-time">{{ formatTime(record.created_at) }}</text>
				</view>
			</view>
		</view>
		
		<!-- 空状态 -->
		<view v-else-if="!loading" class="empty-state">
			<text class="empty-icon">📄</text>
			<text class="empty-text">暂无充值记录</text>
			<button class="recharge-btn" @click="goToRecharge">立即充值</button>
		</view>
		
		<!-- 加载更多 -->
		<view v-if="records.length > 0 && hasMore" class="load-more" @click="loadMore">
			<text>加载更多</text>
		</view>
		
		<view v-if="records.length > 0 && !hasMore" class="no-more">
			<text>没有更多了</text>
		</view>
	</view>
</template>

<script>
import api from '@/utils/api.js'

export default {
	data() {
		return {
			records: [],
			page: 1,
			pageSize: 10,
			total: 0,
			loading: false,
			statusText: {
				'pending': '待支付',
				'success': '充值成功',
				'failed': '充值失败',
				'refunded': '已退款'
			}
		}
	},
	
	computed: {
		hasMore() {
			return this.records.length < this.total
		}
	},
	
	onLoad() {
		this.loadRecords()
	},
	
	onPullDownRefresh() {
		this.page = 1
		this.records = []
		this.loadRecords().then(() => {
			uni.stopPullDownRefresh()
		})
	},
	
	methods: {
		async loadRecords() {
			if (this.loading) return
			
			try {
				this.loading = true
				const res = await api.getRechargeRecords({
					page: this.page,
					page_size: this.pageSize
				})
				
				if (this.page === 1) {
					this.records = res.data.items
				} else {
					this.records.push(...res.data.items)
				}
				
				this.total = res.data.total
				this.loading = false
				
			} catch (error) {
				console.error('加载充值记录失败', error)
				this.loading = false
				uni.showToast({
					title: '加载失败',
					icon: 'none'
				})
			}
		},
		
		loadMore() {
			if (this.hasMore && !this.loading) {
				this.page++
				this.loadRecords()
			}
		},
		
		formatTime(timeStr) {
			if (!timeStr) return ''
			const date = new Date(timeStr)
			const year = date.getFullYear()
			const month = String(date.getMonth() + 1).padStart(2, '0')
			const day = String(date.getDate()).padStart(2, '0')
			const hour = String(date.getHours()).padStart(2, '0')
			const minute = String(date.getMinutes()).padStart(2, '0')
			return `${year}-${month}-${day} ${hour}:${minute}`
		},
		
		viewDetail(record) {
			uni.showModal({
				title: '充值详情',
				content: `订单号：${record.recharge_no}\n充值金额：¥${record.amount}\n赠送金额：¥${record.bonus_amount}\n到账金额：¥${record.actual_amount}\n状态：${this.statusText[record.status]}\n时间：${this.formatTime(record.created_at)}`,
				showCancel: false
			})
		},
		
		goToRecharge() {
			uni.navigateBack()
		}
	}
}
</script>

<style scoped>
.records-page {
	min-height: 100vh;
	background: #f5f5f5;
}

.records-list {
	padding: 24rpx;
}

.record-item {
	background: white;
	border-radius: 16rpx;
	padding: 32rpx;
	margin-bottom: 24rpx;
}

.record-header {
	display: flex;
	align-items: center;
	justify-content: space-between;
	margin-bottom: 24rpx;
}

.record-title {
	font-size: 32rpx;
	font-weight: bold;
	color: #333;
}

.record-status {
	font-size: 24rpx;
	padding: 8rpx 16rpx;
	border-radius: 24rpx;
}

.status-pending {
	background: #fff5eb;
	color: #ff9800;
}

.status-success {
	background: #e8f5e9;
	color: #4caf50;
}

.status-failed {
	background: #ffebee;
	color: #f44336;
}

.status-refunded {
	background: #f5f5f5;
	color: #999;
}

.record-amount {
	display: flex;
	align-items: baseline;
	margin-bottom: 20rpx;
}

.amount-symbol {
	font-size: 40rpx;
	font-weight: bold;
	color: #4caf50;
	margin-right: 8rpx;
}

.amount-value {
	font-size: 56rpx;
	font-weight: bold;
	color: #4caf50;
}

.amount-unit {
	font-size: 28rpx;
	color: #999;
	margin-left: 8rpx;
}

.record-detail {
	background: #f8f8f8;
	border-radius: 12rpx;
	padding: 20rpx;
	margin-bottom: 20rpx;
}

.detail-item {
	display: flex;
	align-items: center;
	justify-content: space-between;
	margin-bottom: 12rpx;
	font-size: 28rpx;
}

.detail-item:last-child {
	margin-bottom: 0;
}

.detail-item .label {
	color: #666;
}

.detail-item .value {
	color: #333;
	font-weight: 500;
}

.detail-item .value.bonus {
	color: #ff6b6b;
}

.record-footer {
	display: flex;
	align-items: center;
	justify-content: space-between;
	padding-top: 20rpx;
	border-top: 1rpx solid #f0f0f0;
}

.record-no {
	font-size: 24rpx;
	color: #999;
}

.record-time {
	font-size: 24rpx;
	color: #999;
}

.empty-state {
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	padding: 120rpx 48rpx;
	text-align: center;
}

.empty-icon {
	font-size: 120rpx;
	margin-bottom: 32rpx;
}

.empty-text {
	font-size: 28rpx;
	color: #999;
	margin-bottom: 48rpx;
}

.recharge-btn {
	background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
	color: white;
	border: none;
	border-radius: 48rpx;
	height: 80rpx;
	line-height: 80rpx;
	padding: 0 48rpx;
	font-size: 30rpx;
}

.load-more,
.no-more {
	text-align: center;
	padding: 32rpx;
	font-size: 28rpx;
	color: #999;
}
</style>


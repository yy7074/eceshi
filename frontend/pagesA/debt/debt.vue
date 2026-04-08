<template>
	<view class="debt-page">
		<!-- 信用额度卡片 -->
		<view class="credit-card">
			<view class="credit-header">
				<text class="credit-title">信用额度</text>
				<text class="credit-apply" @click="applyLimit">申请提额</text>
			</view>
			<view class="credit-amount">
				<text class="amount-label">可用额度</text>
				<text class="amount-value">¥{{ formatMoney(creditInfo.available_credit) }}</text>
			</view>
			<view class="credit-detail">
				<view class="detail-item">
					<text class="item-label">总额度</text>
					<text class="item-value">¥{{ formatMoney(creditInfo.credit_limit) }}</text>
				</view>
				<view class="detail-item">
					<text class="item-label">已用额度</text>
					<text class="item-value">¥{{ formatMoney(creditInfo.used_credit) }}</text>
				</view>
				<view class="detail-item">
					<text class="item-label">总欠款</text>
					<text class="item-value debt-value">¥{{ formatMoney(creditInfo.total_debt) }}</text>
				</view>
			</view>
		</view>

		<!-- Tab切换 -->
		<view class="tab-bar">
			<view
				class="tab-item"
				:class="{ active: currentTab === 'debt' }"
				@click="currentTab = 'debt'"
			>
				<text>欠款明细</text>
			</view>
			<view
				class="tab-item"
				:class="{ active: currentTab === 'record' }"
				@click="currentTab = 'record'"
			>
				<text>交易记录</text>
			</view>
		</view>

		<!-- 欠款列表 -->
		<view class="debt-list" v-if="currentTab === 'debt'">
			<view class="list-header" v-if="debtList.length > 0">
				<text class="header-text">共{{ debtCount }}笔欠款，合计¥{{ formatMoney(creditInfo.total_debt) }}</text>
				<text class="repay-all-btn" @click="repayAll" v-if="creditInfo.total_debt > 0">全部还款</text>
			</view>

			<view class="debt-item" v-for="item in debtList" :key="item.id">
				<view class="debt-info">
					<view class="debt-main">
						<text class="order-no">订单 {{ item.order_no }}</text>
						<text class="debt-amount">-¥{{ formatMoney(item.original_amount) }}</text>
					</view>
					<view class="debt-sub">
						<text class="debt-time">{{ formatDate(item.created_at) }}</text>
						<text class="debt-status" :class="'status-' + item.status">
							{{ getStatusText(item.status) }}
						</text>
					</view>
					<view class="debt-remaining" v-if="item.status !== 'paid'">
						<text>剩余待还：</text>
						<text class="remaining-amount">¥{{ formatMoney(item.remaining_amount) }}</text>
					</view>
				</view>
				<view class="debt-action" v-if="item.status !== 'paid'">
					<button class="repay-btn" @click="repayDebt(item)">还款</button>
				</view>
			</view>

			<view class="empty-state" v-if="debtList.length === 0 && !loading">
				<text class="empty-icon">💰</text>
				<text class="empty-text">暂无欠款记录</text>
			</view>

			<view class="loading-more" v-if="loading">
				<text>加载中...</text>
			</view>
		</view>

		<!-- 交易记录 -->
		<view class="record-list" v-if="currentTab === 'record'">
			<view class="record-item" v-for="item in recordList" :key="item.id">
				<view class="record-icon" :class="'type-' + item.transaction_type">
					<text>{{ getTypeIcon(item.transaction_type) }}</text>
				</view>
				<view class="record-info">
					<text class="record-title">{{ getTypeText(item.transaction_type) }}</text>
					<text class="record-time">{{ formatDate(item.created_at) }}</text>
					<text class="record-remark" v-if="item.remark">{{ item.remark }}</text>
				</view>
				<view class="record-amount" :class="item.transaction_type === 'repay' ? 'positive' : 'negative'">
					<text>{{ item.transaction_type === 'repay' ? '+' : '-' }}¥{{ formatMoney(item.amount) }}</text>
				</view>
			</view>

			<view class="empty-state" v-if="recordList.length === 0 && !loading">
				<text class="empty-icon">📝</text>
				<text class="empty-text">暂无交易记录</text>
			</view>
		</view>

		<!-- 还款弹窗 -->
		<uni-popup ref="repayPopup" type="bottom">
			<view class="repay-popup">
				<view class="popup-header">
					<text class="popup-title">还款</text>
					<text class="popup-close" @click="$refs.repayPopup.close()">×</text>
				</view>
				<view class="popup-content">
					<view class="repay-info">
						<text class="repay-label">待还金额</text>
						<text class="repay-total">¥{{ formatMoney(repayAmount) }}</text>
					</view>

					<view class="payment-methods">
						<text class="methods-title">支付方式</text>
						<view
							class="method-item"
							v-for="method in paymentMethods"
							:key="method.value"
							:class="{ active: selectedMethod === method.value }"
							@click="selectedMethod = method.value"
						>
							<text class="method-icon">{{ method.icon }}</text>
							<text class="method-name">{{ method.label }}</text>
							<text class="method-check" v-if="selectedMethod === method.value">✓</text>
						</view>
					</view>

					<button class="confirm-repay-btn" @click="confirmRepay" :disabled="repaying">
						{{ repaying ? '处理中...' : '确认还款' }}
					</button>
				</view>
			</view>
		</uni-popup>

		<!-- 提额申请弹窗 -->
		<uni-popup ref="limitPopup" type="center">
			<view class="limit-popup">
				<view class="popup-header">
					<text class="popup-title">申请提升额度</text>
				</view>
				<view class="popup-content">
					<view class="form-item">
						<text class="form-label">当前额度</text>
						<text class="form-value">¥{{ formatMoney(creditInfo.credit_limit) }}</text>
					</view>
					<view class="form-item">
						<text class="form-label">申请额度</text>
						<input
							type="number"
							v-model="applyForm.requested_limit"
							placeholder="请输入申请额度"
							class="form-input"
						/>
					</view>
					<view class="form-item">
						<text class="form-label">申请理由</text>
						<textarea
							v-model="applyForm.reason"
							placeholder="请输入申请理由（选填）"
							class="form-textarea"
						/>
					</view>
					<view class="popup-tip">
						<text>提交后请联系您的技术老师进行审核</text>
					</view>
					<view class="popup-buttons">
						<button class="cancel-btn" @click="$refs.limitPopup.close()">取消</button>
						<button class="submit-btn" @click="submitLimitApply" :disabled="applying">
							{{ applying ? '提交中...' : '提交申请' }}
						</button>
					</view>
				</view>
			</view>
		</uni-popup>
	</view>
</template>

<script>
import api from '@/utils/api.js'

export default {
	data() {
		return {
			currentTab: 'debt',
			loading: false,

			// 信用信息
			creditInfo: {
				credit_limit: 0,
				used_credit: 0,
				available_credit: 0,
				total_debt: 0,
				is_certified: false
			},

			// 欠款列表
			debtList: [],
			debtCount: 0,
			debtPage: 1,

			// 交易记录
			recordList: [],
			recordPage: 1,

			// 还款相关
			repayAmount: 0,
			selectedDebt: null,
			selectedMethod: 'balance',
			repaying: false,

			paymentMethods: [
				{ value: 'balance', label: '余额支付', icon: '💰' },
				{ value: 'wechat', label: '微信支付', icon: '💚' }
			],

			// 提额申请
			applyForm: {
				requested_limit: '',
				reason: ''
			},
			applying: false
		}
	},
	onLoad() {
		this.loadCreditInfo()
		this.loadDebtList()
	},
	onPullDownRefresh() {
		this.loadCreditInfo()
		if (this.currentTab === 'debt') {
			this.loadDebtList()
		} else {
			this.loadRecordList()
		}
		setTimeout(() => {
			uni.stopPullDownRefresh()
		}, 500)
	},
	watch: {
		currentTab(val) {
			if (val === 'record' && this.recordList.length === 0) {
				this.loadRecordList()
			}
		}
	},
	methods: {
		// 加载信用信息
		async loadCreditInfo() {
			try {
				const res = await api.getCreditInfo()
				if (res.data) {
					this.creditInfo = res.data
				}
			} catch (e) {
				console.error('加载信用信息失败', e)
			}
		},

		// 加载欠款列表
		async loadDebtList() {
			this.loading = true
			try {
				const res = await api.getDebtList({
					page: this.debtPage,
					page_size: 20
				})
				if (res.data) {
					this.debtList = res.data.debts || []
					this.debtCount = res.data.debt_count || 0
				}
			} catch (e) {
				console.error('加载欠款列表失败', e)
			} finally {
				this.loading = false
			}
		},

		// 加载交易记录
		async loadRecordList() {
			this.loading = true
			try {
				const res = await api.getCreditRecords({
					page: this.recordPage,
					page_size: 20
				})
				if (res.data) {
					this.recordList = res.data.records || []
				}
			} catch (e) {
				console.error('加载交易记录失败', e)
			} finally {
				this.loading = false
			}
		},

		// 还款单笔
		repayDebt(item) {
			this.selectedDebt = item
			this.repayAmount = item.remaining_amount
			this.$refs.repayPopup.open()
		},

		// 全部还款
		repayAll() {
			this.selectedDebt = null
			this.repayAmount = this.creditInfo.total_debt
			this.$refs.repayPopup.open()
		},

		// 确认还款
		async confirmRepay() {
			if (this.repaying) return

			this.repaying = true
			try {
				const data = {
					amount: this.repayAmount,
					payment_method: this.selectedMethod
				}

				if (this.selectedDebt) {
					data.debt_ids = [this.selectedDebt.id]
				}

				const res = await api.repayDebt(data)

					if (res.data) {
						if (res.data.status === 'success') {
							uni.showToast({ title: '还款成功', icon: 'success' })
							this.$refs.repayPopup.close()
							this.loadCreditInfo()
							this.loadDebtList()
						} else if (res.data.payment_url) {
							// 跳转支付
							uni.showToast({ title: '请完成支付', icon: 'none' })
						}
					}
			} catch (e) {
				console.error('还款失败', e)
				uni.showToast({ title: e.message || '还款失败', icon: 'none' })
			} finally {
				this.repaying = false
			}
		},

		// 申请提额
		applyLimit() {
			if (!this.creditInfo.is_certified) {
				uni.showToast({ title: '请先完成实名认证', icon: 'none' })
				return
			}
			this.applyForm = {
				requested_limit: '',
				reason: ''
			}
			this.$refs.limitPopup.open()
		},

		// 提交提额申请
		async submitLimitApply() {
			if (this.applying) return
			if (!this.applyForm.requested_limit) {
				uni.showToast({ title: '请输入申请额度', icon: 'none' })
				return
			}

			const amount = parseFloat(this.applyForm.requested_limit)
			if (amount <= this.creditInfo.credit_limit) {
				uni.showToast({ title: '申请额度需大于当前额度', icon: 'none' })
				return
			}

			this.applying = true
			try {
				await api.applyLimitIncrease({
					requested_limit: amount,
					reason: this.applyForm.reason
				})

				uni.showToast({ title: '申请已提交', icon: 'success' })
				this.$refs.limitPopup.close()
			} catch (e) {
				console.error('申请失败', e)
				uni.showToast({ title: e.message || '申请失败', icon: 'none' })
			} finally {
				this.applying = false
			}
		},

		// 格式化金额
		formatMoney(amount) {
			if (amount === null || amount === undefined) return '0.00'
			return parseFloat(amount).toFixed(2)
		},

		// 格式化日期
		formatDate(dateStr) {
			if (!dateStr) return ''
			const date = new Date(dateStr)
			const Y = date.getFullYear()
			const M = String(date.getMonth() + 1).padStart(2, '0')
			const D = String(date.getDate()).padStart(2, '0')
			const h = String(date.getHours()).padStart(2, '0')
			const m = String(date.getMinutes()).padStart(2, '0')
			return `${Y}-${M}-${D} ${h}:${m}`
		},

		// 获取状态文本
		getStatusText(status) {
			const map = {
				'unpaid': '待还款',
				'partial': '部分还款',
				'paid': '已还清'
			}
			return map[status] || status
		},

		// 获取交易类型图标
		getTypeIcon(type) {
			const map = {
				'consume': '💳',
				'repay': '💰',
				'refund': '↩️',
				'grant': '🎁',
				'adjust': '⚙️'
			}
			return map[type] || '📝'
		},

		// 获取交易类型文本
		getTypeText(type) {
			const map = {
				'consume': '信用消费',
				'repay': '还款',
				'refund': '退款',
				'grant': '额度发放',
				'adjust': '额度调整'
			}
			return map[type] || type
		}
	}
}
</script>

<style lang="scss" scoped>
.debt-page {
	min-height: 100vh;
	background: #f5f5f5;
	padding-bottom: env(safe-area-inset-bottom);
}

/* 信用卡片 */
.credit-card {
	background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
	margin: 20rpx;
	border-radius: 20rpx;
	padding: 30rpx;
	color: white;

	.credit-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 30rpx;

		.credit-title {
			font-size: 28rpx;
			opacity: 0.9;
		}

		.credit-apply {
			font-size: 24rpx;
			padding: 8rpx 20rpx;
			background: rgba(255, 255, 255, 0.2);
			border-radius: 20rpx;
		}
	}

	.credit-amount {
		text-align: center;
		margin-bottom: 30rpx;

		.amount-label {
			font-size: 24rpx;
			opacity: 0.8;
			display: block;
			margin-bottom: 10rpx;
		}

		.amount-value {
			font-size: 56rpx;
			font-weight: bold;
		}
	}

	.credit-detail {
		display: flex;
		justify-content: space-around;
		padding-top: 20rpx;
		border-top: 1rpx solid rgba(255, 255, 255, 0.2);

		.detail-item {
			text-align: center;

			.item-label {
				font-size: 22rpx;
				opacity: 0.8;
				display: block;
				margin-bottom: 8rpx;
			}

			.item-value {
				font-size: 28rpx;
				font-weight: 500;

				&.debt-value {
					color: #ffeb3b;
				}
			}
		}
	}
}

/* Tab栏 */
.tab-bar {
	display: flex;
	background: white;
	margin: 0 20rpx;
	border-radius: 12rpx;
	overflow: hidden;

	.tab-item {
		flex: 1;
		text-align: center;
		padding: 25rpx 0;
		font-size: 28rpx;
		color: #666;
		position: relative;

		&.active {
			color: #667eea;
			font-weight: 500;

			&::after {
				content: '';
				position: absolute;
				bottom: 0;
				left: 50%;
				transform: translateX(-50%);
				width: 60rpx;
				height: 4rpx;
				background: #667eea;
				border-radius: 2rpx;
			}
		}
	}
}

/* 欠款列表 */
.debt-list {
	padding: 20rpx;

	.list-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 20rpx 0;

		.header-text {
			font-size: 24rpx;
			color: #999;
		}

		.repay-all-btn {
			font-size: 26rpx;
			color: #667eea;
		}
	}
}

.debt-item {
	background: white;
	border-radius: 12rpx;
	padding: 25rpx;
	margin-bottom: 20rpx;
	display: flex;
	justify-content: space-between;
	align-items: center;

	.debt-info {
		flex: 1;

		.debt-main {
			display: flex;
			justify-content: space-between;
			align-items: center;
			margin-bottom: 10rpx;

			.order-no {
				font-size: 28rpx;
				color: #333;
				font-weight: 500;
			}

			.debt-amount {
				font-size: 28rpx;
				color: #ff4d4f;
				font-weight: 500;
			}
		}

		.debt-sub {
			display: flex;
			justify-content: space-between;
			align-items: center;
			margin-bottom: 8rpx;

			.debt-time {
				font-size: 24rpx;
				color: #999;
			}

			.debt-status {
				font-size: 22rpx;
				padding: 4rpx 12rpx;
				border-radius: 4rpx;

				&.status-unpaid {
					background: #fff2f0;
					color: #ff4d4f;
				}

				&.status-partial {
					background: #fff7e6;
					color: #fa8c16;
				}

				&.status-paid {
					background: #f6ffed;
					color: #52c41a;
				}
			}
		}

		.debt-remaining {
			font-size: 24rpx;
			color: #666;

			.remaining-amount {
				color: #ff4d4f;
				font-weight: 500;
			}
		}
	}

	.debt-action {
		margin-left: 20rpx;

		.repay-btn {
			font-size: 24rpx;
			padding: 12rpx 30rpx;
			background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
			color: white;
			border-radius: 30rpx;
			border: none;

			&::after {
				border: none;
			}
		}
	}
}

/* 交易记录 */
.record-list {
	padding: 20rpx;
}

.record-item {
	background: white;
	border-radius: 12rpx;
	padding: 25rpx;
	margin-bottom: 15rpx;
	display: flex;
	align-items: center;

	.record-icon {
		width: 80rpx;
		height: 80rpx;
		border-radius: 50%;
		display: flex;
		align-items: center;
		justify-content: center;
		font-size: 36rpx;
		margin-right: 20rpx;
		background: #f5f5f5;

		&.type-consume {
			background: #fff2f0;
		}

		&.type-repay {
			background: #f6ffed;
		}
	}

	.record-info {
		flex: 1;

		.record-title {
			font-size: 28rpx;
			color: #333;
			display: block;
			margin-bottom: 6rpx;
		}

		.record-time {
			font-size: 22rpx;
			color: #999;
			display: block;
		}

		.record-remark {
			font-size: 22rpx;
			color: #666;
			margin-top: 6rpx;
			display: block;
		}
	}

	.record-amount {
		font-size: 30rpx;
		font-weight: 500;

		&.positive {
			color: #52c41a;
		}

		&.negative {
			color: #ff4d4f;
		}
	}
}

/* 空状态 */
.empty-state {
	text-align: center;
	padding: 100rpx 0;

	.empty-icon {
		font-size: 80rpx;
		display: block;
		margin-bottom: 20rpx;
	}

	.empty-text {
		font-size: 28rpx;
		color: #999;
	}
}

.loading-more {
	text-align: center;
	padding: 30rpx;
	color: #999;
	font-size: 24rpx;
}

/* 还款弹窗 */
.repay-popup {
	background: white;
	border-radius: 24rpx 24rpx 0 0;

	.popup-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 30rpx;
		border-bottom: 1rpx solid #f0f0f0;

		.popup-title {
			font-size: 32rpx;
			font-weight: bold;
			color: #333;
		}

		.popup-close {
			font-size: 40rpx;
			color: #999;
		}
	}

	.popup-content {
		padding: 30rpx;

		.repay-info {
			text-align: center;
			padding: 30rpx 0;

			.repay-label {
				font-size: 26rpx;
				color: #999;
				display: block;
				margin-bottom: 10rpx;
			}

			.repay-total {
				font-size: 48rpx;
				font-weight: bold;
				color: #ff4d4f;
			}
		}

		.payment-methods {
			.methods-title {
				font-size: 28rpx;
				color: #333;
				margin-bottom: 20rpx;
				display: block;
			}

			.method-item {
				display: flex;
				align-items: center;
				padding: 25rpx;
				background: #f5f5f5;
				border-radius: 12rpx;
				margin-bottom: 15rpx;

				&.active {
					background: #f5f7ff;
					border: 1rpx solid #667eea;
				}

				.method-icon {
					font-size: 36rpx;
					margin-right: 15rpx;
				}

				.method-name {
					flex: 1;
					font-size: 28rpx;
					color: #333;
				}

				.method-check {
					color: #667eea;
					font-weight: bold;
				}
			}
		}

		.confirm-repay-btn {
			width: 100%;
			height: 90rpx;
			line-height: 90rpx;
			background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
			color: white;
			border-radius: 45rpx;
			font-size: 32rpx;
			font-weight: bold;
			border: none;
			margin-top: 30rpx;

			&::after {
				border: none;
			}

			&[disabled] {
				opacity: 0.6;
			}
		}
	}
}

/* 提额弹窗 */
.limit-popup {
	background: white;
	border-radius: 16rpx;
	width: 600rpx;

	.popup-header {
		text-align: center;
		padding: 30rpx;
		border-bottom: 1rpx solid #f0f0f0;

		.popup-title {
			font-size: 32rpx;
			font-weight: bold;
			color: #333;
		}
	}

	.popup-content {
		padding: 30rpx;

		.form-item {
			margin-bottom: 25rpx;

			.form-label {
				font-size: 26rpx;
				color: #666;
				display: block;
				margin-bottom: 10rpx;
			}

			.form-value {
				font-size: 32rpx;
				color: #333;
				font-weight: 500;
			}

			.form-input {
				width: 100%;
				height: 80rpx;
				padding: 0 20rpx;
				background: #f5f5f5;
				border-radius: 8rpx;
				font-size: 28rpx;
			}

			.form-textarea {
				width: 100%;
				height: 150rpx;
				padding: 15rpx 20rpx;
				background: #f5f5f5;
				border-radius: 8rpx;
				font-size: 28rpx;
			}
		}

		.popup-tip {
			text-align: center;
			padding: 20rpx 0;

			text {
				font-size: 24rpx;
				color: #999;
			}
		}

		.popup-buttons {
			display: flex;
			gap: 20rpx;
			margin-top: 20rpx;

			.cancel-btn,
			.submit-btn {
				flex: 1;
				height: 80rpx;
				line-height: 80rpx;
				font-size: 28rpx;
				border-radius: 40rpx;
				border: none;

				&::after {
					border: none;
				}
			}

			.cancel-btn {
				background: #f5f5f5;
				color: #666;
			}

			.submit-btn {
				background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
				color: white;

				&[disabled] {
					opacity: 0.6;
				}
			}
		}
	}
}
</style>

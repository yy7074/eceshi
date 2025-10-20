<template>
	<view class="recharge-page">
		<!-- 账户余额 -->
		<view class="balance-card">
			<view class="balance-label">账户余额（元）</view>
			<view class="balance-amount">{{ balance.toFixed(2) }}</view>
		</view>
		
		<!-- 充值金额选择 -->
		<view class="recharge-section">
			<view class="section-title">选择充值金额</view>
			<view class="amount-grid">
				<view 
					v-for="item in amountOptions" 
					:key="item.value"
					class="amount-item"
					:class="{ active: selectedAmount === item.value }"
					@click="selectAmount(item.value)"
				>
					<view class="amount-value">{{ item.label }}</view>
					<view v-if="item.bonus > 0" class="amount-bonus">送{{ item.bonus }}元</view>
				</view>
			</view>
			
			<!-- 自定义金额 -->
			<view class="custom-amount">
				<view class="custom-label">其他金额</view>
				<view class="custom-input">
					<input 
						type="digit" 
						v-model="customAmount" 
						placeholder="请输入充值金额" 
						@input="onCustomInput"
					/>
					<text class="unit">元</text>
				</view>
			</view>
		</view>
		
		<!-- 赠送提示 -->
		<view v-if="bonusAmount > 0" class="bonus-tip">
			<text class="bonus-icon">🎁</text>
			<text class="bonus-text">充{{ finalAmount }}元，赠送{{ bonusAmount }}元，到账{{ actualAmount }}元</text>
		</view>
		
		<!-- 充值规则 -->
		<view class="rules-section">
			<view class="section-title">充值优惠规则</view>
			<view class="rules-list">
				<view v-for="(rule, index) in rules" :key="index" class="rule-item">
					<text class="rule-dot">•</text>
					<text class="rule-text">{{ rule.description }}</text>
				</view>
			</view>
		</view>
		
		<!-- 支付方式 -->
		<view class="payment-section">
			<view class="section-title">支付方式</view>
			<view class="payment-list">
				<view 
					class="payment-item"
					:class="{ active: paymentMethod === 'wechat' }"
					@click="selectPayment('wechat')"
				>
					<view class="payment-left">
						<text class="payment-icon">💳</text>
						<text class="payment-name">微信支付</text>
					</view>
					<view class="payment-radio" :class="{ checked: paymentMethod === 'wechat' }"></view>
				</view>
			</view>
		</view>
		
		<!-- 充值按钮 -->
		<view class="recharge-footer">
			<view class="recharge-info">
				<text class="info-label">实付金额：</text>
				<text class="info-amount">¥{{ finalAmount }}</text>
			</view>
			<button class="recharge-btn" @click="doRecharge" :disabled="!finalAmount || finalAmount < 0.01">
				立即充值
			</button>
		</view>
		
		<!-- 充值记录入口 -->
		<view class="records-entry" @click="goToRecords">
			<text>充值记录</text>
			<text class="arrow">→</text>
		</view>
	</view>
</template>

<script>
import api from '@/utils/api.js'

export default {
	data() {
		return {
			balance: 0,
			selectedAmount: 0,
			customAmount: '',
			paymentMethod: 'wechat',
			rules: [],
			amountOptions: [
				{ value: 100, label: '100元', bonus: 5 },
				{ value: 200, label: '200元', bonus: 10 },
				{ value: 500, label: '500元', bonus: 50 },
				{ value: 1000, label: '1000元', bonus: 150 },
				{ value: 2000, label: '2000元', bonus: 300 },
				{ value: 5000, label: '5000元', bonus: 1000 }
			]
		}
	},
	
	computed: {
		finalAmount() {
			if (this.customAmount) {
				return parseFloat(this.customAmount) || 0
			}
			return this.selectedAmount
		},
		
		bonusAmount() {
			const amount = this.finalAmount
			if (amount < 100) return 0
			if (amount < 500) return Math.floor(amount * 0.05)
			if (amount < 1000) return Math.floor(amount * 0.10)
			if (amount < 5000) return Math.floor(amount * 0.15)
			return Math.floor(amount * 0.20)
		},
		
		actualAmount() {
			return this.finalAmount + this.bonusAmount
		}
	},
	
	onLoad() {
		this.loadBalance()
		this.loadRules()
	},
	
	methods: {
		async loadBalance() {
			try {
				const res = await api.getBalance()
				this.balance = res.data.prepaid_balance || 0
			} catch (error) {
				console.error('加载余额失败', error)
			}
		},
		
		async loadRules() {
			try {
				const res = await api.getBonusRules()
				this.rules = res.data.rules || []
			} catch (error) {
				console.error('加载规则失败', error)
				this.rules = [
					{ description: '100元以下不赠送' },
					{ description: '充100送5，赠送5%' },
					{ description: '充500送50，赠送10%' },
					{ description: '充1000送150，赠送15%' },
					{ description: '充5000送1000，赠送20%' }
				]
			}
		},
		
		selectAmount(amount) {
			this.selectedAmount = amount
			this.customAmount = ''
		},
		
		onCustomInput(e) {
			this.selectedAmount = 0
			let value = e.detail.value
			// 限制最多两位小数
			if (value.includes('.')) {
				const parts = value.split('.')
				if (parts[1].length > 2) {
					this.customAmount = parts[0] + '.' + parts[1].substring(0, 2)
				}
			}
		},
		
		selectPayment(method) {
			this.paymentMethod = method
		},
		
		async doRecharge() {
			if (!this.finalAmount || this.finalAmount < 0.01) {
				uni.showToast({ title: '请输入充值金额', icon: 'none' })
				return
			}
			
			if (this.finalAmount > 50000) {
				uni.showToast({ title: '单笔充值不能超过50000元', icon: 'none' })
				return
			}
			
			try {
				uni.showLoading({ title: '正在创建订单...' })
				
				const res = await api.createRecharge({
					amount: this.finalAmount,
					payment_method: this.paymentMethod
				})
				
				uni.hideLoading()
				
				// 调起微信支付
				if (this.paymentMethod === 'wechat') {
					this.wechatPay(res.data)
				}
				
			} catch (error) {
				uni.hideLoading()
				console.error('创建充值订单失败', error)
				uni.showToast({
					title: error.data?.message || '创建订单失败',
					icon: 'none'
				})
			}
		},
		
		wechatPay(payData) {
			console.log('微信支付参数:', payData)
			
			uni.requestPayment({
				provider: 'wxpay',
				timeStamp: payData.timeStamp,
				nonceStr: payData.nonceStr,
				package: payData.package,
				signType: payData.signType,
				paySign: payData.paySign,
				success: () => {
					uni.showToast({ title: '充值成功', icon: 'success' })
					setTimeout(() => {
						this.loadBalance()
						this.selectedAmount = 0
						this.customAmount = ''
					}, 1500)
				},
				fail: (err) => {
					console.error('微信支付失败:', err)
					if (err.errMsg.includes('cancel')) {
						uni.showToast({ title: '已取消支付', icon: 'none' })
					} else {
						uni.showToast({ title: '支付失败', icon: 'none' })
					}
				}
			})
		},
		
		goToRecords() {
			uni.navigateTo({
				url: '/pagesA/recharge-records/recharge-records'
			})
		}
	}
}
</script>

<style scoped>
.recharge-page {
	min-height: 100vh;
	background: #f5f5f5;
	padding-bottom: 120rpx;
}

.balance-card {
	background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
	margin: 24rpx;
	padding: 48rpx 32rpx;
	border-radius: 16rpx;
	color: white;
}

.balance-label {
	font-size: 28rpx;
	opacity: 0.9;
	margin-bottom: 16rpx;
}

.balance-amount {
	font-size: 72rpx;
	font-weight: bold;
}

.recharge-section,
.rules-section,
.payment-section {
	background: white;
	margin: 24rpx;
	padding: 32rpx;
	border-radius: 16rpx;
}

.section-title {
	font-size: 32rpx;
	font-weight: bold;
	color: #333;
	margin-bottom: 24rpx;
}

.amount-grid {
	display: grid;
	grid-template-columns: repeat(3, 1fr);
	gap: 24rpx;
}

.amount-item {
	background: #f8f8f8;
	border: 2rpx solid #f8f8f8;
	padding: 32rpx 16rpx;
	border-radius: 12rpx;
	text-align: center;
	transition: all 0.3s;
}

.amount-item.active {
	background: #f0f7ff;
	border-color: #667eea;
}

.amount-value {
	font-size: 32rpx;
	font-weight: bold;
	color: #333;
	margin-bottom: 8rpx;
}

.amount-bonus {
	font-size: 24rpx;
	color: #ff6b6b;
}

.custom-amount {
	margin-top: 32rpx;
}

.custom-label {
	font-size: 28rpx;
	color: #666;
	margin-bottom: 16rpx;
}

.custom-input {
	display: flex;
	align-items: center;
	background: #f8f8f8;
	border-radius: 12rpx;
	padding: 0 24rpx;
	height: 88rpx;
}

.custom-input input {
	flex: 1;
	font-size: 32rpx;
	color: #333;
}

.unit {
	font-size: 28rpx;
	color: #999;
	margin-left: 16rpx;
}

.bonus-tip {
	background: linear-gradient(135deg, #fff5eb 0%, #ffe9d6 100%);
	margin: 24rpx;
	padding: 24rpx 32rpx;
	border-radius: 12rpx;
	display: flex;
	align-items: center;
}

.bonus-icon {
	font-size: 40rpx;
	margin-right: 16rpx;
}

.bonus-text {
	font-size: 28rpx;
	color: #ff6b00;
	flex: 1;
}

.rules-list {
	padding-left: 16rpx;
}

.rule-item {
	display: flex;
	align-items: flex-start;
	margin-bottom: 16rpx;
}

.rule-dot {
	color: #667eea;
	margin-right: 12rpx;
	margin-top: 4rpx;
}

.rule-text {
	flex: 1;
	font-size: 28rpx;
	color: #666;
	line-height: 1.6;
}

.payment-list {
	display: flex;
	flex-direction: column;
	gap: 16rpx;
}

.payment-item {
	display: flex;
	align-items: center;
	justify-content: space-between;
	background: #f8f8f8;
	padding: 32rpx;
	border-radius: 12rpx;
	border: 2rpx solid #f8f8f8;
	transition: all 0.3s;
}

.payment-item.active {
	background: #f0f7ff;
	border-color: #667eea;
}

.payment-left {
	display: flex;
	align-items: center;
}

.payment-icon {
	font-size: 48rpx;
	margin-right: 16rpx;
}

.payment-name {
	font-size: 30rpx;
	color: #333;
}

.payment-radio {
	width: 40rpx;
	height: 40rpx;
	border: 2rpx solid #ddd;
	border-radius: 50%;
	position: relative;
}

.payment-radio.checked::after {
	content: '';
	position: absolute;
	top: 50%;
	left: 50%;
	transform: translate(-50%, -50%);
	width: 24rpx;
	height: 24rpx;
	background: #667eea;
	border-radius: 50%;
}

.recharge-footer {
	position: fixed;
	bottom: 0;
	left: 0;
	right: 0;
	background: white;
	padding: 24rpx 32rpx;
	box-shadow: 0 -4rpx 20rpx rgba(0, 0, 0, 0.08);
	display: flex;
	align-items: center;
	justify-content: space-between;
}

.recharge-info {
	display: flex;
	align-items: baseline;
}

.info-label {
	font-size: 28rpx;
	color: #666;
}

.info-amount {
	font-size: 40rpx;
	font-weight: bold;
	color: #ff6b6b;
	margin-left: 8rpx;
}

.recharge-btn {
	background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
	color: white;
	border: none;
	border-radius: 48rpx;
	height: 80rpx;
	line-height: 80rpx;
	padding: 0 48rpx;
	font-size: 32rpx;
	font-weight: bold;
}

.recharge-btn[disabled] {
	opacity: 0.5;
}

.records-entry {
	background: white;
	margin: 24rpx;
	padding: 32rpx;
	border-radius: 16rpx;
	display: flex;
	align-items: center;
	justify-content: space-between;
	font-size: 30rpx;
	color: #333;
}

.arrow {
	color: #999;
	font-size: 36rpx;
}
</style>


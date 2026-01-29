<template>
	<view class="payment-container">
		<!-- 订单信息 -->
		<view class="order-info card">
			<view class="info-row">
				<text class="label">订单号</text>
				<text class="value">{{ order.order_no }}</text>
			</view>
			<view class="info-row">
				<text class="label">项目名称</text>
				<text class="value">{{ order.project_name }}</text>
			</view>
			<view class="info-row total">
				<text class="label">支付金额</text>
				<text class="value price">¥{{ order.total_fee }}</text>
			</view>
		</view>
		
		<!-- 支付方式 -->
		<view class="payment-methods">
			<text class="section-title">支付方式</text>
			
			<view 
				v-for="method in paymentMethods" 
				:key="method.value"
				class="method-item card"
				:class="{ selected: selectedMethod === method.value }"
				@click="selectMethod(method.value)"
			>
				<view class="method-info">
					<text class="method-icon">{{ method.icon }}</text>
					<view class="method-detail">
						<text class="method-name">{{ method.name }}</text>
						<text v-if="method.desc" class="method-desc">{{ method.desc }}</text>
					</view>
				</view>
				<view class="radio" :class="{ checked: selectedMethod === method.value }"></view>
			</view>
		</view>
		
		<!-- 余额支付密码 -->
		<view v-if="selectedMethod === 'balance'" class="password-section">
			<text class="section-title">支付密码</text>
			<view class="password-input card">
				<input 
					v-model="paymentPassword" 
					type="password"
					maxlength="6"
					placeholder="请输入支付密码"
					class="input"
				/>
			</view>
			<text class="password-tip">提示：开发模式下，支付密码与登录密码相同</text>
		</view>
		
		<!-- 底部操作栏 -->
		<view class="bottom-bar">
			<view class="total-info">
				<text class="label">需支付：</text>
				<text class="price">¥{{ order.total_fee }}</text>
			</view>
			<button class="btn-pay" :loading="paying" @click="confirmPay">
				{{ paying ? '支付中...' : '确认支付' }}
			</button>
		</view>
	</view>
</template>

<script>
	import api from '@/utils/api.js'
	
	export default {
		data() {
			return {
				orderId: null,
				order: {
					order_no: '',
					project_name: '',
					total_fee: 0
				},
				
				paymentMethods: [
					{ 
						value: 'balance', 
						name: '余额支付', 
						desc: '当前余额：¥1000.00',
						icon: '💰' 
					},
					{ 
						value: 'wechat', 
						name: '微信支付',
						desc: '',
						icon: '💚'
					}
				],
				
				selectedMethod: 'balance',
				paymentPassword: '',
				paying: false
			}
		},
		onLoad(options) {
			this.orderId = options.order_id
			this.loadOrderInfo()
		},
		methods: {
			// 加载订单信息
			async loadOrderInfo() {
				try {
					const res = await api.getOrderDetail(this.orderId)
					this.order = res.data
				} catch (error) {
					console.error('加载订单失败', error)
					uni.showToast({
						title: '加载订单失败',
						icon: 'none'
					})
				}
			},
			
			// 选择支付方式
			selectMethod(value) {
				const method = this.paymentMethods.find(m => m.value === value)
				if (method && !method.disabled) {
					this.selectedMethod = value
				}
			},
			
			// 确认支付
			async confirmPay() {
				// 验证
				if (this.selectedMethod === 'balance') {
					if (!this.paymentPassword) {
						return uni.showToast({
							title: '请输入支付密码',
							icon: 'none'
						})
					}
				}
				
				this.paying = true
				try {
					const data = {
						order_id: this.orderId,
						payment_method: this.selectedMethod,
						payment_password: this.paymentPassword
					}
					
					const res = await api.createPayment(data)
					
					// 余额支付直接成功
					if (this.selectedMethod === 'balance') {
						if (res.data.status === 'success') {
							uni.showToast({
								title: '支付成功',
								icon: 'success'
							})
							
							// 跳转订单详情
							setTimeout(() => {
								uni.redirectTo({
									url: `/pagesA/order-detail/order-detail?id=${this.orderId}`
								})
							}, 1500)
						}
				} else if (this.selectedMethod === 'wechat') {
					// 微信支付
					console.log('微信支付参数:', res.data)
					
					uni.requestPayment({
						provider: 'wxpay',
						timeStamp: res.data.timeStamp,
						nonceStr: res.data.nonceStr,
						package: res.data.package,
						signType: res.data.signType,
						paySign: res.data.paySign,
						success: () => {
							uni.showToast({ title: '支付成功', icon: 'success' })
							setTimeout(() => {
								uni.redirectTo({
									url: `/pagesA/order-detail/order-detail?id=${this.orderId}`
								})
							}, 1500)
						},
						fail: (err) => {
							console.error('微信支付失败:', err)
							uni.showToast({ title: '支付取消', icon: 'none' })
						}
					})
				} else {
					// 支付宝等其他支付
					uni.showToast({
						title: '该支付方式暂未开通',
						icon: 'none'
					})
				}
					
				} catch (error) {
					console.error('支付失败', error)
					uni.showToast({
						title: error.message || '支付失败',
						icon: 'none'
					})
				} finally {
					this.paying = false
				}
			}
		}
	}
</script>

<style lang="scss" scoped>
	.payment-container {
		min-height: 100vh;
		background-color: #f8f8f8;
		padding: 20rpx 30rpx 160rpx;
	}
	
	.order-info {
		padding: 30rpx;
		margin-bottom: 20rpx;
		
		.info-row {
			display: flex;
			justify-content: space-between;
			align-items: center;
			padding: 20rpx 0;
			border-bottom: 2rpx solid #f5f5f5;
			
			&:last-child {
				border-bottom: none;
			}
			
			.label {
				font-size: 28rpx;
				color: #666;
			}
			
			.value {
				font-size: 28rpx;
				color: #333;
				
				&.price {
					font-size: 40rpx;
					font-weight: bold;
					color: #ff4d4f;
				}
			}
			
			&.total {
				padding-top: 30rpx;
				margin-top: 10rpx;
				border-top: 2rpx solid #f0f0f0;
			}
		}
	}
	
	.payment-methods {
		margin-bottom: 20rpx;
		
		.section-title {
			display: block;
			font-size: 32rpx;
			font-weight: bold;
			color: #333;
			margin-bottom: 20rpx;
		}
		
		.method-item {
			display: flex;
			justify-content: space-between;
			align-items: center;
			padding: 30rpx;
			margin-bottom: 20rpx;
			border: 2rpx solid #e0e0e0;
			
			&.selected {
				border-color: #007AFF;
				background-color: rgba(0, 122, 255, 0.05);
			}
			
			.method-info {
				display: flex;
				align-items: center;
				flex: 1;
				
				.method-icon {
					font-size: 48rpx;
					margin-right: 20rpx;
				}
				
				.method-detail {
					flex: 1;
					
					.method-name {
						display: block;
						font-size: 30rpx;
						font-weight: bold;
						color: #333;
						margin-bottom: 8rpx;
					}
					
					.method-desc {
						display: block;
						font-size: 24rpx;
						color: #999;
					}
				}
			}
			
			.radio {
				width: 40rpx;
				height: 40rpx;
				border: 2rpx solid #ccc;
				border-radius: 50%;
				position: relative;
				
				&.checked {
					border-color: #007AFF;
					
					&::after {
						content: '';
						position: absolute;
						top: 50%;
						left: 50%;
						transform: translate(-50%, -50%);
						width: 24rpx;
						height: 24rpx;
						background-color: #007AFF;
						border-radius: 50%;
					}
				}
			}
		}
	}
	
	.password-section {
		margin-bottom: 20rpx;
		
		.section-title {
			display: block;
			font-size: 32rpx;
			font-weight: bold;
			color: #333;
			margin-bottom: 20rpx;
		}
		
		.password-input {
			padding: 30rpx;
			margin-bottom: 16rpx;
			
			.input {
				width: 100%;
				height: 80rpx;
				padding: 0 24rpx;
				border: 2rpx solid #e0e0e0;
				border-radius: 12rpx;
				font-size: 32rpx;
			}
		}
		
		.password-tip {
			display: block;
			font-size: 24rpx;
			color: #999;
			padding-left: 30rpx;
		}
	}
	
	.bottom-bar {
		position: fixed;
		bottom: 0;
		left: 0;
		right: 0;
		display: flex;
		align-items: center;
		padding: 20rpx 30rpx;
		background-color: #ffffff;
		box-shadow: 0 -4rpx 12rpx rgba(0, 0, 0, 0.08);
		
		.total-info {
			flex: 1;
			
			.label {
				font-size: 28rpx;
				color: #666;
			}
			
			.price {
				font-size: 40rpx;
				font-weight: bold;
				color: #ff4d4f;
			}
		}
		
		.btn-pay {
			padding: 0 60rpx;
			height: 80rpx;
			line-height: 80rpx;
			background: #1890ff;
			color: #ffffff;
			border-radius: 40rpx;
			font-size: 32rpx;
			border: none;
		}
	}
</style>


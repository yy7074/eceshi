<template>
	<view class="coupon-page">
		<view class="empty-state">
			<text class="empty-icon">🎫</text>
			<text class="empty-text">暂无可用优惠券</text>
			<text class="empty-desc">完成订单可获得优惠券</text>
			<button class="btn-back" @click="goBack">返回首页</button>
		</view>
	</view>
</template>

<script>
export default {
	data() {
		return {}
	},
	methods: {
		goBack() {
			uni.switchTab({
				url: '/pages/index/index'
			})
		}
	}
}
</script>

<style lang="scss" scoped>
.coupon-page {
	min-height: 100vh;
	background: #f5f5f5;
}

.empty-state {
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	padding: 200rpx 60rpx;
	
	.empty-icon {
		font-size: 120rpx;
		margin-bottom: 30rpx;
	}
	
	.empty-text {
		font-size: 32rpx;
		color: #333;
		margin-bottom: 15rpx;
	}
	
	.empty-desc {
		font-size: 26rpx;
		color: #999;
		margin-bottom: 60rpx;
	}
	
	.btn-back {
		width: 300rpx;
		height: 80rpx;
		line-height: 80rpx;
		background: #4facfe;
		color: white;
		border-radius: 40rpx;
		font-size: 28rpx;
		border: none;
		
		&::after {
			border: none;
		}
	}
}
</style>


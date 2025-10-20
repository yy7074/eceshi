<template>
	<view class="group-page">
		<!-- 创建团队卡片 -->
		<view class="action-card purple" @click="goCreateGroup">
			<view class="card-left">
				<text class="card-title">创建团队</text>
				<text class="card-desc">我是团长，团体我来管</text>
			</view>
			<view class="card-icon">
				<text class="icon-emoji">👥</text>
			</view>
		</view>
		
		<!-- 扫码入团卡片 -->
		<view class="action-card green" @click="scanToJoin">
			<view class="card-left">
				<text class="card-title">扫码入团</text>
				<text class="card-desc">扫描团队二维码，扫码入团</text>
			</view>
			<view class="card-icon">
				<text class="icon-emoji">📷</text>
			</view>
		</view>
		
		<!-- 加入团队卡片 -->
		<view class="action-card orange" @click="joinByPhone">
			<view class="card-left">
				<text class="card-title">加入团队</text>
				<text class="card-desc">我知道团长手机号，申请入团</text>
			</view>
			<view class="card-icon">
				<text class="icon-emoji">🔍</text>
			</view>
		</view>
	</view>
</template>

<script>
export default {
	data() {
		return {}
	},
	
	methods: {
		// 去创建团队
		goCreateGroup() {
			uni.navigateTo({
				url: '/pagesA/create-group/create-group'
			})
		},
		
		// 扫码入团
		scanToJoin() {
			uni.scanCode({
				success: (res) => {
					console.log('扫码结果：', res.result)
					// TODO: 解析二维码，加入团队
					uni.showToast({
						title: '扫码入团功能开发中',
						icon: 'none'
					})
				},
				fail: () => {
					uni.showToast({
						title: '扫码失败',
						icon: 'none'
					})
				}
			})
		},
		
		// 通过手机号加入
	async joinByPhone() {
		uni.showModal({
			title: '加入团队',
			content: '请输入团长手机号',
			editable: true,
			placeholderText: '请输入手机号',
			success: async (res) => {
				if (res.confirm && res.content) {
					try {
						await api.joinGroupByPhone(res.content)
						uni.showToast({
							title: '申请已提交',
							icon: 'success'
						})
					} catch (error) {
						console.error('加入团队失败', error)
						uni.showToast({
							title: '申请失败',
							icon: 'none'
						})
					}
				}
			}
		})
	}
	}
}
</script>

<style lang="scss" scoped>
.group-page {
	min-height: 100vh;
	background: #f5f5f5;
	padding: 20rpx 30rpx;
}

.action-card {
	background: white;
	border-radius: 20rpx;
	padding: 50rpx 40rpx;
	margin-bottom: 30rpx;
	display: flex;
	justify-content: space-between;
	align-items: center;
	position: relative;
	overflow: hidden;
	
	&::before {
		content: '';
		position: absolute;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		opacity: 1;
		z-index: 0;
	}
	
	&.purple::before {
		background: linear-gradient(135deg, #a78bfa 0%, #8b5cf6 100%);
	}
	
	&.green::before {
		background: linear-gradient(135deg, #34d399 0%, #10b981 100%);
	}
	
	&.orange::before {
		background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
	}
}

.card-left {
	flex: 1;
	display: flex;
	flex-direction: column;
	position: relative;
	z-index: 1;
}

.card-title {
	font-size: 40rpx;
	font-weight: bold;
	color: white;
	margin-bottom: 15rpx;
	display: block;
}

.card-desc {
	font-size: 26rpx;
	color: white;
	opacity: 0.9;
	display: block;
}

.card-icon {
	width: 120rpx;
	height: 120rpx;
	display: flex;
	align-items: center;
	justify-content: center;
	position: relative;
	z-index: 1;
}

.icon-emoji {
	font-size: 80rpx;
	filter: brightness(0) invert(1);
	opacity: 0.5;
}
</style>

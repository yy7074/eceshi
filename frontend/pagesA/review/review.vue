<template>
	<view class="review-page">
		<!-- 订单信息 -->
		<view class="order-info">
			<image :src="orderInfo.project_image || 'https://picsum.photos/200/200'" mode="aspectFill" class="project-image"></image>
			<view class="project-info">
				<text class="project-name">{{ orderInfo.project_name }}</text>
				<text class="project-lab">{{ orderInfo.lab_name }}</text>
			</view>
		</view>
		
		<!-- 评分 -->
		<view class="rating-section">
			<view class="rating-item">
				<text class="rating-label">服务质量</text>
				<view class="stars">
					<text 
						v-for="n in 5" 
						:key="n"
						:class="['star', n <= ratings.service ? 'active' : '']"
						@click="setRating('service', n)"
					>
						{{ n <= ratings.service ? '⭐' : '☆' }}
					</text>
				</view>
			</view>
			<view class="rating-item">
				<text class="rating-label">检测效果</text>
				<view class="stars">
					<text 
						v-for="n in 5" 
						:key="n"
						:class="['star', n <= ratings.quality ? 'active' : '']"
						@click="setRating('quality', n)"
					>
						{{ n <= ratings.quality ? '⭐' : '☆' }}
					</text>
				</view>
			</view>
			<view class="rating-item">
				<text class="rating-label">物流配送</text>
				<view class="stars">
					<text 
						v-for="n in 5" 
						:key="n"
						:class="['star', n <= ratings.logistics ? 'active' : '']"
						@click="setRating('logistics', n)"
					>
						{{ n <= ratings.logistics ? '⭐' : '☆' }}
					</text>
				</view>
			</view>
		</view>
		
		<!-- 评价内容 -->
		<view class="content-section">
			<textarea 
				v-model="content"
				class="textarea"
				placeholder="说说您的使用体验吧~（选填）"
				maxlength="500"
				:show-count="true"
			></textarea>
		</view>
		
		<!-- 上传图片 -->
		<view class="images-section">
			<view class="section-title">添加图片（选填）</view>
			<view class="images-list">
				<view v-for="(img, index) in images" :key="index" class="image-item">
					<image :src="img" mode="aspectFill" class="preview-img"></image>
					<view class="delete-btn" @click="deleteImage(index)">×</view>
				</view>
				<view v-if="images.length < 6" class="upload-btn" @click="chooseImage">
					<text class="upload-icon">📷</text>
					<text class="upload-text">上传图片</text>
				</view>
			</view>
			<view class="upload-tip">最多可上传6张图片</view>
		</view>
		
		<!-- 标签选择 -->
		<view class="tags-section">
			<view class="section-title">选择标签（选填）</view>
			<view class="tags-list">
				<view 
					v-for="(tag, index) in allTags" 
					:key="index"
					:class="['tag-item', selectedTags.includes(tag) ? 'active' : '']"
					@click="toggleTag(tag)"
				>
					{{ tag }}
				</view>
			</view>
		</view>
		
		<!-- 匿名评价 -->
		<view class="anonymous-section">
			<view class="anonymous-item" @click="anonymous = !anonymous">
				<text class="anonymous-label">匿名评价</text>
				<text :class="['checkbox', anonymous ? 'checked' : '']">{{ anonymous ? '☑' : '☐' }}</text>
			</view>
		</view>
		
		<!-- 提交按钮 -->
		<view class="footer-btn">
			<button class="submit-btn" @click="submitReview">提交评价</button>
		</view>
	</view>
</template>

<script>
import api from '@/utils/api.js'

export default {
	data() {
		return {
			orderId: '',
			orderInfo: {},
			ratings: {
				service: 5,
				quality: 5,
				logistics: 5
			},
			content: '',
			images: [],
			allTags: [
				'服务好', '效率高', '专业', '准确',
				'价格实惠', '态度好', '报告详细', '推荐'
			],
			selectedTags: [],
			anonymous: false
		}
	},
	
	onLoad(options) {
		if (options.orderId) {
			this.orderId = options.orderId
			this.loadOrderInfo()
		}
	},
	
	methods: {
		// 加载订单信息
		async loadOrderInfo() {
			try {
				const res = await api.getOrderDetail(this.orderId)
				const order = res.data || {}
				this.orderInfo = {
					project_name: order.project_name || '',
					lab_name: order.lab_name || '',
					project_image: order.project_image || order.cover_image || ''
				}
			} catch (error) {
				console.error('加载订单信息失败', error)
			}
		},
		
		// 设置评分
		setRating(type, value) {
			this.ratings[type] = value
		},
		
		// 选择图片
		chooseImage() {
			uni.chooseImage({
				count: 6 - this.images.length,
				sizeType: ['compressed'],
				sourceType: ['album', 'camera'],
				success: (res) => {
					this.images.push(...res.tempFilePaths)
				}
			})
		},
		
		// 删除图片
		deleteImage(index) {
			this.images.splice(index, 1)
		},
		
		// 切换标签
		toggleTag(tag) {
			const index = this.selectedTags.indexOf(tag)
			if (index > -1) {
				this.selectedTags.splice(index, 1)
			} else {
				this.selectedTags.push(tag)
			}
		},
		
	// 提交评价
	async submitReview() {
		// 计算平均分
		const avgRating = (this.ratings.service + this.ratings.quality + this.ratings.logistics) / 3
		
		if (avgRating < 3 && !this.content.trim()) {
			uni.showModal({
				title: '提示',
				content: '评分较低时，请填写评价内容帮助我们改进',
				showCancel: false
			})
			return
		}
		
		try {
			uni.showLoading({ title: '提交中...' })

			// 提交评价
			await api.createReview({
				order_id: parseInt(this.orderId),
				service_rating: this.ratings.service,
				quality_rating: this.ratings.quality,
				logistics_rating: this.ratings.logistics,
				content: this.content.trim() || null,
				images: this.images,
				tags: this.selectedTags,
				is_anonymous: this.anonymous
			})
			
			uni.hideLoading()
			
			uni.showToast({
				title: '评价成功',
				icon: 'success',
				duration: 2000
			})
			
			setTimeout(() => {
				uni.navigateBack()
			}, 2000)
		} catch (error) {
			uni.hideLoading()
			console.error('提交评价失败', error)
			uni.showToast({
				title: error.data?.message || '提交失败',
				icon: 'none'
			})
		}
	}
	}
}
</script>

<style lang="scss" scoped>
.review-page {
	min-height: 100vh;
	background: #f5f5f5;
	padding-bottom: 120rpx;
}

.order-info {
	background: white;
	padding: 30rpx;
	display: flex;
	align-items: center;
	margin-bottom: 20rpx;
	
	.project-image {
		width: 120rpx;
		height: 120rpx;
		border-radius: 12rpx;
		margin-right: 20rpx;
	}
	
	.project-info {
		flex: 1;
		display: flex;
		flex-direction: column;
		
		.project-name {
			font-size: 28rpx;
			font-weight: bold;
			color: #333;
			margin-bottom: 10rpx;
		}
		
		.project-lab {
			font-size: 24rpx;
			color: #999;
		}
	}
}

.rating-section {
	background: white;
	padding: 30rpx;
	margin-bottom: 20rpx;
	
	.rating-item {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 25rpx 0;
		border-bottom: 1rpx solid #f5f5f5;
		
		&:last-child {
			border-bottom: none;
		}
		
		.rating-label {
			font-size: 28rpx;
			color: #333;
		}
		
		.stars {
			display: flex;
			gap: 10rpx;
			
			.star {
				font-size: 40rpx;
				
				&.active {
					color: #ffb700;
				}
			}
		}
	}
}

.content-section {
	background: white;
	padding: 30rpx;
	margin-bottom: 20rpx;
	
	.textarea {
		width: 100%;
		min-height: 200rpx;
		font-size: 28rpx;
		line-height: 1.6;
	}
}

.images-section,
.tags-section {
	background: white;
	padding: 30rpx;
	margin-bottom: 20rpx;
	
	.section-title {
		font-size: 28rpx;
		color: #333;
		margin-bottom: 20rpx;
	}
	
	.images-list {
		display: flex;
		flex-wrap: wrap;
		gap: 20rpx;
		
		.image-item {
			width: 200rpx;
			height: 200rpx;
			position: relative;
			
			.preview-img {
				width: 100%;
				height: 100%;
				border-radius: 12rpx;
			}
			
			.delete-btn {
				position: absolute;
				top: -10rpx;
				right: -10rpx;
				width: 40rpx;
				height: 40rpx;
				background: #ff4444;
				color: white;
				border-radius: 50%;
				display: flex;
				align-items: center;
				justify-content: center;
				font-size: 32rpx;
				line-height: 1;
			}
		}
		
		.upload-btn {
			width: 200rpx;
			height: 200rpx;
			background: #f5f5f5;
			border-radius: 12rpx;
			border: 2rpx dashed #ddd;
			display: flex;
			flex-direction: column;
			align-items: center;
			justify-content: center;
			
			.upload-icon {
				font-size: 50rpx;
				margin-bottom: 10rpx;
			}
			
			.upload-text {
				font-size: 24rpx;
				color: #999;
			}
		}
	}
	
	.upload-tip {
		font-size: 24rpx;
		color: #999;
		margin-top: 15rpx;
	}
	
	.tags-list {
		display: flex;
		flex-wrap: wrap;
		gap: 20rpx;
		
		.tag-item {
			padding: 15rpx 30rpx;
			background: #f5f5f5;
			color: #666;
			border-radius: 50rpx;
			font-size: 26rpx;
			border: 2rpx solid transparent;
			
			&.active {
				background: #fff0f0;
				color: #ff4444;
				border-color: #ff4444;
			}
		}
	}
}

.anonymous-section {
	background: white;
	padding: 30rpx;
	margin-bottom: 20rpx;
	
	.anonymous-item {
		display: flex;
		justify-content: space-between;
		align-items: center;
		
		.anonymous-label {
			font-size: 28rpx;
			color: #333;
		}
		
		.checkbox {
			font-size: 36rpx;
			
			&.checked {
				color: #667eea;
			}
		}
	}
}

.footer-btn {
	position: fixed;
	bottom: 0;
	left: 0;
	right: 0;
	padding: 20rpx 30rpx;
	background: white;
	box-shadow: 0 -2rpx 10rpx rgba(0, 0, 0, 0.05);
	
	.submit-btn {
		width: 100%;
		background: #1890ff;
		color: white;
		border: none;
		border-radius: 50rpx;
		padding: 30rpx;
		font-size: 32rpx;
		font-weight: bold;
	}
}
</style>

<template>
	<view class="feedback-page">
		<!-- 表单 -->
		<view class="feedback-form">
			<!-- 反馈类型 -->
			<view class="form-item">
				<view class="label">反馈类型 <text class="required">*</text></view>
				<view class="type-list">
					<view 
						v-for="(type, index) in types" 
						:key="index"
						:class="['type-item', selectedType === type.value ? 'active' : '']"
						@click="selectType(type.value)"
					>
						<text class="type-icon">{{ type.icon }}</text>
						<text class="type-text">{{ type.label }}</text>
					</view>
				</view>
			</view>
			
			<!-- 反馈内容 -->
			<view class="form-item">
				<view class="label">问题描述 <text class="required">*</text></view>
				<textarea 
					v-model="content"
					class="textarea"
					placeholder="请详细描述您遇到的问题或建议（至少10个字）"
					maxlength="500"
					:show-count="true"
				></textarea>
			</view>
			
			<!-- 上传图片 -->
			<view class="form-item">
				<view class="label">上传图片（选填）</view>
				<view class="upload-list">
					<view v-for="(img, index) in images" :key="index" class="upload-item">
						<image :src="img" mode="aspectFill" class="upload-img"></image>
						<view class="delete-btn" @click="deleteImage(index)">×</view>
					</view>
					<view v-if="images.length < 3" class="upload-btn" @click="chooseImage">
						<text class="upload-icon">📷</text>
						<text class="upload-text">上传图片</text>
					</view>
				</view>
				<view class="upload-tip">最多可上传3张图片</view>
			</view>
			
			<!-- 联系方式 -->
			<view class="form-item">
				<view class="label">联系方式（选填）</view>
				<input 
					v-model="contact"
					class="input"
					placeholder="请输入您的手机号或邮箱，方便我们联系您"
					maxlength="50"
				/>
			</view>
		</view>
		
		<!-- 历史反馈 -->
		<view class="history-section">
			<view class="section-header">
				<text class="section-title">历史反馈</text>
			</view>
			<view v-if="historyList.length > 0" class="history-list">
				<view v-for="(item, index) in historyList" :key="index" class="history-item" @click="viewDetail(item)">
					<view class="item-header">
						<text class="item-type">{{ item.typeText }}</text>
						<text :class="['item-status', 'status-' + item.status]">{{ item.statusText }}</text>
					</view>
					<text class="item-content">{{ item.content }}</text>
					<text class="item-time">{{ item.time }}</text>
				</view>
			</view>
			<view v-else class="empty-tip">
				暂无历史反馈
			</view>
		</view>
		
		<!-- 提交按钮 -->
		<view class="footer-btn">
			<button class="submit-btn" @click="submitFeedback">提交反馈</button>
		</view>
	</view>
</template>

<script>
export default {
	data() {
		return {
			types: [
				{ value: 'suggestion', label: '功能建议', icon: '💡' },
				{ value: 'bug', label: '问题反馈', icon: '🐛' },
				{ value: 'complaint', label: '服务投诉', icon: '💢' },
				{ value: 'other', label: '其他', icon: '📝' }
			],
			selectedType: '',
			content: '',
			images: [],
			contact: '',
			historyList: []
		}
	},
	
	onLoad() {
		this.loadHistory()
	},
	
	methods: {
		// 选择类型
		selectType(value) {
			this.selectedType = value
		},
		
		// 选择图片
		chooseImage() {
			uni.chooseImage({
				count: 3 - this.images.length,
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
		
		// 提交反馈
		async submitFeedback() {
			// 验证
			if (!this.selectedType) {
				uni.showToast({
					title: '请选择反馈类型',
					icon: 'none'
				})
				return
			}
			
			if (!this.content || this.content.trim().length < 10) {
				uni.showToast({
					title: '请输入至少10个字的问题描述',
					icon: 'none'
				})
				return
			}
			
			try {
				uni.showLoading({ title: '提交中...' })
				
				// TODO: 上传图片
				// TODO: 提交反馈
				
				uni.hideLoading()
				uni.showToast({
					title: '反馈功能开发中',
					icon: 'none'
				})
				
				// 清空表单
				this.selectedType = ''
				this.content = ''
				this.images = []
				this.contact = ''
				
				// 刷新历史
				this.loadHistory()
			} catch (error) {
				uni.hideLoading()
				uni.showToast({
					title: '提交失败',
					icon: 'none'
				})
			}
		},
		
		// 加载历史反馈
		async loadHistory() {
			try {
				// TODO: 调用API获取历史反馈
				this.historyList = []
			} catch (error) {
				console.error('加载历史反馈失败', error)
			}
		},
		
		// 查看详情
		viewDetail(item) {
			uni.showToast({
				title: '详情功能开发中',
				icon: 'none'
			})
		}
	}
}
</script>

<style lang="scss" scoped>
.feedback-page {
	min-height: 100vh;
	background: #f5f5f5;
	padding-bottom: 120rpx;
}

.feedback-form {
	background: white;
	margin: 20rpx 30rpx;
	border-radius: 16rpx;
	padding: 30rpx;
	
	.form-item {
		margin-bottom: 40rpx;
		
		&:last-child {
			margin-bottom: 0;
		}
		
		.label {
			font-size: 28rpx;
			color: #333;
			margin-bottom: 20rpx;
			
			.required {
				color: #ff4444;
			}
		}
		
		.type-list {
			display: grid;
			grid-template-columns: repeat(2, 1fr);
			gap: 20rpx;
			
			.type-item {
				display: flex;
				flex-direction: column;
				align-items: center;
				padding: 30rpx;
				background: #f5f5f5;
				border-radius: 12rpx;
				border: 2rpx solid transparent;
				transition: all 0.3s;
				
				&.active {
					background: #f0f4ff;
					border-color: #667eea;
					
					.type-text {
						color: #667eea;
						font-weight: bold;
					}
				}
				
				.type-icon {
					font-size: 40rpx;
					margin-bottom: 10rpx;
				}
				
				.type-text {
					font-size: 26rpx;
					color: #666;
				}
			}
		}
		
		.textarea {
			width: 100%;
			min-height: 200rpx;
			padding: 20rpx;
			background: #f5f5f5;
			border-radius: 12rpx;
			font-size: 28rpx;
			line-height: 1.6;
		}
		
		.input {
			width: 100%;
			padding: 20rpx;
			background: #f5f5f5;
			border-radius: 12rpx;
			font-size: 28rpx;
		}
		
		.upload-list {
			display: flex;
			flex-wrap: wrap;
			gap: 20rpx;
			
			.upload-item {
				width: 200rpx;
				height: 200rpx;
				position: relative;
				
				.upload-img {
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
	}
}

.history-section {
	background: white;
	margin: 20rpx 30rpx;
	border-radius: 16rpx;
	padding: 30rpx;
	
	.section-header {
		margin-bottom: 30rpx;
		
		.section-title {
			font-size: 32rpx;
			font-weight: bold;
			color: #333;
		}
	}
	
	.history-list {
		.history-item {
			padding: 30rpx;
			background: #f5f5f5;
			border-radius: 12rpx;
			margin-bottom: 20rpx;
			
			&:last-child {
				margin-bottom: 0;
			}
			
			.item-header {
				display: flex;
				justify-content: space-between;
				align-items: center;
				margin-bottom: 15rpx;
				
				.item-type {
					font-size: 26rpx;
					color: #667eea;
				}
				
				.item-status {
					font-size: 24rpx;
					padding: 5rpx 15rpx;
					border-radius: 8rpx;
					
					&.status-pending {
						background: #fff3e0;
						color: #ff9800;
					}
					
					&.status-processing {
						background: #e3f2fd;
						color: #2196f3;
					}
					
					&.status-completed {
						background: #e8f5e9;
						color: #4caf50;
					}
				}
			}
			
			.item-content {
				font-size: 26rpx;
				color: #666;
				line-height: 1.6;
				display: block;
				margin-bottom: 15rpx;
				overflow: hidden;
				text-overflow: ellipsis;
				white-space: nowrap;
			}
			
			.item-time {
				font-size: 24rpx;
				color: #999;
				display: block;
			}
		}
	}
	
	.empty-tip {
		text-align: center;
		padding: 60rpx 0;
		font-size: 26rpx;
		color: #999;
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
		background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
		color: white;
		border: none;
		border-radius: 50rpx;
		padding: 30rpx;
		font-size: 32rpx;
		font-weight: bold;
	}
}
</style>


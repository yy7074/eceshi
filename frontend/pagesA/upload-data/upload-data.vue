<template>
	<view class="upload-page">
		<!-- 订单信息 -->
		<view class="order-info" v-if="orderInfo.id">
			<view class="info-header">
				<text class="order-no">订单号：{{ orderInfo.order_no }}</text>
				<text class="order-status">{{ orderInfo.status_text }}</text>
			</view>
			<view class="info-content">
				<text class="project-name">{{ orderInfo.project_name }}</text>
				<text class="sample-name">样品：{{ orderInfo.sample_name }}</text>
			</view>
		</view>
		
		<!-- 上传类型选择 -->
		<view class="upload-types">
			<view class="type-item" :class="{ active: uploadType === 'sample' }" @click="uploadType = 'sample'">
				<text class="type-icon">📦</text>
				<text class="type-name">样品图片</text>
			</view>
			<view class="type-item" :class="{ active: uploadType === 'data' }" @click="uploadType = 'data'">
				<text class="type-icon">📊</text>
				<text class="type-name">原始数据</text>
			</view>
			<view class="type-item" :class="{ active: uploadType === 'other' }" @click="uploadType = 'other'">
				<text class="type-icon">📎</text>
				<text class="type-name">其他文件</text>
			</view>
		</view>
		
		<!-- 已上传文件列表 -->
		<view class="section" v-if="uploadedFiles.length > 0">
			<view class="section-title">已上传文件</view>
			<view class="file-list">
				<view class="file-item" v-for="(file, index) in uploadedFiles" :key="index">
					<view class="file-icon">
						<text>{{ getFileIcon(file.type) }}</text>
					</view>
					<view class="file-info">
						<text class="file-name">{{ file.name }}</text>
						<text class="file-size">{{ file.size }}</text>
					</view>
					<view class="file-actions">
						<text class="action-btn" @click="previewFile(file)">预览</text>
						<text class="action-btn delete" @click="deleteFile(index)">删除</text>
					</view>
				</view>
			</view>
		</view>
		
		<!-- 上传区域 -->
		<view class="upload-area" @click="chooseFile">
			<view class="upload-icon">📤</view>
			<text class="upload-text">点击上传{{ uploadTypeText }}</text>
			<text class="upload-tip">支持图片、PDF、Excel等格式，单个文件不超过50MB</text>
		</view>
		
		<!-- 备注 -->
		<view class="section">
			<view class="section-title">备注说明</view>
			<textarea 
				v-model="remark" 
				placeholder="请输入备注信息（可选）"
				:maxlength="500"
			></textarea>
		</view>
		
		<!-- 提交按钮 -->
		<view class="submit-section">
			<button class="submit-btn" @click="submitUpload" :disabled="uploadedFiles.length === 0 || submitting">
				{{ submitting ? '提交中...' : '确认提交' }}
			</button>
		</view>
	</view>
</template>

<script>
export default {
	data() {
		return {
			orderId: '',
			orderInfo: {},
			uploadType: 'sample',
			uploadedFiles: [],
			remark: '',
			submitting: false
		}
	},
	computed: {
		uploadTypeText() {
			const texts = {
				sample: '样品图片',
				data: '原始数据',
				other: '其他文件'
			}
			return texts[this.uploadType] || '文件'
		}
	},
	onLoad(options) {
		if (options.orderId) {
			this.orderId = options.orderId
			this.loadOrderInfo()
		}
	},
	methods: {
		async loadOrderInfo() {
			// 模拟加载订单信息
			this.orderInfo = {
				id: this.orderId,
				order_no: 'ORD2025120100001',
				project_name: 'X射线衍射分析(XRD)',
				sample_name: 'XRD测试样品',
				status_text: '检测中'
			}
		},
		
		chooseFile() {
			uni.showActionSheet({
				itemList: ['拍照', '从相册选择', '选择文件'],
				success: (res) => {
					if (res.tapIndex === 0) {
						this.takePhoto()
					} else if (res.tapIndex === 1) {
						this.chooseImage()
					} else {
						this.chooseDocument()
					}
				}
			})
		},
		
		takePhoto() {
			uni.chooseImage({
				count: 1,
				sourceType: ['camera'],
				success: (res) => {
					this.handleFileSelected(res.tempFilePaths[0], 'image')
				}
			})
		},
		
		chooseImage() {
			uni.chooseImage({
				count: 9,
				sourceType: ['album'],
				success: (res) => {
					res.tempFilePaths.forEach(path => {
						this.handleFileSelected(path, 'image')
					})
				}
			})
		},
		
		chooseDocument() {
			// #ifdef H5
			uni.showToast({ title: 'H5暂不支持选择文件', icon: 'none' })
			// #endif
			
			// #ifndef H5
			uni.chooseMessageFile({
				count: 9,
				type: 'file',
				success: (res) => {
					res.tempFiles.forEach(file => {
						this.handleFileSelected(file.path, 'file', file.name, file.size)
					})
				}
			})
			// #endif
		},
		
		handleFileSelected(path, type, name = '', size = 0) {
			const fileName = name || path.split('/').pop()
			const fileSize = size ? this.formatFileSize(size) : '未知'
			
			this.uploadedFiles.push({
				path,
				type,
				name: fileName,
				size: fileSize
			})
		},
		
		formatFileSize(bytes) {
			if (bytes < 1024) return bytes + 'B'
			if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + 'KB'
			return (bytes / 1024 / 1024).toFixed(1) + 'MB'
		},
		
		getFileIcon(type) {
			const icons = {
				image: '🖼️',
				pdf: '📄',
				excel: '📊',
				file: '📎'
			}
			return icons[type] || '📎'
		},
		
		previewFile(file) {
			if (file.type === 'image') {
				uni.previewImage({
					urls: [file.path]
				})
			} else {
				uni.openDocument({
					filePath: file.path,
					fail: () => {
						uni.showToast({ title: '无法预览该文件', icon: 'none' })
					}
				})
			}
		},
		
		deleteFile(index) {
			uni.showModal({
				title: '确认删除',
				content: '确定要删除这个文件吗？',
				success: (res) => {
					if (res.confirm) {
						this.uploadedFiles.splice(index, 1)
					}
				}
			})
		},
		
		submitUpload() {
			if (this.uploadedFiles.length === 0) {
				uni.showToast({ title: '请先上传文件', icon: 'none' })
				return
			}
			
			this.submitting = true
			
			// 模拟上传
			setTimeout(() => {
				this.submitting = false
				uni.showModal({
					title: '上传成功',
					content: '文件已成功上传，工作人员将尽快处理。',
					showCancel: false,
					success: () => {
						uni.navigateBack()
					}
				})
			}, 2000)
		}
	}
}
</script>

<style lang="scss" scoped>
.upload-page {
	min-height: 100vh;
	background: #f5f5f5;
	padding-bottom: 120rpx;
}

.order-info {
	background: #fff;
	padding: 24rpx;
	margin-bottom: 16rpx;
	
	.info-header {
		display: flex;
		justify-content: space-between;
		margin-bottom: 12rpx;
		
		.order-no {
			font-size: 26rpx;
			color: #999;
		}
		
		.order-status {
			font-size: 26rpx;
			color: #1890ff;
		}
	}
	
	.info-content {
		.project-name {
			display: block;
			font-size: 30rpx;
			font-weight: 600;
			color: #333;
			margin-bottom: 8rpx;
		}
		
		.sample-name {
			font-size: 26rpx;
			color: #666;
		}
	}
}

.upload-types {
	display: flex;
	background: #fff;
	padding: 24rpx;
	gap: 16rpx;
	margin-bottom: 16rpx;
	
	.type-item {
		flex: 1;
		display: flex;
		flex-direction: column;
		align-items: center;
		padding: 20rpx;
		background: #f5f5f5;
		border-radius: 12rpx;
		border: 2rpx solid transparent;
		
		&.active {
			background: #e6f7ff;
			border-color: #1890ff;
		}
		
		.type-icon {
			font-size: 40rpx;
			margin-bottom: 8rpx;
		}
		
		.type-name {
			font-size: 24rpx;
			color: #333;
		}
	}
}

.section {
	background: #fff;
	padding: 24rpx;
	margin-bottom: 16rpx;
	
	.section-title {
		font-size: 28rpx;
		font-weight: 600;
		color: #333;
		margin-bottom: 16rpx;
	}
	
	textarea {
		width: 100%;
		height: 150rpx;
		background: #f5f5f5;
		border-radius: 8rpx;
		padding: 16rpx;
		font-size: 28rpx;
		box-sizing: border-box;
	}
}

.file-list {
	.file-item {
		display: flex;
		align-items: center;
		padding: 16rpx 0;
		border-bottom: 1rpx solid #f0f0f0;
		
		&:last-child {
			border-bottom: none;
		}
		
		.file-icon {
			width: 60rpx;
			height: 60rpx;
			background: #f5f5f5;
			border-radius: 8rpx;
			display: flex;
			align-items: center;
			justify-content: center;
			font-size: 32rpx;
			margin-right: 16rpx;
		}
		
		.file-info {
			flex: 1;
			
			.file-name {
				display: block;
				font-size: 28rpx;
				color: #333;
				margin-bottom: 4rpx;
				overflow: hidden;
				text-overflow: ellipsis;
				white-space: nowrap;
			}
			
			.file-size {
				font-size: 24rpx;
				color: #999;
			}
		}
		
		.file-actions {
			display: flex;
			gap: 16rpx;
			
			.action-btn {
				font-size: 26rpx;
				color: #1890ff;
				
				&.delete {
					color: #ff4d4f;
				}
			}
		}
	}
}

.upload-area {
	background: #fff;
	margin: 0 24rpx 16rpx;
	padding: 48rpx;
	border-radius: 12rpx;
	border: 2rpx dashed #d9d9d9;
	text-align: center;
	
	.upload-icon {
		font-size: 64rpx;
		margin-bottom: 16rpx;
	}
	
	.upload-text {
		display: block;
		font-size: 30rpx;
		color: #333;
		margin-bottom: 12rpx;
	}
	
	.upload-tip {
		font-size: 24rpx;
		color: #999;
	}
}

.submit-section {
	position: fixed;
	bottom: 0;
	left: 0;
	right: 0;
	padding: 20rpx 24rpx;
	padding-bottom: calc(20rpx + env(safe-area-inset-bottom));
	background: #fff;
	box-shadow: 0 -2rpx 10rpx rgba(0,0,0,0.05);
	
	.submit-btn {
		width: 100%;
		height: 88rpx;
		line-height: 88rpx;
		background: #1890ff;
		color: #fff;
		font-size: 32rpx;
		border-radius: 44rpx;
		border: none;
		
		&[disabled] {
			background: #d9d9d9;
		}
	}
}
</style>


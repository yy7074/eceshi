<template>
	<view class="booking-container">
		<!-- 步骤条 -->
		<view class="steps">
			<view 
				v-for="(step, index) in steps" 
				:key="index"
				class="step-item"
				:class="{ active: currentStep >= index }"
			>
				<view class="step-number">{{ index + 1 }}</view>
				<text class="step-text">{{ step }}</text>
			</view>
		</view>
		
		<!-- 项目信息 -->
		<view class="project-info card">
			<view class="project-header">
				<image :src="project.cover_image" mode="aspectFill" class="project-image"></image>
				<view class="project-detail">
					<text class="project-name">{{ project.name }}</text>
					<text class="lab-name">{{ project.lab_name }}</text>
					<view class="price">
						<text class="amount">¥{{ project.current_price }}</text>
						<text class="unit">/样品</text>
					</view>
				</view>
			</view>
		</view>
		
		<!-- 第一步：样品信息 -->
		<view v-show="currentStep === 0" class="step-content">
			<view class="section-title">📝 样品信息</view>
			
			<view v-for="(sample, index) in form.samples" :key="index" class="sample-card card">
				<view class="sample-header">
					<text class="sample-title">样品 {{ index + 1 }}</text>
					<text v-if="form.samples.length > 1" class="btn-remove" @click="removeSample(index)">删除</text>
				</view>
				
				<view class="form-item">
					<text class="label"><text class="required">*</text>样品名称</text>
					<input 
						v-model="sample.sample_name" 
						placeholder="请输入样品名称"
						class="input"
					/>
				</view>
				
				<view class="form-item">
					<text class="label">样品类型</text>
					<picker :range="sampleTypes" @change="e => sample.sample_type = sampleTypes[e.detail.value]">
						<view class="picker">
							{{ sample.sample_type || '请选择样品类型' }}
						</view>
					</picker>
				</view>
				
				<view class="form-item">
					<text class="label">样品描述</text>
					<textarea 
						v-model="sample.sample_desc" 
						placeholder="请描述样品的外观、状态等"
						class="textarea"
						maxlength="200"
					></textarea>
				</view>
				
				<view class="form-item">
					<text class="label"><text class="required">*</text>样品数量</text>
					<view class="quantity-control">
						<text class="btn-qty" @click="changeQuantity(index, -1)">-</text>
						<input 
							v-model.number="sample.quantity" 
							type="number"
							class="qty-input"
						/>
						<text class="btn-qty" @click="changeQuantity(index, 1)">+</text>
					</view>
				</view>
				
				<view class="form-item">
					<text class="label">样品照片（选填）</text>
					<view class="photo-upload">
						<view 
							v-for="(photo, pIndex) in sample.photos" 
							:key="pIndex"
							class="photo-item"
						>
							<image :src="photo" mode="aspectFill" class="photo"></image>
							<text class="photo-remove" @click="removePhoto(index, pIndex)">×</text>
						</view>
						<view v-if="!sample.photos || sample.photos.length < 3" class="photo-add" @click="uploadPhoto(index)">
							<text class="icon">+</text>
							<text class="text">上传照片</text>
						</view>
					</view>
				</view>
			</view>
			
			<button class="btn-add-sample" @click="addSample">+ 添加样品</button>
		</view>
		
		<!-- 第二步：配送方式 -->
		<view v-show="currentStep === 1" class="step-content">
			<view class="section-title">🚚 配送方式</view>
			
			<view class="shipping-methods">
				<view 
					v-for="method in shippingMethods" 
					:key="method.value"
					class="method-item card"
					:class="{ selected: form.shipping_method === method.value }"
					@click="selectShipping(method.value)"
				>
					<view class="method-info">
						<text class="method-icon">{{ method.icon }}</text>
						<view class="method-detail">
							<text class="method-name">{{ method.name }}</text>
							<text class="method-desc">{{ method.desc }}</text>
						</view>
					</view>
					<view class="method-fee">
						<text v-if="method.fee > 0">¥{{ method.fee }}</text>
						<text v-else class="free">免费</text>
					</view>
				</view>
			</view>
			
			<!-- 快递地址选择 -->
			<view v-if="form.shipping_method === 'express'" class="address-section">
				<view class="section-title">📍 收样地址</view>
				<view v-if="selectedAddress" class="address-card card" @click="chooseAddress">
					<view class="address-info">
						<text class="receiver">{{ selectedAddress.receiver_name }} {{ selectedAddress.phone }}</text>
						<text class="address">{{ selectedAddress.province }}{{ selectedAddress.city }}{{ selectedAddress.district }}{{ selectedAddress.detail_address }}</text>
					</view>
					<text class="change-btn">更换</text>
				</view>
				<button v-else class="btn-choose-address" @click="chooseAddress">选择收货地址</button>
			</view>
		</view>
		
		<!-- 第三步：费用确认 -->
		<view v-show="currentStep === 2" class="step-content">
			<view class="section-title">💰 费用明细</view>
			
			<view class="fee-card card">
				<view class="fee-item">
					<text class="fee-label">检测费用</text>
					<text class="fee-value">¥{{ feeCalculation.project_fee }}</text>
				</view>
				<view v-if="form.is_urgent" class="fee-item">
					<text class="fee-label">加急费用</text>
					<text class="fee-value urgent">+¥{{ feeCalculation.urgent_fee }}</text>
				</view>
				<view v-if="feeCalculation.shipping_fee > 0" class="fee-item">
					<text class="fee-label">运费</text>
					<text class="fee-value">¥{{ feeCalculation.shipping_fee }}</text>
				</view>
				<view v-if="feeCalculation.discount_amount > 0" class="fee-item discount">
					<text class="fee-label">优惠</text>
					<text class="fee-value">-¥{{ feeCalculation.discount_amount }}</text>
				</view>
				<view class="fee-divider"></view>
				<view class="fee-item total">
					<text class="fee-label">总计</text>
					<text class="fee-value">¥{{ feeCalculation.total_fee }}</text>
				</view>
			</view>
			
			<!-- 加急选项 -->
			<view class="option-card card">
				<view class="option-item" @click="form.is_urgent = !form.is_urgent">
					<view class="option-info">
						<text class="option-name">⚡ 加急服务</text>
						<text class="option-desc">缩短50%服务周期，+¥100</text>
					</view>
					<switch :checked="form.is_urgent" @change="toggleUrgent" color="#007AFF"></switch>
				</view>
			</view>
			
			<!-- 备注 -->
			<view class="remark-section">
				<view class="section-title">📌 订单备注</view>
				<textarea 
					v-model="form.remark" 
					placeholder="有什么特殊要求告诉实验室..."
					class="remark-textarea"
					maxlength="200"
				></textarea>
			</view>
		</view>
		
		<!-- 底部操作栏 -->
		<view class="bottom-bar">
			<view class="total-info">
				<text class="label">合计：</text>
				<text class="price">¥{{ feeCalculation.total_fee }}</text>
			</view>
			<view class="actions">
				<button v-if="currentStep > 0" class="btn-prev" @click="prevStep">上一步</button>
				<button v-if="currentStep < 2" class="btn-next" @click="nextStep">下一步</button>
				<button v-if="currentStep === 2" class="btn-submit" @click="submitOrder" :loading="submitting">提交订单</button>
			</view>
		</view>
	</view>
</template>

<script>
	import api from '@/utils/api.js'
	
	export default {
		data() {
			return {
				projectId: null,
				project: {
					name: '',
					lab_name: '',
					current_price: 0,
					cover_image: ''
				},
				currentStep: 0,
				steps: ['样品信息', '配送方式', '费用确认'],
				
				form: {
					project_id: null,
					samples: [
						{
							sample_name: '',
							sample_type: '',
							sample_desc: '',
							quantity: 1,
							photos: [],
							test_params: {},
							special_requirements: ''
						}
					],
					shipping_method: 'self',
					address_id: null,
					is_urgent: false,
					remark: ''
				},
				
				sampleTypes: ['粉末', '液体', '固体', '薄膜', '块体', '其他'],
				shippingMethods: [
					{ value: 'self', name: '自送样品', desc: '自行送至实验室', fee: 0, icon: '🚶' },
					{ value: 'express', name: '快递寄送', desc: '寄送至实验室', fee: 20, icon: '📦' },
					{ value: 'platform', name: '平台代收', desc: '平台上门收样', fee: 30, icon: '🚗' }
				],
				
				selectedAddress: null,
				feeCalculation: {
					project_fee: 0,
					urgent_fee: 0,
					shipping_fee: 0,
					discount_amount: 0,
					total_fee: 0
				},
				
				submitting: false
			}
		},
		onLoad(options) {
			this.projectId = options.project_id
			this.form.project_id = options.project_id
			this.loadProjectInfo()
		},
		methods: {
			// 加载项目信息
			async loadProjectInfo() {
				// TODO: 调用API
				// 临时模拟数据
				this.project = {
					name: '场发射扫描电镜（SEM）',
					lab_name: '某985高校材料实验室',
					current_price: 312.00,
					cover_image: 'https://via.placeholder.com/200x150'
				}
				this.calculateFee()
			},
			
			// 添加样品
			addSample() {
				this.form.samples.push({
					sample_name: '',
					sample_type: '',
					sample_desc: '',
					quantity: 1,
					photos: [],
					test_params: {},
					special_requirements: ''
				})
			},
			
			// 移除样品
			removeSample(index) {
				this.form.samples.splice(index, 1)
				this.calculateFee()
			},
			
			// 修改数量
			changeQuantity(index, delta) {
				const newQty = this.form.samples[index].quantity + delta
				if (newQty >= 1 && newQty <= 99) {
					this.form.samples[index].quantity = newQty
					this.calculateFee()
				}
			},
			
			// 上传照片
			uploadPhoto(sampleIndex) {
				uni.chooseImage({
					count: 1,
					sizeType: ['compressed'],
					sourceType: ['camera', 'album'],
					success: (res) => {
						if (!this.form.samples[sampleIndex].photos) {
							this.form.samples[sampleIndex].photos = []
						}
						this.form.samples[sampleIndex].photos.push(res.tempFilePaths[0])
					}
				})
			},
			
			// 移除照片
			removePhoto(sampleIndex, photoIndex) {
				this.form.samples[sampleIndex].photos.splice(photoIndex, 1)
			},
			
			// 选择配送方式
			selectShipping(value) {
				this.form.shipping_method = value
				this.calculateFee()
			},
			
			// 选择地址
			chooseAddress() {
				uni.navigateTo({
					url: '/pagesA/address/address?mode=select',
					events: {
						selectAddress: (address) => {
							this.selectedAddress = address
							this.form.address_id = address.id
						}
					}
				})
			},
			
			// 切换加急
			toggleUrgent(e) {
				this.form.is_urgent = e.detail.value
				this.calculateFee()
			},
			
			// 计算费用
			async calculateFee() {
				const totalSamples = this.form.samples.reduce((sum, s) => sum + s.quantity, 0)
				
				const data = {
					project_id: this.projectId,
					sample_count: totalSamples,
					is_urgent: this.form.is_urgent,
					shipping_method: this.form.shipping_method,
					coupon_id: null,
					use_points: 0
				}
				
				// 本地计算（后续接入API）
				let project_fee = this.project.current_price * totalSamples
				let urgent_fee = this.form.is_urgent ? 100 : 0
				let shipping_fee = 0
				
				const method = this.shippingMethods.find(m => m.value === this.form.shipping_method)
				if (method) {
					shipping_fee = method.fee
				}
				
				let discount_amount = 0
				let total_fee = project_fee + urgent_fee + shipping_fee - discount_amount
				
				this.feeCalculation = {
					project_fee: project_fee.toFixed(2),
					urgent_fee: urgent_fee.toFixed(2),
					shipping_fee: shipping_fee.toFixed(2),
					discount_amount: discount_amount.toFixed(2),
					total_fee: total_fee.toFixed(2)
				}
			},
			
			// 下一步
			nextStep() {
				if (!this.validateStep()) {
					return
				}
				if (this.currentStep < 2) {
					this.currentStep++
				}
			},
			
			// 上一步
			prevStep() {
				if (this.currentStep > 0) {
					this.currentStep--
				}
			},
			
			// 验证当前步骤
			validateStep() {
				if (this.currentStep === 0) {
					// 验证样品信息
					for (let sample of this.form.samples) {
						if (!sample.sample_name) {
							uni.showToast({ title: '请填写样品名称', icon: 'none' })
							return false
						}
						if (sample.quantity < 1) {
							uni.showToast({ title: '样品数量至少为1', icon: 'none' })
							return false
						}
					}
				} else if (this.currentStep === 1) {
					// 验证配送方式
					if (this.form.shipping_method === 'express' && !this.form.address_id) {
						uni.showToast({ title: '请选择收货地址', icon: 'none' })
						return false
					}
				}
				return true
			},
			
			// 提交订单
			async submitOrder() {
				if (!this.validateStep()) {
					return
				}
				
				this.submitting = true
				try {
					// TODO: 调用创建订单API
					const res = await api.createOrder(this.form)
					
					uni.showToast({
						title: '订单创建成功',
						icon: 'success'
					})
					
					// 跳转支付页面
					setTimeout(() => {
						uni.redirectTo({
							url: `/pagesA/payment/payment?order_id=${res.data.order_id}`
						})
					}, 1500)
					
				} catch (error) {
					console.error('创建订单失败', error)
					uni.showToast({
						title: error.message || '创建订单失败',
						icon: 'none'
					})
				} finally {
					this.submitting = false
				}
			}
		}
	}
</script>

<style lang="scss" scoped>
	.booking-container {
		min-height: 100vh;
		background-color: #f8f8f8;
		padding-bottom: 160rpx;
	}
	
	.steps {
		display: flex;
		justify-content: space-around;
		padding: 30rpx;
		background-color: #ffffff;
		margin-bottom: 20rpx;
		
		.step-item {
			display: flex;
			flex-direction: column;
			align-items: center;
			
			.step-number {
				width: 60rpx;
				height: 60rpx;
				border-radius: 50%;
				background-color: #e0e0e0;
				color: #999;
				display: flex;
				align-items: center;
				justify-content: center;
				font-size: 28rpx;
				margin-bottom: 12rpx;
			}
			
			.step-text {
				font-size: 24rpx;
				color: #999;
			}
			
			&.active {
				.step-number {
					background-color: #007AFF;
					color: #ffffff;
				}
				
				.step-text {
					color: #007AFF;
				}
			}
		}
	}
	
	.project-info {
		margin: 0 30rpx 20rpx;
		padding: 30rpx;
		
		.project-header {
			display: flex;
			
			.project-image {
				width: 160rpx;
				height: 120rpx;
				border-radius: 12rpx;
				flex-shrink: 0;
			}
			
			.project-detail {
				flex: 1;
				margin-left: 20rpx;
				display: flex;
				flex-direction: column;
				justify-content: space-between;
				
				.project-name {
					font-size: 32rpx;
					font-weight: bold;
					color: #333;
				}
				
				.lab-name {
					font-size: 24rpx;
					color: #999;
				}
				
				.price {
					.amount {
						font-size: 36rpx;
						font-weight: bold;
						color: #ff4d4f;
					}
					
					.unit {
						font-size: 24rpx;
						color: #999;
						margin-left: 8rpx;
					}
				}
			}
		}
	}
	
	.step-content {
		padding: 0 30rpx;
	}
	
	.section-title {
		font-size: 32rpx;
		font-weight: bold;
		color: #333;
		margin: 30rpx 0 20rpx;
	}
	
	.sample-card {
		padding: 30rpx;
		margin-bottom: 20rpx;
		
		.sample-header {
			display: flex;
			justify-content: space-between;
			align-items: center;
			margin-bottom: 20rpx;
			
			.sample-title {
				font-size: 30rpx;
				font-weight: bold;
				color: #333;
			}
			
			.btn-remove {
				font-size: 26rpx;
				color: #ff4d4f;
			}
		}
		
		.form-item {
			margin-bottom: 30rpx;
			
			&:last-child {
				margin-bottom: 0;
			}
			
			.label {
				display: block;
				font-size: 28rpx;
				color: #333;
				margin-bottom: 16rpx;
				
				.required {
					color: #ff4d4f;
					margin-right: 4rpx;
				}
			}
			
			.input, .picker {
				width: 100%;
				height: 80rpx;
				padding: 0 24rpx;
				border: 2rpx solid #e0e0e0;
				border-radius: 12rpx;
				font-size: 28rpx;
			}
			
			.picker {
				line-height: 80rpx;
				color: #333;
			}
			
			.textarea {
				width: 100%;
				min-height: 150rpx;
				padding: 20rpx;
				border: 2rpx solid #e0e0e0;
				border-radius: 12rpx;
				font-size: 28rpx;
			}
			
			.quantity-control {
				display: flex;
				align-items: center;
				
				.btn-qty {
					width: 60rpx;
					height: 60rpx;
					border: 2rpx solid #e0e0e0;
					border-radius: 8rpx;
					display: flex;
					align-items: center;
					justify-content: center;
					font-size: 32rpx;
					color: #333;
				}
				
				.qty-input {
					flex: 1;
					height: 60rpx;
					text-align: center;
					border: 2rpx solid #e0e0e0;
					border-radius: 8rpx;
					margin: 0 16rpx;
				}
			}
			
			.photo-upload {
				display: flex;
				flex-wrap: wrap;
				gap: 20rpx;
				
				.photo-item {
					position: relative;
					width: 150rpx;
					height: 150rpx;
					
					.photo {
						width: 100%;
						height: 100%;
						border-radius: 12rpx;
					}
					
					.photo-remove {
						position: absolute;
						top: -10rpx;
						right: -10rpx;
						width: 40rpx;
						height: 40rpx;
						background-color: #ff4d4f;
						color: #ffffff;
						border-radius: 50%;
						display: flex;
						align-items: center;
						justify-content: center;
						font-size: 32rpx;
					}
				}
				
				.photo-add {
					width: 150rpx;
					height: 150rpx;
					border: 2rpx dashed #ccc;
					border-radius: 12rpx;
					display: flex;
					flex-direction: column;
					align-items: center;
					justify-content: center;
					
					.icon {
						font-size: 48rpx;
						color: #999;
					}
					
					.text {
						font-size: 22rpx;
						color: #999;
						margin-top: 8rpx;
					}
				}
			}
		}
	}
	
	.btn-add-sample {
		width: 100%;
		height: 80rpx;
		line-height: 80rpx;
		background-color: #f5f5f5;
		color: #007AFF;
		border-radius: 12rpx;
		font-size: 28rpx;
		border: none;
		margin-top: 20rpx;
	}
	
	.shipping-methods {
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
				
				.method-icon {
					font-size: 48rpx;
					margin-right: 20rpx;
				}
				
				.method-detail {
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
			
			.method-fee {
				font-size: 32rpx;
				font-weight: bold;
				color: #ff4d4f;
				
				.free {
					color: #52c41a;
				}
			}
		}
	}
	
	.address-section {
		margin-top: 30rpx;
		
		.address-card {
			display: flex;
			justify-content: space-between;
			align-items: center;
			padding: 30rpx;
			
			.address-info {
				flex: 1;
				
				.receiver {
					display: block;
					font-size: 30rpx;
					font-weight: bold;
					color: #333;
					margin-bottom: 12rpx;
				}
				
				.address {
					display: block;
					font-size: 26rpx;
					color: #666;
					line-height: 1.5;
				}
			}
			
			.change-btn {
				font-size: 26rpx;
				color: #007AFF;
			}
		}
		
		.btn-choose-address {
			width: 100%;
			height: 88rpx;
			line-height: 88rpx;
			background-color: #007AFF;
			color: #ffffff;
			border-radius: 12rpx;
			font-size: 30rpx;
			border: none;
		}
	}
	
	.fee-card {
		padding: 30rpx;
		margin-bottom: 20rpx;
		
		.fee-item {
			display: flex;
			justify-content: space-between;
			align-items: center;
			padding: 20rpx 0;
			
			.fee-label {
				font-size: 28rpx;
				color: #666;
			}
			
			.fee-value {
				font-size: 30rpx;
				color: #333;
				
				&.urgent {
					color: #ff9800;
				}
			}
			
			&.discount {
				.fee-value {
					color: #52c41a;
				}
			}
			
			&.total {
				.fee-label {
					font-size: 32rpx;
					font-weight: bold;
					color: #333;
				}
				
				.fee-value {
					font-size: 40rpx;
					font-weight: bold;
					color: #ff4d4f;
				}
			}
		}
		
		.fee-divider {
			height: 2rpx;
			background-color: #f0f0f0;
			margin: 10rpx 0;
		}
	}
	
	.option-card {
		padding: 30rpx;
		margin-bottom: 20rpx;
		
		.option-item {
			display: flex;
			justify-content: space-between;
			align-items: center;
			
			.option-info {
				flex: 1;
				
				.option-name {
					display: block;
					font-size: 30rpx;
					font-weight: bold;
					color: #333;
					margin-bottom: 8rpx;
				}
				
				.option-desc {
					display: block;
					font-size: 24rpx;
					color: #999;
				}
			}
		}
	}
	
	.remark-section {
		.remark-textarea {
			width: 100%;
			min-height: 200rpx;
			padding: 20rpx;
			border: 2rpx solid #e0e0e0;
			border-radius: 12rpx;
			font-size: 28rpx;
			background-color: #ffffff;
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
		
		.actions {
			display: flex;
			gap: 16rpx;
			
			button {
				padding: 0 40rpx;
				height: 80rpx;
				line-height: 80rpx;
				border-radius: 40rpx;
				font-size: 30rpx;
				border: none;
			}
			
			.btn-prev {
				background-color: #f5f5f5;
				color: #666;
			}
			
			.btn-next, .btn-submit {
				background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
				color: #ffffff;
			}
		}
	}
</style>


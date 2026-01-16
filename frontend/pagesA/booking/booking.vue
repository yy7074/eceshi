<template>
	<view class="booking-container">
		<!-- 顶部步骤条 -->
		<view class="steps">
			<view class="step" :class="{ active: currentStep >= 1, completed: currentStep > 1 }">
				<view class="step-number">01</view>
				<view class="step-text">填写样品信息</view>
			</view>
			<view class="step" :class="{ active: currentStep >= 2, completed: currentStep > 2 }">
				<view class="step-number">02</view>
				<view class="step-text">完善配送信息</view>
			</view>
			<view class="step" :class="{ active: currentStep >= 3 }">
				<view class="step-number">03</view>
				<view class="step-text">提交文档和支付</view>
			</view>
		</view>
		
		<!-- 项目标题 -->
		<view class="project-title">预约：{{ projectName }}</view>
		
		<!-- 当前步骤下拉 -->
		<view class="current-step-dropdown">
			<text>{{ stepNames[currentStep - 1] }}</text>
			<text class="arrow">▼</text>
		</view>
		
		<!-- 步骤1：样品信息 -->
		<view class="form-container" v-if="currentStep === 1">
			<view class="form-section">
				<view class="section-title">样品信息</view>
				
				<view class="form-item">
					<text class="label">样品数量</text>
					<view class="quantity-control">
						<button class="btn-minus" @click="decreaseSampleCount">-</button>
						<input class="quantity-input" type="number" v-model.number="formData.sampleCount" />
						<button class="btn-plus" @click="increaseSampleCount">+</button>
					</view>
				</view>
				
				<view class="form-item">
					<text class="label">样品编号</text>
					<text class="value">{{ formData.sampleCount }}</text>
				</view>
				
				<view class="form-item">
					<text class="label">样品名称</text>
					<input class="input" placeholder="请输入样品名称" v-model="formData.sampleName" />
				</view>
				
				<view class="form-item">
					<text class="label">样品成分</text>
					<input class="input" placeholder="请输入样品成分" v-model="formData.sampleComposition" />
				</view>
				
				<view class="form-item column">
					<text class="label">样品状态</text>
					<view class="options">
						<view 
							class="option-btn" 
							:class="{ active: formData.sampleState === item }"
							v-for="item in sampleStates" 
							:key="item"
							@click="formData.sampleState = item"
						>
							{{ item }}
						</view>
					</view>
				</view>
				
				<view class="form-item column">
					<text class="label">危险性</text>
					<view class="options multi-row">
						<view 
							class="option-btn" 
							:class="{ active: formData.dangerType === item }"
							v-for="item in dangerTypes" 
							:key="item"
							@click="formData.dangerType = item"
						>
							{{ item }}
						</view>
					</view>
				</view>
			</view>
			
			<view class="form-section">
				<view class="section-title">存放要求</view>
				<view class="tips">*样品若有特殊存放要求，请勾选告知我们</view>
				<view class="options multi-row">
					<view 
						class="option-btn" 
						:class="{ active: formData.storageRequirement === item }"
						v-for="item in storageRequirements" 
						:key="item"
						@click="formData.storageRequirement = item"
					>
						{{ item }}
					</view>
				</view>
			</view>
			
			<view class="form-section">
				<view class="section-title">备注</view>
				<textarea class="textarea" placeholder="请输入备注" v-model="formData.remark" />
			</view>

			<!-- 动态检测选项 -->
			<dynamic-options-form
				v-if="optionsTree.length > 0"
				ref="optionsForm"
				:options-tree="optionsTree"
				:project-id="projectId"
				:sample-count="formData.sampleCount"
				@change="handleOptionsChange"
			/>
		</view>

		<!-- 步骤2：配送信息 -->
		<view class="form-container" v-if="currentStep === 2">
			<!-- 收货地址 -->
			<view class="form-section">
				<view class="section-title">收货地址</view>
				
				<view class="address-card" v-if="selectedAddress" @click="selectAddress">
					<view class="address-header">
						<text class="name">{{ selectedAddress.name }}</text>
						<text class="phone">{{ selectedAddress.phone }}</text>
					</view>
					<view class="address-detail">
						{{ selectedAddress.province }} {{ selectedAddress.city }} {{ selectedAddress.district }} {{ selectedAddress.detail }}
					</view>
					<text class="change-btn">更换地址</text>
				</view>
				
				<view class="no-address" v-else @click="selectAddress">
					<text class="add-icon">+</text>
					<text class="add-text">添加收货地址</text>
				</view>
			</view>
			
			<!-- 寄送方式 -->
			<view class="form-section">
				<view class="section-title">寄送方式</view>
				<view class="options">
					<view 
						class="option-btn large" 
						:class="{ active: formData.deliveryMethod === item.value }"
						v-for="item in deliveryMethods" 
						:key="item.value"
						@click="formData.deliveryMethod = item.value"
					>
						<text class="option-label">{{ item.label }}</text>
						<text class="option-desc">{{ item.desc }}</text>
					</view>
				</view>
			</view>
			
			<!-- 送达时间 -->
			<view class="form-section">
				<view class="section-title">送达时间</view>
				<picker mode="date" :value="formData.deliveryDate" @change="onDeliveryDateChange">
					<view class="picker-input">
						<text>{{ formData.deliveryDate || '请选择送达日期' }}</text>
						<text class="arrow">▶</text>
					</view>
				</picker>
			</view>
			
			<!-- 配送备注 -->
			<view class="form-section">
				<view class="section-title">配送备注</view>
				<textarea class="textarea" placeholder="请输入配送备注（选填）" v-model="formData.deliveryRemark" />
			</view>
		</view>
		
		<!-- 步骤3：提交文档和支付 -->
		<view class="form-container" v-if="currentStep === 3">
			<!-- 订单信息 -->
			<view class="form-section">
				<view class="section-title">订单信息</view>
				<view class="order-info">
					<view class="info-row">
						<text class="info-label">项目名称</text>
						<text class="info-value">{{ projectName }}</text>
					</view>
					<view class="info-row">
						<text class="info-label">样品数量</text>
						<text class="info-value">{{ formData.sampleCount }} 个</text>
					</view>
					<view class="info-row">
						<text class="info-label">寄送方式</text>
						<text class="info-value">{{ getDeliveryMethodLabel() }}</text>
					</view>
					<view class="info-row">
						<text class="info-label">收货地址</text>
						<text class="info-value">{{ getAddressText() }}</text>
					</view>
				</view>
			</view>
			
			<!-- 上传附件 -->
			<view class="form-section">
				<view class="section-title">上传附件</view>
				<view class="tips">*请上传样品相关文档（如检测要求、样品图片等）</view>
				
				<view class="upload-area" @click="chooseFile">
					<text class="upload-icon">📁</text>
					<text class="upload-text">点击上传文件</text>
				</view>
				
				<view class="file-list" v-if="formData.files.length > 0">
					<view class="file-item" v-for="(file, index) in formData.files" :key="index">
						<text class="file-name">{{ file.name }}</text>
						<text class="file-remove" @click="removeFile(index)">删除</text>
					</view>
				</view>
			</view>
			
			<!-- 费用明细 -->
			<view class="form-section">
				<view class="section-title">费用明细</view>
				<view class="fee-list">
					<view class="fee-row">
						<text class="fee-label">测试费用</text>
						<text class="fee-value">¥{{ projectPrice.toFixed(2) }}</text>
					</view>
					<view class="fee-row">
						<text class="fee-label">样品数量</text>
						<text class="fee-value">x{{ formData.sampleCount }}</text>
					</view>
					<view class="fee-row" v-if="optionsFee > 0">
						<text class="fee-label">选项费用</text>
						<text class="fee-value">¥{{ optionsFee.toFixed(2) }}</text>
					</view>
					<view class="fee-row">
						<text class="fee-label">配送费用</text>
						<text class="fee-value">¥{{ deliveryFee.toFixed(2) }}</text>
					</view>
					<view class="fee-row total">
						<text class="fee-label">总计</text>
						<text class="fee-value">¥{{ totalPrice.toFixed(2) }}</text>
					</view>
				</view>
			</view>
			
			<!-- 支付方式 -->
			<view class="form-section">
				<view class="section-title">支付方式</view>
				<view class="payment-methods">
					<view 
						class="payment-item" 
						:class="{ active: formData.paymentMethod === item.value }"
						v-for="item in paymentMethods" 
						:key="item.value"
						@click="formData.paymentMethod = item.value"
					>
						<image :src="item.icon" class="payment-icon" mode="aspectFit"></image>
						<text class="payment-name">{{ item.name }}</text>
						<text class="check-icon" v-if="formData.paymentMethod === item.value">✓</text>
					</view>
				</view>
			</view>
		</view>
		
		<!-- 底部操作栏 -->
		<view class="bottom-bar">
			<view class="total-price">
				<text class="label">费用合计</text>
				<text class="price">¥{{ totalPrice.toFixed(2) }}</text>
			</view>
			<view class="action-btns">
				<button class="btn-back" v-if="currentStep > 1" @click="prevStep">上一步</button>
				<button class="btn-draft" @click="saveDraft">存为草稿</button>
				<button class="btn-next" @click="nextStep">{{ currentStep === 3 ? '提交订单' : '下一步' }}</button>
			</view>
		</view>
	</view>
</template>

<script>
import api from '@/utils/api.js'
import DynamicOptionsForm from '@/components/DynamicOptionsForm.vue'

export default {
	components: {
		DynamicOptionsForm
	},
	data() {
		return {
			projectId: null,
			projectName: 'XRD织构测试',
			projectPrice: 0,
			deliveryFee: 0,
			optionsFee: 0,
			optionsTree: [],
			optionSelections: [],
			currentStep: 1,
			stepNames: ['填写样品信息', '完善配送信息', '提交文档和支付'],
			
			// 表单选项
			sampleStates: ['粉末', '块状/薄膜', '溶液', '气体', '其它'],
			dangerTypes: ['普通', '易燃', '氧化性', '放射性', '腐蚀性', '有毒', '无'],
			storageRequirements: ['冷藏', '干燥', '避光', '真空', '其它', '无'],
			deliveryMethods: [
				{ value: 'express', label: '快递', desc: '3-5个工作日' },
				{ value: 'self', label: '自送', desc: '自行送达实验室' }
			],
			paymentMethods: [
				{ value: 'wechat', name: '微信支付', icon: '/static/wechat-pay.png' },
				{ value: 'alipay', name: '支付宝', icon: '/static/alipay.png' }
			],
			
			// 选中的地址
			selectedAddress: null,
			
			// 表单数据
			formData: {
				// 步骤1
				sampleCount: 1,
				sampleName: '',
				sampleComposition: '',
				sampleState: '',
				dangerType: '',
				storageRequirement: '',
				remark: '',
				
				// 步骤2
				addressId: null,
				deliveryMethod: 'express',
				deliveryDate: '',
				deliveryRemark: '',
				
				// 步骤3
				files: [],
				paymentMethod: 'wechat'
			}
		}
	},
	computed: {
		totalPrice() {
			return this.projectPrice * this.formData.sampleCount + this.optionsFee + this.deliveryFee
		}
	},
	onLoad(options) {
		if (options.projectId) {
			this.projectId = options.projectId
			this.loadProjectInfo()
		}
		if (options.projectName) {
			this.projectName = decodeURIComponent(options.projectName)
		}
		
		// 尝试加载草稿
		this.loadDraft()
	},
	methods: {
	// 加载项目信息
	async loadProjectInfo() {
		try {
			if (this.projectId) {
				const res = await api.getProjectDetail(this.projectId)
				const project = res.data

				// 设置项目价格
				this.projectPrice = project.current_price || 0

				// 配送费用（可以根据地区或项目类型计算）
				this.deliveryFee = 20.00

				// 加载项目选项
				this.loadProjectOptions()
			}
		} catch (e) {
			console.error('加载项目信息失败', e)
			// 失败时使用默认值
			this.projectPrice = 0
			this.deliveryFee = 20.00
		}
	},

	// 加载项目选项
	async loadProjectOptions() {
		try {
			if (this.projectId) {
				const res = await api.getProjectOptions(this.projectId)
				if (res.code === 200 && res.data) {
					this.optionsTree = res.data.options || []
				}
			}
		} catch (e) {
			console.error('加载项目选项失败', e)
			this.optionsTree = []
		}
	},

	// 处理选项变化
	handleOptionsChange(data) {
		this.optionSelections = data.selections || []
		this.optionsFee = data.totalOptionsFee || 0
	},
		
		// 样品数量控制
		decreaseSampleCount() {
			if (this.formData.sampleCount > 1) {
				this.formData.sampleCount--
			}
		},
		increaseSampleCount() {
			this.formData.sampleCount++
		},
		
		// 选择地址
		selectAddress() {
			uni.navigateTo({
				url: '/pagesA/address/address?mode=select',
				events: {
					selectAddress: (address) => {
						this.selectedAddress = address
						this.formData.addressId = address.id
					}
				}
			})
		},
		
		// 配送日期变化
		onDeliveryDateChange(e) {
			this.formData.deliveryDate = e.detail.value
		},
		
		// 获取配送方式名称
		getDeliveryMethodLabel() {
			const method = this.deliveryMethods.find(m => m.value === this.formData.deliveryMethod)
			return method ? method.label : '快递'
		},
		
		// 获取地址文本
		getAddressText() {
			if (!this.selectedAddress) return '未选择'
			const addr = this.selectedAddress
			return `${addr.name} ${addr.phone} ${addr.province}${addr.city}${addr.district}${addr.detail}`
		},
		
		// 文件上传
		chooseFile() {
			uni.chooseImage({
				count: 9,
				sizeType: ['compressed'],
				sourceType: ['album', 'camera'],
				success: (res) => {
					res.tempFilePaths.forEach((path, index) => {
						this.formData.files.push({
							name: `附件${this.formData.files.length + 1}`,
							path: path
						})
					})
					uni.showToast({
						title: '文件已添加',
						icon: 'success'
					})
				}
			})
		},
		
		// 删除文件
		removeFile(index) {
			this.formData.files.splice(index, 1)
		},
		
		// 存为草稿
		saveDraft() {
			const draft = {
				projectId: this.projectId,
				projectName: this.projectName,
				currentStep: this.currentStep,
				formData: this.formData,
				selectedAddress: this.selectedAddress
			}
			uni.setStorageSync('booking_draft', JSON.stringify(draft))
			uni.showToast({
				title: '已保存为草稿',
				icon: 'success'
			})
		},
		
		// 加载草稿
		loadDraft() {
			try {
				const draft = uni.getStorageSync('booking_draft')
				if (draft) {
					const data = JSON.parse(draft)
					if (data.projectId == this.projectId) {
						this.currentStep = data.currentStep || 1
						this.formData = data.formData
						this.selectedAddress = data.selectedAddress
					}
				}
			} catch (e) {
				console.error('加载草稿失败', e)
			}
		},
		
		// 上一步
		prevStep() {
			if (this.currentStep > 1) {
				this.currentStep--
			}
		},
		
		// 下一步/提交订单
		async nextStep() {
			// 验证当前步骤
			if (this.currentStep === 1) {
				if (!this.formData.sampleName) {
					uni.showToast({ title: '请输入样品名称', icon: 'none' })
					return
				}
				if (!this.formData.sampleState) {
					uni.showToast({ title: '请选择样品状态', icon: 'none' })
					return
				}
				this.currentStep = 2
			} else if (this.currentStep === 2) {
				if (!this.selectedAddress) {
					uni.showToast({ title: '请选择收货地址', icon: 'none' })
					return
				}
				if (!this.formData.deliveryDate) {
					uni.showToast({ title: '请选择送达日期', icon: 'none' })
					return
				}
				this.currentStep = 3
			} else if (this.currentStep === 3) {
				// 提交订单
				await this.submitOrder()
			}
		},
		
		// 提交订单
		async submitOrder() {
			uni.showLoading({ title: '提交中...' })

			try {
				// 上传文件
				const uploadedFiles = await this.uploadFiles()

				// 创建订单
				const orderData = {
					project_id: this.projectId,
					sample_count: this.formData.sampleCount,
					sample_name: this.formData.sampleName,
					sample_composition: this.formData.sampleComposition,
					sample_state: this.formData.sampleState,
					danger_type: this.formData.dangerType,
					storage_requirement: this.formData.storageRequirement,
					remark: this.formData.remark,
					address_id: this.formData.addressId,
					delivery_method: this.formData.deliveryMethod,
					delivery_date: this.formData.deliveryDate,
					delivery_remark: this.formData.deliveryRemark,
					attachments: uploadedFiles,
					total_amount: this.totalPrice,
					option_selections: this.optionSelections
				}

				const res = await api.createOrder(orderData)
				
				uni.hideLoading()
				
				// 跳转支付
				if (res.code === 200) {
					const orderId = res.data.order_id
					this.goPay(orderId)
				}
				
			} catch (e) {
				uni.hideLoading()
				uni.showToast({
					title: e.message || '提交失败',
					icon: 'none'
				})
			}
		},
		
		// 上传文件
		async uploadFiles() {
			const uploadedFiles = []
			for (let file of this.formData.files) {
				try {
					const res = await this.uploadFile(file.path)
					uploadedFiles.push(res.data.url)
				} catch (e) {
					console.error('文件上传失败', e)
				}
			}
			return uploadedFiles
		},
		
		// 上传单个文件
		uploadFile(filePath) {
			return new Promise((resolve, reject) => {
				const token = uni.getStorageSync('token')
				uni.uploadFile({
					url: 'https://catdog.dachaonet.com/api/v1/upload/image',
					filePath: filePath,
					name: 'file',
					header: {
						'Authorization': `Bearer ${token}`
					},
					success: (res) => {
						const data = JSON.parse(res.data)
						if (data.code === 200) {
							resolve(data)
						} else {
							reject(new Error(data.message))
						}
					},
					fail: reject
				})
			})
		},
		
		// 跳转支付
		goPay(orderId) {
			// 清除草稿
			uni.removeStorageSync('booking_draft')
			
			// 调起支付
			if (this.formData.paymentMethod === 'wechat') {
				this.wechatPay(orderId)
			} else if (this.formData.paymentMethod === 'alipay') {
				this.alipayPay(orderId)
			}
		},
		
	// 微信支付
	async wechatPay(orderId) {
		try {
			// 调用后端获取支付参数
			const res = await api.createPayment({
				order_id: orderId,
				payment_method: 'wechat'
			})
			
			console.log('微信支付参数:', res.data)
			
			// 调起微信支付
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
							url: `/pagesA/order-detail/order-detail?id=${orderId}`
						})
					}, 1500)
				},
				fail: (err) => {
					console.error('微信支付失败:', err)
						uni.showToast({ title: '支付取消', icon: 'none' })
					}
				})
			} catch (e) {
				uni.showToast({
					title: '支付失败',
					icon: 'none'
				})
			}
		},
		
		// 支付宝支付
		async alipayPay(orderId) {
			uni.showToast({
				title: '支付宝支付开发中',
				icon: 'none'
			})
		}
	}
}
</script>

<style lang="scss" scoped>
.booking-container {
	min-height: 100vh;
	background: #f5f5f5;
	padding-bottom: 200rpx;
}

/* 步骤条 */
.steps {
	display: flex;
	justify-content: space-between;
	padding: 30rpx 40rpx;
	background: white;
	
	.step {
		flex: 1;
		text-align: center;
		position: relative;
		
		&::after {
			content: '';
			position: absolute;
			top: 20rpx;
			left: 60%;
			width: 80%;
			height: 2rpx;
			background: #e0e0e0;
		}
		
		&:last-child::after {
			display: none;
		}
		
		&.active {
			.step-number {
				background: #4facfe;
				color: white;
			}
			
			.step-text {
				color: #4facfe;
			}
		}
		
		&.completed {
			&::after {
				background: #4facfe;
			}
		}
		
		.step-number {
			width: 50rpx;
			height: 50rpx;
			line-height: 50rpx;
			margin: 0 auto 10rpx;
			background: #e0e0e0;
			color: #999;
			border-radius: 50%;
			font-size: 24rpx;
			font-weight: bold;
		}
		
		.step-text {
			font-size: 22rpx;
			color: #999;
		}
	}
}

/* 项目标题 */
.project-title {
	padding: 30rpx;
	background: white;
	font-size: 32rpx;
	font-weight: bold;
	border-top: 1rpx solid #f0f0f0;
}

/* 当前步骤下拉 */
.current-step-dropdown {
	display: flex;
	justify-content: space-between;
	align-items: center;
	padding: 25rpx 30rpx;
	background: white;
	border-top: 1rpx solid #f0f0f0;
	color: #4facfe;
	font-size: 28rpx;
	
	.arrow {
		font-size: 20rpx;
	}
}

/* 表单容器 */
.form-container {
	padding: 20rpx 0;
}

/* 表单区块 */
.form-section {
	background: white;
	margin-bottom: 20rpx;
	padding: 30rpx;
	
	.section-title {
		font-size: 30rpx;
		font-weight: bold;
		margin-bottom: 20rpx;
		
		&::before {
			content: '* ';
			color: #ff0000;
		}
	}
	
	.tips {
		font-size: 22rpx;
		color: #ff6b6b;
		margin-bottom: 20rpx;
		line-height: 1.6;
	}
}

/* 表单项 */
.form-item {
	display: flex;
	align-items: center;
	padding: 20rpx 0;
	border-bottom: 1rpx solid #f0f0f0;
	
	&.column {
		flex-direction: column;
		align-items: flex-start;
	}
	
	&:last-child {
		border-bottom: none;
	}
	
	.label {
		font-size: 28rpx;
		color: #333;
		margin-bottom: 15rpx;
		
		&::before {
			content: '* ';
			color: #ff0000;
		}
	}
	
	.value {
		flex: 1;
		text-align: right;
		color: #666;
	}
	
	.input {
		flex: 1;
		text-align: right;
		font-size: 28rpx;
	}
}

/* 数量控制 */
.quantity-control {
	display: flex;
	align-items: center;
	margin-left: auto;
	
	.btn-minus,
	.btn-plus {
		width: 60rpx;
		height: 60rpx;
		line-height: 60rpx;
		text-align: center;
		background: #f0f0f0;
		border: none;
		border-radius: 8rpx;
		font-size: 32rpx;
		color: #666;
		padding: 0;
		
		&::after {
			border: none;
		}
	}
	
	.quantity-input {
		width: 100rpx;
		height: 60rpx;
		text-align: center;
		margin: 0 15rpx;
		font-size: 28rpx;
	}
}

/* 选项按钮 */
.options {
	display: flex;
	flex-wrap: wrap;
	gap: 20rpx;
	width: 100%;
	
	&.multi-row {
		.option-btn {
			width: calc((100% - 60rpx) / 4);
		}
	}
	
	.option-btn {
		padding: 15rpx 30rpx;
		background: #f5f5f5;
		border-radius: 8rpx;
		font-size: 26rpx;
		color: #666;
		text-align: center;
		
		&.active {
			background: #4facfe;
			color: white;
		}
		
		&.large {
			width: 100%;
			display: flex;
			flex-direction: column;
			align-items: flex-start;
			padding: 25rpx;
			
			.option-label {
				font-size: 30rpx;
				font-weight: bold;
				margin-bottom: 10rpx;
			}
			
			.option-desc {
				font-size: 24rpx;
				color: #999;
			}
		}
	}
}

/* 文本域 */
.textarea {
	width: 100%;
	height: 200rpx;
	padding: 20rpx;
	background: #f5f5f5;
	border-radius: 8rpx;
	font-size: 28rpx;
}

/* 地址卡片 */
.address-card {
	padding: 30rpx;
	background: #f5f8ff;
	border-radius: 12rpx;
	border: 2rpx solid #4facfe;
	position: relative;
	
	.address-header {
		display: flex;
		justify-content: space-between;
		margin-bottom: 15rpx;
		
		.name {
			font-size: 32rpx;
			font-weight: bold;
		}
		
		.phone {
			font-size: 28rpx;
			color: #666;
		}
	}
	
	.address-detail {
		font-size: 26rpx;
		color: #666;
		line-height: 1.6;
		margin-bottom: 20rpx;
	}
	
	.change-btn {
		font-size: 26rpx;
		color: #4facfe;
	}
}

.no-address {
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	padding: 60rpx 0;
	border: 2rpx dashed #ddd;
	border-radius: 12rpx;
	
	.add-icon {
		font-size: 60rpx;
		color: #4facfe;
		margin-bottom: 15rpx;
	}
	
	.add-text {
		font-size: 28rpx;
		color: #999;
	}
}

/* 日期选择器 */
.picker-input {
	display: flex;
	justify-content: space-between;
	align-items: center;
	padding: 25rpx 20rpx;
	background: #f5f5f5;
	border-radius: 8rpx;
	font-size: 28rpx;
	
	.arrow {
		color: #999;
	}
}

/* 订单信息 */
.order-info {
	.info-row {
		display: flex;
		justify-content: space-between;
		padding: 20rpx 0;
		border-bottom: 1rpx solid #f0f0f0;
		
		&:last-child {
			border-bottom: none;
		}
		
		.info-label {
			font-size: 28rpx;
			color: #666;
		}
		
		.info-value {
			font-size: 28rpx;
			color: #333;
			flex: 1;
			text-align: right;
		}
	}
}

/* 上传区域 */
.upload-area {
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	padding: 60rpx;
	background: #f5f8ff;
	border: 2rpx dashed #4facfe;
	border-radius: 12rpx;
	
	.upload-icon {
		font-size: 60rpx;
		margin-bottom: 15rpx;
	}
	
	.upload-text {
		font-size: 28rpx;
		color: #4facfe;
	}
}

/* 文件列表 */
.file-list {
	margin-top: 20rpx;
	
	.file-item {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 20rpx;
		background: #f5f5f5;
		border-radius: 8rpx;
		margin-bottom: 15rpx;
		
		.file-name {
			font-size: 26rpx;
			color: #333;
		}
		
		.file-remove {
			font-size: 24rpx;
			color: #ff6b6b;
		}
	}
}

/* 费用列表 */
.fee-list {
	.fee-row {
		display: flex;
		justify-content: space-between;
		padding: 20rpx 0;
		border-bottom: 1rpx solid #f0f0f0;
		
		&.total {
			border-bottom: none;
			border-top: 2rpx solid #333;
			margin-top: 10rpx;
			padding-top: 20rpx;
			
			.fee-label,
			.fee-value {
				font-size: 32rpx;
				font-weight: bold;
				color: #ff6b6b;
			}
		}
		
		.fee-label {
			font-size: 28rpx;
			color: #666;
		}
		
		.fee-value {
			font-size: 28rpx;
			color: #333;
		}
	}
}

/* 支付方式 */
.payment-methods {
	.payment-item {
		display: flex;
		align-items: center;
		padding: 25rpx;
		background: #f5f5f5;
		border-radius: 12rpx;
		margin-bottom: 15rpx;
		position: relative;
		border: 2rpx solid transparent;
		
		&.active {
			background: #f5f8ff;
			border-color: #4facfe;
		}
		
		.payment-icon {
			width: 60rpx;
			height: 60rpx;
			margin-right: 20rpx;
		}
		
		.payment-name {
			flex: 1;
			font-size: 30rpx;
			color: #333;
		}
		
		.check-icon {
			font-size: 36rpx;
			color: #4facfe;
		}
	}
}

/* 底部操作栏 */
.bottom-bar {
	position: fixed;
	bottom: 0;
	left: 0;
	right: 0;
	background: white;
	padding: 20rpx 30rpx;
	padding-bottom: calc(20rpx + env(safe-area-inset-bottom));
	box-shadow: 0 -2rpx 10rpx rgba(0,0,0,0.1);
	z-index: 100;
	
	.total-price {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 15rpx;
		
		.label {
			font-size: 28rpx;
			color: #666;
		}
		
		.price {
			font-size: 36rpx;
			color: #ff6b6b;
			font-weight: bold;
		}
	}
	
	.action-btns {
		display: flex;
		align-items: center;
		gap: 15rpx;
		
		.btn-back,
		.btn-draft,
		.btn-next {
			flex: 1;
			height: 80rpx;
			line-height: 80rpx;
			text-align: center;
			border-radius: 40rpx;
			font-size: 28rpx;
			border: none;
			
			&::after {
				border: none;
			}
		}
		
		.btn-back {
			background: #f0f0f0;
			color: #666;
		}
		
		.btn-draft {
			background: #fff;
			color: #4facfe;
			border: 2rpx solid #4facfe;
		}
		
		.btn-next {
			background: #4facfe;
			color: white;
		}
	}
}
</style>

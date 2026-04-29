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
			<!-- 样品模式切换 -->
			<view class="mode-toggle">
				<view
					class="mode-btn"
					:class="{ active: sampleMode === 'single' }"
					@click="sampleMode = 'single'"
				>
					<text class="mode-icon">📦</text>
					<text class="mode-text">单样品模式</text>
				</view>
				<view
					class="mode-btn"
					:class="{ active: sampleMode === 'group' }"
					@click="sampleMode = 'group'"
				>
					<text class="mode-icon">📁</text>
					<text class="mode-text">分组模式</text>
					<text class="mode-tag">推荐</text>
				</view>
			</view>

			<!-- 分组模式 -->
			<view v-if="sampleMode === 'group'">
				<SampleGroupList
					ref="sampleGroupList"
					:project-id="projectId"
					:base-price="projectPrice"
					:options-tree="optionsTree"
					@change="handleGroupsChange"
				/>
			</view>

			<!-- 单样品模式 -->
			<view v-else>
			<!-- 样品数量控制 -->
			<view class="form-section">
				<view class="section-title-no-required">样品数量</view>
				<view class="quantity-row">
					<view class="quantity-control">
						<button class="btn-minus" @click="decreaseSampleCount">-</button>
						<input class="quantity-input" type="number" v-model.number="formData.sampleCount" />
						<button class="btn-plus" @click="increaseSampleCount">+</button>
					</view>
					<text class="quantity-hint">共 {{ formData.sampleCount }} 个样品</text>
				</view>
			</view>

			<!-- 动态表单（样品信息、测试参数、服务选项等全部由后端配置） -->
			<dynamic-options-form
				v-if="optionsTree.length > 0"
				ref="optionsForm"
				:options-tree="optionsTree"
				:project-id="projectId"
				:sample-count="formData.sampleCount"
				@change="handleOptionsChange"
			/>

			<!-- 无配置时的提示 -->
			<view class="empty-options" v-if="optionsTree.length === 0 && !optionsLoading">
				<text class="empty-text">该项目暂未配置样品信息/测试参数等选项</text>
				<text class="empty-tip">如需补充项目相关字段，请联系管理员在后台为此项目添加</text>
			</view>

			<!-- 备注 -->
			<view class="form-section">
				<view class="section-title-no-required">备注（选填）</view>
				<textarea class="textarea" placeholder="请输入特殊要求或备注信息" v-model="formData.remark" />
			</view>
			</view>
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

			<!-- 优惠券 -->
			<view class="form-section">
				<view class="section-title-no-required">优惠券</view>
				<view v-if="availableCoupons.length > 0" class="coupon-list">
					<view
						v-for="coupon in availableCoupons"
						:key="coupon.id"
						class="coupon-card"
						:class="{ active: formData.couponId === coupon.id }"
						@click="toggleCoupon(coupon.id)"
					>
						<view class="coupon-main">
							<text class="coupon-name">{{ coupon.coupon_name }}</text>
							<text class="coupon-desc">{{ getCouponSummary(coupon) }}</text>
						</view>
						<text class="coupon-select">{{ formData.couponId === coupon.id ? '已选择' : '选择' }}</text>
					</view>
				</view>
				<view v-else class="coupon-empty">
					<text>暂无可用优惠券</text>
					<text class="coupon-link" @click="goCouponCenter">去领券</text>
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
					<view class="fee-row" v-if="couponDiscount > 0">
						<text class="fee-label">优惠券</text>
						<text class="fee-value discount">-¥{{ couponDiscount.toFixed(2) }}</text>
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
			
			<!-- 支付方式（统一信用支付，不再展示选择） -->
			<view class="form-section" v-if="false">
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
import SampleGroupList from '@/components/SampleGroupList.vue'

export default {
	components: {
		DynamicOptionsForm,
		SampleGroupList
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
			optionsFormData: {}, // 动态表单数据
			optionsLoading: false,
			currentStep: 1,
			stepNames: ['填写样品信息', '完善配送信息', '提交文档和支付'],

			// 样品模式：single - 单样品模式，group - 分组模式
			sampleMode: 'single',
			sampleGroups: [],
			groupsTotalPrice: 0,
			availableCoupons: [],
			
			// 配送和支付选项
			deliveryMethods: [
				{ value: 'express', label: '自行邮寄', desc: '3-5个工作日送达' },
				{ value: 'self', label: '上门取样', desc: '部分院校支持，请提前联系确认' }
			],
			paymentMethods: [
				{ value: 'credit', name: '信用支付', icon: '/static/wechat-pay.svg' }
			],
			
			// 选中的地址
			selectedAddress: null,
			
			// 表单数据
			formData: {
				// 步骤1 - 样品数量和备注（其他信息由动态表单收集）
				sampleCount: 1,
				remark: '',
				
				// 步骤2
				addressId: null,
				deliveryMethod: 'express',
				deliveryDate: '',
				deliveryRemark: '',
				
				// 步骤3
				couponId: null,
				files: [],
				paymentMethod: 'credit'
			}
		}
	},
	computed: {
		subtotalPrice() {
			if (this.sampleMode === 'group') {
				return this.groupsTotalPrice + this.deliveryFee
			}
			return this.projectPrice * this.formData.sampleCount + this.optionsFee + this.deliveryFee
		},
		selectedCoupon() {
			return this.availableCoupons.find(coupon => coupon.id === this.formData.couponId) || null
		},
		couponDiscount() {
			const coupon = this.selectedCoupon
			if (!coupon) {
				return 0
			}
			let discount = 0
			if (coupon.coupon_type === 'discount') {
				discount = this.subtotalPrice * (1 - Number(coupon.discount_value || 1))
			} else {
				discount = Number(coupon.discount_value || 0)
			}
			return Math.max(0, Math.min(discount, this.subtotalPrice))
		},
		totalPrice() {
			return Math.max(0, this.subtotalPrice - this.couponDiscount)
		},
		effectiveSampleCount() {
			if (this.sampleMode === 'group') {
				return this.sampleGroups.reduce((sum, g) => {
					const items = g.items || []
					return sum + items.reduce((s, i) => s + (i.quantity || 1), 0)
				}, 0)
			}
			return this.formData.sampleCount
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
		
		// 加载默认地址（如果草稿中没有地址）
		if (!this.selectedAddress) {
			this.loadDefaultAddress()
		}
		this.loadCoupons()
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
		this.optionsLoading = true
		try {
			if (this.projectId) {
				const res = await api.getProjectOptions(this.projectId)
				if (res.code === 200 && res.data) {
					this.optionsTree = res.data.options || []
				} else {
					this.optionsTree = []
					console.warn('加载选项接口返回异常', res)
				}
			}
		} catch (e) {
			console.error('加载项目选项失败', e)
			this.optionsTree = []
			uni.showToast({
				title: '加载选项失败：' + (e.message || e.detail || '请稍后重试'),
				icon: 'none',
				duration: 2500
			})
		} finally {
			this.optionsLoading = false
		}
	},

	// 处理选项变化
	handleOptionsChange(data) {
		this.optionSelections = data.selections || []
		this.optionsFee = data.totalOptionsFee || 0
		this.optionsFormData = data.formData || {}
	},

	// 处理样品分组变化
	handleGroupsChange(data) {
		this.sampleGroups = data.groups || []
		this.groupsTotalPrice = data.totalPrice || 0
	},

	async loadCoupons() {
		try {
			const res = await api.getMyCoupons({ status: 'available', page: 1, page_size: 50 })
			this.availableCoupons = res.data?.items || []
		} catch (e) {
			console.error('加载优惠券失败', e)
			this.availableCoupons = []
		}
	},

	toggleCoupon(couponId) {
		this.formData.couponId = this.formData.couponId === couponId ? null : couponId
	},

	getCouponSummary(coupon) {
		if (!coupon) {
			return ''
		}
		if (coupon.coupon_type === 'discount') {
			const rate = Number(coupon.discount_value || 1)
			return `${Math.round(rate * 10)}折优惠`
		}
		return `立减¥${Number(coupon.discount_value || 0).toFixed(2)}`
	},

	goCouponCenter() {
		uni.navigateTo({
			url: '/pagesA/coupon/coupon'
		})
	},

	getDynamicValue(keys) {
		for (const key of keys) {
			if (this.optionsFormData[key]) {
				return this.optionsFormData[key]
			}
		}
		return ''
	},

	buildOrderSamples(uploadedFiles) {
		const count = Math.max(1, Number(this.formData.sampleCount || 1))
		const sampleName = this.getDynamicValue(['样品名称', '样品名', '样品编号', '名称']) || '样品'
		const sampleType = this.getDynamicValue(['样品类型', '样品类别', '样品状态', '类型'])
		const sampleDesc = this.getDynamicValue(['样品描述', '样品说明', '样品成分', '描述'])
		const samples = []

		for (let i = 0; i < count; i++) {
			samples.push({
				sample_name: count > 1 ? `${sampleName}${i + 1}` : sampleName,
				sample_type: sampleType || null,
				sample_desc: sampleDesc || null,
				quantity: 1,
				photos: uploadedFiles,
				test_params: this.optionsFormData,
				special_requirements: this.formData.remark
			})
		}

		return samples
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
		
		// 加载默认地址
		async loadDefaultAddress() {
			try {
				const res = await api.getAddresses()
				if (res.data && res.data.length > 0) {
					// 优先使用默认地址，否则用第一个
					const defaultAddr = res.data.find(a => a.is_default) || res.data[0]
					this.selectedAddress = {
						id: defaultAddr.id,
						name: defaultAddr.receiver_name || defaultAddr.name,
						phone: defaultAddr.phone,
						province: defaultAddr.province,
						city: defaultAddr.city,
						district: defaultAddr.district || '',
						detail: defaultAddr.detail_address || defaultAddr.detail
					}
					this.formData.addressId = defaultAddr.id
				}
			} catch (error) {
				console.error('加载默认地址失败', error)
			}
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
				selectedAddress: this.selectedAddress,
				sampleMode: this.sampleMode
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
						this.sampleMode = data.sampleMode || 'single'
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
				// 分组模式验证
				if (this.sampleMode === 'group') {
					if (this.sampleGroups.length === 0) {
						uni.showToast({ title: '请至少创建一个样品分组', icon: 'none' })
						return
					}
					const emptyGroups = this.sampleGroups.filter(g => !g.items || g.items.length === 0)
					if (emptyGroups.length > 0) {
						uni.showToast({ title: '所有分组都需要添加样品', icon: 'none' })
						return
					}
				} else {
					// 单样品模式验证 - 使用动态表单验证
					if (this.$refs.optionsForm) {
						const errors = this.$refs.optionsForm.validate()
						if (errors && errors.length > 0) {
							uni.showToast({ title: errors[0], icon: 'none' })
							return
						}
					}
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

				// 分组模式提交
				if (this.sampleMode === 'group') {
					const groupIds = this.sampleGroups.map(g => g.id)
					const res = await api.submitSampleGroups({
						group_ids: groupIds,
						merge_order: true, // 合并为一个订单
						address_id: this.formData.addressId,
						coupon_id: this.formData.couponId,
						remark: this.formData.remark
					})

					uni.hideLoading()

					if (res.code === 200 && res.data.order_ids.length > 0) {
						await this.paySubmittedOrders(res.data.order_ids)
					}
					return
				}

				// 单样品模式提交
				const orderData = {
					project_id: this.projectId,
					sample_count: this.formData.sampleCount,
					samples: this.buildOrderSamples(uploadedFiles),
					// 动态表单数据
					form_data: this.optionsFormData,
					remark: this.formData.remark,
					address_id: this.formData.addressId,
					delivery_method: this.formData.deliveryMethod,
					delivery_date: this.formData.deliveryDate,
					delivery_remark: this.formData.deliveryRemark,
					coupon_id: this.formData.couponId,
					attachments: uploadedFiles,
					total_amount: this.totalPrice,
					option_selections: this.optionSelections
				}

				const res = await api.createOrder(orderData)

				uni.hideLoading()

				// 跳转支付
				if (res.code === 200) {
					const orderId = res.data.order_id
					await this.paySubmittedOrders([orderId])
				}

			} catch (e) {
				console.error('提交订单失败', e)
				uni.hideLoading()
				uni.showToast({
					title: e.message || e.detail || '提交失败',
					icon: 'none'
				})
			}
		},

		async paySubmittedOrders(orderIds) {
			const ids = (orderIds || []).filter(Boolean)
			if (ids.length === 0) {
				return
			}

			try {
				for (const orderId of ids) {
					await api.creditPay({
						order_id: orderId,
						amount: this.totalPrice
					})
				}
				uni.showToast({ title: '提交成功，已扣减信用额度', icon: 'success' })
				setTimeout(() => {
					uni.redirectTo({
						url: `/pagesA/order-detail/order-detail?id=${ids[0]}`
					})
				}, 1200)
			} catch (e) {
				console.error('信用支付失败，转入支付页', e)
				uni.showToast({
					title: e.message || e.detail || '订单已创建，请完成支付',
					icon: 'none'
				})
				setTimeout(() => {
					this.goPay(ids[0])
				}, 1200)
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
					url: `${api.baseUrl}/api/v1/upload/image`,
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
		
		// 跳转支付（统一走信用支付页）
		goPay(orderId) {
			uni.removeStorageSync('booking_draft')
			uni.redirectTo({
				url: `/pagesA/payment/payment?order_id=${orderId}`
			})
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
			try {
				const res = await api.createPayment({
					order_id: orderId,
					payment_method: 'alipay'
				})
				if (res.data?.pay_url) {
					uni.showModal({
						title: '支付宝支付',
						content: '已生成支付宝支付链接，是否复制到剪贴板？',
						confirmText: '复制链接',
						cancelText: '取消',
						success: (modalRes) => {
							if (modalRes.confirm) {
								uni.setClipboardData({
									data: res.data.pay_url,
									success: () => {
										uni.showToast({ title: '链接已复制', icon: 'success' })
									}
								})
							}
						}
					})
					return
				}
				uni.showToast({
					title: '请在新页面完成支付',
					icon: 'none'
				})
			} catch (e) {
				uni.showToast({
					title: e.message || '支付失败',
					icon: 'none'
				})
			}
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

	.section-title-no-required {
		font-size: 30rpx;
		font-weight: bold;
		margin-bottom: 20rpx;
	}
	
	.tips {
		font-size: 22rpx;
		color: #ff6b6b;
		margin-bottom: 20rpx;
		line-height: 1.6;
	}
}

/* 样品数量行 */
.quantity-row {
	display: flex;
	align-items: center;
	justify-content: space-between;

	.quantity-hint {
		font-size: 26rpx;
		color: #999;
	}
}

/* 空选项提示 */
.empty-options {
	padding: 60rpx 30rpx;
	background: white;
	margin-bottom: 20rpx;
	text-align: center;

	.empty-text {
		font-size: 28rpx;
		color: #999;
		display: block;
	}

	.empty-tip {
		font-size: 24rpx;
		color: #bbb;
		display: block;
		margin-top: 12rpx;
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

/* 样品模式切换 */
.mode-toggle {
	display: flex;
	gap: 20rpx;
	padding: 20rpx;
	background: white;
	margin-bottom: 20rpx;

	.mode-btn {
		flex: 1;
		display: flex;
		flex-direction: column;
		align-items: center;
		padding: 30rpx 20rpx;
		background: #f5f5f5;
		border-radius: 16rpx;
		border: 2rpx solid transparent;
		position: relative;
		transition: all 0.3s;

		&.active {
			background: #f5f8ff;
			border-color: #4facfe;
		}

		.mode-icon {
			font-size: 48rpx;
			margin-bottom: 12rpx;
		}

		.mode-text {
			font-size: 28rpx;
			color: #333;
			font-weight: 500;
		}

		.mode-tag {
			position: absolute;
			top: -10rpx;
			right: -10rpx;
			background: linear-gradient(135deg, #ff6b6b 0%, #ff8e53 100%);
			color: white;
			font-size: 20rpx;
			padding: 4rpx 12rpx;
			border-radius: 20rpx;
		}
	}
}

.coupon-list {
	display: flex;
	flex-direction: column;
	gap: 16rpx;
}

.coupon-card {
	display: flex;
	justify-content: space-between;
	align-items: center;
	padding: 24rpx;
	background: #f8fafc;
	border: 2rpx solid transparent;
	border-radius: 16rpx;

	&.active {
		border-color: #4facfe;
		background: #eef7ff;
	}
}

.coupon-main {
	display: flex;
	flex-direction: column;
	gap: 8rpx;
}

.coupon-name {
	font-size: 28rpx;
	color: #333;
	font-weight: 600;
}

.coupon-desc {
	font-size: 24rpx;
	color: #666;
}

.coupon-select {
	font-size: 24rpx;
	color: #4facfe;
}

.coupon-empty {
	display: flex;
	justify-content: space-between;
	align-items: center;
	padding: 24rpx;
	background: #f8fafc;
	border-radius: 16rpx;
	font-size: 26rpx;
	color: #666;
}

.coupon-link {
	color: #4facfe;
}

.discount {
	color: #ff6b6b;
}
</style>

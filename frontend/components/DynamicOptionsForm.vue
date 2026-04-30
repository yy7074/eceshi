<template>
	<view class="dynamic-options-form" v-if="optionsTree && optionsTree.length > 0">
		<!-- 按分组显示选项 -->
		<view
			class="options-group"
			v-for="(group, groupName) in groupedOptions"
			:key="groupName"
		>
			<view class="group-header">
				<view class="group-title">{{ groupName }}</view>
			</view>
			<view class="group-content">
				<option-node
					v-for="option in group"
					:key="option.id"
					:option="option"
					:siblings="group"
					:selections="selections"
					:level="0"
					@select="handleOptionSelect"
					@input="handleOptionInput"
				/>
			</view>
		</view>

		<!-- 未分组的选项（兼容旧数据） -->
		<view class="options-section" v-if="ungroupedOptions.length > 0">
			<view class="section-title">
				<text>{{ groupedOptionsKeys.length > 0 ? '其他选项' : '检测选项' }}</text>
				<text class="section-tip" v-if="!hasSelections">请选择检测选项</text>
			</view>

			<option-node
				v-for="option in ungroupedOptions"
				:key="option.id"
				:option="option"
				:siblings="ungroupedOptions"
				:selections="selections"
				:level="0"
				@select="handleOptionSelect"
				@input="handleOptionInput"
			/>
		</view>

		<!-- 价格显示区域（仅在有选择且有费用时显示） -->
		<view class="price-summary" v-if="hasSelections && totalOptionsFee > 0">
			<view class="price-header">
				<text class="price-title">选项费用明细</text>
			</view>
			<view class="price-details">
				<view
					class="price-item"
					v-for="detail in priceDetails"
					:key="detail.option_id"
				>
					<text class="item-name">{{ detail.option_path || detail.option_name }}</text>
					<text class="item-price">+¥{{ formatPrice(detail.calculated_price) }}</text>
				</view>
			</view>
			<view class="price-total">
				<text class="total-label">选项费用小计</text>
				<text class="total-value">¥{{ formatPrice(totalOptionsFee) }}</text>
			</view>
		</view>
	</view>
</template>

<script>
import OptionNode from './OptionNode.vue'

export default {
	name: 'DynamicOptionsForm',
	components: {
		OptionNode
	},
	props: {
		// 选项树数据
		optionsTree: {
			type: Array,
			default: () => []
		},
		// 项目ID（用于价格计算）
		projectId: {
			type: [Number, String],
			required: true
		},
		// 样品数量（用于价格计算）
		sampleCount: {
			type: Number,
			default: 1
		},
		// 已保存的选项，用于编辑样品组时回显
		initialSelections: {
			type: Array,
			default: () => []
		}
	},
	data() {
		return {
			// 用户选择的选项 { option_id: { selected: true, input_value: '' } }
			selections: {},
			// 价格明细
			priceDetails: [],
			// 选项总费用
			totalOptionsFee: 0,
			// 计算定时器（防抖）
			calculateTimer: null
		}
	},
	computed: {
		// 按 group_name 分组的选项
		groupedOptions() {
			const groups = {}
			this.optionsTree.forEach(option => {
				if (option.group_name) {
					if (!groups[option.group_name]) {
						groups[option.group_name] = []
					}
					groups[option.group_name].push(option)
				}
			})
			return groups
		},
		groupedOptionsKeys() {
			return Object.keys(this.groupedOptions)
		},
		// 未分组的选项
		ungroupedOptions() {
			return this.optionsTree.filter(option => !option.group_name)
		},
		// 是否有选择
		hasSelections() {
			return Object.keys(this.selections).some(id => {
				const sel = this.selections[id]
				return sel && (sel.selected || sel.input_value || this.normalizeInputValues(sel).length > 0)
			})
		},
		// 格式化的选项选择列表（用于提交）
		formattedSelections() {
			const result = []
			for (const [optionId, data] of Object.entries(this.selections)) {
				if (data.selected || data.input_value || this.normalizeInputValues(data).length > 0) {
					const inputValues = this.normalizeInputValues(data)
					const inputMode = data.input_mode || (inputValues.length > 1 ? 'multiple' : 'single')
					const inputValue = inputMode === 'multiple'
						? (inputValues.length > 0 ? JSON.stringify(inputValues) : null)
						: (data.input_value || inputValues[0] || null)
					const item = {
						option_id: parseInt(optionId),
						input_value: inputValue,
						input_mode: inputMode
					}
					if (inputValues.length > 0) {
						item.input_values = inputValues
					}
					result.push(item)
				}
			}
			return result
		}
	},
	watch: {
		sampleCount() {
			this.debouncedCalculate()
		},
		optionsTree: {
			handler() {
				// 选项树变化时按已保存选项回显
				this.applyInitialSelections()
				this.priceDetails = []
				this.totalOptionsFee = 0
			},
			deep: true
		},
		initialSelections: {
			handler() {
				this.applyInitialSelections()
			},
			deep: true
		}
	},
	created() {
		this.applyInitialSelections()
	},
	methods: {
		optionRequiresInput(option) {
			return !!(option && (option.requires_input || option.option_type === 'input'))
		},

		optionAllowsChildren(option) {
			return !!(option && option.allow_children !== false)
		},

		optionIsGroupControl(option) {
			return !!(option && ['dropdown', 'checkbox_group', 'radio_group'].includes(option.option_type))
		},

		getOptionInputMode(option, fallback = 'single') {
			const mode = (option && option.input_mode) || fallback || 'single'
			return ['multiple', 'multi'].includes(mode) ? 'multiple' : 'single'
		},

		normalizeInputValues(data) {
			if (!data) return []
			if (Array.isArray(data.input_values)) {
				return data.input_values.map(value => `${value}`.trim()).filter(Boolean)
			}
			if (typeof data.input_value === 'string' && data.input_value.trim()) {
				const raw = data.input_value.trim()
				if (raw.startsWith('[')) {
					try {
						const parsed = JSON.parse(raw)
						if (Array.isArray(parsed)) {
							return parsed.map(value => `${value}`.trim()).filter(Boolean)
						}
					} catch (e) {
						// 兼容旧的普通字符串输入
					}
				}
				return [raw]
			}
			return []
		},

		createSelection(option, overrides = {}) {
			const inputMode = this.getOptionInputMode(option, overrides.input_mode)
			return {
				selected: false,
				input_value: '',
				input_values: inputMode === 'multiple' ? [''] : [],
				input_mode: inputMode,
				...overrides
			}
		},

		ensureSelection(option) {
			const optionId = option.id
			if (!this.selections[optionId]) {
				this.selections[optionId] = this.createSelection(option)
			}
			return this.selections[optionId]
		},

		applyInitialSelections() {
			const nextSelections = {}
			;(this.initialSelections || []).forEach(item => {
				const optionId = item.option_id || item.optionId || item.id
				if (!optionId) return

				const inputValues = this.normalizeInputValues(item)
				const inputMode = ['multiple', 'multi'].includes(item.input_mode) || inputValues.length > 1 ? 'multiple' : 'single'
				nextSelections[optionId] = {
					selected: true,
					input_value: inputMode === 'single' ? (item.input_value || inputValues[0] || '') : '',
					input_values: inputMode === 'multiple' ? (inputValues.length ? inputValues : ['']) : inputValues,
					input_mode: inputMode
				}
			})
			this.selections = nextSelections
		},

		// 处理选项选择（单选/多选）
		handleOptionSelect({ option, selected, siblings, isRadioGroup, isCheckboxGroup }) {
			const optionId = option.id
			const optionType = option.option_type

			// 单选类型处理：取消同级其他选项
			// 包括：single 类型、dropdown 类型、radio_group 的子选项
			const isSingleSelect = (optionType === 'single' && !isCheckboxGroup) || optionType === 'dropdown' || isRadioGroup
			if (isSingleSelect && selected && siblings) {
				siblings.forEach(sibling => {
					if (sibling.id !== optionId && this.selections[sibling.id]) {
						this.selections[sibling.id].selected = false
						this.selections[sibling.id].input_value = ''
						this.selections[sibling.id].input_values = []
						// 级联取消子选项
						this.cancelChildSelections(sibling)
					}
				})
			}

			// 设置当前选项
			const selection = this.ensureSelection(option)
			selection.selected = selected
			selection.input_mode = this.getOptionInputMode(option, selection.input_mode)

			// 如果取消选择，级联取消子选项
			if (!selected) {
				selection.input_value = ''
				selection.input_values = []
				this.cancelChildSelections(option)
			} else if (this.optionRequiresInput(option) && selection.input_mode === 'multiple' && (!selection.input_values || !selection.input_values.length)) {
				selection.input_values = ['']
			}

			// 触发价格计算
			this.debouncedCalculate()

			// 通知父组件
			this.emitChange()
		},

		// 处理输入类型选项
		handleOptionInput({ option, value }) {
			const inputMode = this.getOptionInputMode(option, value && value.input_mode)
			const selection = this.ensureSelection(option)

			selection.selected = true
			selection.input_mode = inputMode
			if (value && typeof value === 'object') {
				selection.input_values = Array.isArray(value.input_values) ? value.input_values : []
				selection.input_value = value.input_value || ''
			} else {
				selection.input_value = value || ''
				selection.input_values = value ? [value] : []
			}

			// 触发价格计算
			this.debouncedCalculate()

			// 通知父组件
			this.emitChange()
		},

		// 级联取消子选项
		cancelChildSelections(option) {
			if (option.children && option.children.length > 0) {
				option.children.forEach(child => {
					if (this.selections[child.id]) {
						this.selections[child.id].selected = false
						this.selections[child.id].input_value = ''
						this.selections[child.id].input_values = []
					}
					this.cancelChildSelections(child)
				})
			}
		},

		// 防抖计算价格
		debouncedCalculate() {
			if (this.calculateTimer) {
				clearTimeout(this.calculateTimer)
			}
			this.calculateTimer = setTimeout(() => {
				this.calculatePrice()
			}, 300)
		},

		// 计算价格
		async calculatePrice() {
			if (!this.hasSelections) {
				this.priceDetails = []
				this.totalOptionsFee = 0
				this.emitChange()
				return
			}

			try {
				const api = require('@/utils/api.js').default
				const res = await api.calculateOptionsPrice({
					project_id: this.projectId,
					sample_count: this.sampleCount,
					selections: this.formattedSelections
				})

				if (res.code === 200 && res.data) {
					this.priceDetails = res.data.details || []
					this.totalOptionsFee = res.data.total_options_fee || 0
				}
			} catch (e) {
				console.error('计算选项价格失败', e)
			}

			this.emitChange()
		},

		// 格式化价格
		formatPrice(price) {
			return parseFloat(price || 0).toFixed(2)
		},

		// 通知父组件变化
		emitChange() {
			this.$emit('change', {
				selections: this.formattedSelections,
				totalOptionsFee: this.totalOptionsFee,
				priceDetails: this.priceDetails,
				// 额外返回表单数据（供提交使用）
				formData: this.getFormData()
			})
		},

		// 获取表单数据（将选择转换为键值对形式）
		getFormData() {
			const formData = {}
			
			// 遍历所有选项，收集选中的值
			const collectValues = (options) => {
				options.forEach(option => {
					const sel = this.selections[option.id]

					if (this.optionIsGroupControl(option)) {
						const selectedChildren = (option.children || []).filter(child => {
							const childSelection = this.selections[child.id]
							return childSelection && childSelection.selected
						})
						if (selectedChildren.length > 0) {
							const names = selectedChildren.map(child => child.name)
							formData[option.name] = option.option_type === 'checkbox_group' ? names : names[0]
						}
						selectedChildren.forEach(child => {
							if (child.children && this.optionAllowsChildren(child)) {
								collectValues(child.children)
							}
						})
						return
					}
					
					if (sel && sel.selected) {
						if (this.optionRequiresInput(option)) {
							const inputValues = this.normalizeInputValues(sel)
							formData[option.name] = this.getOptionInputMode(option, sel.input_mode) === 'multiple'
								? inputValues
								: (inputValues[0] || sel.input_value || '')
						} else {
							formData[option.name] = true
						}
					}

					// 递归处理子选项，父节点选中且允许展开时继续向下
					if (option.children && this.optionAllowsChildren(option) && sel && sel.selected) {
						collectValues(option.children)
					}
				})
			}

			collectValues(this.optionsTree)
			return formData
		},

		// 重置选择
		reset() {
			this.selections = {}
			this.priceDetails = []
			this.totalOptionsFee = 0
			this.emitChange()
		},

		// 获取选择数据（供父组件调用）
		getSelections() {
			return this.formattedSelections
		},

		// 验证必填项
		validate() {
			const errors = []
			
			const checkRequired = (options) => {
				options.forEach(option => {
					const sel = this.selections[option.id]
					if (option.is_required) {
						if (this.optionIsGroupControl(option)) {
							const hasSelectedChild = (option.children || []).some(child => {
								const childSelection = this.selections[child.id]
								return childSelection && childSelection.selected
							})
							if (!hasSelectedChild) {
								errors.push(`请选择${option.name}`)
							}
						} else if (!sel || !sel.selected) {
							errors.push(`请选择${option.name}`)
						} else if (this.optionRequiresInput(option)) {
							if (this.normalizeInputValues(sel).length === 0) {
								errors.push(`请填写${option.name}`)
							}
						}
					}

					// 递归检查子选项（仅当父选项已选中时）
					if (this.optionIsGroupControl(option)) {
						;(option.children || []).forEach(child => {
							const childSelection = this.selections[child.id]
							if (childSelection && childSelection.selected && child.children && this.optionAllowsChildren(child)) {
								checkRequired(child.children)
							}
						})
					} else if (option.children && this.optionAllowsChildren(option) && sel && sel.selected) {
						checkRequired(option.children)
					}
				})
			}

			checkRequired(this.optionsTree)
			return errors
		}
	}
}
</script>

<style lang="scss" scoped>
.dynamic-options-form {
	background: #fff;
}

/* 分组样式 */
.options-group {
	margin-bottom: 20rpx;
	background: #fff;

	.group-header {
		padding: 30rpx 30rpx 0;

		.group-title {
			font-size: 32rpx;
			font-weight: bold;
			color: #333;
			position: relative;
			padding-left: 20rpx;

			&::before {
				content: '';
				position: absolute;
				left: 0;
				top: 50%;
				transform: translateY(-50%);
				width: 6rpx;
				height: 32rpx;
				background: #4facfe;
				border-radius: 3rpx;
			}
		}
	}

	.group-content {
		padding: 20rpx 30rpx;
	}
}

/* 未分组选项区块样式 */
.options-section {
	padding: 30rpx;
	background: #fff;
	margin-bottom: 20rpx;

	.section-title {
		display: flex;
		justify-content: space-between;
		align-items: center;
		font-size: 30rpx;
		font-weight: bold;
		margin-bottom: 20rpx;

		.section-tip {
			font-size: 24rpx;
			font-weight: normal;
			color: #999;
		}
	}
}

/* 价格汇总区域 */
.price-summary {
	padding: 30rpx;
	border-top: 1rpx solid #f0f0f0;
	background: #fafafa;

	.price-header {
		margin-bottom: 20rpx;

		.price-title {
			font-size: 28rpx;
			font-weight: bold;
			color: #333;
		}
	}

	.price-details {
		margin-bottom: 20rpx;

		.price-item {
			display: flex;
			justify-content: space-between;
			align-items: center;
			padding: 15rpx 0;
			border-bottom: 1rpx dashed #e0e0e0;

			&:last-child {
				border-bottom: none;
			}

			.item-name {
				font-size: 26rpx;
				color: #666;
				flex: 1;
				margin-right: 20rpx;
			}

			.item-price {
				font-size: 26rpx;
				color: #ff6b6b;
			}
		}
	}

	.price-total {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding-top: 20rpx;
		border-top: 2rpx solid #e0e0e0;

		.total-label {
			font-size: 28rpx;
			font-weight: bold;
			color: #333;
		}

		.total-value {
			font-size: 32rpx;
			font-weight: bold;
			color: #ff6b6b;
		}
	}
}
</style>

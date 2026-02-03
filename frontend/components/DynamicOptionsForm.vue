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
				<text>检测选项</text>
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
		// 未分组的选项
		ungroupedOptions() {
			return this.optionsTree.filter(option => !option.group_name)
		},
		// 是否有选择
		hasSelections() {
			return Object.keys(this.selections).some(id => {
				const sel = this.selections[id]
				return sel && (sel.selected || sel.input_value)
			})
		},
		// 格式化的选项选择列表（用于提交）
		formattedSelections() {
			const result = []
			for (const [optionId, data] of Object.entries(this.selections)) {
				if (data.selected || data.input_value) {
					result.push({
						option_id: parseInt(optionId),
						input_value: data.input_value || null
					})
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
				// 选项树变化时重置选择
				this.selections = {}
				this.priceDetails = []
				this.totalOptionsFee = 0
			},
			deep: true
		}
	},
	methods: {
		// 处理选项选择（单选/多选）
		handleOptionSelect({ option, selected, siblings, isRadioGroup }) {
			const optionId = option.id
			const optionType = option.option_type

			// 单选类型处理：取消同级其他选项
			// 包括：single 类型、dropdown 类型、radio_group 的子选项
			const isSingleSelect = optionType === 'single' || optionType === 'dropdown' || isRadioGroup
			if (isSingleSelect && selected && siblings) {
				siblings.forEach(sibling => {
					if (sibling.id !== optionId && this.selections[sibling.id]) {
						this.selections[sibling.id].selected = false
						// 级联取消子选项
						this.cancelChildSelections(sibling)
					}
				})
			}

			// 设置当前选项
			if (!this.selections[optionId]) {
				this.$set(this.selections, optionId, { selected: false, input_value: '' })
			}
			this.selections[optionId].selected = selected

			// 如果取消选择，级联取消子选项
			if (!selected) {
				this.cancelChildSelections(option)
			}

			// 触发价格计算
			this.debouncedCalculate()

			// 通知父组件
			this.emitChange()
		},

		// 处理输入类型选项
		handleOptionInput({ option, value }) {
			const optionId = option.id

			if (!this.selections[optionId]) {
				this.$set(this.selections, optionId, { selected: true, input_value: '' })
			}
			this.selections[optionId].selected = !!value
			this.selections[optionId].input_value = value

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
					option_selections: this.formattedSelections
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
					
					if (option.option_type === 'input' && sel && sel.input_value) {
						// 输入类型：直接取值
						formData[option.name] = sel.input_value
					} else if (option.option_type === 'dropdown' && option.children) {
						// 下拉类型：找到选中的子选项
						const selectedChild = option.children.find(c => {
							const cSel = this.selections[c.id]
							return cSel && cSel.selected
						})
						if (selectedChild) {
							formData[option.name] = selectedChild.name
						}
					} else if (option.option_type === 'radio_group' && option.children) {
						// 单选组：找到选中的子选项
						const selectedChild = option.children.find(c => {
							const cSel = this.selections[c.id]
							return cSel && cSel.selected
						})
						if (selectedChild) {
							formData[option.name] = selectedChild.name
						}
					} else if (option.option_type === 'checkbox_group' && option.children) {
						// 复选框组：收集所有选中的子选项
						const selectedChildren = option.children.filter(c => {
							const cSel = this.selections[c.id]
							return cSel && cSel.selected
						})
						if (selectedChildren.length > 0) {
							formData[option.name] = selectedChildren.map(c => c.name)
						}
					} else if (sel && sel.selected) {
						// 卡片式单选/多选
						formData[option.name] = true
					}

					// 递归处理子选项
					if (option.children && ['single', 'multi'].includes(option.option_type)) {
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
					if (option.is_required) {
						const sel = this.selections[option.id]
						
						if (option.option_type === 'input') {
							if (!sel || !sel.input_value) {
								errors.push(`请填写${option.name}`)
							}
						} else if (['dropdown', 'radio_group'].includes(option.option_type)) {
							// 检查是否有子选项被选中
							const hasSelected = option.children && option.children.some(c => {
								const cSel = this.selections[c.id]
								return cSel && cSel.selected
							})
							if (!hasSelected) {
								errors.push(`请选择${option.name}`)
							}
						} else if (option.option_type === 'checkbox_group') {
							// 复选框组：至少选一个
							const hasSelected = option.children && option.children.some(c => {
								const cSel = this.selections[c.id]
								return cSel && cSel.selected
							})
							if (!hasSelected) {
								errors.push(`请选择${option.name}`)
							}
						} else {
							// 卡片式
							if (!sel || !sel.selected) {
								errors.push(`请选择${option.name}`)
							}
						}
					}

					// 递归检查子选项（仅当父选项已选中时）
					if (option.children && ['single', 'multi'].includes(option.option_type)) {
						const sel = this.selections[option.id]
						if (sel && sel.selected) {
							checkRequired(option.children)
						}
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

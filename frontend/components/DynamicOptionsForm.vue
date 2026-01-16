<template>
	<view class="dynamic-options-form" v-if="optionsTree && optionsTree.length > 0">
		<view class="options-section">
			<view class="section-title">
				<text>检测选项</text>
				<text class="section-tip" v-if="!hasSelections">请选择检测选项</text>
			</view>

			<!-- 递归渲染选项树 -->
			<option-node
				v-for="option in optionsTree"
				:key="option.id"
				:option="option"
				:selections="selections"
				:level="0"
				@select="handleOptionSelect"
				@input="handleOptionInput"
			/>
		</view>

		<!-- 价格显示区域（仅在有选择时显示） -->
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
					<text class="item-name">{{ detail.option_path }}</text>
					<text class="item-price">+¥{{ detail.calculated_price.toFixed(2) }}</text>
				</view>
			</view>
			<view class="price-total">
				<text class="total-label">选项费用小计</text>
				<text class="total-value">¥{{ totalOptionsFee.toFixed(2) }}</text>
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
		// 是否有选择
		hasSelections() {
			return Object.keys(this.selections).some(id => this.selections[id].selected)
		},
		// 格式化的选项选择列表（用于提交）
		formattedSelections() {
			const result = []
			for (const [optionId, data] of Object.entries(this.selections)) {
				if (data.selected) {
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
		}
	},
	methods: {
		// 处理选项选择（单选/多选）
		handleOptionSelect({ option, selected, siblings }) {
			const optionId = option.id
			const optionType = option.option_type

			// 单选处理：取消同级其他选项
			if (optionType === 'single' && selected && siblings) {
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
			this.selections[optionId].selected = true
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

		// 通知父组件变化
		emitChange() {
			this.$emit('change', {
				selections: this.formattedSelections,
				totalOptionsFee: this.totalOptionsFee,
				priceDetails: this.priceDetails
			})
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
		}
	}
}
</script>

<style lang="scss" scoped>
.dynamic-options-form {
	background: #fff;
	margin-bottom: 20rpx;
}

.options-section {
	padding: 30rpx;

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

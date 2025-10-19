<template>
	<view class="booking-container">
		<!-- 顶部步骤条 -->
		<view class="steps">
			<view class="step" :class="{ active: currentStep >= 1 }">
				<view class="step-number">01</view>
				<view class="step-text">填写样品信息</view>
			</view>
			<view class="step" :class="{ active: currentStep >= 2 }">
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
		<view class="current-step-dropdown" @click="showStepMenu = !showStepMenu">
			<text>填写样品信息</text>
			<text class="arrow">▼</text>
		</view>
		
		<!-- 表单内容 - 步骤1：样品信息 -->
		<view class="form-container" v-if="currentStep === 1">
			<!-- 样品信息 -->
			<view class="form-section">
				<view class="section-title">样品信息</view>
				
				<!-- 样品数量 -->
				<view class="form-item">
					<text class="label">样品数量</text>
					<view class="quantity-control">
						<button class="btn-minus" @click="decreaseSampleCount">-</button>
						<input class="quantity-input" type="number" v-model.number="formData.sampleCount" />
						<button class="btn-plus" @click="increaseSampleCount">+</button>
					</view>
				</view>
				
				<!-- 样品编号 -->
				<view class="form-item">
					<text class="label">样品编号</text>
					<text class="value">{{ formData.sampleCount }}</text>
				</view>
				
				<!-- 样品名称 -->
				<view class="form-item">
					<text class="label">样品名称</text>
					<input class="input" placeholder="请输入样品名称" v-model="formData.sampleName" />
				</view>
				
				<!-- 样品成分 -->
				<view class="form-item">
					<text class="label">样品成分</text>
					<input class="input" placeholder="请输入样品成分" v-model="formData.sampleComposition" />
				</view>
				
				<!-- 样品状态 -->
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
				
				<!-- 危险性 -->
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
			
			<!-- 存放要求 -->
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
			
			<!-- 测试信息 -->
			<view class="form-section">
				<view class="section-title">测试信息</view>
				
				<!-- 数据格式 -->
				<view class="form-item column">
					<text class="label">数据格式</text>
					<view class="tips">*该项目需ODF函数需满足3个测试晶面以上支持测量</view>
					<view class="options">
						<view 
							class="option-btn" 
							:class="{ active: formData.dataFormat === item }"
							v-for="item in dataFormats" 
							:key="item"
							@click="formData.dataFormat = item"
						>
							{{ item }}
						</view>
					</view>
				</view>
				
				<!-- 晶体结构 -->
				<view class="form-item column">
					<text class="label">晶体结构</text>
					<view class="options">
						<view 
							class="option-btn" 
							:class="{ active: formData.crystalStructure === item }"
							v-for="item in crystalStructures" 
							:key="item"
							@click="formData.crystalStructure = item"
						>
							{{ item }}
						</view>
					</view>
				</view>
				
				<!-- 测试晶面 -->
				<view class="form-item column">
					<text class="label">测试晶面</text>
					<view class="tips">*立方晶系3个晶面，请输入六方晶系需4个及以上晶面</view>
					<view class="options">
						<view 
							class="option-btn" 
							:class="{ active: formData.testSurfaceCount === item }"
							v-for="item in testSurfaceCounts" 
							:key="item"
							@click="formData.testSurfaceCount = item"
						>
							{{ item }}个
						</view>
					</view>
					<view class="sub-tips">其他，请联系技术顾问</view>
				</view>
			</view>
			
			<!-- 晶面位置 -->
			<view class="form-section">
				<view class="section-title">晶面位置</view>
				<view class="tips">*需要强调特定晶面？如1100，200，2200，三个晶面测试所需晶体的200晶面</view>
				<input class="input-area" placeholder="请输入晶面位置" v-model="formData.surfacePosition" />
			</view>
			
			<!-- 轧制方向 -->
			<view class="form-section">
				<view class="section-title">轧制方向</view>
				<input class="input-area" placeholder="请输入轧制方向" v-model="formData.rollingDirection" />
			</view>
			
			<!-- 备注 -->
			<view class="form-section">
				<view class="section-title">备注</view>
				<view class="tips">*包括轧制机料等要求，或请勾选非原创性作假或谎报测试信息，将会影响最终数据精度</view>
				<textarea class="textarea" placeholder="请输入备注" v-model="formData.remark" />
			</view>
			
			<!-- 附件 -->
			<view class="form-section">
				<view class="section-title">附件</view>
				<view class="tips red">包括背景、景品</view>
				<view class="upload-area" @click="chooseFile">
					<image class="upload-icon" src="/static/upload-icon.png" mode="aspectFit" />
					<text class="upload-text">上传</text>
				</view>
				<view class="file-list" v-if="formData.files.length > 0">
					<view class="file-item" v-for="(file, index) in formData.files" :key="index">
						<text class="file-name">{{ file.name }}</text>
						<text class="file-remove" @click="removeFile(index)">删除</text>
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
				<text class="fee-tips" @click="showFeeTips">费用说明</text>
				<button class="btn-draft" @click="saveDraft">存为草稿</button>
				<button class="btn-next" @click="nextStep">下一步</button>
			</view>
		</view>
	</view>
</template>

<script>
export default {
	data() {
		return {
			projectId: null,
			projectName: 'XRD织构测试',
			currentStep: 1,
			showStepMenu: false,
			totalPrice: 0.00,
			
			// 表单选项
			sampleStates: ['粉末', '块状/薄膜', '溶液', '气体', '其它'],
			dangerTypes: ['普通', '易燃', '氧化性', '放射性', '腐蚀性', '有毒', '无'],
			storageRequirements: ['冷藏', '干燥', '避光', '真空', '其它', '无'],
			dataFormats: ['包图', '反应图', 'ODF函数'],
			crystalStructures: ['面心立方', '体心立方', '密排六方'],
			testSurfaceCounts: [1, 2, 3, 4],
			
			// 表单数据
			formData: {
				sampleCount: 1,
				sampleName: '',
				sampleComposition: '',
				sampleState: '',
				dangerType: '',
				storageRequirement: '',
				dataFormat: '',
				crystalStructure: '',
				testSurfaceCount: null,
				surfacePosition: '',
				rollingDirection: '',
				remark: '',
				files: []
			}
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
	},
	methods: {
		// 加载项目信息
		async loadProjectInfo() {
			// TODO: 从API加载项目详情和价格
			this.totalPrice = 0.00
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
		
		// 文件上传
		chooseFile() {
			uni.chooseImage({
				count: 9,
				success: (res) => {
					res.tempFilePaths.forEach((path, index) => {
						this.formData.files.push({
							name: `文件${this.formData.files.length + 1}`,
							path: path
						})
					})
				}
			})
		},
		
		// 删除文件
		removeFile(index) {
			this.formData.files.splice(index, 1)
		},
		
		// 费用说明
		showFeeTips() {
			uni.showModal({
				title: '费用说明',
				content: '费用根据样品数量、测试项目等因素计算',
				showCancel: false
			})
		},
		
		// 存为草稿
		saveDraft() {
			uni.setStorageSync('booking_draft', this.formData)
			uni.showToast({
				title: '已保存为草稿',
				icon: 'success'
			})
		},
		
		// 下一步
		nextStep() {
			// 验证表单
			if (!this.formData.sampleName) {
				uni.showToast({
					title: '请输入样品名称',
					icon: 'none'
				})
				return
			}
			
			// TODO: 进入步骤2
			this.currentStep = 2
			uni.showToast({
				title: '步骤2开发中',
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
	padding-bottom: 180rpx;
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
		
		&.red {
			color: #ff0000;
		}
	}
	
	.sub-tips {
		font-size: 22rpx;
		color: #999;
		margin-top: 15rpx;
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
	}
}

/* 输入框 */
.input-area {
	width: 100%;
	padding: 20rpx;
	background: #f5f5f5;
	border-radius: 8rpx;
	font-size: 28rpx;
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

/* 上传区域 */
.upload-area {
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	width: 150rpx;
	height: 150rpx;
	background: #f5f5f5;
	border-radius: 8rpx;
	margin-top: 20rpx;
	
	.upload-icon {
		width: 60rpx;
		height: 60rpx;
		margin-bottom: 10rpx;
	}
	
	.upload-text {
		font-size: 24rpx;
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
		padding: 15rpx 0;
		border-bottom: 1rpx solid #f0f0f0;
		
		.file-name {
			font-size: 26rpx;
			color: #666;
		}
		
		.file-remove {
			font-size: 24rpx;
			color: #ff6b6b;
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
		gap: 20rpx;
		
		.fee-tips {
			font-size: 24rpx;
			color: #4facfe;
			text-decoration: underline;
		}
		
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
		
		.btn-draft {
			background: #f0f0f0;
			color: #666;
		}
		
		.btn-next {
			background: #4facfe;
			color: white;
		}
	}
}
</style>


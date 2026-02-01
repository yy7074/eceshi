<template>
	<view class="search-page">
		<!-- 搜索框 -->
		<view class="search-bar">
			<view class="search-input-wrapper">
				<text class="search-icon">🔍</text>
				<input 
					v-model="keyword"
					class="search-input"
					placeholder="搜索检测项目"
					confirm-type="search"
					@confirm="handleSearch"
					:focus="true"
				/>
				<text v-if="keyword" class="clear-icon" @click="clearKeyword">×</text>
			</view>
			<text class="cancel-btn" @click="goBack">取消</text>
		</view>
		
		<!-- 搜索结果 -->
		<view v-if="showResults" class="search-results">
			<view v-if="results.length > 0" class="results-list">
				<view class="results-header">
					<text class="results-count">找到 {{ total }} 个相关项目</text>
					<view class="sort-btn" @click="showSortMenu">
						<text>{{ sortOptions[currentSort].label }}</text>
						<text class="arrow">▼</text>
					</view>
				</view>
				<view v-for="(item, index) in results" :key="index" class="result-item" @click="goProjectDetail(item.id)">
					<image :src="item.cover_image || 'https://picsum.photos/200/200'" mode="aspectFill" class="item-image"></image>
					<view class="item-info">
						<text class="item-name">{{ highlightKeyword(item.name) }}</text>
						<text class="item-lab">{{ item.lab_name }}</text>
						<view class="item-stats">
							<text class="stat">满意度 {{ item.satisfaction }}%</text>
							<text class="stat">已测{{ item.order_count }}次</text>
						</view>
						<view class="item-footer">
							<view class="item-price">
								<text class="current-price">¥{{ item.current_price }}</text>
								<text v-if="item.original_price > item.current_price" class="original-price">¥{{ item.original_price }}</text>
							</view>
						</view>
					</view>
				</view>
			</view>
			
			<!-- 空结果 -->
			<view v-else class="empty-result">
				<text class="empty-icon">🔍</text>
				<text class="empty-text">没有找到相关项目</text>
				<text class="empty-tip">试试其他关键词吧</text>
			</view>
		</view>
		
		<!-- 搜索建议 -->
		<view v-else class="search-suggest">
			<!-- 搜索历史 -->
			<view v-if="history.length > 0" class="suggest-section">
				<view class="section-header">
					<text class="section-title">搜索历史</text>
					<text class="clear-history" @click="clearHistory">清空</text>
				</view>
				<view class="history-list">
					<view 
						v-for="(item, index) in history" 
						:key="index"
						class="history-item"
						@click="searchHistory(item)"
					>
						<text class="history-icon">🕐</text>
						<text class="history-text">{{ item }}</text>
						<text class="delete-icon" @click.stop="deleteHistory(index)">×</text>
					</view>
				</view>
			</view>
			
			<!-- 热门搜索 -->
			<view class="suggest-section">
				<view class="section-header">
					<text class="section-title">热门搜索</text>
				</view>
				<view class="hot-list">
					<view 
						v-for="(item, index) in hotKeywords" 
						:key="index"
						class="hot-item"
						@click="searchHistory(item.keyword)"
					>
						<text :class="['hot-rank', index < 3 ? 'top' : '']">{{ index + 1 }}</text>
						<text class="hot-text">{{ item.keyword }}</text>
						<text v-if="item.hot" class="hot-badge">热</text>
					</view>
				</view>
			</view>
		</view>
	</view>
</template>

<script>
import api from '@/utils/api.js'

export default {
	data() {
		return {
			keyword: '',
			showResults: false,
			results: [],
			total: 0,
			currentSort: 0,
			sortOptions: [
				{ value: 'default', label: '综合排序' },
				{ value: 'price_asc', label: '价格升序' },
				{ value: 'price_desc', label: '价格降序' },
				{ value: 'popularity', label: '人气优先' }
			],
			history: [],
			hotKeywords: [
				{ keyword: '水质检测', hot: true },
				{ keyword: '土壤检测', hot: true },
				{ keyword: '食品检测', hot: true },
				{ keyword: '环境监测', hot: false },
				{ keyword: '材料分析', hot: false },
				{ keyword: 'PCR检测', hot: false },
				{ keyword: '重金属检测', hot: false },
				{ keyword: '微生物检测', hot: false }
			]
		}
	},
	
	onLoad(options) {
		// 从其他页面传入的关键词
		if (options.keyword) {
			this.keyword = options.keyword
			this.handleSearch()
		}
		
		// 加载搜索历史
		this.loadHistory()
	},
	
	methods: {
		// 搜索
		async handleSearch() {
			if (!this.keyword.trim()) {
				uni.showToast({
					title: '请输入搜索关键词',
					icon: 'none'
				})
				return
			}
			
			try {
				uni.showLoading({ title: '搜索中...' })
				
				// 保存到搜索历史
				this.saveHistory(this.keyword)
				
				// 调用API搜索
				const res = await api.getProjects({
					keyword: this.keyword,
					page: 1,
					page_size: 20
				})
				
				// 响应格式: {code, data: {list, total}}
				const data = res.data || res
				this.results = data.items || data.list || []
				this.total = data.total || 0
				this.showResults = true
				
				uni.hideLoading()
			} catch (error) {
				uni.hideLoading()
				console.error('搜索失败', error)
				uni.showToast({
					title: '搜索失败',
					icon: 'none'
				})
			}
		},
		
		// 清空关键词
		clearKeyword() {
			this.keyword = ''
			this.showResults = false
		},
		
		// 高亮关键词
		highlightKeyword(text) {
			// TODO: 实现关键词高亮
			return text
		},
		
		// 显示排序菜单
		showSortMenu() {
			uni.showActionSheet({
				itemList: this.sortOptions.map(item => item.label),
				success: (res) => {
					this.currentSort = res.tapIndex
					this.handleSearch()
				}
			})
		},
		
		// 加载历史
		loadHistory() {
			try {
				const history = uni.getStorageSync('search_history') || []
				this.history = history
			} catch (error) {
				console.error('加载搜索历史失败', error)
			}
		},
		
		// 保存历史
		saveHistory(keyword) {
			try {
				let history = uni.getStorageSync('search_history') || []
				
				// 移除重复项
				history = history.filter(item => item !== keyword)
				
				// 添加到开头
				history.unshift(keyword)
				
				// 最多保留10条
				if (history.length > 10) {
					history = history.slice(0, 10)
				}
				
				uni.setStorageSync('search_history', history)
				this.history = history
			} catch (error) {
				console.error('保存搜索历史失败', error)
			}
		},
		
		// 搜索历史项
		searchHistory(keyword) {
			this.keyword = keyword
			this.handleSearch()
		},
		
		// 删除历史项
		deleteHistory(index) {
			this.history.splice(index, 1)
			uni.setStorageSync('search_history', this.history)
		},
		
		// 清空历史
		clearHistory() {
			uni.showModal({
				title: '提示',
				content: '确定要清空搜索历史吗？',
				success: (res) => {
					if (res.confirm) {
						this.history = []
						uni.removeStorageSync('search_history')
						uni.showToast({
							title: '已清空',
							icon: 'success'
						})
					}
				}
			})
		},
		
		// 跳转项目详情
		goProjectDetail(projectId) {
			uni.navigateTo({
				url: `/pages/project/detail?id=${projectId}`
			})
		},
		
		// 返回
		goBack() {
			uni.navigateBack()
		}
	}
}
</script>

<style lang="scss" scoped>
.search-page {
	min-height: 100vh;
	background: #f5f5f5;
}

.search-bar {
	background: white;
	padding: 20rpx 30rpx;
	display: flex;
	align-items: center;
	position: sticky;
	top: 0;
	z-index: 100;
	
	.search-input-wrapper {
		flex: 1;
		display: flex;
		align-items: center;
		background: #f5f5f5;
		border-radius: 50rpx;
		padding: 15rpx 30rpx;
		margin-right: 20rpx;
		
		.search-icon {
			font-size: 32rpx;
			margin-right: 15rpx;
		}
		
		.search-input {
			flex: 1;
			font-size: 28rpx;
			line-height: 1.5;
		}
		
		.clear-icon {
			font-size: 40rpx;
			color: #999;
			line-height: 1;
		}
	}
	
	.cancel-btn {
		font-size: 28rpx;
		color: #667eea;
	}
}

.search-results {
	.results-list {
		.results-header {
			display: flex;
			justify-content: space-between;
			align-items: center;
			padding: 30rpx;
			background: white;
			margin-bottom: 2rpx;
			
			.results-count {
				font-size: 26rpx;
				color: #999;
			}
			
			.sort-btn {
				display: flex;
				align-items: center;
				font-size: 26rpx;
				color: #666;
				
				.arrow {
					margin-left: 5rpx;
					font-size: 20rpx;
				}
			}
		}
		
		.result-item {
			background: white;
			padding: 20rpx 30rpx;
			margin-bottom: 2rpx;
			display: flex;
			
			.item-image {
				width: 180rpx;
				height: 180rpx;
				border-radius: 12rpx;
				flex-shrink: 0;
				margin-right: 20rpx;
			}
			
			.item-info {
				flex: 1;
				display: flex;
				flex-direction: column;
				justify-content: space-between;
				
				.item-name {
					font-size: 28rpx;
					font-weight: bold;
					color: #333;
					margin-bottom: 10rpx;
					overflow: hidden;
					text-overflow: ellipsis;
					display: -webkit-box;
					-webkit-line-clamp: 2;
					-webkit-box-orient: vertical;
				}
				
				.item-lab {
					font-size: 24rpx;
					color: #999;
					margin-bottom: 10rpx;
				}
				
				.item-stats {
					display: flex;
					gap: 20rpx;
					margin-bottom: 10rpx;
					
					.stat {
						font-size: 22rpx;
						color: #999;
					}
				}
				
				.item-footer {
					.item-price {
						display: flex;
						align-items: baseline;
						gap: 10rpx;
						
						.current-price {
							font-size: 32rpx;
							font-weight: bold;
							color: #ff4444;
						}
						
						.original-price {
							font-size: 24rpx;
							color: #999;
							text-decoration: line-through;
						}
					}
				}
			}
		}
	}
	
	.empty-result {
		display: flex;
		flex-direction: column;
		align-items: center;
		padding: 200rpx 0;
		
		.empty-icon {
			font-size: 120rpx;
			margin-bottom: 30rpx;
			opacity: 0.5;
		}
		
		.empty-text {
			font-size: 28rpx;
			color: #999;
			margin-bottom: 10rpx;
		}
		
		.empty-tip {
			font-size: 24rpx;
			color: #ccc;
		}
	}
}

.search-suggest {
	.suggest-section {
		background: white;
		margin-bottom: 20rpx;
		padding: 30rpx;
		
		.section-header {
			display: flex;
			justify-content: space-between;
			align-items: center;
			margin-bottom: 30rpx;
			
			.section-title {
				font-size: 28rpx;
				font-weight: bold;
				color: #333;
			}
			
			.clear-history {
				font-size: 24rpx;
				color: #999;
			}
		}
		
		.history-list {
			.history-item {
				display: flex;
				align-items: center;
				padding: 25rpx 0;
				border-bottom: 1rpx solid #f5f5f5;
				
				&:last-child {
					border-bottom: none;
				}
				
				.history-icon {
					font-size: 28rpx;
					margin-right: 15rpx;
				}
				
				.history-text {
					flex: 1;
					font-size: 26rpx;
					color: #666;
				}
				
				.delete-icon {
					font-size: 36rpx;
					color: #ccc;
					line-height: 1;
				}
			}
		}
		
		.hot-list {
			.hot-item {
				display: flex;
				align-items: center;
				padding: 25rpx 0;
				border-bottom: 1rpx solid #f5f5f5;
				
				&:last-child {
					border-bottom: none;
				}
				
				.hot-rank {
					width: 40rpx;
					text-align: center;
					font-size: 24rpx;
					color: #999;
					margin-right: 15rpx;
					
					&.top {
						color: #ff4444;
						font-weight: bold;
					}
				}
				
				.hot-text {
					flex: 1;
					font-size: 26rpx;
					color: #666;
				}
				
				.hot-badge {
					font-size: 20rpx;
					color: #ff4444;
					border: 1rpx solid #ff4444;
					border-radius: 4rpx;
					padding: 2rpx 8rpx;
				}
			}
		}
	}
}
</style>


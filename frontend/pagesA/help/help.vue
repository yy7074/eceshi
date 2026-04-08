<template>
	<view class="help-page">
		<!-- 搜索栏 -->
		<view class="search-bar">
			<view class="search-input">
				<text class="search-icon">🔍</text>
				<input type="text" v-model="searchKeyword" placeholder="搜索问题" @confirm="searchArticles" />
			</view>
		</view>
		
		<!-- 快捷问题 -->
		<view class="quick-questions">
			<view class="quick-item" v-for="(q, index) in quickQuestions" :key="index" @click="showAnswer(q)">
				<text class="question-text">{{ q.title }}</text>
				<text class="arrow">›</text>
			</view>
		</view>
		
		<!-- 分类列表 -->
		<view class="category-section">
			<view class="section-title">常见问题分类</view>
			<view class="category-grid">
				<view class="category-item" v-for="cat in categories" :key="cat.id" @click="selectCategory(cat)">
					<view class="category-icon" :style="{ background: cat.color }">
						<text>{{ cat.icon }}</text>
					</view>
					<text class="category-name">{{ cat.name }}</text>
				</view>
			</view>
		</view>
		
		<!-- 问题列表 -->
		<view class="article-section" v-if="activeCategory">
			<view class="section-title">{{ activeCategory.name }}</view>
			<view class="article-list">
				<view class="article-item" v-for="article in articles" :key="article.id" @click="showAnswer(article)">
					<text class="article-title">{{ article.title }}</text>
					<text class="arrow">›</text>
				</view>
			</view>
		</view>
		
		<!-- 联系客服 -->
		<view class="contact-section">
			<view class="contact-card" @click="goChat">
				<view class="contact-icon">💬</view>
				<view class="contact-info">
					<text class="contact-title">在线客服</text>
					<text class="contact-desc">工作时间：9:00-18:00</text>
				</view>
				<text class="arrow">›</text>
			</view>
			<view class="contact-card" @click="callPhone">
				<view class="contact-icon">📞</view>
				<view class="contact-info">
					<text class="contact-title">电话咨询</text>
					<text class="contact-desc">400-123-4567</text>
				</view>
				<text class="arrow">›</text>
			</view>
		</view>
	</view>
</template>

<script>
import api from '@/utils/api.js'

export default {
	data() {
		return {
			searchKeyword: '',
			activeCategory: null,
			categories: [],
			quickQuestions: [
				{ id: 1, title: '如何注册账号？', content: '点击登录页面，输入手机号获取验证码即可完成注册。' },
				{ id: 2, title: '如何下单检测？', content: '选择检测项目后，点击"立即预约"，填写样品信息并支付即可。' },
				{ id: 3, title: '检测周期多久？', content: '常规检测3-5个工作日，具体以项目详情页显示为准。' },
				{ id: 4, title: '如何获取检测报告？', content: '检测完成后，可在"订单详情"中下载电子版报告。' }
			],
			articles: [],
			loading: false
		}
	},
	onLoad() {
		this.loadCategories()
		this.loadHotArticles()
	},
	methods: {
		async loadCategories() {
			try {
				const res = await api.getHelpCategories()
				this.categories = (res.data?.items || []).map((cat, index) => ({
					id: cat.id,
					name: cat.name,
					icon: cat.icon || '❓',
					color: ['#e6f7ff', '#fff7e6', '#f6ffed', '#fff0f6', '#f9f0ff', '#e6fffb', '#fffbe6', '#f5f5f5'][index % 8]
				}))
			} catch (e) {
				console.error('加载帮助分类失败', e)
			}
		},
		async loadHotArticles() {
			try {
				const res = await api.getHelpArticles({ is_hot: true, page: 1, page_size: 10 })
				this.articles = (res.data?.items || []).map(item => ({
					id: item.id,
					title: item.title,
					content: item.content || ''
				}))
			} catch (e) {
				console.error('加载帮助文章失败', e)
			}
		},
		async searchArticles() {
			if (!this.searchKeyword.trim()) return
			try {
				this.loading = true
				const res = await api.getHelpArticles({ keyword: this.searchKeyword.trim(), page: 1, page_size: 20 })
				this.articles = (res.data?.items || []).map(item => ({
					id: item.id,
					title: item.title,
					content: item.content || ''
				}))
				this.activeCategory = { name: `搜索结果：${this.searchKeyword.trim()}` }
			} catch (e) {
				uni.showToast({ title: '搜索失败', icon: 'none' })
			} finally {
				this.loading = false
			}
		},
		async selectCategory(cat) {
			this.activeCategory = cat
			try {
				const res = await api.getHelpArticles({ category_id: cat.id, page: 1, page_size: 20 })
				this.articles = (res.data?.items || []).map(item => ({
					id: item.id,
					title: item.title,
					content: item.content || ''
				}))
			} catch (e) {
				uni.showToast({ title: '加载失败', icon: 'none' })
			}
		},
		async showAnswer(item) {
			try {
				const res = await api.getHelpArticleDetail(item.id)
				const detail = res.data || item
				uni.showModal({
					title: detail.title,
					content: detail.content,
					showCancel: false,
					confirmText: '我知道了'
				})
			} catch (e) {
				uni.showModal({
					title: item.title,
					content: item.content,
					showCancel: false,
					confirmText: '我知道了'
				})
			}
		},
		goChat() {
			uni.navigateTo({ url: '/pagesA/chat/chat' })
		},
		callPhone() {
			uni.makePhoneCall({ phoneNumber: '400-123-4567' })
		}
	}
}
</script>

<style lang="scss" scoped>
.help-page {
	min-height: 100vh;
	background: #f5f5f5;
	padding-bottom: 40rpx;
}

.search-bar {
	background: #fff;
	padding: 20rpx 24rpx;
	
	.search-input {
		display: flex;
		align-items: center;
		background: #f5f5f5;
		border-radius: 8rpx;
		padding: 16rpx 24rpx;
		
		.search-icon {
			font-size: 28rpx;
			margin-right: 12rpx;
		}
		
		input {
			flex: 1;
			font-size: 28rpx;
		}
	}
}

.quick-questions {
	background: #fff;
	margin: 16rpx 24rpx;
	border-radius: 12rpx;
	
	.quick-item {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 28rpx 24rpx;
		border-bottom: 1rpx solid #f0f0f0;
		
		&:last-child {
			border-bottom: none;
		}
		
		.question-text {
			font-size: 28rpx;
			color: #333;
		}
		
		.arrow {
			font-size: 32rpx;
			color: #ccc;
		}
	}
}

.category-section, .article-section {
	background: #fff;
	margin: 16rpx 24rpx;
	border-radius: 12rpx;
	padding: 24rpx;
	
	.section-title {
		font-size: 30rpx;
		font-weight: 600;
		color: #333;
		margin-bottom: 24rpx;
	}
}

.category-grid {
	display: grid;
	grid-template-columns: repeat(4, 1fr);
	gap: 24rpx;
	
	.category-item {
		display: flex;
		flex-direction: column;
		align-items: center;
		
		.category-icon {
			width: 88rpx;
			height: 88rpx;
			border-radius: 16rpx;
			display: flex;
			align-items: center;
			justify-content: center;
			font-size: 40rpx;
			margin-bottom: 12rpx;
		}
		
		.category-name {
			font-size: 24rpx;
			color: #666;
		}
	}
}

.article-list {
	.article-item {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 24rpx 0;
		border-bottom: 1rpx solid #f0f0f0;
		
		&:last-child {
			border-bottom: none;
		}
		
		.article-title {
			font-size: 28rpx;
			color: #333;
		}
		
		.arrow {
			font-size: 32rpx;
			color: #ccc;
		}
	}
}

.contact-section {
	margin: 16rpx 24rpx;
	
	.contact-card {
		display: flex;
		align-items: center;
		background: #fff;
		padding: 28rpx 24rpx;
		border-radius: 12rpx;
		margin-bottom: 16rpx;
		
		.contact-icon {
			font-size: 48rpx;
			margin-right: 20rpx;
		}
		
		.contact-info {
			flex: 1;
			
			.contact-title {
				display: block;
				font-size: 30rpx;
				font-weight: 500;
				color: #333;
				margin-bottom: 4rpx;
			}
			
			.contact-desc {
				font-size: 24rpx;
				color: #999;
			}
		}
		
		.arrow {
			font-size: 32rpx;
			color: #ccc;
		}
	}
}
</style>

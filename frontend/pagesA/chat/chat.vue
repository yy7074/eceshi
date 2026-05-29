<template>
	<view class="chat-page">
		<!-- 客服状态栏 -->
		<view class="status-bar">
			<view class="status-indicator online"></view>
			<text class="status-text">客服在线</text>
			<text class="work-time">工作时间：9:00-18:00</text>
		</view>
		
		<!-- 消息列表 -->
		<scroll-view class="message-list" scroll-y :scroll-top="scrollTop" @scrolltoupper="loadMore">
			<view class="message-item" v-for="msg in messages" :key="msg.id" :class="{ 'user-msg': msg.isUser }">
				<view class="avatar" v-if="!msg.isUser">
					<text>客</text>
				</view>
				<view class="message-bubble">
					<text class="message-text">{{ msg.content }}</text>
					<text class="message-time">{{ msg.time }}</text>
				</view>
				<view class="avatar user-avatar" v-if="msg.isUser">
					<text>我</text>
				</view>
			</view>
		</scroll-view>
		
		<!-- 快捷问题 -->
		<view class="quick-questions">
			<scroll-view scroll-x class="quick-scroll">
				<view class="quick-item" v-for="(q, index) in quickQuestions" :key="index" @click="sendQuickQuestion(q)">
					{{ q }}
				</view>
			</scroll-view>
		</view>
		
		<!-- 输入区域 -->
		<view class="input-area">
			<view class="input-wrapper">
				<input 
					type="text" 
					v-model="inputText" 
					placeholder="请输入您的问题..."
					@confirm="sendMessage"
					:adjust-position="true"
				/>
			</view>
			<view class="send-btn" :class="{ active: inputText.trim() }" @click="sendMessage">
				发送
			</view>
		</view>
	</view>
</template>

<script>
import api from '@/utils/api.js'

export default {
	data() {
		return {
			messages: [
				{
					id: 1,
					content: '您好！欢迎咨询博才科研百测，请直接描述您的问题。',
					isUser: false,
					time: '刚刚'
				}
			],
			inputText: '',
			scrollTop: 0,
			sessionId: null,
			sending: false,
			pollTimer: null,
			quickQuestions: [
				'如何下单？',
				'检测周期多久？',
				'如何获取报告？',
				'发票问题',
				'优惠活动',
				'退款问题'
			]
		}
	},
	async onLoad() {
		await this.loadSession()
		await this.loadHistory()
		this.startPolling()
	},
	onShow() {
		this.startPolling()
	},
	onHide() {
		this.stopPolling()
	},
	onUnload() {
		this.stopPolling()
	},
	methods: {
		startPolling() {
			if (this.pollTimer) return
			this.pollTimer = setInterval(() => {
				this.loadHistory(false)
			}, 5000)
		},

		stopPolling() {
			if (this.pollTimer) {
				clearInterval(this.pollTimer)
				this.pollTimer = null
			}
		},

		async loadSession() {
			try {
				const res = await api.getChatSession()
				this.sessionId = res.data?.session_id || null
			} catch (e) {
				console.error('获取会话失败', e)
			}
		},

		async loadHistory(scroll = true) {
			try {
				const res = await api.getChatHistory()
				const items = res.data?.items || []
				if (items.length > 0) {
					this.messages = items.map(item => ({
						id: item.id,
						content: item.content,
						isUser: item.sender_type === 'user',
						time: (item.created_at || '').slice(11, 16) || '刚刚'
					}))
				}
				if (scroll) this.scrollToBottom()
			} catch (e) {
				console.error('加载聊天记录失败', e)
			}
		},

		async sendMessage() {
			if (!this.inputText.trim() || this.sending) return
			
			const content = this.inputText.trim()
			this.inputText = ''
			this.sending = true
			
			const tempId = Date.now()
			this.messages.push({
				id: tempId,
				content: content,
				isUser: true,
				time: this.formatTime(new Date())
			})
			
			this.scrollToBottom()

			try {
				await api.sendChatMessage({
					content,
					message_type: 'text'
				})
				await this.loadHistory()
			} catch (e) {
				this.messages = this.messages.filter(msg => msg.id !== tempId)
				uni.showToast({
					title: e.message || '发送失败，请稍后重试',
					icon: 'none'
				})
			} finally {
				this.sending = false
			}
		},

		sendQuickQuestion(question) {
			this.inputText = question
			this.sendMessage()
		},
		
		scrollToBottom() {
			this.$nextTick(() => {
				this.scrollTop = 99999
			})
		},
		
		loadMore() {
			this.loadHistory()
		},
		
		formatTime(date) {
			const hours = date.getHours().toString().padStart(2, '0')
			const minutes = date.getMinutes().toString().padStart(2, '0')
			return `${hours}:${minutes}`
		}
	}
}
</script>

<style lang="scss" scoped>
.chat-page {
	display: flex;
	flex-direction: column;
	height: 100vh;
	background: #f5f5f5;
}

.status-bar {
	display: flex;
	align-items: center;
	background: #fff;
	padding: 20rpx 24rpx;
	border-bottom: 1rpx solid #f0f0f0;
	
	.status-indicator {
		width: 16rpx;
		height: 16rpx;
		border-radius: 50%;
		margin-right: 12rpx;
		
		&.online {
			background: #52c41a;
		}
		
		&.offline {
			background: #d9d9d9;
		}
	}
	
	.status-text {
		font-size: 28rpx;
		color: #333;
		margin-right: 16rpx;
	}
	
	.work-time {
		font-size: 24rpx;
		color: #999;
	}
}

.message-list {
	flex: 1;
	padding: 24rpx;
}

.message-item {
	display: flex;
	margin-bottom: 24rpx;
	
	&.user-msg {
		flex-direction: row-reverse;
		
		.message-bubble {
			background: #1890ff;
			
			.message-text {
				color: #fff;
			}
			
			.message-time {
				color: rgba(255,255,255,0.8);
			}
		}
	}
	
	.avatar {
		width: 72rpx;
		height: 72rpx;
		border-radius: 50%;
		background: #1890ff;
		display: flex;
		align-items: center;
		justify-content: center;
		flex-shrink: 0;
		
		text {
			color: #fff;
			font-size: 28rpx;
			font-weight: 500;
		}
		
		&.user-avatar {
			background: #52c41a;
		}
	}
	
	.message-bubble {
		max-width: 70%;
		background: #fff;
		padding: 20rpx 24rpx;
		border-radius: 16rpx;
		margin: 0 16rpx;
		
		.message-text {
			font-size: 28rpx;
			color: #333;
			line-height: 1.6;
			white-space: pre-wrap;
		}
		
		.message-time {
			display: block;
			font-size: 22rpx;
			color: #999;
			margin-top: 8rpx;
		}
	}
}

.quick-questions {
	background: #fff;
	padding: 16rpx 24rpx;
	border-top: 1rpx solid #f0f0f0;
	
	.quick-scroll {
		white-space: nowrap;
	}
	
	.quick-item {
		display: inline-block;
		padding: 12rpx 24rpx;
		background: #f5f5f5;
		border-radius: 24rpx;
		font-size: 26rpx;
		color: #666;
		margin-right: 16rpx;
	}
}

.input-area {
	display: flex;
	align-items: center;
	background: #fff;
	padding: 16rpx 24rpx;
	padding-bottom: calc(16rpx + env(safe-area-inset-bottom));
	
	.input-wrapper {
		flex: 1;
		background: #f5f5f5;
		border-radius: 8rpx;
		padding: 16rpx 24rpx;
		margin-right: 16rpx;
		
		input {
			font-size: 28rpx;
		}
	}
	
	.send-btn {
		padding: 16rpx 32rpx;
		background: #d9d9d9;
		border-radius: 8rpx;
		font-size: 28rpx;
		color: #fff;
		
		&.active {
			background: #1890ff;
		}
	}
}
</style>

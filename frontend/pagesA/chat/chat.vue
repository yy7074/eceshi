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
					content: '您好！欢迎咨询科研检测服务平台，我是您的专属客服，请问有什么可以帮助您的？',
					isUser: false,
					time: '刚刚'
				}
			],
			inputText: '',
			scrollTop: 0,
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
	methods: {
		sendMessage() {
			if (!this.inputText.trim()) return
			
			const content = this.inputText
			this.inputText = ''
			
			// 添加用户消息
			this.messages.push({
				id: Date.now(),
				content: content,
				isUser: true,
				time: this.formatTime(new Date())
			})
			
			this.scrollToBottom()
			
			// 模拟客服回复
			setTimeout(() => {
				this.handleAutoReply(content)
			}, 1000)
		},
		
		sendQuickQuestion(question) {
			this.inputText = question
			this.sendMessage()
		},
		
		handleAutoReply(question) {
			let reply = '感谢您的咨询，客服正在为您处理，请稍候...'
			
			// 简单的自动回复匹配
			if (question.includes('下单')) {
				reply = '下单流程：\n1. 浏览检测项目，选择需要的服务\n2. 点击"立即预约"填写样品信息\n3. 确认订单并完成支付\n4. 按指引寄送样品即可'
			} else if (question.includes('周期') || question.includes('多久')) {
				reply = '常规检测周期为3-5个工作日，具体以项目详情页显示为准。加急服务请联系人工客服。'
			} else if (question.includes('报告')) {
				reply = '检测完成后，您可以在"订单详情"页面下载电子版报告，也可以选择邮寄纸质报告（额外收费）。'
			} else if (question.includes('发票')) {
				reply = '支付完成后，您可以在"我的发票"页面申请开具发票。支持电子发票和纸质发票，电子发票即时发送，纸质发票3-5个工作日寄出。'
			} else if (question.includes('优惠') || question.includes('活动')) {
				reply = '当前优惠活动：\n1. 新用户首单立减50元\n2. 热门检测项目6折起\n3. 充值满1000送100\n\n更多优惠请关注首页公告！'
			} else if (question.includes('退款')) {
				reply = '退款规则：\n1. 未寄送样品的订单可全额退款\n2. 已寄送未检测的订单扣除物流费用后退款\n3. 检测中或已完成的订单不支持退款\n\n如需退款，请在订单详情页申请。'
			}
			
			this.messages.push({
				id: Date.now(),
				content: reply,
				isUser: false,
				time: this.formatTime(new Date())
			})
			
			this.scrollToBottom()
		},
		
		scrollToBottom() {
			this.$nextTick(() => {
				this.scrollTop = 99999
			})
		},
		
		loadMore() {
			// 加载更多历史消息
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


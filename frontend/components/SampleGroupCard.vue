<template>
  <view class="sample-group-card" :class="{ collapsed: group.is_collapsed }">
    <!-- 卡片头部 -->
    <view class="card-header" @click="toggleCollapse">
      <view class="header-left">
        <view class="group-index">分组 {{ group.group_index }}</view>
        <view class="group-name" v-if="group.group_name">{{ group.group_name }}</view>
      </view>
      <view class="header-right">
        <view class="sample-count">{{ sampleCount }} 个样品</view>
        <view class="options-fee" v-if="group.options_fee > 0">+¥{{ group.options_fee }}</view>
        <text class="collapse-icon" :class="{ expanded: !group.is_collapsed }">&#xe60d;</text>
      </view>
    </view>

    <!-- 卡片内容（可折叠） -->
    <view class="card-content" v-show="!group.is_collapsed">
      <!-- 分组名称编辑 -->
      <view class="section">
        <view class="section-title">测试目的</view>
        <input
          class="group-name-input"
          type="text"
          v-model="editGroupName"
          placeholder="请输入测试目的（可选）"
          @blur="updateGroupName"
        />
      </view>

      <!-- 样品列表 -->
      <view class="section">
        <view class="section-header">
          <view class="section-title">样品列表</view>
          <view class="section-actions">
            <view class="action-btn" @click="showBatchAdd = true">批量添加</view>
            <view class="action-btn primary" @click="addSample">添加样品</view>
          </view>
        </view>

        <!-- 样品列表 -->
        <view class="sample-list">
          <view
            class="sample-item"
            v-for="(item, index) in group.items"
            :key="item.id"
          >
            <view class="sample-header">
              <view class="sample-no">{{ item.sample_no || `样品${index + 1}` }}</view>
              <view class="sample-actions">
                <text class="action-icon" @click="editSample(item)">编辑</text>
                <text class="action-icon delete" @click="deleteSample(item.id)">删除</text>
              </view>
            </view>
            <view class="sample-info" v-if="item.sample_name">
              <text class="label">名称：</text>
              <text class="value">{{ item.sample_name }}</text>
            </view>
            <view class="sample-info" v-if="item.quantity > 1">
              <text class="label">数量：</text>
              <text class="value">{{ item.quantity }}</text>
            </view>
          </view>

          <!-- 空状态 -->
          <view class="empty-samples" v-if="!group.items || group.items.length === 0">
            <text>暂无样品，请添加样品</text>
          </view>
        </view>
      </view>

      <!-- 选项选择（集成动态选项组件） -->
      <view class="section" v-if="showOptions">
        <view class="section-title">检测选项</view>
        <slot name="options"></slot>
      </view>

      <!-- 操作按钮 -->
      <view class="card-actions">
        <view class="action-btn" @click="$emit('copy', group.id)">
          <text class="icon">&#xe631;</text>复制分组
        </view>
        <view class="action-btn danger" @click="$emit('delete', group.id)">
          <text class="icon">&#xe632;</text>删除分组
        </view>
      </view>
    </view>

    <!-- 批量添加弹窗 -->
    <uni-popup ref="batchPopup" type="center" v-if="showBatchAdd" @change="onPopupChange">
      <view class="batch-popup">
        <view class="popup-header">
          <text class="popup-title">批量添加样品</text>
          <text class="popup-close" @click="showBatchAdd = false">×</text>
        </view>
        <view class="popup-content">
          <view class="form-item">
            <text class="form-label">添加数量</text>
            <input
              type="number"
              v-model.number="batchForm.count"
              placeholder="请输入数量"
              class="form-input"
            />
          </view>
          <view class="form-item">
            <text class="form-label">编号前缀</text>
            <input
              type="text"
              v-model="batchForm.prefix"
              placeholder="如：SAMPLE_"
              class="form-input"
            />
          </view>
          <view class="form-item">
            <text class="form-label">起始编号</text>
            <input
              type="number"
              v-model.number="batchForm.start_number"
              placeholder="1"
              class="form-input"
            />
          </view>
        </view>
        <view class="popup-footer">
          <view class="popup-btn cancel" @click="showBatchAdd = false">取消</view>
          <view class="popup-btn confirm" @click="confirmBatchAdd">确认添加</view>
        </view>
      </view>
    </uni-popup>

    <!-- 样品编辑弹窗 -->
    <uni-popup ref="samplePopup" type="center" v-if="showSampleEdit" @change="onSamplePopupChange">
      <view class="sample-popup">
        <view class="popup-header">
          <text class="popup-title">{{ editingItem ? '编辑样品' : '添加样品' }}</text>
          <text class="popup-close" @click="showSampleEdit = false">×</text>
        </view>
        <view class="popup-content">
          <view class="form-item">
            <text class="form-label">样品编号</text>
            <input
              type="text"
              v-model="sampleForm.sample_no"
              placeholder="仅支持英文、数字、下划线"
              class="form-input"
            />
          </view>
          <view class="form-item">
            <text class="form-label">样品名称</text>
            <input
              type="text"
              v-model="sampleForm.sample_name"
              placeholder="请输入样品名称"
              class="form-input"
            />
          </view>
          <view class="form-item">
            <text class="form-label">样品成分</text>
            <textarea
              v-model="sampleForm.sample_composition"
              placeholder="请输入样品成分"
              class="form-textarea"
            />
          </view>
          <view class="form-item">
            <text class="form-label">样品状态</text>
            <picker
              :range="sampleStates"
              @change="sampleForm.sample_state = sampleStates[$event.detail.value]"
            >
              <view class="form-picker">
                {{ sampleForm.sample_state || '请选择' }}
              </view>
            </picker>
          </view>
          <view class="form-item">
            <text class="form-label">危险性</text>
            <picker
              :range="dangerTypes"
              @change="sampleForm.danger_type = dangerTypes[$event.detail.value]"
            >
              <view class="form-picker">
                {{ sampleForm.danger_type || '请选择' }}
              </view>
            </picker>
          </view>
          <view class="form-item">
            <text class="form-label">存放要求</text>
            <input
              type="text"
              v-model="sampleForm.storage_requirement"
              placeholder="如：冷藏、避光"
              class="form-input"
            />
          </view>
          <view class="form-item">
            <text class="form-label">数量</text>
            <input
              type="number"
              v-model.number="sampleForm.quantity"
              placeholder="1"
              class="form-input"
            />
          </view>
          <view class="form-item">
            <text class="form-label">备注</text>
            <textarea
              v-model="sampleForm.remark"
              placeholder="其他备注信息"
              class="form-textarea"
            />
          </view>
        </view>
        <view class="popup-footer">
          <view class="popup-btn cancel" @click="showSampleEdit = false">取消</view>
          <view class="popup-btn confirm" @click="confirmSampleEdit">确认</view>
        </view>
      </view>
    </uni-popup>
  </view>
</template>

<script>
export default {
  name: 'SampleGroupCard',
  props: {
    group: {
      type: Object,
      required: true
    },
    showOptions: {
      type: Boolean,
      default: true
    }
  },
  data() {
    return {
      editGroupName: '',
      showBatchAdd: false,
      showSampleEdit: false,
      editingItem: null,
      batchForm: {
        count: 5,
        prefix: '',
        start_number: 1
      },
      sampleForm: {
        sample_no: '',
        sample_name: '',
        sample_composition: '',
        sample_state: '',
        danger_type: '',
        storage_requirement: '',
        quantity: 1,
        remark: ''
      },
      sampleStates: ['固体', '液体', '气体', '粉末', '膏状', '其他'],
      dangerTypes: ['无危险', '易燃', '易爆', '腐蚀性', '有毒', '放射性', '其他']
    }
  },
  computed: {
    sampleCount() {
      if (!this.group.items) return 0
      return this.group.items.reduce((sum, item) => sum + (item.quantity || 1), 0)
    }
  },
  watch: {
    'group.group_name': {
      immediate: true,
      handler(val) {
        this.editGroupName = val || ''
      }
    }
  },
  methods: {
    toggleCollapse() {
      this.$emit('toggle-collapse', this.group.id)
    },

    updateGroupName() {
      if (this.editGroupName !== this.group.group_name) {
        this.$emit('update', this.group.id, { group_name: this.editGroupName })
      }
    },

    addSample() {
      this.editingItem = null
      this.sampleForm = {
        sample_no: '',
        sample_name: '',
        sample_composition: '',
        sample_state: '',
        danger_type: '',
        storage_requirement: '',
        quantity: 1,
        remark: ''
      }
      this.showSampleEdit = true
    },

    editSample(item) {
      this.editingItem = item
      this.sampleForm = { ...item }
      this.showSampleEdit = true
    },

    deleteSample(itemId) {
      uni.showModal({
        title: '确认删除',
        content: '确定要删除这个样品吗？',
        success: (res) => {
          if (res.confirm) {
            this.$emit('delete-sample', this.group.id, itemId)
          }
        }
      })
    },

    confirmSampleEdit() {
      // 验证样品编号格式
      if (this.sampleForm.sample_no && !/^[a-zA-Z0-9_]+$/.test(this.sampleForm.sample_no)) {
        uni.showToast({
          title: '样品编号只能包含英文、数字和下划线',
          icon: 'none'
        })
        return
      }

      if (this.editingItem) {
        this.$emit('update-sample', this.group.id, this.editingItem.id, this.sampleForm)
      } else {
        this.$emit('add-sample', this.group.id, this.sampleForm)
      }
      this.showSampleEdit = false
    },

    confirmBatchAdd() {
      if (!this.batchForm.count || this.batchForm.count < 1) {
        uni.showToast({
          title: '请输入有效数量',
          icon: 'none'
        })
        return
      }

      if (this.batchForm.count > 100) {
        uni.showToast({
          title: '单次最多添加100个样品',
          icon: 'none'
        })
        return
      }

      // 验证编号前缀格式
      if (this.batchForm.prefix && !/^[a-zA-Z0-9_]*$/.test(this.batchForm.prefix)) {
        uni.showToast({
          title: '编号前缀只能包含英文、数字和下划线',
          icon: 'none'
        })
        return
      }

      this.$emit('batch-add', this.group.id, this.batchForm)
      this.showBatchAdd = false
      this.batchForm = {
        count: 5,
        prefix: '',
        start_number: 1
      }
    },

    onPopupChange(e) {
      if (!e.show) {
        this.showBatchAdd = false
      }
    },

    onSamplePopupChange(e) {
      if (!e.show) {
        this.showSampleEdit = false
      }
    }
  }
}
</script>

<style scoped>
.sample-group-card {
  background: #fff;
  border-radius: 16rpx;
  margin-bottom: 20rpx;
  overflow: hidden;
  box-shadow: 0 2rpx 12rpx rgba(0, 0, 0, 0.05);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24rpx;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 16rpx;
}

.group-index {
  font-size: 28rpx;
  font-weight: 600;
}

.group-name {
  font-size: 24rpx;
  opacity: 0.9;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 16rpx;
}

.sample-count {
  font-size: 24rpx;
  background: rgba(255, 255, 255, 0.2);
  padding: 4rpx 12rpx;
  border-radius: 8rpx;
}

.options-fee {
  font-size: 24rpx;
  color: #ffd700;
}

.collapse-icon {
  font-family: 'iconfont';
  font-size: 24rpx;
  transition: transform 0.3s;
}

.collapse-icon.expanded {
  transform: rotate(180deg);
}

.card-content {
  padding: 24rpx;
}

.section {
  margin-bottom: 24rpx;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16rpx;
}

.section-title {
  font-size: 28rpx;
  font-weight: 600;
  color: #333;
  margin-bottom: 12rpx;
}

.section-actions {
  display: flex;
  gap: 16rpx;
}

.action-btn {
  font-size: 24rpx;
  color: #666;
  padding: 8rpx 16rpx;
  border: 1rpx solid #ddd;
  border-radius: 8rpx;
}

.action-btn.primary {
  color: #667eea;
  border-color: #667eea;
}

.action-btn.danger {
  color: #ff4d4f;
  border-color: #ff4d4f;
}

.group-name-input {
  width: 100%;
  padding: 16rpx;
  border: 1rpx solid #e5e5e5;
  border-radius: 8rpx;
  font-size: 28rpx;
}

.sample-list {
  background: #f8f8f8;
  border-radius: 12rpx;
  padding: 16rpx;
}

.sample-item {
  background: #fff;
  border-radius: 8rpx;
  padding: 16rpx;
  margin-bottom: 12rpx;
}

.sample-item:last-child {
  margin-bottom: 0;
}

.sample-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8rpx;
}

.sample-no {
  font-size: 28rpx;
  font-weight: 500;
  color: #333;
}

.sample-actions {
  display: flex;
  gap: 16rpx;
}

.action-icon {
  font-size: 24rpx;
  color: #667eea;
}

.action-icon.delete {
  color: #ff4d4f;
}

.sample-info {
  font-size: 24rpx;
  color: #666;
  margin-top: 4rpx;
}

.sample-info .label {
  color: #999;
}

.empty-samples {
  text-align: center;
  padding: 40rpx;
  color: #999;
  font-size: 26rpx;
}

.card-actions {
  display: flex;
  justify-content: center;
  gap: 32rpx;
  padding-top: 16rpx;
  border-top: 1rpx solid #f0f0f0;
}

.card-actions .icon {
  margin-right: 8rpx;
}

/* 弹窗样式 */
.batch-popup,
.sample-popup {
  width: 600rpx;
  background: #fff;
  border-radius: 16rpx;
  overflow: hidden;
}

.popup-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24rpx;
  border-bottom: 1rpx solid #f0f0f0;
}

.popup-title {
  font-size: 32rpx;
  font-weight: 600;
  color: #333;
}

.popup-close {
  font-size: 40rpx;
  color: #999;
}

.popup-content {
  padding: 24rpx;
  max-height: 60vh;
  overflow-y: auto;
}

.form-item {
  margin-bottom: 20rpx;
}

.form-label {
  display: block;
  font-size: 26rpx;
  color: #666;
  margin-bottom: 8rpx;
}

.form-input {
  width: 100%;
  padding: 16rpx;
  border: 1rpx solid #e5e5e5;
  border-radius: 8rpx;
  font-size: 28rpx;
}

.form-textarea {
  width: 100%;
  height: 120rpx;
  padding: 16rpx;
  border: 1rpx solid #e5e5e5;
  border-radius: 8rpx;
  font-size: 28rpx;
}

.form-picker {
  padding: 16rpx;
  border: 1rpx solid #e5e5e5;
  border-radius: 8rpx;
  font-size: 28rpx;
  color: #333;
}

.popup-footer {
  display: flex;
  border-top: 1rpx solid #f0f0f0;
}

.popup-btn {
  flex: 1;
  text-align: center;
  padding: 24rpx;
  font-size: 30rpx;
}

.popup-btn.cancel {
  color: #666;
  border-right: 1rpx solid #f0f0f0;
}

.popup-btn.confirm {
  color: #667eea;
  font-weight: 600;
}
</style>

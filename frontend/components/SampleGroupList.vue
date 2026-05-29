<template>
  <view class="sample-group-list">
    <!-- 操作栏 -->
    <view class="list-header">
      <view class="header-title">
        <text class="title">样品分组</text>
        <text class="subtitle">共 {{ groups.length }} 个分组，{{ totalSampleCount }} 个样品</text>
      </view>
      <view class="header-actions">
        <view class="action-btn primary" @click="createGroup">
          <text class="icon">+</text>新增分组
        </view>
      </view>
    </view>

    <!-- 分组列表 -->
    <view class="groups-container">
      <SampleGroupCard
        v-for="group in groups"
        :key="group.id"
        :group="group"
        :show-options="showOptions"
        @toggle-collapse="handleToggleCollapse"
        @update="handleUpdateGroup"
        @delete="handleDeleteGroup"
        @copy="handleCopyGroup"
        @add-sample="handleAddSample"
        @update-sample="handleUpdateSample"
        @delete-sample="handleDeleteSample"
        @batch-add="handleBatchAdd"
      >
        <template #options>
          <DynamicOptionsForm
            v-if="optionsTree.length > 0"
            :options-tree="optionsTree"
            :project-id="projectId"
            :sample-count="getGroupSampleCount(group)"
            :initial-selections="group.option_selections || []"
            @change="data => handleOptionsChange(group.id, data)"
          />
        </template>
      </SampleGroupCard>

      <!-- 空状态 -->
      <view class="empty-state" v-if="groups.length === 0">
        <image src="/static/images/empty-box.png" class="empty-icon" mode="aspectFit" />
        <text class="empty-text">暂无样品分组</text>
        <view class="action-btn primary" @click="createGroup">创建第一个分组</view>
      </view>
    </view>

    <!-- 底部价格汇总 -->
    <view class="price-summary" v-if="groups.length > 0">
      <view class="summary-row" v-if="totalOptionsFee > 0">
        <text class="label">测试条件费用</text>
        <text class="value">¥{{ totalOptionsFee.toFixed(2) }}</text>
      </view>
      <view class="summary-row total">
        <text class="label">合计</text>
        <text class="value">¥{{ totalPrice.toFixed(2) }}</text>
      </view>
    </view>
  </view>
</template>

<script>
import SampleGroupCard from './SampleGroupCard.vue'
import DynamicOptionsForm from './DynamicOptionsForm.vue'
import api from '@/utils/api'

export default {
  name: 'SampleGroupList',
  components: {
    SampleGroupCard,
    DynamicOptionsForm
  },
  props: {
    projectId: {
      type: [Number, String],
      required: true
    },
    basePrice: {
      type: Number,
      default: 0
    },
    optionsTree: {
      type: Array,
      default: () => []
    },
    showOptions: {
      type: Boolean,
      default: true
    }
  },
  data() {
    return {
      groups: [],
      loading: false
    }
  },
  computed: {
    totalSampleCount() {
      return this.groups.reduce((sum, group) => {
        const items = group.items || []
        return sum + items.reduce((s, item) => s + (item.quantity || 1), 0)
      }, 0)
    },
    totalBasePrice() {
      return 0
    },
    totalOptionsFee() {
      return this.groups.reduce((sum, group) => {
        return sum + (parseFloat(group.options_fee) || 0)
      }, 0)
    },
    totalPrice() {
      return this.totalBasePrice + this.totalOptionsFee
    }
  },
  watch: {
    projectId: {
      immediate: true,
      handler(val) {
        if (val) {
          this.loadGroups()
        }
      }
    }
  },
  methods: {
    async loadGroups() {
      this.loading = true
      try {
        const res = await api.getSampleGroups({ project_id: this.projectId, status: 'draft' })
        if (res.code === 200) {
          this.groups = res.data || []
          // 为每个分组加载详细信息
          for (let i = 0; i < this.groups.length; i++) {
            await this.loadGroupDetail(this.groups[i].id, i)
          }
        }
      } catch (e) {
        console.error('加载样品组失败', e)
      } finally {
        this.loading = false
      }
      this.emitChange()
    },

    async loadGroupDetail(groupId, index) {
      try {
        const res = await api.getSampleGroupDetail(groupId)
        if (res.code === 200 && res.data) {
          this.groups.splice(index, 1, res.data)
        }
      } catch (e) {
        console.error('加载分组详情失败', e)
      }
    },

    getGroupSampleCount(group) {
      if (!group.items) return 0
      return group.items.reduce((sum, item) => sum + (item.quantity || 1), 0)
    },

    async createGroup() {
      try {
        const res = await api.createSampleGroup({
          project_id: parseInt(this.projectId),
          group_name: ''
        })
        if (res.code === 200) {
          this.groups.push(res.data)
          uni.showToast({ title: '创建成功', icon: 'success' })
          this.emitChange()
        }
      } catch (e) {
        uni.showToast({ title: '创建失败', icon: 'none' })
      }
    },

    async handleToggleCollapse(groupId) {
      const index = this.groups.findIndex(g => g.id === groupId)
      if (index === -1) return

      const group = this.groups[index]
      try {
        await api.updateSampleGroup(groupId, { is_collapsed: !group.is_collapsed })
        this.groups.splice(index, 1, {
          ...this.groups[index],
          is_collapsed: !group.is_collapsed
        })
      } catch (e) {
        console.error('更新折叠状态失败', e)
      }
    },

    async handleUpdateGroup(groupId, data) {
      const index = this.groups.findIndex(g => g.id === groupId)
      if (index === -1) return

      try {
        const res = await api.updateSampleGroup(groupId, data)
        if (res.code === 200) {
          this.groups.splice(index, 1, { ...this.groups[index], ...res.data })
          this.emitChange()
        }
      } catch (e) {
        uni.showToast({ title: '更新失败', icon: 'none' })
      }
    },

    async handleDeleteGroup(groupId) {
      uni.showModal({
        title: '确认删除',
        content: '删除分组将同时删除组内所有样品，确定删除吗？',
        success: async (res) => {
          if (res.confirm) {
            try {
              const result = await api.deleteSampleGroup(groupId)
              if (result.code === 200) {
                const index = this.groups.findIndex(g => g.id === groupId)
                if (index !== -1) {
                  this.groups.splice(index, 1)
                }
                uni.showToast({ title: '删除成功', icon: 'success' })
                this.emitChange()
              }
            } catch (e) {
              uni.showToast({ title: '删除失败', icon: 'none' })
            }
          }
        }
      })
    },

    async handleCopyGroup(groupId) {
      try {
        const res = await api.copySampleGroup(groupId)
        if (res.code === 200) {
          this.groups.push(res.data.new_group)
          uni.showToast({ title: '复制成功', icon: 'success' })
          this.emitChange()
        }
      } catch (e) {
        uni.showToast({ title: '复制失败', icon: 'none' })
      }
    },

    async handleAddSample(groupId, sampleData) {
      try {
        const res = await api.addSampleItem(groupId, sampleData)
        if (res.code === 200) {
          const index = this.groups.findIndex(g => g.id === groupId)
          if (index !== -1) {
            const items = [...(this.groups[index].items || []), res.data]
            this.groups.splice(index, 1, { ...this.groups[index], items })
          }
          uni.showToast({ title: '添加成功', icon: 'success' })
          this.emitChange()
        }
      } catch (e) {
        uni.showToast({ title: '添加失败', icon: 'none' })
      }
    },

    async handleUpdateSample(groupId, itemId, sampleData) {
      try {
        const res = await api.updateSampleItem(groupId, itemId, sampleData)
        if (res.code === 200) {
          const groupIndex = this.groups.findIndex(g => g.id === groupId)
          if (groupIndex !== -1) {
            const itemIndex = this.groups[groupIndex].items.findIndex(i => i.id === itemId)
            if (itemIndex !== -1) {
              const items = [...this.groups[groupIndex].items]
              items.splice(itemIndex, 1, res.data)
              this.groups.splice(groupIndex, 1, { ...this.groups[groupIndex], items })
            }
          }
          uni.showToast({ title: '更新成功', icon: 'success' })
          this.emitChange()
        }
      } catch (e) {
        uni.showToast({ title: '更新失败', icon: 'none' })
      }
    },

    async handleDeleteSample(groupId, itemId) {
      try {
        const res = await api.deleteSampleItem(groupId, itemId)
        if (res.code === 200) {
          const groupIndex = this.groups.findIndex(g => g.id === groupId)
          if (groupIndex !== -1) {
            const itemIndex = this.groups[groupIndex].items.findIndex(i => i.id === itemId)
            if (itemIndex !== -1) {
              const items = [...this.groups[groupIndex].items]
              items.splice(itemIndex, 1)
              this.groups.splice(groupIndex, 1, { ...this.groups[groupIndex], items })
            }
          }
          uni.showToast({ title: '删除成功', icon: 'success' })
          this.emitChange()
        }
      } catch (e) {
        uni.showToast({ title: '删除失败', icon: 'none' })
      }
    },

    async handleBatchAdd(groupId, batchData) {
      try {
        const res = await api.batchAddSampleItems(groupId, batchData)
        if (res.code === 200) {
          const groupIndex = this.groups.findIndex(g => g.id === groupId)
          if (groupIndex !== -1) {
            const items = [
              ...(this.groups[groupIndex].items || []),
              ...(res.data.items || [])
            ]
            this.groups.splice(groupIndex, 1, { ...this.groups[groupIndex], items })
          }
          uni.showToast({ title: res.data.message || '添加成功', icon: 'success' })
          this.emitChange()
        }
      } catch (e) {
        uni.showToast({ title: '批量添加失败', icon: 'none' })
      }
    },

    async handleOptionsChange(groupId, data) {
      const index = this.groups.findIndex(g => g.id === groupId)
      if (index === -1) return

      const selections = data.selections || []
      const fee = Number(data.totalOptionsFee || 0)

      try {
        await api.updateSampleGroup(groupId, { option_selections: selections })
        this.groups.splice(index, 1, {
          ...this.groups[index],
          option_selections: selections,
          options_fee: fee
        })
        this.emitChange()
      } catch (e) {
        console.error('更新选项失败', e)
      }
    },

    normalizeInputValues(selection) {
      if (!selection) return []
      if (Array.isArray(selection.input_values)) {
        return selection.input_values.map(value => `${value}`.trim()).filter(Boolean)
      }
      if (selection.input_value) {
        const raw = `${selection.input_value}`.trim()
        if (raw.startsWith('[')) {
          try {
            const parsed = JSON.parse(raw)
            if (Array.isArray(parsed)) {
              return parsed.map(value => `${value}`.trim()).filter(Boolean)
            }
          } catch (e) {
            return [raw]
          }
        }
        return [raw]
      }
      return []
    },

    validateOptionsForGroup(group, options = this.optionsTree) {
      const selections = {}
      ;(group.option_selections || []).forEach(item => {
        if (item && item.option_id) {
          selections[item.option_id] = item
        }
      })

      const checkRequired = (nodes) => {
        for (const option of nodes || []) {
          const isGroupControl = ['dropdown', 'checkbox_group', 'radio_group'].includes(option.option_type)
          const requiresInput = option.requires_input || option.option_type === 'input'
          const allowsChildren = option.allow_children !== false
          const selection = selections[option.id]

          if (isGroupControl) {
            const selectedChildren = (option.children || []).filter(child => selections[child.id])
            if (option.is_required && selectedChildren.length === 0) {
              return `分组${group.group_index}请选择${option.name}`
            }
            for (const child of selectedChildren) {
              if (child.children && child.children.length > 0 && child.allow_children !== false) {
                const error = checkRequired(child.children)
                if (error) return error
              }
            }
            continue
          }

          if (option.is_required) {
            if (!selection) {
              return `分组${group.group_index}请选择${option.name}`
            }
            if (requiresInput && this.normalizeInputValues(selection).length === 0) {
              return `分组${group.group_index}请填写${option.name}`
            }
          }

          if (selection && option.children && allowsChildren) {
            const error = checkRequired(option.children)
            if (error) return error
          }
        }
        return ''
      }

      return checkRequired(options)
    },

    validate() {
      for (const group of this.groups) {
        const error = this.validateOptionsForGroup(group)
        if (error) {
          return [error]
        }
      }
      return []
    },

    emitChange() {
      this.$emit('change', {
        groups: this.groups,
        totalSampleCount: this.totalSampleCount,
        totalBasePrice: this.totalBasePrice,
        totalOptionsFee: this.totalOptionsFee,
        totalPrice: this.totalPrice
      })
    },

    // 获取所有草稿分组ID，供提交使用
    getGroupIds() {
      return this.groups.filter(g => g.status === 'draft').map(g => g.id)
    }
  }
}
</script>

<style scoped>
.sample-group-list {
  padding: 20rpx;
}

.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20rpx;
  padding: 20rpx;
  background: #fff;
  border-radius: 12rpx;
}

.header-title .title {
  font-size: 32rpx;
  font-weight: 600;
  color: #333;
  display: block;
}

.header-title .subtitle {
  font-size: 24rpx;
  color: #999;
  margin-top: 4rpx;
}

.action-btn {
  display: flex;
  align-items: center;
  padding: 12rpx 24rpx;
  border-radius: 8rpx;
  font-size: 26rpx;
}

.action-btn.primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
}

.action-btn .icon {
  margin-right: 8rpx;
  font-size: 28rpx;
}

.groups-container {
  min-height: 200rpx;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80rpx 40rpx;
  background: #fff;
  border-radius: 16rpx;
}

.empty-icon {
  width: 160rpx;
  height: 160rpx;
  margin-bottom: 20rpx;
  opacity: 0.5;
}

.empty-text {
  font-size: 28rpx;
  color: #999;
  margin-bottom: 30rpx;
}

.price-summary {
  background: #fff;
  border-radius: 12rpx;
  padding: 20rpx;
  margin-top: 20rpx;
}

.summary-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12rpx 0;
}

.summary-row .label {
  font-size: 26rpx;
  color: #666;
}

.summary-row .value {
  font-size: 28rpx;
  color: #333;
}

.summary-row.total {
  border-top: 1rpx solid #f0f0f0;
  padding-top: 16rpx;
  margin-top: 8rpx;
}

.summary-row.total .label {
  font-size: 30rpx;
  font-weight: 600;
  color: #333;
}

.summary-row.total .value {
  font-size: 36rpx;
  font-weight: 600;
  color: #ff4d4f;
}
</style>

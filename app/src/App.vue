<template>
  <router-view /> <!-- 渲染路由视图 -->

  <!-- 文件上传浮动框 -->
  <uploading-float-frame />

  <!-- 全局消息提示条 -->
  <snack-bar />
</template>

<script setup lang="ts">
import { onMounted, watchEffect, watch } from 'vue'
import { useI18n } from 'vue-i18n' // 导入国际化插件
import { MessagePlugin } from 'tdesign-vue-next' // 导入消息提示插件
import { useWebSocket } from '@vueuse/core' // 导入WebSocket插件
import { useProfileStore, useNoteStore, useFileStore } from '@/store' // 导入状态管理
import { clearExipredStorageData } from '@/utils' // 导入工具函数
import { useVersion } from '@/hooks' // 导入自定义hook
import { FILE_API } from '@/apis' // 导入文件相关API

const { t } = useI18n() // 获取国际化实例
const PROFILE_STORE = useProfileStore() // 使用个人资料Store
const NOTE_STORE = useNoteStore() // 使用笔记Store
const FILE_STORE = useFileStore() // 使用文件Store

onMounted(async () => {
  await NOTE_STORE.getNotes() // 获取笔记列表
  await PROFILE_STORE.getProfile() // 获取个人资料
  await useVersion(t('message.needUpdate')) // 使用版本控制插件检查更新

  clearExipredStorageData() // 清除过期的本地存储数据
})

// ################################ 处理文件上传 start ########################################

// 连接WebSocket到后端以监视正在上传的文件
const { data } = useWebSocket('ws://localhost:51717/ws/file/uploading', {
  autoReconnect: {
    retries: 3,
  },
  heartbeat: {
    message: 'ping',
    interval: 1000,
    pongTimeout: 1000,
  },
})
watchEffect(() => {
  FILE_STORE.uploadingFiles = data.value ? JSON.parse(data.value).data : [] // 更新正在上传的文件列表
  NOTE_STORE.setIsUploadingNotes() // 设置正在上传笔记的状态
})

// 监听正在上传的文件以显示消息提示
watch(
  () => FILE_STORE.uploadingFiles,
  async (list, preList) => {
    const diff = preList.filter(
      (preItem) => !list.map((item) => item.id).includes(preItem.id)
    )
    await Promise.all(
      diff.map(async (item) => {
        const res = await FILE_API.getQuestionCount(item.id) // 获取上传文件相关的问题数量
        MessagePlugin.success( // 显示上传成功消息
        `File ${item.file_name} was uploaded successfully and ${res.data} questions were generated.`,
          6000
        )
      })
    )
  }
)
// ################################ 处理文件上传 end ########################################

</script>

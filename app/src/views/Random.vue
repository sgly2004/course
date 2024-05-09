<template>
  <!-- 使用 Vuetify 的容器组件，限制内容最大宽度为1080px -->
  <v-container style="max-width: 1080px">
    <!-- 空白区块 -->
    <empty-block v-if="questionInfo === 'empty'" type="question"> <!-- 如果问题信息为空，显示空白区块 -->
      <!-- 标题 -->
      <h3 style="margin-top: -50px">
        {{ $t('title.emptyQuestion') }} <!-- 使用国际化函数显示标题 -->
      </h3>
    </empty-block>

    <section v-else> <!-- 如果问题信息不为空，显示问题和答案区块 -->
      <!-- 问题区块 -->
      <question-block
        v-bind="questionInfo" <!-- 动态绑定问题信息 -->
        :type="'random'" <!-- 类型为随机问题 -->
        :loading="getRQLoading" <!-- 加载状态 -->
        @refresh="hanleClickRefresh" <!-- 刷新事件处理函数 -->
      />

      <!-- 答案区块 -->
      <examine-block
        v-if="trigger" <!-- 如果触发条件满足，则显示答案区块 -->
        :id="questionInfo.id" <!-- 问题ID -->
        :questionType="questionInfo.question_type" <!-- 问题类型 -->
        :questionContent="questionInfo.content" <!-- 问题内容 -->
      />
    </section>
  </v-container>
</template>

<script lang="ts">
export default {
  name: 'Random', // 组件名称
}
</script>

<script setup lang="ts">
import { ref, nextTick } from 'vue' // 导入Vue的响应式数据和异步处理函数
import { useDebounceFn } from '@vueuse/core' // 导入防抖函数
import { useFetch } from '@/hooks' // 导入自定义hook
import { QUESTION_API } from '@/apis' // 导入问题相关API

// 处理获取随机问题
const questionInfo = ref<any>(null) // 问题信息
const trigger = ref(true) // 触发条件
const [_getRandomQuestion, getRQLoading] = useFetch( // 使用自定义hook进行异步请求
  QUESTION_API.getRandomQuestion // 获取随机问题的API
)
const getRandomQuestion = async () => { // 获取随机问题的函数
  const { data } = await _getRandomQuestion() // 发送请求
  questionInfo.value = data // 更新问题信息
  trigger.value = false // 取消触发条件
  nextTick(() => { // 使用nextTick确保DOM更新完毕后再重新设置触发条件
    trigger.value = true // 重新设置触发条件
  })
}

// 防抖点击刷新按钮以选择新问题
const hanleClickRefresh = useDebounceFn(async () => { // 使用防抖函数处理点击事件
  await getRandomQuestion() // 调用获取随机问题函数
}, 500)

await getRandomQuestion() // 初始化时获取随机问题
</script>

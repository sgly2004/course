<template>
  <!-- 使用 Vuetify 的容器组件，限制内容最大宽度为1080px -->
  <v-container style="max-width: 1080px">
    <!-- 标题 -->
    <h2>
      {{ $t('menus.questionBank') }} <!-- 显示问题库标题 -->
    </h2>
    <!-- 副标题 -->
    <h5 class="text-medium-emphasis">
      {{ $t('subTitle.questionBank') }}, {{ $t('hint.welcomeTo') }} <!-- 显示副标题和欢迎提示 -->
      <!-- 贡献问题库链接 -->
      <a
        :href="
          locale === 'en'
            ? 'https://github.com/codeacme17/examor/blob/main/docs/contribute/en-bank.md'
            : 'https://github.com/codeacme17/examor/blob/main/docs/contribute/zh-bank.md'
        "
        target="_blank"
      >
        {{ $t('hint.contributeBank') }} <!-- 显示贡献问题库的提示 -->
        <v-icon icon="mdi-open-in-new" style="font-size: 16px" /> <!-- 打开外部链接图标 -->
      </a>
    </h5>

    <!-- 分隔线 -->
    <v-divider class="mt-8"></v-divider>

    <!-- 问题库分类按钮 -->
    <section class="mt-3 w-full">
      <v-btn
        v-for="item in bankCategories"
        size="small"
        class="mr-2 mt-2"
        :variant="selectedCategory === item ? 'flat' : 'tonal'"
        :color="selectedCategory === item ? 'primary' : ''"
        :key="item"
        :elevation="0"
        @click="handleChangeCategory(item)"
      >
        {{ item }}
      </v-btn>
    </section>

    <!-- 问题库列表 -->
    <v-row align="start" class="mt-2">
      <v-col
        v-for="item in bankList"
        :key="item.name"
        sm="6"
        md="4"
        align-self="stretch"
      >
        <!-- 问题库卡片组件 -->
        <question-bank-card
          v-bind="item"
          @clickImportButton="handleClickImportButton"
        />
      </v-col>
    </v-row>

    <!-- 导入问题库对话框 -->
    <import-question-bank-dialog
      v-model:isShowDialog="isShowDialog"
      :currentBank="currentBank"
    />
  </v-container>
</template>

<script lang="ts">
export default {
  name: 'QuesitonBank', // 组件名称
}
</script>

<script setup lang="ts">
import { ref, watch } from 'vue' // 导入Vue的响应式数据
import { useI18n } from 'vue-i18n' // 导入国际化插件
import { useFetch } from '@/hooks' // 导入自定义hook
import { BANK_API } from '@/apis' // 导入问题库相关API
import { QuesitonBankType } from '@/components/card/QuestionBankCard.vue' // 导入问题库类型

const { locale } = useI18n() // 获取当前语言

// 处理问题库分类
const bankCategories = ref(['all']) // 问题库分类
const selectedCategory = ref('all') // 选择的分类
const [getCategories] = useFetch(BANK_API.getCategories) // 获取问题库分类的API
const handleGetCategories = async () => { // 获取问题库分类的函数
  const res = await getCategories(locale.value === 'zh-CN' ? 'zh' : 'en') // 发送请求
  bankCategories.value.splice(1) // 清空原有分类
  bankCategories.value = bankCategories.value.concat(res.data) // 更新分类
}

// 处理问题库列表
const bankList = ref<QuesitonBankType[]>([]) // 问题库列表
const [getBanks] = useFetch(BANK_API.getBanks) // 获取问题库列表的API
const handleGetBanks = async () => { // 获取问题库列表的函数
  const res = await getBanks({ // 发送请求
    language: locale.value === 'zh-CN' ? 'zh' : 'en', // 语言参数
    category: selectedCategory.value.toLowerCase(), // 分类参数
  })
  bankList.value = res.data // 更新问题库列表
}
const handleChangeCategory = async (category: string) => { // 处理分类切换的函数
  selectedCategory.value = category // 更新选择的分类
  await handleGetBanks() // 获取相应的问题库列表
}

const isShowDialog = ref(false) // 是否显示导入问题库对话框
const currentBank = ref({}) // 当前选择的问题库
const handleClickImportButton = (item: QuesitonBankType) => { // 处理点击导入按钮的函数
  currentBank.value = item // 更新当前选择的问题库
  isShowDialog.value = true // 显示导入问题库对话框
}

// 监听语言变化，重新获取问题库分类和列表
watch(
  locale,
  async () => {
    selectedCategory.value = 'all' // 恢复选择的分类为所有
    await handleGetCategories() // 获取问题库分类
    await handleGetBanks() // 获取问题库列表
  },
  { immediate: true } // 立即执行
)
</script>

<template>
  <!-- 系统状态栏 -->
  <v-system-bar
    window
    style="
      justify-content: space-between;
      padding: 12px 15px;
      height: 45px;
      position: fixed;
      backdrop-filter: blur(8px) drop-shadow(4px 4px 10px rgb(226, 202, 202));
      background-color: transparent;
    "
  >
    <!-- 左侧操作区 -->
    <div class="d-flex align-center">
      <!-- 切换侧边栏显示/隐藏按钮 -->
      <v-btn
        variant="text"
        size="small"
        :icon="rail ? 'mdi-dock-right' : 'mdi-dock-left'"
        @click.stop="rail = !rail"
      />

      <!-- 返回按钮 -->
      <v-btn
        icon="mdi-chevron-left"
        size="small"
        elevation="0"
        variant="text"
        @click="router.back()"
      />
    </div>

    <!-- 右侧操作区 -->
    <div class="d-flex align-center">
      <!-- 语言切换菜单 -->
      <v-menu offset="10">
        <template v-slot:activator="{ props }">
          <v-btn
            icon="mdi-translate"
            size="small"
            elevation="0"
            variant="text"
            v-bind="props"
          />
        </template>

        <!-- 语言切换列表 -->
        <v-list density="compact" nav>
          <v-list-item
            v-for="(item, index) in languageList"
            min-height="30px"
            :key="index"
            :value="index"
            :active="storageLang === item.value"
            @click="handleLangSwitch(item.value)"
          >
            <v-list-item-title>{{ item.label }}</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>

      <!-- 进入个人资料页面按钮 -->
      <v-btn
        icon="mdi-cogs"
        size="small"
        elevation="0"
        variant="text"
        @click="router.push('/profile')"
      />

      <!-- 切换主题按钮 -->
      <v-btn
        size="small"
        elevation="0"
        variant="text"
        :icon="isDark ? 'mdi-emoticon-cool' : 'mdi-emoticon-wink'"
        @click="toggleDark()"
      />
    </div>
  </v-system-bar>
</template>

<script lang="ts">
export default {
  name: 'top-bar',
}
</script>

<script setup lang="ts">
import { useTheme } from 'vuetify'
import { useDark, useToggle, useStorage } from '@vueuse/core'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useMessageStore } from '@/store'

// 初始化路由
const router = useRouter()
const MESSAGE_STORE = useMessageStore()

// 侧边栏显示/隐藏状态
const rail = useStorage('side-bar-rail', true)

// 初始化主题切换
const theme = useTheme()
const isDark = useDark({
  onChanged(dark: boolean) {
    theme.global.name.value = dark ? 'dark' : 'light'
    document.documentElement.setAttribute('theme-mode', dark ? 'dark' : 'light')
  },
})
const toggleDark = useToggle(isDark)

// 初始化语言切换
const preferLang = navigator.language === 'zh-CN' ? 'cn' : navigator.language
const storageLang = useStorage('local-lang', preferLang)
const { locale } = useI18n()
const languageList = [
  {
    value: 'en',
    label: 'English',
  },
  {
    value: 'zh-CN',
    label: '简写中文',
  },
]
const handleLangSwitch = (lang: string) => {
  if (lang === locale.value) return
  MESSAGE_STORE.show('message.switchLang', 'default')
  storageLang.value = lang
  locale.value = lang
}
</script>

<style lang="scss" scoped>
:deep(.v-list-item-title) {
  font-size: 14px !important;
  padding: 3px 10px;
}
</style>

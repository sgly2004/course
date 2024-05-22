<template>
  <!-- 导航抽屉 -->
  <v-navigation-drawer :rail="rail" permanent>
    <!-- Logo & 标题 -->
    <v-list-item
      class="pl-2"
      style="user-select: none; transition: padding 0.2s ease-in-out"
      :class="{
        'py-9': !rail,
        'py-3': rail,
      }"
    >
      <template #prepend>
        <div
          :style="{
            width: rail ? '38px' : '50px',
            height: rail ? '38px' : '50px',
          }"
          class="mr-5"
        >
          <!-- 根据主题显示不同的Logo -->
          <v-img
            v-show="isDark"
            src="/src/assets/images/1.svg"
            lazy-src="/src/assets/images/logo-dark.svg"
            alt="logo-dark"
            width="100%"
          />

          <v-img
            v-show="!isDark"
            src="/src/assets/images/1.svg"
            lazy-src="/src/assets/images/logo.svg"
            alt="logo-light"
            width="100%"
          />
        </div>
      </template>

      <template #title>
        <!-- 根据侧边栏状态显示不同的标题 -->
        <Transition :name="rail ? '' : 'footer'" mode="out-in">
          <h3 v-show="!rail">北邮人笔记</h3>
        </Transition>
      </template>

      <template #subtitle>
        <!-- 根据侧边栏状态显示不同的副标题 -->
        <Transition :name="rail ? '' : 'footer'" mode="out-in">
          <p style="font-size: 12px" v-show="!rail">{{ $t('BUPT noter') }}</p>
        </Transition>
      </template>
    </v-list-item>

    <v-divider></v-divider>

    <!-- 默认导航列表 -->
    <v-list density="compact" nav>
      <v-list-item
        v-for="item in defualtNavList"
        v-show="item.isDisplay"
        :key="item.value"
        :prepend-icon="item.icon"
        :title="item.title"
        :to="item.value"
        :active="route.path === item.value"
      />
    </v-list>

    <v-divider></v-divider>

    <!-- 笔记列表 -->
    <v-list density="compact" nav :loading="NOTE_STORE.getNotesLoading">
      <!-- 添加笔记按钮 -->
      <v-list-item
        prepend-icon="mdi-plus"
        style="padding-left: 7px"
        :title="$t('menus.addNote')"
        :border="true"
        :to="'/addNote'"
        :active="route.path === '/addNote'"
      />

      <!-- 笔记项 -->
      <v-list-item
        v-for="item in NOTE_STORE.notes"
        :key="item.id"
        :prepend-icon="item.icon"
        :title="item.name"
        :to="'/note/' + item.id"
        :active="route.path === '/note/' + item.id"
        :disabled="item.isUploading"
        :append-icon="item.isUploading ? 'mdi-upload' : ''"
      />
    </v-list>

  </v-navigation-drawer>
</template>

<script lang="ts">
export default {
  name: 'side-bar',
}
</script>

<script setup lang="ts">
import { computed, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useStorage } from '@vueuse/core'
import { useDark, useWindowSize } from '@vueuse/core'
import { useI18n } from 'vue-i18n'
import { useNoteStore } from '@/store'

const { t } = useI18n()
const route = useRoute()
const isDark = useDark()
const NOTE_STORE = useNoteStore()

// 处理侧边栏展开状态
const rail = useStorage('side-bar-rail', false)
const { width } = useWindowSize()
watch(width, () => {
  if (width.value <= 1030) rail.value = true
  else rail.value = false
})

// 默认导航列表
const defualtNavList = computed(() => [
  {
    icon: 'mdi-view-dashboard',
    title: t('menus.dashboard'),
    value: '/dashboard',
    isDisplay: false,
  },
  {
    icon: 'mdi-notebook-multiple',
    title: t('menus.notes'),
    value: '/notes',
    isDisplay: true,
  },
  {
    icon: 'mdi-head-question',
    title: t('menus.random'),
    value: '/random',
    isDisplay: true,
  },
  {
    icon: 'mdi-folder-question',
    title: t('menus.questionBank'),
    value: '/question-bank',
    isDisplay: true,
  },
])

// 点击Github按钮处理函数
const handleClickGithub = () => {
  window.open('https://github.com/sgly2004/notebook.git')
}
</script>

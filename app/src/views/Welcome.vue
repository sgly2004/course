<template>
  <!-- 欢迎页面的主要部分 -->
  <section
    class="d-flex justify-center" 
    style="padding-top: 100px; padding-right: 200px" 
  >
    <!-- 图片部分 -->
    <div style="width: 200px; height: 200px" class="mr-10"> <!-- 图片容器，宽高200px，右边距10px -->
      <!-- 根据是否为暗黑模式显示不同的欢迎图片 -->
      <v-img
        v-show="isDark"
        src="/src/assets/images/welcome-dark.svg" 
        :lazy-src="'/src/assets/images/welcome-dark.svg'"
      />
      <v-img
        v-show="!isDark" 
        src="/src/assets/images/welcome-light.svg" 
        :lazy-src="'/src/assets/images/welcome-light.svg'"
      />
    </div>

    <!-- 文字部分 -->
    <div>
      <h2 class="mb-4">WELCOME</h2> <!-- 欢迎标题 -->
      <h4 class="mb-2">Hi I'm BUPTer,</h4> <!-- 个人介绍 -->
      <h4 class="mb-2">hope you enjoy this app</h4> <!-- 希望用户喜欢应用 -->
    </div>
  </section>
</template>

<script setup lang="ts">
import { useDark } from '@vueuse/core' // 导入VueUse库中的useDark功能，用于检测暗黑模式
localStorage.setItem('isWelcome', JSON.stringify(true)) // 将欢迎页标记为已显示
const isDark = useDark() // 获取当前是否为暗黑模式
</script>

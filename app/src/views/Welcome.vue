<template>
  <!-- 欢迎页面的主要部分 -->
  <section
    class="d-flex justify-center" <!-- flex布局，水平居中 -->
    style="padding-top: 100px; padding-right: 200px" <!-- 上边距100px，右边距200px -->
  >
    <!-- 图片部分 -->
    <div style="width: 200px; height: 200px" class="mr-10"> <!-- 图片容器，宽高200px，右边距10px -->
      <!-- 根据是否为暗黑模式显示不同的欢迎图片 -->
      <v-img
        v-show="isDark" <!-- 如果为暗黑模式，则显示暗黑图片 -->
        src="/src/assets/images/welcome-dark.svg" <!-- 暗黑模式图片路径 -->
        :lazy-src="'/src/assets/images/welcome-dark.svg'"
      />
      <v-img
        v-show="!isDark" <!-- 如果不是暗黑模式，则显示亮色图片 -->
        src="/src/assets/images/welcome-light.svg" <!-- 亮色模式图片路径 -->
        :lazy-src="'/src/assets/images/welcome-light.svg'"
      />
    </div>

    <!-- 文字部分 -->
    <div>
      <h2 class="mb-4">WELCOME</h2> <!-- 欢迎标题 -->
      <h4 class="mb-2">Hi I'm leyoo,</h4> <!-- 个人介绍 -->
      <h4 class="mb-2">hope you enjoy this app</h4> <!-- 希望用户喜欢应用 -->
      <h4>If you like this app, I hope you can give me a ⭐</h4> <!-- 提示用户给予好评 -->
    </div>
  </section>
</template>

<script setup lang="ts">
import { useDark } from '@vueuse/core' // 导入VueUse库中的useDark功能，用于检测暗黑模式
localStorage.setItem('isWelcome', JSON.stringify(true)) // 将欢迎页标记为已显示
const isDark = useDark() // 获取当前是否为暗黑模式
</script>

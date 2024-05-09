<template>
  <!-- 布局 -->
  <v-layout>
    <!-- Vue应用程序 -->
    <v-app>
      <!-- 侧边栏 -->
      <SideBar style="position: fixed" />
      <!-- 默认视图 -->
      <DefaultView />
    </v-app>
  </v-layout>
</template>

<script lang="ts" setup>
// 引入侧边栏组件和默认视图组件
import SideBar from './SideBar.vue'
import DefaultView from './View.vue'
</script>

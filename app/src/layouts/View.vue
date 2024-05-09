<template>
  <!-- 主要内容区域 -->
  <v-main>
    <!-- 顶部导航栏 -->
    <TopBar />

    <!-- 页面内容区域 -->
    <section class="mt-3">
      <!-- 路由视图 -->
      <RouterView v-slot="{ Component }">
        <!-- 使用动画过渡 -->
        <template v-if="Component">
          <Transition name="fade-transition" mode="out-in">
            <Suspense>
              <!-- 根据当前路由组件动态加载 -->
              <component :is="Component" :key="$route.fullPath"></component>
            </Suspense>
          </Transition>
        </template>
      </RouterView>
    </section>
  </v-main>
</template>

<script lang="ts" setup>
// 引入顶部导航栏组件
import TopBar from './TopBar.vue'
</script>

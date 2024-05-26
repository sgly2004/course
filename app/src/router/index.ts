import { createRouter, createWebHistory } from 'vue-router' // 导入vue-router的相关函数
import NProgress from '@/plugins/nprogress' // 导入NProgress插件

const routes = [ // 路由配置数组
  {
    path: '/', // 根路径
    component: () => import('@/layouts/Default.vue'), // 根布局组件
    redirect: () => { // 重定向函数，根据localStorage中的是否显示欢迎页面决定重定向到欢迎页面或笔记页面
      if (!JSON.parse(localStorage.getItem('isWelcome')!)) return '/welcome' // 如果未显示欢迎页面，则重定向到欢迎页面
      else return '/notes' // 否则重定向到笔记页面
    },
    children: [ // 子路由数组
      {
        path: '/welcome', // 欢迎页面路径
        name: 'Welcome', // 欢迎页面名称
        component: () => import('@/views/Welcome.vue'), // 欢迎页面组件
      },
      {
        path: '/dashboard', // 仪表盘路径
        name: 'Dashboard', // 仪表盘名称
        component: () => import('@/views/Dashboard.vue'), // 仪表盘组件
      },
      {
        path: '/notes', // 笔记页面路径
        name: 'Notes', // 笔记页面名称
        component: () => import('@/views/Notes.vue'), // 笔记页面组件
      },
      {
        path: '/random', // 随机页面路径
        name: 'Random', // 随机页面名称
        component: () => import('@/views/Random.vue'), // 随机页面组件
      },
      // {
      //   path: '/question-bank', // 问题库页面路径
      //   name: 'QuesitonBank', // 问题库页面名称
      //   component: () => import('@/views/QuestionBank.vue'), // 问题库页面组件
      // },
      {
        path: '/addNote', // 添加笔记页面路径
        name: 'AddNote', // 添加笔记页面名称
        component: () => import('@/views/AddNote.vue'), // 添加笔记页面组件
      },
      {
        path: '/profile', // 个人资料页面路径
        name: 'Profile', // 个人资料页面名称
        component: () => import('@/views/Profile.vue'), // 个人资料页面组件
      },
      {
        path: '/note/:id', // 笔记详情页面路径，带参数id
        name: 'Note', // 笔记详情页面名称
        component: () => import('@/views/Note.vue'), // 笔记详情页面组件
      },
    ],
  },
]

const router = createRouter({ // 创建路由实例
  history: createWebHistory(process.env.BASE_URL), // 使用HTML5 history模式，基础URL为环境变量中的BASE_URL
  routes, // 路由配置数组
})

router.beforeEach((to, from, next) => { // 全局前置守卫，在每次路由切换前触发
  NProgress.start() // 开始进度条动画
  next() // 继续路由导航
})

router.afterEach(() => { // 全局后置钩子，在每次路由切换后触发
  NProgress.done() // 完成进度条动画
  NProgress.remove() // 移除进度条
})

export default router // 导出路由实例

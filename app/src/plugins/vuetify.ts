import '@mdi/font/css/materialdesignicons.css' // 导入 Material Design Icons 字体图标的 CSS 文件
import 'vuetify/styles' // 导入 Vuetify 的样式文件
import { createVuetify } from 'vuetify' // 导入 createVuetify 函数

// 导出一个通过 createVuetify 函数创建的 Vuetify 实例，用于配置 Vuetify 主题
export default createVuetify({
  // 主题配置
  theme: {
    // 亮色主题
    themes: {
      light: {
        // 定义颜色变量
        colors: {
          background: '#FFFFFF', // 背景色
          surface: '#FFFFFF', // 表面颜色
          primary: '#7d09f1', // 主要颜色
          secondary: '#03DAC6', // 次要颜色
          'primary-darken-1': '#474787', // 主要颜色变暗
          'secondary-darken-1': '#018786', // 次要颜色变暗
          error: '#B00020', // 错误颜色
          info: '#2196F3', // 信息颜色
          success: '#4CAF50', // 成功颜色
          warning: '#FB8C00', // 警告颜色
          gray: '#3f3f46', // 灰色
        },
      },
      // 暗色主题
      dark: {
        // 定义颜色变量
        colors: {
          background: '#1e1e1e', // 背景色
          surface: '#1e1e1e', // 表面颜色
          primary: '#a858f9', // 主要颜色
          secondary: '#03DAC6', // 次要颜色
          'primary-darken-1': '#474787', // 主要颜色变暗
          'secondary-darken-1': '#018786', // 次要颜色变暗
          gray: '#71717a', // 灰色
        },
      },
    },
  },
})

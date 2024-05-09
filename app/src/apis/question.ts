import _axios from '@/plugins/axios' // 导入axios插件，使用_axios命名，@符号代表src目录的绝对路径

export const QUESTION_API = {
  // 获取问题的最新答案
  getLastAnswer(id: number) {
    return _axios({
      method: 'GET',
      url: `/api/question/${id}/lastAnswer`, // 拼接请求URL，使用问题ID获取最新答案
    })
  },

  // 获取问题的文档
  getDocument(id: number) {
    return _axios({
      method: 'GET',
      url: `/api/question/${id}/document`, // 拼接请求URL，使用问题ID获取文档
    })
  },

  // 获取随机问题
  getRandomQuestion() {
    return _axios({
      method: 'GET',
      url: '/api/question/random', // 请求随机问题的URL
    })
  },

  // 检查答案
  examingAnswer(data: any) {
    return fetch('/api/question/examine', {
      method: 'POST', // 发送POST请求
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json', // 设置请求头为JSON格式
      },
      body: JSON.stringify(data), // 将数据转换为JSON字符串并作为请求体发送
    })
  },
}

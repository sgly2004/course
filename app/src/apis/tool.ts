import _axios from '@/plugins/axios'

export const TOOL_API = {
  getTagVersion() {
    return _axios({
      method: 'GET',
      url: 'https://github.com/sgly2004/notebook/tags',
    })
  },
}

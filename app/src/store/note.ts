import { defineStore } from 'pinia'
import { NOTE_API } from '@/apis'
import { useFetch } from '@/hooks'
import { useFileStore, type UploadingFileItem } from './file'

// 定义状态的类型
type State = {
  notes: NoteItem[] // 笔记列表
  currentIcon: string // 当前图标
  getNotesLoading: boolean // 获取笔记加载状态
}

// 笔记项的类型
export type NoteItem = {
  id: number // 笔记ID
  name: string // 笔记名称
  icon: string // 笔记图标
  upload_date?: string // 上传日期（可选）
  isUploading?: boolean // 是否正在上传（可选）
}

// 初始状态
const state: State = {
  notes: [], // 笔记列表为空数组
  currentIcon: '', // 当前图标为空字符串
  getNotesLoading: false, // 获取笔记加载状态为假
}

// 定义笔记存储
export const useNoteStore = defineStore('noteStore', {
  state: () => state,

  actions: {
    // 异步获取笔记列表
    async getNotes() {
      const [_getNotes, loading] = useFetch(NOTE_API.getNotes) // 使用自定义hook进行笔记列表获取
      // @ts-ignore
      this.$state.getNotesLoading = loading // 将加载状态设置为获取笔记的加载状态
      const { data } = await _getNotes() // 获取笔记数据
      this.$state.notes = data // 将笔记数据存储到状态中
    },

    // 设置笔记是否正在上传的状态
    setIsUploadingNotes() {
      const FILE_STORE = useFileStore() // 使用文件存储hook
      const noteIdsSet = new Set(
        FILE_STORE.uploadingFiles.map((item: UploadingFileItem) => item.note_id) // 获取正在上传的文件的笔记ID集合
      )

      // 遍历笔记列表，设置每个笔记是否正在上传
      this.$state.notes.forEach((note: NoteItem) => {
        note.isUploading = noteIdsSet.has(note.id)
      })
    },
  },
})

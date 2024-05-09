<template>
  <v-container style="max-width: 1080px">
    <!-- 主要内容 -->
    <section v-if="NOTE_STORE.notes.length">
      <h2>
        {{ $t('title.notes') }}
      </h2>
      <h5 class="text-medium-emphasis">{{ $t('subTitle.notes') }}</h5>

      <v-divider class="mt-8"></v-divider>

      <section class="d-flex flex-row pt-5">
        <Transition name="v-fade-transition">
          <!-- 如果不是正在更改笔记 -->
          <v-card
            v-if="!isChangeNote"
            class="flex-1-1 px-3"
            color="transparent"
            :elevation="0"
          >
            <!-- 笔记名称和图标 -->
            <note-header v-bind="currentNote" :index="currentIndex" />

            <!-- 添加文件按钮 -->
            <v-btn
              variant="tonal"
              class="mt-3 mb-3"
              prepend-icon="mdi-text-box-plus-outline"
              style="height: 36px"
              :block="true"
              @click="isShowUploadDialog = true"
            >
              {{ $t('button.addFile') }}
            </v-btn>

            <!-- 文件表格 -->
            <v-card class="pt-1" color="transparent" :elevation="0">
              <files-table :id="currentNote.id" />
            </v-card>
          </v-card>
        </Transition>

        <!-- 侧边栏：标签、笔记信息和删除笔记 -->
        <section class="ml-5">
          <!-- 标签 -->
          <v-card
            class="align-self-start"
            width="240px"
            :color="defaultBgColor"
            :elevation="0"
          >
            <v-tabs direction="vertical">
              <v-tab
                v-for="(item, index) in NOTE_STORE.notes"
                v-model="currentIndex"
                class="text-body-1"
                :value="index"
                :key="item.id"
                @click="handleClickTab(index)"
              >
                <v-icon start> {{ item.icon }} </v-icon>
                {{ item.name }}
              </v-tab>
            </v-tabs>
          </v-card>

          <!-- 笔记信息 -->
          <v-card
            class="align-self-start mt-3"
            :color="defaultBgColor"
            :elevation="0"
          >
            <Transition name="fade-transition">
              <v-list
                v-if="!isChangeNote"
                lines="two"
                :bg-color="defaultBgColor"
              >
                <v-list-item
                  :title="$t('title.createDate')"
                  :subtitle="handleDatetime(currentNote.upload_date!)"
                />
                <!-- 不要删除
                <v-list-item :title="$t('title.finishedAmount')" subtitle="10" />
                <v-list-item :title="$t('title.totalAmount')" subtitle="200" /> -->
              </v-list>
            </Transition>
          </v-card>

          <!-- 删除按钮 -->
          <v-btn
            v-if="!isShowConfirmDeleteBtn"
            block
            class="mt-3"
            id="delete_btn"
            type="icon"
            variant="tonal"
            :color="orangeBgColor"
            @click="isShowConfirmDeleteBtn = true"
          >
            <v-icon
              icon="mdi-delete-empty"
              style="font-size: 20px; margin-right: 8px"
            />
            {{ $t('button.deleteNote') }}
          </v-btn>
          <!-- 确认删除按钮 -->
          <v-btn
            v-show="isShowConfirmDeleteBtn"
            block
            class="mt-3"
            id="delete_btn"
            type="icon"
            variant="tonal"
            :color="greenBgColor"
            :loading="deleteNodeLoading"
            @click="handleDeleteNote"
          >
            <v-icon
              icon="mdi-check-all"
              style="font-size: 20px; margin-right: 8px"
            />
            {{ $t('button.confirmDelete') }}
          </v-btn>
        </section>
      </section>
    </section>

    <!-- 空提示块 -->
    <empty-block v-else type="note">
      <h2 class="mb-2">{{ $t('title.emptyNote') }}</h2>
      <h4 class="d-flex align-center">
        {{ $t('subTitle.emptyNoteStart') }}
        <v-btn
          variant="text"
          color="primary"
          class=""
          @click="$router.push('/addNote')"
        >
          {{ $t('menus.addNote') }}
        </v-btn>
        {{ $t('subTitle.emptyNoteEnd') }}
      </h4>
    </empty-block>

    <!-- 上传文件对话框 -->
    <upload-file-dialog
      v-model="isShowUploadDialog"
      :noteId="currentNote && currentNote.id"
      :noteName="currentNote && currentNote.name"
      @submitted="handleUploadSubmit"
    />
  </v-container>
</template>

<script lang="ts">
export default {
  name: 'Notes',
}
</script>

<script setup lang="ts">
import { ref, nextTick } from 'vue'
import { useNoteStore } from '@/store'
import { NOTE_API } from '@/apis'
import { useFetch } from '@/hooks'
import {
  defaultBgColor,
  orangeBgColor,
  greenBgColor,
  handleDatetime,
} from '@/utils'

const NOTE_STORE = useNoteStore()
const isShowUploadDialog = ref(false)

// 处理点击标签事件
let currentNote = NOTE_STORE.notes[0]
NOTE_STORE.currentIcon = currentNote ? currentNote.icon : ''
const currentIndex = ref(0)
const isChangeNote = ref(false)
const handleClickTab = async (index: number) => {
  if (index === currentIndex.value) return
  currentIndex.value = index
  switchNote()
}

// 处理删除笔记事件
const isShowConfirmDeleteBtn = ref(false)
const [deleteNote, deleteNodeLoading] = useFetch(
  NOTE_API.deleteNote,
  'delete successfully'
)
const handleDeleteNote = async () => {
  const { code } = await deleteNote(currentNote.id)
  if (code !== 0) return
  await NOTE_STORE.getNotes()
  const length = NOTE_STORE.notes.length

  if (!length) return
  if (currentIndex.value === length) currentIndex.value = length - 1

  switchNote()
}

// 处理切换笔记标签事件
const switchNote = () => {
  isShowConfirmDeleteBtn.value = false
  isChangeNote.value = true
  currentNote = NOTE_STORE.notes[currentIndex.value]
  NOTE_STORE.currentIcon = currentNote ? currentNote.icon : ''
  nextTick(() => {
    isChangeNote.value = false
  })
}

// 处理提交上传文件事件
const handleUploadSubmit = () => {
  isShowUploadDialog.value = false
  isChangeNote.value = true
  nextTick(() => {
    isChangeNote.value = false
  })
}
</script>

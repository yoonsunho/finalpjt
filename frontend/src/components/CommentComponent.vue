<template>
  <div>
    <form @submit.prevent="store.createComment">
      <fwb-textarea
        v-model="store.newComment"
        :rows="3"
        custom
        label="댓글"
        placeholder="댓글을 입력하세요."
      >
        <template #footer>
          <div class="flex items-center justify-between">
            <fwb-button type="submit"> 댓글 작성 </fwb-button>
          </div>
        </template>
      </fwb-textarea>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { FwbA, FwbButton, FwbTextarea } from 'flowbite-vue'
import { useArticleStore } from '@/stores/article'

const store = useArticleStore()
</script>

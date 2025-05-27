<template>
  <div class="create-article">
    <h2 class="form-title">{{ isEditMode ? '글 수정' : '새 글 작성' }}</h2>

    <form @submit.prevent="handleSubmit">
      <input v-model="title" class="input" placeholder="제목" required />
      <select v-model="category" class="input" required>
        <option disabled value="">카테고리 선택</option>
        <option value="REVIEW">예적금 후기</option>
        <option value="TIP">절약 꿀팁</option>
        <option value="FREE">자유게시판</option>
      </select>
      <textarea v-model="content" class="textarea" placeholder="내용" rows="10" required></textarea>

      <button class="submit-btn" type="submit">
        {{ isEditMode ? '수정 완료' : '작성 완료' }}
      </button>

      <button v-if="isEditMode" class="delete-btn" type="button" @click="handleDelete">
        삭제하기
      </button>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useArticleStore } from '@/stores/article'

const route = useRoute()
const router = useRouter()
const store = useArticleStore()

const title = ref('')
const content = ref('')
const category = ref('')

const isEditMode = computed(() => route.query.mode === 'edit')
const articleId = computed(() => route.query.id)

watch(
  () => store.articleDetail,
  (newDetail) => {
    if (newDetail && isEditMode.value && newDetail.id == articleId.value) {
      console.log('데이터 로드됨:', newDetail)
      title.value = newDetail.title || ''
      content.value = newDetail.content || ''
      category.value = newDetail.category || ''
    }
  },
  { immediate: true, deep: true },
)

onMounted(() => {
  console.log('수정 모드:', isEditMode.value, '글 ID:', articleId.value)

  if (isEditMode.value && articleId.value) {
    if (store.articleDetail && store.articleDetail.id == articleId.value) {
      title.value = store.articleDetail.title || ''
      content.value = store.articleDetail.content || ''
      category.value = store.articleDetail.category || ''
    } else {
      store.getArticleDetail(articleId.value)
    }
  }
})

const handleSubmit = () => {
  const payload = {
    title: title.value,
    content: content.value,
    category: category.value,
  }

  if (isEditMode.value && articleId.value) {
    store
      .updateArticle(articleId.value, payload)
      .then((res) => {
        alert('수정 완료!')
        console.log(res.data)
        router.push({ name: 'ArticleDetail', params: { id: res.data.id } })
      })
      .catch((err) => {
        console.error('수정 실패:', err.response?.data || err)
        alert('수정 실패')
      })
  } else {
    store
      .createArticle(payload)
      .then((res) => {
        alert('작성 완료!')
        router.push({ name: 'ArticleDetail', params: { id: res.data.id } })
      })
      .catch((err) => {
        console.error('작성 실패:', err.response?.data || err)
        alert('작성 실패')
      })
  }
}

const handleDelete = () => {
  if (confirm('정말 삭제할까요?')) {
    store
      .deleteArticle(articleId.value)
      .then(() => {
        alert('삭제 완료!')
        router.push('/community')
      })
      .catch((err) => {
        console.error('삭제 실패:', err.response?.data || err)
        alert('삭제 실패')
      })
  }
}
</script>
<style scoped>
* {
  font-family: 'Pretendard', sans-serif;
  box-sizing: border-box;
}

.create-article {
  max-width: 640px;
  margin: 40px auto;
  padding: 32px 20px;
  background-color: #ffffff;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
}

.form-title {
  font-size: 24px;
  font-weight: 700;
  color: #191f28;
  text-align: center;
  margin-bottom: 32px;
}

.input,
.textarea {
  width: 100%;
  padding: 14px 16px;
  font-size: 15px;
  border: 1px solid #e5e8eb;
  border-radius: 12px;
  background-color: #f9fafb;
  margin-bottom: 20px;
  transition: border-color 0.2s ease;
}

.input:focus,
.textarea:focus {
  border-color: #3182f6;
  background-color: #ffffff;
  outline: none;
}

.textarea {
  resize: vertical;
  min-height: 180px;
}

.submit-btn,
.delete-btn {
  width: 100%;
  padding: 14px;
  font-size: 15px;
  font-weight: 600;
  border-radius: 12px;
  cursor: pointer;
  transition: background-color 0.2s ease;
  border: none;
  margin-bottom: 12px;
}

.submit-btn {
  background-color: #3182f6;
  color: white;
}

.submit-btn:hover {
  background-color: #1b64da;
}

.delete-btn {
  background-color: #f1f3f5;
  color: #4e5968;
}

.delete-btn:hover {
  background-color: #e5e8eb;
}
</style>

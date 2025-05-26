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
      .then(() => {
        alert('수정 완료!')
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
.create-article {
  max-width: 600px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

.form-title {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 2rem;
  text-align: center;
}

.input,
.textarea {
  width: 100%;
  border: none;
  border-bottom: 1px solid #ccc;
  padding: 0.75rem 0;
  font-size: 1rem;
  margin-bottom: 1.5rem;
  background-color: transparent;
}

.input:focus,
.textarea:focus {
  border-bottom: 1px solid #000;
  outline: none;
}

.submit-btn,
.delete-btn {
  width: 100%;
  padding: 0.9rem 0;
  font-weight: 600;
  font-size: 1rem;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  margin-bottom: 1rem;
}

.submit-btn {
  background: #000;
  color: #fff;
}

.delete-btn {
  background: #eee;
  color: #000;
}
</style>

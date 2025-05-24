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
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useArticleStore } from '@/stores/article'

const route = useRoute()
const router = useRouter()
const store = useArticleStore()

const title = ref('')
const content = ref('')
const category = ref('')
const isEditMode = computed(() => !!route.params.id)

onMounted(() => {
  if (isEditMode.value) {
    store.getArticleDetail(route.params.id)
    // articleDetail은 ref니까 onMounted에서 바로 접근 가능
    setTimeout(() => {
      const detail = store.articleDetail
      if (detail) {
        title.value = detail.title
        content.value = detail.content
        category.value = detail.category
      }
    }, 100) // 잠깐 딜레이 주면 store에서 값 들어오고 세팅됨
  }
})

const handleSubmit = () => {
  const payload = {
    title: title.value,
    content: content.value,
    category: category.value,
  }

  if (isEditMode.value) {
    store
      .updateArticle(route.params.id, payload)
      .then(() => {
        router.push(`/community/${route.params.id}`)
      })
      .catch((err) => {
        console.error('수정 실패:', err.response?.data || err)
      })
  } else {
    store
      .createArticle(payload)
      .then((res) => {
        router.push(`/community/${res.data.id}`)
      })
      .catch((err) => {
        console.error('작성 실패:', err.response?.data || err)
      })
  }
}

const handleDelete = () => {
  if (confirm('정말 삭제할까요? ㅠㅠ')) {
    store
      .deleteArticle(route.params.id)
      .then(() => {
        router.push({ name: 'CommunityPage' })
      })
      .catch((err) => {
        console.error('삭제 실패:', err.response?.data || err)
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

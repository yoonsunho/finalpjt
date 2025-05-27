<template>
  <div class="table-wrapper">
    <div class="category-title">
      <h2>{{ categoryLabels[store.selectedCategory] || '커뮤니티' }}</h2>
    </div>

    <div class="filter-bar">
      <select v-model="store.selectedOrdering" @change="handleOrderingChange">
        <option value="">기본 정렬</option>
        <option value="latest">최신순</option>
        <option value="oldest">등록일순</option>
        <option value="popular">인기순</option>
      </select>
      <select v-model="searchField">
        <option value="title">제목</option>
        <option value="content">내용</option>
        <option value="nickname">작성자</option>
      </select>

      <input v-model="searchQuery" placeholder="검색어 입력" @keyup.enter="searchArticles" />
      <button @click="searchArticles">검색</button>
    </div>

    <table class="custom-table">
      <thead>
        <tr>
          <th>번호</th>
          <th>제목</th>
          <th>작성자</th>
          <th>작성일</th>
          <th>좋아요</th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="(article, index) in store.articles"
          :key="article.id"
          @click="$router.push({ name: 'ArticleDetail', params: { id: article.id } })"
        >
          <td>{{ index + 1 }}</td>
          <td class="highlight">
            <RouterLink :to="{ name: 'ArticleDetail', params: { id: article.id } }">
              {{ article.title }}
            </RouterLink>
          </td>
          <td>{{ article.user }}</td>
          <td>{{ formatDate(article.created_at) }}</td>
          <td>{{ article.likes_count || 0 }}</td>
        </tr>
      </tbody>
    </table>

    <div class="write-button" v-if="accountStore.isLogin">
      <RouterLink :to="{ name: 'CreateArticle' }">
        <button>글 작성하기</button>
      </RouterLink>
    </div>
  </div>
</template>

<script setup>
import { onMounted, watch, ref } from 'vue'
import { useArticleStore } from '@/stores/article'
import { useRoute, RouterLink } from 'vue-router'
import { useAccountStore } from '@/stores/user'
const accountStore = useAccountStore()
const store = useArticleStore()
const route = useRoute()
const searchField = ref('title')
const searchQuery = ref('')

const categoryLabels = {
  REVIEW: '예적금 후기',
  TIP: '절약 꿀팁',
  FREE: '자유게시판',
}

watch(
  () => route.params.category,
  (newCategory) => {
    if (newCategory) {
      store.selectedCategory = newCategory.toUpperCase()
      store.getArticles()
    }
  },
  { immediate: true },
)

const formatDate = (isoString) => {
  const date = new Date(isoString)
  return date.toLocaleString('ko-KR', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  })
}

const handleOrderingChange = () => {
  console.log('정렬 변경:', store.selectedOrdering)
  store.getArticles()
}

const searchArticles = () => {
  store.getArticles({
    search_field: searchField.value,
    search: searchQuery.value,
  })
}

onMounted(() => {
  if (route.params.category) {
    store.selectedCategory = route.params.category.toUpperCase()
  }
  store.getArticles()
})
</script>
<style scoped>
* {
  font-family: 'Pretendard', sans-serif;
  box-sizing: border-box;
}

.table-wrapper {
  margin: 2rem auto;
  padding: 2rem 1.5rem;
  border-radius: 16px;
  background-color: #ffffff;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
  max-width: 1000px;
}

.category-title h2 {
  font-size: 24px;
  font-weight: 600;
  margin-bottom: 1.5rem;
  color: #1f2937;
}

.filter-bar {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  justify-content: flex-end;
  margin-bottom: 1.5rem;
}

.filter-bar select,
.filter-bar input {
  padding: 0.5rem 0.75rem;
  font-size: 14px;
  border-radius: 10px;
  border: 1px solid #e5e7eb;
  background-color: #f9fafb;
  outline: none;
  transition: border-color 0.2s;
}

.filter-bar select:focus,
.filter-bar input:focus {
  border-color: #3b82f6;
}

.filter-bar button {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 10px;
  background-color: #3b82f6;
  color: white;
  font-weight: 600;
  transition: background-color 0.2s;
}

.filter-bar button:hover {
  background-color: #2563eb;
}

.custom-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0 8px;
}

.custom-table thead th {
  text-align: left;
  font-size: 13px;
  color: #6b7280;
  padding: 0.75rem 1rem;
}

.custom-table tbody tr {
  background-color: #f9fafb;
  border-radius: 12px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.03);
  transition: transform 0.15s ease;
  cursor: pointer;
}

.custom-table tbody tr:hover {
  transform: translateY(-2px);
}

.custom-table td {
  padding: 0.75rem 1rem;
  font-size: 14px;
  color: #111827;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.highlight {
  color: #2563eb;
  font-weight: 600;
}

.write-button {
  margin-top: 2rem;
  text-align: right;
}

.write-button button {
  padding: 0.75rem 1.5rem;
  background-color: #111827;
  color: #ffffff;
  border: none;
  border-radius: 12px;
  font-weight: 600;
  transition: background-color 0.2s;
}

.write-button button:hover {
  background-color: #374151;
}
</style>

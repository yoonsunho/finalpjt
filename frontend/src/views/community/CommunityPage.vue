<template>
  <div class="table-wrapper">
    <div class="category-title">
      <h2>{{ categoryLabels[store.selectedCategory] || '전체 게시글' }}</h2>
    </div>

    <div class="filter-bar">
      <select v-model="store.selectedOrdering" @change="handleOrderingChange">
        <option value="">기본 정렬</option>
        <option value="latest">최신순</option>
        <option value="oldest">등록일순</option>
        <option value="popular">인기순</option>
      </select>
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

    <div class="write-button">
      <RouterLink :to="{ name: 'CreateArticle' }">
        <button>글 작성하기</button>
      </RouterLink>
    </div>
  </div>
</template>

<script setup>
import { onMounted, watch } from 'vue'
import { useArticleStore } from '@/stores/article'
import { useRoute, RouterLink } from 'vue-router'

const store = useArticleStore()
const route = useRoute()

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
    } else {
      store.selectedCategory = ''
    }
    store.getArticles()
  },
  { immediate: true },
)

const changeCategory = (category) => {
  store.selectedCategory = category
  store.getArticles()
}

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

// onMounted(() => {
//   store.getArticles()
// })
</script>

<style scoped>
.table-wrapper {
  /* max-width: 1000px; */
  margin: 2rem auto;
  background-color: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  overflow-x: auto;
  padding: 1rem;
}

.custom-table {
  width: 100%;
  border-collapse: collapse;
  font-family: 'Segoe UI', sans-serif;
  font-size: 15px;
  color: #191f28;
}

.custom-table thead {
  background-color: #f1f5f9;
  text-transform: uppercase;
  font-size: 13px;
  color: #191f28;
}

.custom-table th,
.custom-table td {
  padding: 14px 16px;
  border-bottom: 1px solid #e5e7eb;
  text-align: left;
}

.custom-table tbody tr {
  transition: background-color 0.2s;
  cursor: pointer;
}

.custom-table tbody tr:hover {
  background-color: #f0f4f8;
}

.highlight {
  font-weight: bold;
  color: #2563eb;
}

.filter-bar {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 1rem;
}

.filter-bar select {
  padding: 0.5rem;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  background-color: white;
  cursor: pointer;
}

.write-button {
  text-align: right;
  margin-top: 1rem;
}

.write-button button {
  background-color: #3b82f6;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 6px;
  cursor: pointer;
  font-weight: bold;
  transition: background-color 0.2s;
}

.write-button button:hover {
  background-color: #2563eb;
}
</style>

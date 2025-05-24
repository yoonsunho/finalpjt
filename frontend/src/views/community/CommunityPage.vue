<template>
  <div class="table-wrapper">
    <div class="category-filter">
      
      <button @click="filterByCategory('REVIEW')">예적금 후기</button>
      <button @click="filterByCategory('TIP')">절약 꿀팁</button>
      <button @click="filterByCategory('FREE')">자유게시판</button>
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
          <!-- <td>{{ article.category }}</td> -->
          <td>{{ article.created_at }}</td>
          <td>{{ article.likes_count }}</td>
        </tr>
      </tbody>
    </table>
    <div>
      <RouterLink :to="{ name: 'CreateArticle' }"><button>글 작성하기</button></RouterLink>
    </div>
  </div>
</template>

<script setup>
// import { ref } from 'vue'
import { RouterLink } from 'vue-router'
import { ref, onMounted } from 'vue'
import { useArticleStore } from '@/stores/article'

const store = useArticleStore()
const selectedCategory = ref('REVIEW')

const filterByCategory = (category) => {
  selectedCategory.value = category
  store.getArticles(category)
}
onMounted(() => {
  store.getArticles(selectedCategory.value)
})
</script>

<style scoped>
.table-wrapper {
  max-width: 1000px;
  margin: 2rem auto;
  /* padding: 1rem; */
  background-color: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  overflow-x: auto;
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

.category-filter {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-bottom: 1rem;
}

.category-filter button {
  background-color: #e0e7ff;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  font-weight: bold;
}

.category-filter button:hover {
  background-color: #c7d2fe;
}
</style>

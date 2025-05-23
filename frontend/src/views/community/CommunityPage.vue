<template>
  <table class="article-table">
    <thead>
      <tr>
        <th>번호</th>
        <th>제목</th>
        <th>작성자</th>
        <th>카테고리</th>
        <th>작성일</th>
        <th>좋아요</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="(article, index) in store.articles" :key="article.id">
        <td>{{ index + 1 }}</td>
        <td>
          <RouterLink :to="{ name: 'ArticleDetail', params: { id: article.id } }">
            {{ article.title }}
          </RouterLink>
        </td>
        <td>{{ article.user }}</td>
        <td>{{ article.category }}</td>
        <td>{{ article.created_at }}</td>
        <td>{{ article.likes_count }}</td>
      </tr>
    </tbody>
  </table>
</template>

<script setup>
// import { ref } from 'vue'
import { RouterLink } from 'vue-router'
import { onMounted } from 'vue'
import { useArticleStore } from '@/stores/article'

const store = useArticleStore()

onMounted(() => {
  store.getArticles()
})
</script>

<style scoped>
.article-table {
  width: 100%;
  border-collapse: collapse;
  text-align: center;
}
.article-table th,
.article-table td {
  border: 1px solid #ccc;
  padding: 8px;
}
.article-table th {
  background-color: #f4f4f4;
}
</style>

<template>
  <div class="category-title">
    <h2>{{ categoryLabels[store.selectedCategory] || '커뮤니티' }}</h2>
    <p class="subtext"></p>
    <!-- <hr /> -->
  </div>
  <div class="table-wrapper">
    <div class="filter-bar">
      <div class="left">
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
      </div>
      <div><button @click="searchArticles">검색</button></div>
    </div>

    <fwb-table hoverable>
      <fwb-table-head>
        <fwb-table-head-cell>번호</fwb-table-head-cell>
        <fwb-table-head-cell>제목</fwb-table-head-cell>
        <fwb-table-head-cell>작성자</fwb-table-head-cell>
        <fwb-table-head-cell>작성일</fwb-table-head-cell>
        <fwb-table-head-cell>좋아요</fwb-table-head-cell>
      </fwb-table-head>
      <fwb-table-body>
        <fwb-table-row
          v-for="(article, index) in store.articles"
          :key="article.id"
          class="hover:cursor-pointer hover:bg-gray-100"
          @click="$router.push({ name: 'ArticleDetail', params: { id: article.id } })"
        >
          <fwb-table-cell>{{ index + 1 }}</fwb-table-cell>
          <fwb-table-cell class="highlight">
            <RouterLink :to="{ name: 'ArticleDetail', params: { id: article.id } }">
              {{ article.title }}
            </RouterLink>
          </fwb-table-cell>
          <fwb-table-cell>{{ article.user }}</fwb-table-cell>
          <fwb-table-cell>{{ formatDate(article.created_at) }}</fwb-table-cell>
          <fwb-table-cell>{{ article.likes_count || 0 }}</fwb-table-cell>
        </fwb-table-row>
      </fwb-table-body>
    </fwb-table>

    <div class="write-button" v-if="accountStore.isLogin">
      <RouterLink :to="{ name: 'CreateArticle' }">
        <button>글 작성하기</button>
      </RouterLink>
    </div>
  </div>
</template>

<script setup>
import {
  FwbTable,
  FwbTableBody,
  FwbTableCell,
  FwbTableHead,
  FwbTableHeadCell,
  FwbTableRow,
} from 'flowbite-vue'
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

.category-title h2 {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 8px;
  text-align: center;
}

.subtext {
  font-size: 1.1rem;
  text-align: center;
  color: black;
  margin: 0;
}
.left {
  flex-grow: 1;
}
.table-wrapper {
  margin: 0px auto;
  /* padding: 32px 20px; */
  /* max-width: 960px; */
  width: 100%;
  background-color: #ffffff;
  border-radius: 16px;
  /* box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03); */
}
select {
  /* gap: 16px; */
  margin-right: 20px;
}
.filter-bar {
  /* max-width: 1200px; */
  width: 100%;
  margin: 0 auto 24px;
  padding: 24px;
  background: #ffffff;
  border: 1px solid #f2f4f6;
  border-radius: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  align-items: center;
  /* justify-content: space-between; */
}

.filter-bar select,
.filter-bar input {
  padding: 10px 14px;
  font-size: 14px;
  border: 1px solid #e5e8eb;
  border-radius: 10px;
  background-color: #f9fafb;
  color: #191f28;
  min-width: 120px;
  transition: border-color 0.2s;
}

.filter-bar select:focus,
.filter-bar input:focus {
  border-color: #3182f6;
  outline: none;
}

.filter-bar button {
  padding: 10px 16px;
  background-color: #3182f6;
  color: #ffffff;
  border: none;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s;
}

.filter-bar button:hover {
  background-color: #1b64da;
}

.custom-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0 10px;
}

.custom-table thead th {
  text-align: left;
  font-size: 13px;
  color: #8b95a1;
  padding: 12px 16px;
}

.custom-table tbody tr {
  background-color: #f9fafb;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
  transition: transform 0.15s ease;
  cursor: pointer;
}

.custom-table tbody tr:hover {
  transform: translateY(-2px);
}

.custom-table td {
  padding: 12px 16px;
  font-size: 14px;
  color: #4e5968;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.highlight {
  color: #3182f6;
  font-weight: 600;
}

.write-button {
  margin-top: 32px;
  text-align: right;
}

.write-button button {
  padding: 12px 20px;
  background-color: #191f28;
  color: #ffffff;
  border: none;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 600;
  transition: background-color 0.2s;
}

.write-button button:hover {
  background-color: #2a3441;
}

/* 반응형 */
@media (max-width: 768px) {
  .filter-bar {
    flex-direction: column;
    align-items: stretch;
  }

  .filter-bar input,
  .filter-bar select,
  .filter-bar button {
    width: 100%;
  }

  .category-title h2 {
    text-align: center;
  }

  .custom-table td,
  .custom-table th {
    font-size: 13px;
    padding: 10px;
  }
}
</style>

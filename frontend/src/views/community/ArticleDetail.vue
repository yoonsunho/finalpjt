<template>
  <div class="article-container" v-if="store.articleDetail">
    <div class="article-header">
      <p class="article-category"># {{ store.articleDetail.category }}</p>
      <h1 class="article-title">{{ store.articleDetail.title }}</h1>
      <p class="username">{{ store.articleDetail.user }}</p>
      <p class="created_at">{{ store.articleDetail.created_at }}</p>
    </div>
    <div class="article-content">
      <p>{{ store.articleDetail.content }}</p>
    </div>
    <div class="article-footer">
      <button type="button" class="like-article" @click="toggleLike">
        좋아요 {{ store.articleDetail.likes_count }}
      </button>
    </div>
    <hr />
    <CommentComponent />
  </div>
</template>

<script setup>
import CommentComponent from '@/components/CommentComponent.vue'
// import { ref } from 'vue'
import { onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useArticleStore } from '@/stores/article'

const route = useRoute()
const store = useArticleStore()

const articleId = route.params.id

onMounted(() => {
  store.getArticleDetail(articleId)
})
</script>

<style scoped>
.article-container {
  padding: 0px 20rem;
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
}
.article-header {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
}
h1 {
  font-size: 2rem;
  font-weight: bold;
}
.created_at {
  color: #888;
  font-size: 0.8rem;
}
.like-article {
  background-color: dodgerblue;
  color: white;
}
</style>

<template>
  <div class="article-container" v-if="store.articleDetail">
    <div class="article-card">
      <div class="article-header">
        <p class="article-category"># {{ store.articleDetail.category }}</p>
        <h1 class="article-title">{{ store.articleDetail.title }}</h1>
        <div class="article-meta">
          <span class="username">{{ store.articleDetail.user }}</span>
          <span class="created_at">{{ store.articleDetail.created_at }}</span>
        </div>
      </div>
      <div class="article-content">
        <p>{{ store.articleDetail.content }}</p>
      </div>
      <div class="article-footer">
        <button type="button" class="like-button" @click="store.toggleLike(articleId)">
          {{ store.articleDetail.is_liked ? '💔 좋아요 취소' : '❤️ 좋아요' }}
          {{ store.articleDetail.likes_count }}
        </button>
        <div v-if="accountStore.token && accountStore.user_id === store.articleDetail.user_id">
          <button @click="editArticle">수정</button>
          <button @click="deleteArticle">삭제</button>
        </div>
      </div>
      <hr class="divider" />
      <div class="comment">
        <div v-if="accountStore.isLogin">
          <!-- <textarea v-model="newComment" placeholder="댓글을 작성하세요" />
          <button @click="createComment">작성</button> -->
          <CommentComponent />
        </div>
      </div>
    </div>
  </div>
  <div class="comment-container">
    <div v-for="comment in store.comments" :key="comment.id" class="border p-2 mb-2">
      <!-- 수정 중일 때 -->
      <div v-if="store.editCommentId === comment.id">
        <input v-model="store.editContent" class="border p-1 w-full" />
        <button @click="store.updateComment(comment.id)" class="text-blue-600 mr-2">저장</button>
        <button @click="store.editCommentId = null" class="text-gray-500">취소</button>
      </div>
      <!-- 평소 표시 -->
      <div v-else>
        <!-- 디버깅 -->
        <div class="text-xs text-gray-400 mb-2">
          로그인상태={{ accountStore.isLogin }}, 댓글작성자={{ comment.user }}, 로그인유저={{
            accountStore.userInfo.nickname
          }}
        </div>
        <p>{{ comment.user }} {{ comment.content }}</p>
        <!-- 로그인 상태이고 댓글단 유저가 로그인한 유저이면 -->
        <div v-if="accountStore.isLogin && comment.user === accountStore.userInfo.nickname">
          <button @click="store.startEdit(comment)" class="text-sm text-blue-600 mr-2">수정</button>
          <button @click="store.deleteComment(comment.id)" class="text-sm text-red-600">
            삭제
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import CommentComponent from '@/components/CommentComponent.vue'
// import { ref } from 'vue'
import { onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useArticleStore } from '@/stores/article'
import { useAccountStore } from '@/stores/user'

const route = useRoute()
const router = useRouter()
const store = useArticleStore()
const accountStore = useAccountStore()

const articleId = route.params.id
const editArticle = () => {
  router.push({ name: 'CreateArticle', query: { mode: 'edit', id: articleId } })
}
const deleteArticle = () => {
  if (confirm('정말 삭제할까요?')) {
    store
      .deleteArticle(articleId)
      .then(() => {
        alert('삭제 완료!')
        router.push('/community')
      })
      .catch((err) => {
        console.error('삭제 실패:', err)
        alert('삭제 실패 ㅠㅠ')
      })
  }
}
onMounted(() => {
  store.getArticleDetail(articleId)
  store.getComments(articleId)
})
</script>
<style scoped>
.article-container {
  min-width: 1200px;
  margin: 1rem auto;
  padding: 1rem;
  /* box-shadow: inset 0 0 3px dodgerblue; */
}

.article-card {
  display: flex;
  flex-direction: column;
  gap: 10px;
  background-color: #fff;
  padding: 3rem;
  border-radius: 12px;
  width: 100%;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.article-header {
  margin-bottom: 1.5rem;
}

.article-category {
  font-size: 14px;
  font-weight: bold;
  color: #2563eb;
  margin-bottom: 0.5rem;
}

.article-title {
  font-size: 2rem;
  font-weight: 700;
  color: #191f28;
  margin-bottom: 0.25rem;
}

.article-meta {
  font-size: 0.8rem;
  color: #6b7280;
  display: flex;
  gap: 1rem;
}

.article-content {
  font-size: 1rem;
  line-height: 1.7;
  color: #374151;
  margin-bottom: 2rem;
}

.article-footer {
  text-align: center;
}

.like-button {
  background-color: #2563eb;
  color: white;
  padding: 10px;
  font-size: 0.8rem;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  transition: background-color 0.17s ease-in-out;
}

.like-button:hover {
  background-color: #1e40af;
}

.divider {
  margin-top: 3rem;
  border: none;
  border-top: 1px solid #e5e7eb;
}
</style>

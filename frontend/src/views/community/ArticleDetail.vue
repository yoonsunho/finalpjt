<template>
  <div class="article-container" v-if="store.articleDetail">
    <div class="article-card">
      <div class="article-header">
        <p class="article-category"># {{ store.articleDetail.category }}</p>
        <h1 class="article-title">{{ store.articleDetail.title }}</h1>
        <div class="article-meta">
          <span class="username">{{ store.articleDetail.user }}</span>
          <span class="created_at">{{ formatDate(store.articleDetail.created_at) }}</span>
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
        <!-- 글 작성자만 보이게 -->
        <div
          v-if="accountStore.isLogin && accountStore.userInfo.nickname === store.articleDetail.user"
        >
          <button @click="editArticle">수정</button>
          <button @click="deleteArticle">삭제</button>
        </div>
      </div>
      <hr class="divider" />
      <!-- 댓글 작성 영역 -->
      <div class="comment">
        <div v-if="accountStore.isLogin">
          <CommentComponent />
        </div>
        <div v-else class="text-sm text-gray-500 mt-2">댓글을 작성하려면 로그인이 필요해요.</div>
      </div>

      <!-- 댓글 목록은 항상 보여줌 -->
      <div class="comment-container">
        <div v-for="comment in store.comments" :key="comment.id" class="border p-2 mb-2">
          <!-- 수정 중일 때 -->
          <div v-if="store.editCommentId === comment.id">
            <input v-model="store.editContent" class="border p-1 w-full" />
            <button @click="store.updateComment(comment.id)" class="text-blue-600 mr-2">
              저장
            </button>
            <button @click="store.editCommentId = null" class="text-gray-500">취소</button>
          </div>
          <!-- 기본 댓글 표시 -->
          <div v-else>
            <p>
              <strong>{{ comment.user }}</strong> {{ comment.content }}
            </p>
            <div v-if="accountStore.isLogin && comment.user === accountStore.userInfo.nickname">
              <button @click="store.startEdit(comment)" class="text-sm text-blue-600 mr-2">
                수정
              </button>
              <button @click="store.deleteComment(comment.id)" class="text-sm text-red-600">
                삭제
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div v-for="comment in store.comments" :key="comment.id" class="">
    <!-- 수정 중일 때 -->
    <div v-if="store.editCommentId === comment.id">
      <input v-model="store.editContent" class="border p-1 w-full" />
      <button @click="store.updateComment(comment.id)" class="text-blue-600 mr-2">저장</button>
      <button @click="store.editCommentId = null" class="text-gray-500">취소</button>
    </div>
    <!-- 평소 표시 -->
    <div v-else>
      <div v-if="accountStore.isLogin && comment.user === accountStore.userInfo.nickname">
        <button @click="store.startEdit(comment)" class="text-sm text-blue-600 mr-2">수정</button>
        <button @click="store.deleteComment(comment.id)" class="text-sm text-red-600">삭제</button>
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
        alert('삭제 실패')
      })
  }
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

onMounted(() => {
  store.getArticleDetail(articleId)
  store.getComments(articleId)
})
</script>

<style scoped>
* {
  font-family: 'Pretendard', sans-serif;
  box-sizing: border-box;
}

.article-container {
  max-width: 800px;
  margin: 2rem auto;
  padding: 0 1rem;
}

.article-card {
  background: #ffffff;
  border-radius: 20px;
  padding: 2.5rem;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.05);
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.article-header {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.article-category {
  font-size: 13px;
  font-weight: 600;
  color: #3b82f6;
  letter-spacing: 0.5px;
}

.article-title {
  font-size: 28px;
  font-weight: 700;
  color: #111827;
  margin: 0;
}

.article-meta {
  font-size: 13px;
  color: #6b7280;
  display: flex;
  gap: 0.75rem;
}

.article-content {
  font-size: 15px;
  color: #374151;
  line-height: 1.7;
  white-space: pre-wrap;
}

.article-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
}

.like-button {
  background-color: #3b82f6;
  color: white;
  font-weight: 600;
  padding: 0.6rem 1.2rem;
  border-radius: 9999px;
  font-size: 14px;
  border: none;
  transition: background-color 0.2s ease;
  cursor: pointer;
}

.like-button:hover {
  background-color: #2563eb;
}

.article-footer > div button {
  margin-left: 0.5rem;
  background: transparent;
  border: 1px solid #d1d5db;
  padding: 0.4rem 0.9rem;
  font-size: 13px;
  border-radius: 9999px;
  cursor: pointer;
  color: #374151;
  transition: background-color 0.2s ease;
}

.article-footer > div button:hover {
  background-color: #f3f4f6;
}

.divider {
  border: none;
  border-top: 1px solid #e5e7eb;
}

.comment-container {
  max-width: 800px;
  margin: 2rem auto;
  padding: 0 1rem;
}

.comment-container .border {
  background: #f9fafb;
  border-radius: 12px;
  padding: 1rem;
  font-size: 14px;
  color: #374151;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
}

.comment-container input {
  border: 1px solid #d1d5db;
  padding: 0.5rem 0.75rem;
  width: 100%;
  border-radius: 8px;
  margin-bottom: 0.5rem;
}

.comment-container button {
  font-size: 13px;
  margin-right: 0.5rem;
  border: none;
  background: none;
  cursor: pointer;
}

.comment-container .text-blue-600 {
  color: #3b82f6;
}

.comment-container .text-red-600 {
  color: #ef4444;
}

.comment-container .text-gray-500 {
  color: #6b7280;
}

.text-xs {
  font-size: 12px;
  color: #9ca3af;
}
</style>

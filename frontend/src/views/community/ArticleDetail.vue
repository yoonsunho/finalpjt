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
  margin: 0;
  padding: 0;
}

.article-container {
  width: 100%;
  margin: 32px auto;
  /* padding: 0 16px; */
}

.article-card {
  background: #ffffff;
  border: 1px solid #f1f3f5;
  border-radius: 20px;
  padding: 50px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
  display: flex;
  flex-direction: column;
  gap: 32px;
}

.article-header {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.article-category {
  font-size: 13px;
  font-weight: 600;
  color: #3182f6;
}

.article-title {
  font-size: 26px;
  font-weight: 700;
  color: #191f28;
  margin-bottom: 4px;
}

.article-meta {
  font-size: 13px;
  color: #8b95a1;
  display: flex;
  gap: 8px;
}

.article-content {
  font-size: 15px;
  color: #4e5968;
  line-height: 1.7;
  white-space: pre-wrap;
}

.article-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
}

.like-button {
  background-color: #3182f6;
  color: #ffffff;
  font-weight: 600;
  padding: 10px 20px;
  border-radius: 9999px;
  font-size: 14px;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
}

.like-button:hover {
  background-color: #1b64da;
}

.article-footer > div button {
  margin-left: 8px;
  background: #f9fafb;
  border: 1px solid #e5e8eb;
  padding: 8px 16px;
  font-size: 13px;
  border-radius: 9999px;
  color: #4e5968;
  cursor: pointer;
  transition: all 0.2s ease;
}

.article-footer > div button:hover {
  background-color: #f1f3f5;
}

.divider {
  border: none;
  border-top: 1px solid #e5e8eb;
}

.comment-container {
  margin-top: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.comment-container .border {
  background: #f8f9fa;
  border-radius: 12px;
  padding: 16px;
  font-size: 14px;
  color: #374151;
  border: 1px solid #e5e8eb;
}

.comment-container input {
  border: 1px solid #d1d5db;
  padding: 10px 14px;
  width: 100%;
  border-radius: 10px;
  margin-bottom: 8px;
  font-size: 14px;
}

.comment-container button {
  font-size: 13px;
  margin-right: 6px;
  border: none;
  background: none;
  cursor: pointer;
  font-weight: 500;
}

.comment-container .text-blue-600 {
  color: #3182f6;
}

.comment-container .text-red-600 {
  color: #ef4444;
}

.comment-container .text-gray-500 {
  color: #8b95a1;
}

.text-xs {
  font-size: 12px;
  color: #9ca3af;
}

/* 반응형 */
@media (max-width: 640px) {
  .article-card {
    padding: 24px;
  }

  .article-title {
    font-size: 22px;
  }

  .like-button {
    width: 100%;
    text-align: center;
  }

  .article-footer {
    flex-direction: column;
    align-items: stretch;
  }

  .article-footer > div {
    width: 100%;
    margin-top: 8px;
  }

  .article-footer > div button {
    width: 100%;
    margin-left: 0;
    margin-top: 8px;
  }
}
</style>

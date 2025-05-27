<template>
  <div class="detail-page">
    <div v-if="video" class="detail-container">
      <button class="back-button" @click="goBack">
        <svg
          width="20"
          height="20"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
        >
          <polyline points="15,18 9,12 15,6"></polyline>
        </svg>
        뒤로가기
      </button>

      <div class="video-header">
        <h1 class="video-title">{{ video.snippet.title }}</h1>
        <div class="video-meta">
          <span class="channel-name">{{ video.snippet.channelTitle }}</span>
          <span class="separator">•</span>
          <span class="upload-date">{{ formatDate(video.snippet.publishedAt) }}</span>
        </div>
      </div>

      <div class="video-player-container">
        <div class="video-frame">
          <iframe
            :src="`https://www.youtube.com/embed/${videoId}?autoplay=0&rel=0&modestbranding=1`"
            frameborder="0"
            allowfullscreen
            title="YouTube video player"
          ></iframe>
        </div>
      </div>

      <div class="video-description-container">
        <h3 class="description-title">동영상 설명</h3>
        <div class="description-content">
          <p class="description" :class="{ expanded: isDescriptionExpanded }">
            {{ video.snippet.description || '설명이 없습니다.' }}
          </p>
          <button
            v-if="video.snippet.description && video.snippet.description.length > 200"
            @click="toggleDescription"
            class="toggle-description"
          >
            {{ isDescriptionExpanded ? '접기' : '더보기' }}
          </button>
        </div>
      </div>
    </div>

    <div v-else class="loading-container">
      <div class="spinner"></div>
      <p>동영상 정보를 불러오는 중입니다...</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const API_KEY = import.meta.env.VITE_YOUTUBE_API_KEY
const route = useRoute()
const router = useRouter()

const videoId = route.params.id
const video = ref(null)
const isDescriptionExpanded = ref(false)

// 날짜 포맷팅 함수
const formatDate = (dateString) => {
  const date = new Date(dateString)
  const now = new Date()
  const diffTime = Math.abs(now - date)
  const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24))

  if (diffDays === 0) return '오늘'
  if (diffDays === 1) return '1일 전'
  if (diffDays < 7) return `${diffDays}일 전`
  if (diffDays < 30) return `${Math.floor(diffDays / 7)}주 전`
  if (diffDays < 365) return `${Math.floor(diffDays / 30)}개월 전`
  return `${Math.floor(diffDays / 365)}년 전`
}

const fetchVideoDetail = () => {
  const params = new URLSearchParams({
    part: 'snippet,statistics',
    id: videoId,
    key: API_KEY,
  })

  fetch(`https://www.googleapis.com/youtube/v3/videos?${params}`)
    .then((res) => {
      if (!res.ok) throw new Error('API 요청 실패')
      return res.json()
    })
    .then((data) => {
      if (data.items && data.items.length > 0) {
        video.value = data.items[0]
      } else {
        throw new Error('동영상을 찾을 수 없습니다')
      }
    })
    .catch((error) => {
      console.error('동영상 정보 로딩 오류:', error)
      // 오류 처리 로직 추가 가능
    })
}

const goBack = () => {
  router.back()
}

const toggleDescription = () => {
  isDescriptionExpanded.value = !isDescriptionExpanded.value
}

fetchVideoDetail()
</script>

<style scoped>
.detail-page {
  min-height: 100vh;
  /* background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); */
  padding: 20px;
}

.detail-container {
  max-width: 1000px;
  margin: 0 auto;
}

.back-button {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 30px;
  padding: 12px 20px;
  background: rgba(255, 255, 255, 0.9);
  border: none;
  border-radius: 50px;
  cursor: pointer;
  font-weight: 600;
  color: #333;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.back-button:hover {
  background: rgba(255, 255, 255, 1);
  transform: translateY(-2px);
  box-shadow: 0 6px 25px rgba(0, 0, 0, 0.15);
}

.video-header {
  background: rgba(255, 255, 255, 0.95);
  padding: 30px;
  border-radius: 20px;
  margin-bottom: 20px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
}

.video-title {
  font-size: 28px;
  font-weight: 700;
  line-height: 1.3;
  color: #333;
  margin: 0 0 16px 0;
  word-break: keep-all;
}

.video-meta {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 16px;
  color: #666;
}

.channel-name {
  font-weight: 600;
  color: #4a5568;
}

.separator {
  color: #cbd5e0;
}

.upload-date {
  color: #718096;
}

.video-player-container {
  background: rgba(255, 255, 255, 0.95);
  padding: 20px;
  border-radius: 20px;
  margin-bottom: 20px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
}

.video-frame {
  position: relative;
  padding-bottom: 56.25%; /* 16:9 비율 */
  height: 0;
  overflow: hidden;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.video-frame iframe {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  border-radius: 16px;
}

.video-description-container {
  background: rgba(255, 255, 255, 0.95);
  padding: 30px;
  border-radius: 20px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
}

.description-title {
  font-size: 20px;
  font-weight: 600;
  color: #333;
  margin: 0 0 20px 0;
}

.description-content {
  position: relative;
}

.description {
  font-size: 16px;
  line-height: 1.6;
  color: #4a5568;
  white-space: pre-wrap;
  word-break: break-word;
  margin: 0;
  max-height: 120px;
  overflow: hidden;
  transition: max-height 0.3s ease;
}

.description.expanded {
  max-height: none;
}

.toggle-description {
  margin-top: 16px;
  padding: 8px 16px;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 20px;
  cursor: pointer;
  font-weight: 600;
  font-size: 14px;
  transition: all 0.3s ease;
}

.toggle-description:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 60vh;
  text-align: center;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 20px;
  padding: 60px 20px;
  margin: 0 auto;
  max-width: 600px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
}

.loading-container p {
  font-size: 18px;
  color: #666;
  margin-top: 20px;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 4px solid rgba(102, 126, 234, 0.2);
  border-top: 4px solid #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .detail-page {
    padding: 10px;
  }

  .video-header {
    padding: 20px;
    margin-bottom: 15px;
  }

  .video-title {
    font-size: 22px;
  }

  .video-meta {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }

  .separator {
    display: none;
  }

  .video-player-container {
    padding: 15px;
    margin-bottom: 15px;
  }

  .video-description-container {
    padding: 20px;
  }

  .description-title {
    font-size: 18px;
  }

  .description {
    font-size: 14px;
  }
}

@media (max-width: 480px) {
  .back-button {
    padding: 10px 16px;
    font-size: 14px;
  }

  .video-title {
    font-size: 20px;
    line-height: 1.4;
  }

  .video-meta {
    font-size: 14px;
  }

  .video-player-container {
    padding: 10px;
  }

  .video-description-container {
    padding: 15px;
  }
}
</style>

<template>
  <div>
    <div class="header-content">
      <h1 class="title">주식 정보 검색</h1>
      <p class="subtext">관심 종목과 관련된 동영상을 검색할 수 있어요.</p>
      <br /><br />
      <hr />
    </div>
  </div>
  <div class="container">
    <div class="search-container">
      <div class="search-box">
        <input
          type="text"
          ref="searchInput"
          v-model="searchQuery"
          placeholder="YouTube 동영상을 검색해 보세요."
          @keyup.enter="searchVideos"
          class="search-input"
        />
        <button @click="searchVideos" class="search-button">
          <svg
            width="20"
            height="20"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
          >
            <circle cx="11" cy="11" r="8"></circle>
            <path d="m21 21-4.35-4.35"></path>
          </svg>
          검색
        </button>
      </div>
    </div>

    <div class="content">
      <div v-if="loading" class="status-message">
        <div class="spinner"></div>
        <p>검색 중입니다...</p>
      </div>

      <div v-else-if="error" class="status-message error-state">
        <div class="error-icon">⚠️</div>
        <p>{{ error }}</p>
        <button @click="searchVideos" class="retry-button">다시 시도</button>
      </div>

      <div v-else-if="!hasSearched" class="status-message welcome-state">
        <div class="search-icon">🔍</div>
        <h3>영상을 찾아보세요</h3>
        <p>관심 있는 주제나 키워드를 검색해 보세요.</p>
      </div>

      <div v-else-if="videos.length === 0" class="status-message no-results">
        <div class="empty-icon">📭</div>
        <h3>검색 결과가 없습니다</h3>
        <p>"{{ lastSearchQuery }}"에 대한 결과를 찾을 수 없습니다</p>
      </div>

      <div v-else class="results">
        <div class="results-header">
          <!-- <h3>검색 결과 ({{ videos.length }}개)</h3> -->

          <h3>검색 결과</h3>
          <p>"{{ lastSearchQuery }}"에 대한 결과</p>
        </div>

        <div class="video-grid">
          <div v-for="video in videos" :key="video.id.videoId" class="video-item">
            <RouterLink
              :to="{ name: 'StockInfoDetailView', params: { id: video.id.videoId } }"
              class="video-link"
            >
              <div class="thumbnail-container">
                <img
                  :src="video.snippet.thumbnails.medium.url"
                  :alt="video.snippet.title"
                  class="thumbnail"
                />
                <div class="play-overlay">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="white">
                    <polygon points="5,3 5,21 19,12"></polygon>
                  </svg>
                </div>
              </div>

              <div class="video-info">
                <h4 class="video-title">{{ video.snippet.title }}</h4>
                <p class="channel-name">{{ video.snippet.channelTitle }}</p>
                <p class="upload-date">{{ formatDate(video.snippet.publishedAt) }}</p>
              </div>
            </RouterLink>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineOptions({ name: 'StockInfoView' })
import { ref, onMounted } from 'vue'
import { useRoute, useRouter, RouterLink } from 'vue-router'

const API_KEY = import.meta.env.VITE_YOUTUBE_API_KEY
const searchQuery = ref('')
const videos = ref([])
const loading = ref(false)
const error = ref(null)
const hasSearched = ref(false)
const lastSearchQuery = ref('')
const route = useRoute()
const router = useRouter()
const searchInput = ref(null)

onMounted(() => {
  searchInput.value?.focus()

  // 마운트 시 쿼리에서 검색어 복원
  const queryFromRoute = route.query.q
  if (queryFromRoute) {
    searchQuery.value = queryFromRoute
    searchVideos()
  }
})

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

// 동영상 검색
const searchVideos = () => {
  if (!searchQuery.value.trim()) return

  // 쿼리로 검색어 반영
  router.replace({ query: { q: searchQuery.value } })

  loading.value = true
  error.value = null
  hasSearched.value = true
  lastSearchQuery.value = searchQuery.value

  const params = new URLSearchParams({
    part: 'snippet',
    maxResults: 50,
    q: searchQuery.value,
    type: 'video',
    key: API_KEY,
  })

  fetch(`https://www.googleapis.com/youtube/v3/search?${params}`)
    .then((response) => {
      if (!response.ok) throw new Error('API 요청에 실패했습니다')
      return response.json()
    })
    .then((data) => {
      videos.value = data.items || []
      loading.value = false
    })
    .catch((err) => {
      console.error('API 요청 오류:', err)
      error.value = '동영상을 불러오는 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요.'
      loading.value = false
    })
}
</script>

<style scoped>
* {
  font-family: 'Pretendard', sans-serif;
  box-sizing: border-box;
}

.container {
  min-height: 100vh;
  padding: 20px;
}

.search-container {
  display: flex;
  justify-content: center;
  padding-top: 40px;
  margin-bottom: 40px;
}

.search-box {
  display: flex;
  align-items: center;
  gap: 8px;
  max-width: 600px;
  width: 100%;
  padding: 8px;
  border-radius: 50px;
  background: rgba(255, 255, 255, 0.95);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.03);
  backdrop-filter: blur(10px);
}

.search-input {
  flex: 1;
  padding: 16px 24px;
  border: none;
  background: transparent;
  font-size: 16px;
  color: #333;
  outline: none;
}

.search-input::placeholder {
  color: #888;
}

.search-input:focus {
  border: 2px solid dodgerblue;
  border-radius: 50px;
}

.search-button {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 16px 24px;
  background: dodgerblue;
  color: white;
  border: none;
  border-radius: 50px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.search-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 10px rgba(30, 144, 255, 0.4);
}

.content {
  /* max-width: 1200px; */
  width: 100%;
  margin: 0 auto;
}

.header {
  text-align: center;
  margin-top: 10px;
  /* margin-bottom: 10px; */
  /* padding-bottom: 50px; */
}

hr {
  color: #eeeeee;
  font-weight: bold;
}
.header-content h1 {
  text-align: center;
  font-size: 2.5rem;
  font-weight: 700;
  /* margin-bottom: 8px; */
}

.subtext {
  text-align: center;
  font-size: 1.1rem;
  color: black;
  /* margin-bottom: 30px; */
}

/* 상태 메시지 공통 */
.status-message {
  text-align: center;
  padding: 60px 20px;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 20px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.04);
  backdrop-filter: blur(10px);
}

.welcome-state .search-icon,
.error-state .error-icon,
.no-results .empty-icon {
  font-size: 48px;
  margin-bottom: 20px;
}

.welcome-state h3,
.no-results h3 {
  font-size: 24px;
  font-weight: 600;
  color: #333;
  margin-bottom: 12px;
}

.status-message p {
  font-size: 16px;
  color: #666;
}

.error-state p {
  color: #e74c3c;
  margin-bottom: 20px;
}

.retry-button {
  padding: 12px 24px;
  background: #3498db;
  color: white;
  border: none;
  border-radius: 25px;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.3s;
}

.retry-button:hover {
  background: #2980b9;
}

.spinner {
  width: 40px;
  height: 40px;
  margin: 0 auto 20px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3498db;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  100% {
    transform: rotate(360deg);
  }
}

.results {
  padding: 30px;
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.95);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
}

.results-header {
  text-align: center;
  margin-bottom: 30px;
}

.results-header h3 {
  font-size: 24px;
  font-weight: 600;
  color: #333;
  margin-bottom: 8px;
}

.results-header p {
  font-size: 14px;
  color: #666;
}

.video-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 24px;
}

.video-item {
  transition:
    transform 0.3s ease,
    box-shadow 0.3s ease;
}

.video-item:hover {
  transform: translateY(-4px);
}

.video-link {
  display: block;
  border-radius: 16px;
  overflow: hidden;
  background: white;
  text-decoration: none;
  color: inherit;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
}

.video-link:hover {
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);
}

.thumbnail-container {
  position: relative;
  width: 100%;
  padding-bottom: 56.25%;
  overflow: hidden;
}

.thumbnail {
  position: absolute;
  width: 100%;
  height: 100%;
  object-fit: cover;
  top: 0;
  left: 0;
  transition: transform 0.3s ease;
}

.video-link:hover .thumbnail {
  transform: scale(1.05);
}

.play-overlay {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 60px;
  height: 60px;
  background: rgba(0, 0, 0, 0.7);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.video-link:hover .play-overlay {
  opacity: 1;
}

.video-info {
  padding: 20px;
}

.video-title {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin-bottom: 12px;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.channel-name {
  font-size: 14px;
  color: #666;
  margin-bottom: 6px;
  font-weight: 500;
}

.upload-date {
  font-size: 12px;
  color: #999;
}

/* 반응형 */
@media (max-width: 768px) {
  .container {
    padding: 10px;
  }

  .search-container {
    padding-top: 20px;
    margin-bottom: 30px;
  }

  .search-box {
    flex-direction: column;
    border-radius: 16px;
    padding: 16px;
  }

  .search-button {
    justify-content: center;
    border-radius: 12px;
  }

  .video-grid {
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 16px;
  }

  .status-message {
    padding: 40px 20px;
  }

  .welcome-state h3 {
    font-size: 22px;
  }
}

@media (max-width: 480px) {
  .video-grid {
    grid-template-columns: 1fr;
  }

  .search-input {
    font-size: 16px;
  }
}
</style>

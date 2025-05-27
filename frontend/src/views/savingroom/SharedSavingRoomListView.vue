<template>
  <div class="room-list">
    <div class="header">
      <div class="header-content">
        <h1>공동 저축방 리스트</h1>
        <p class="subtitle">친구들과 함께 목표를 달성해보세요</p>
      </div>
      <button @click="goToCreate" class="btn-create">
        <svg
          width="20"
          height="20"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
        >
          <path d="M12 5v14M5 12h14" />
        </svg>
        방 만들기
      </button>
    </div>

    <!-- 검색창 -->
    <form class="search-bar" @submit.prevent="applyFilter">
      <input v-model="filters.name" type="text" placeholder="방 제목" />
      <input v-model="filters.description" type="text" placeholder="방 설명" />
      <input v-model="filters.owner" type="text" placeholder="방장 닉네임" />
      <button type="submit" class="btn-search">검색</button>
    </form>

    <div v-if="loading" class="loading">
      <div class="spinner"></div>
      <p>저축방을 불러오는 중...</p>
    </div>

    <div v-else-if="error" class="error">
      <div class="error-icon">⚠️</div>
      <h3>오류가 발생했습니다</h3>
      <p>{{ error }}</p>
      <button @click="fetchRooms" class="btn-retry">다시 시도</button>
    </div>

    <div v-else-if="filteredRooms.length === 0" class="empty">
      <div class="empty-illustration">
        <svg
          width="120"
          height="120"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="1.5"
        >
          <path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z" />
          <polyline points="17,21 17,13 7,13 7,21" />
          <polyline points="7,3 7,8 15,8" />
        </svg>
      </div>
      <h2>조건에 맞는 저축방이 없어요</h2>
      <p>검색어를 다시 입력하거나 새로운 방을 만들어보세요!</p>
      <button @click="goToCreate" class="btn-create-empty">
        <svg
          width="20"
          height="20"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
        >
          <path d="M12 5v14M5 12h14" />
        </svg>
        첫 번째 저축방 만들기
      </button>
    </div>

    <div v-else class="content">
      <div class="room-grid">
        <div
          v-for="room in filteredRooms"
          :key="room.id"
          class="room-item"
          @click="goToRoom(room.id)"
        >
          <SharedSavingRoomCard :room="room" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import SharedSavingRoomCard from '@/components/savingroom/SharedSavingRoomCard.vue'
import axios from 'axios'

import { useAccountStore } from '@/stores/user'

const accountStore = useAccountStore()
const API_URL = 'http://127.0.0.1:8000'
const rooms = ref([])
const loading = ref(false)
const error = ref('')
const router = useRouter()

const activeRoomsCount = computed(() => {
  if (!rooms.value || !Array.isArray(rooms.value)) return 0
  return rooms.value.filter((room) => room.status === 'active' || room.is_active).length
})

const goToRoom = (id) => {
  router.push({
    name: 'SharedSavingRoomDetailView',
    params: { id: id.toString() },
  })
}

const goToCreate = () => {
  router.push({ name: 'SharedSavingRoomCreateView' })
}

const fetchRooms = async () => {
  try {
    loading.value = true
    error.value = ''

    const res = await axios.get(`${API_URL}/savingroom/`, {
      headers: {
        Authorization: `Token ${accountStore.token}`,
      },
    })
    console.log('응답 확인:', res.data)
    // API 응답이 배열인지 확인하고, 아니면 빈 배열로 초기화
    rooms.value = Array.isArray(res.data) ? res.data : []
  } catch (err) {
    console.error('Failed to fetch rooms:', err)
    // 에러 발생 시 빈 배열로 초기화
    rooms.value = []

    if (err.response) {
      if (err.response.status === 401) {
        error.value = '로그인이 필요합니다.'
      } else if (err.response.status === 500) {
        error.value = '서버에 일시적인 문제가 발생했습니다.'
      } else {
        error.value = '데이터를 불러오는데 실패했습니다.'
      }
    } else if (err.request) {
      error.value = '네트워크 연결을 확인해주세요.'
    } else {
      error.value = '알 수 없는 오류가 발생했습니다.'
    }
  } finally {
    loading.value = false
  }
}
const filters = ref({
  name: '',
  description: '',
  owner: '',
})

const filteredRooms = ref([])
const applyFilter = () => {
  const { name, description, owner } = filters.value
  filteredRooms.value = rooms.value.filter((room) => {
    const title = room.name?.toLowerCase() || ''
    const desc = room.description?.toLowerCase() || ''
    const nickname = room.created_by?.toLowerCase() || ''

    return (
      title.includes(name.trim().toLowerCase()) &&
      desc.includes(description.trim().toLowerCase()) &&
      nickname.includes(owner.trim().toLowerCase())
    )
  })
}

onMounted(async () => {
  await fetchRooms()
  filteredRooms.value = rooms.value // 처음엔 전체 보여주기
})
</script>

<style scoped>
.search-bar {
  max-width: 800px;
  margin: 0 auto 32px auto;
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  justify-content: center;
}

.search-bar input {
  padding: 10px 16px;
  font-size: 14px;
  border: 1px solid #cbd5e1;
  border-radius: 10px;
  flex: 1 1 200px;
}

.btn-search {
  background: #3b82f6;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-search:hover {
  background: #2563eb;
}
.room-list {
  max-width: 1400px;
  margin: 0 auto;
  padding: 32px 24px;
  min-height: 100vh;
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 40px;
  background: white;
  padding: 32px;
  border-radius: 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.header-content h1 {
  color: #1e293b;
  margin: 0 0 8px 0;
  font-size: 32px;
  font-weight: 700;
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.subtitle {
  color: #64748b;
  margin: 0;
  font-size: 16px;
  font-weight: 400;
}

.btn-create {
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  color: white;
  border: none;
  padding: 16px 24px;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 8px;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

.btn-create:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(59, 130, 246, 0.4);
}

.btn-create:active {
  transform: translateY(0);
}

.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 20px;
  background: white;
  border-radius: 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #e2e8f0;
  border-top: 3px solid #3b82f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 16px;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.loading p {
  color: #64748b;
  font-size: 16px;
  margin: 0;
}

.error {
  text-align: center;
  padding: 60px 40px;
  background: white;
  border-radius: 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  border-left: 4px solid #ef4444;
}

.error-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.error h3 {
  color: #1e293b;
  margin: 0 0 12px 0;
  font-size: 24px;
  font-weight: 600;
}

.error p {
  color: #64748b;
  margin: 0 0 24px 0;
  font-size: 16px;
}

.btn-retry {
  background: linear-gradient(135deg, #ef4444, #dc2626);
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-retry:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
}

.empty {
  text-align: center;
  padding: 80px 40px;
  background: white;
  border-radius: 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.empty-illustration {
  margin-bottom: 32px;
  opacity: 0.6;
}

.empty-illustration svg {
  color: #94a3b8;
}

.empty h2 {
  color: #1e293b;
  margin: 0 0 12px 0;
  font-size: 28px;
  font-weight: 600;
}

.empty p {
  color: #64748b;
  margin: 0 0 32px 0;
  font-size: 16px;
  line-height: 1.6;
}

.btn-create-empty {
  background: linear-gradient(135deg, #10b981, #059669);
  color: white;
  border: none;
  padding: 16px 32px;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
}

.btn-create-empty:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(16, 185, 129, 0.4);
}

.content {
  space-y: 32px;
}

.stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 32px;
}

.stat-item {
  background: white;
  padding: 24px;
  border-radius: 16px;
  text-align: center;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.2);
  transition: transform 0.3s ease;
}

.stat-item:hover {
  transform: translateY(-4px);
}

.stat-number {
  display: block;
  font-size: 32px;
  font-weight: 700;
  color: #3b82f6;
  margin-bottom: 8px;
}

.stat-label {
  color: #64748b;
  font-size: 14px;
  font-weight: 500;
}

.room-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 24px;
}

.room-item {
  cursor: pointer;
  transition: all 0.3s ease;
  border-radius: 16px;
  overflow: hidden;
}

.room-item:hover {
  transform: translateY(-4px);
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .room-list {
    padding: 16px;
  }

  .header {
    flex-direction: column;
    gap: 20px;
    text-align: center;
    padding: 24px;
  }

  .header-content h1 {
    font-size: 24px;
  }

  .room-grid {
    grid-template-columns: 1fr;
  }

  .stats {
    grid-template-columns: 1fr;
  }

  .empty {
    padding: 60px 20px;
  }

  .empty h2 {
    font-size: 24px;
  }
}

@media (max-width: 480px) {
  .header-content h1 {
    font-size: 20px;
  }

  .btn-create,
  .btn-create-empty {
    padding: 12px 20px;
    font-size: 14px;
  }
}
</style>

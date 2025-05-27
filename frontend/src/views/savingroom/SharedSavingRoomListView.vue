<template>
  <div class="header-content">
    <h1 class="title">공유 저축방</h1>
    <p class="subtext">친구들과 함께 목표를 달성해보세요</p>
    <hr />
    <br />
    <br />
  </div>
  <div class="room-list">
    <div class="header">
      <!-- 방 만들기 버튼 (로그인한 경우에만 표시) -->
      <button v-if="accountStore.isLogin" @click="goToCreate" class="btn-create">
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

    <!-- 검색창 (로그인 상태에서만 표시) -->
    <form class="search-bar" v-if="accountStore.isLogin" @submit.prevent="applyFilter">
      <input v-model="filters.name" type="text" placeholder="방 제목" />
      <input v-model="filters.owner" type="text" placeholder="방장 닉네임" />
      <button type="submit" class="btn-search">검색</button>
    </form>

    <div v-if="!accountStore.isLogin" class="blur-wrapper">
      <div class="blur-list room-grid">
        <div v-for="n in 6" :key="n" class="room-item blur-list-item" style="height: 200px"></div>
      </div>
      <div class="blur-overlay"></div>
      <div class="blur-message">
        <p>저축방 목록은 로그인 후 확인할 수 있어요.</p>
        <RouterLink to="/login" class="btn-login">로그인하러 가기</RouterLink>
      </div>
    </div>
    <div v-else-if="loading" class="loading">
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
      <!-- 탭을 content보다 먼저 렌더링되게 위로 올림 -->
      <div class="tabs" v-if="accountStore.isLogin">
        <button :class="{ active: activeTab === 'incomplete' }" @click="activeTab = 'incomplete'">
          미완료방
        </button>
        <button :class="{ active: activeTab === 'complete' }" @click="activeTab = 'complete'">
          완료방
        </button>
      </div>

      <div class="room-grid">
        <div
          v-for="room in filteredRoomsByTab"
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
const activeTab = ref('incomplete') // 'complete' 또는 'incomplete'
const filteredRoomsByTab = computed(() => {
  return filteredRooms.value.filter((room) =>
    activeTab.value === 'complete' ? room.achievement_rate >= 100 : room.achievement_rate < 100,
  )
})
const accountStore = useAccountStore()
const API_URL = 'http://127.0.0.1:8000'
const rooms = ref([])
const loading = ref(false)
const error = ref('')
const router = useRouter()
const isLogin = computed(() => accountStore.isLogin)
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
.room-list {
  /* max-width: 720px; */
  width: 100%;
  margin: 0 auto;
  padding: 24px 16px;
  background: #ffffff;
}

.header {
  text-align: center;
  margin-top: 10px;
  margin-bottom: 20px;
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
  /* margin-bottom: 28px; */
}

.subtext {
  text-align: center;
  font-size: 1.1rem;
  color: black;
  margin-bottom: 30px;
}

.search-bar {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 24px;
  justify-content: center;
}

.search-bar input {
  padding: 10px 16px;
  font-size: 14px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  flex: 1 1 200px;
}

.btn-search {
  background: #3182f6;
  color: white;
  border: none;
  padding: 10px 16px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
}

.btn-search:hover {
  background: #2563eb;
}
.tabs {
  display: flex;
  width: 100%;
  margin-bottom: 24px;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}

.tabs button {
  flex: 1; /* 반반 차지하도록 */
  padding: 12px 0;
  font-size: 14px;
  font-weight: 600;
  border: none;
  background: #f3f4f6;
  color: #374151;
  cursor: pointer;
  transition: background 0.2s;
}

.tabs button.active {
  background: #3182f6;
  color: white;
}

.room-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.room-item {
  cursor: pointer;
  transition: 0.2s;
  border-radius: 12px;
  overflow: hidden;
}

.room-item:hover {
  transform: translateY(-4px);
}
.btn-create {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 14px;
  background: #10b981;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-create:hover {
  background: #059669;
}

.btn-create svg {
  stroke: white;
}
@media (max-width: 768px) {
  .room-list {
    padding: 16px;
  }

  .header {
    flex-direction: column;
    gap: 16px;
    text-align: center;
  }

  .room-grid {
    grid-template-columns: 1fr;
  }
}
</style>

<template>
  <div class="room-list">
    <div class="header">
      <h1>공동 저축방 리스트</h1>
      <button @click="goToCreate" class="btn-create">➕ 방 만들기</button>
    </div>

    <div v-if="loading" class="loading">로딩 중...</div>

    <div v-else-if="error" class="error">
      {{ error }}
      <button @click="fetchRooms" class="btn-retry">다시 시도</button>
    </div>

    <div v-else-if="rooms.length === 0" class="empty">
      <p>아직 생성된 저축방이 없습니다.</p>
      <button @click="goToCreate" class="btn-create-empty">첫 번째 저축방 만들기</button>
    </div>

    <div v-else class="room-grid">
      <div v-for="room in rooms" :key="room.id" class="room-item" @click="goToRoom(room.id)">
        <SharedSavingRoomCard :room="room" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import SharedSavingRoomCard from '@/components/savingroom/SharedSavingRoomCard.vue'
import axios from 'axios'

const rooms = ref([])
const loading = ref(false)
const error = ref('')
const router = useRouter()

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

    const res = await axios.get('/savingroom/')
    rooms.value = res.data
  } catch (err) {
    console.error('Failed to fetch rooms:', err)

    if (err.response) {
      if (err.response.status === 401) {
        error.value = '로그인이 필요합니다.'
      } else if (err.response.status === 500) {
        error.value = '서버 오류가 발생했습니다.'
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

onMounted(() => {
  fetchRooms()
})
</script>

<style scoped>
.room-list {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.header h1 {
  color: #333;
  margin: 0;
}

.btn-create {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 12px 20px;
  border-radius: 8px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-create:hover {
  background-color: #0056b3;
}

.loading {
  text-align: center;
  padding: 50px;
  font-size: 18px;
  color: #666;
}

.error {
  text-align: center;
  padding: 50px;
  color: #dc3545;
}

.btn-retry {
  background-color: #dc3545;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 6px;
  margin-top: 10px;
  cursor: pointer;
}

.btn-retry:hover {
  background-color: #c82333;
}

.empty {
  text-align: center;
  padding: 50px 20px;
}

.empty p {
  font-size: 18px;
  color: #666;
  margin-bottom: 20px;
}

.btn-create-empty {
  background-color: #28a745;
  color: white;
  border: none;
  padding: 15px 30px;
  border-radius: 8px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-create-empty:hover {
  background-color: #218838;
}

.room-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.room-item {
  cursor: pointer;
  transition: transform 0.2s;
}

.room-item:hover {
  transform: translateY(-2px);
}

@media (max-width: 768px) {
  .header {
    flex-direction: column;
    gap: 15px;
    text-align: center;
  }

  .room-grid {
    grid-template-columns: 1fr;
  }
}
</style>

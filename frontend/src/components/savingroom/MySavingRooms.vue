<template>
  <div>
    <div v-if="loading">불러오는 중...</div>
    <div v-else-if="!depositedRooms.length">입금한 방이 없습니다.</div>
    <div v-else>
      <SharedSavingRoomCard v-for="room in depositedRooms" :key="room.id" :room="room" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import SharedSavingRoomCard from '@/components/savingroom/SharedSavingRoomCard.vue'
import { useAccountStore } from '@/stores/user'

const accountStore = useAccountStore()
const allJoinedRooms = ref([])
const depositedRooms = ref([])
const loading = ref(false)
const fetchJoinedRooms = async () => {
  loading.value = true
  try {
    // 1. 기본 참가한 방 목록 가져오기
    const res = await axios.get('http://localhost:8000/savingroom/my-rooms/joined/', {
      headers: { Authorization: `Token ${accountStore.token}` },
    })
    allJoinedRooms.value = res.data

    // 2. 각 방 상세 호출해서 나의 deposits가 있는지 확인
    const filtered = []

    for (const room of allJoinedRooms.value) {
      try {
        const detailRes = await axios.get(`http://localhost:8000/savingroom/${room.id}/`, {
          headers: { Authorization: `Token ${accountStore.token}` },
        })

        const participants = detailRes.data.participants || []
        const myParticipant = participants.find(
          (p) => p.user?.nickname === accountStore.userInfo.nickname,
        )

        if (myParticipant?.total_saved > 0) {
          filtered.push(detailRes.data)
        }
      } catch (e) {
        console.warn(`방 ${room.id} 상세 조회 실패`, e)
      }
    }

    depositedRooms.value = filtered
  } catch (err) {
    console.error('참여한 방 목록 조회 실패:', err)
  } finally {
    loading.value = false
  }
}

onMounted(fetchJoinedRooms)
</script>

<style scoped>
.my-deposits {
  max-width: 720px;
  margin: 40px auto;
  padding: 32px 20px;
  background-color: #ffffff;
  border-radius: 20px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.06);
  font-family: 'Pretendard', sans-serif;
}

h1 {
  font-size: 1.8rem;
  font-weight: 600;
  color: #212529;
  text-align: center;
  margin-bottom: 32px;
}

.loading-text {
  text-align: center;
  font-size: 1rem;
  color: #6c757d;
  padding: 32px 0;
}

.no-data {
  text-align: center;
  font-size: 1rem;
  color: #868e96;
  padding: 48px 0;
}

.room-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}
</style>

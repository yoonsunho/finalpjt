<template>
  <div v-if="room">
    <h1>{{ room.name }}</h1>
    <p>{{ room.description }}</p>
    <p>목표: {{ room.goal_amount.toLocaleString() }}원</p>
    <p>달성률: {{ room.achievement_rate }}%</p>
    <button v-if="!joined" @click="joinRoom">참가하기</button>

    <SavingInput :roomId="room.id" :socket="socket" />
    <SavingLog :logList="logList" />

    <h2>참가자 목록</h2>
    <ul>
      <li v-for="p in room.participants" :key="p.id">
        {{ p.user.nickname }}: {{ p.total_saved }}원
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import SavingInput from '@/components/savingroom/SavingInput.vue'
import SavingLog from '@/components/savingroom/SavingLog.vue'

const route = useRoute()
const room = ref(null)
const socket = ref(null)
const logList = ref([])
const joined = ref(false)
onMounted(async () => {
  const res = await axios.get(`/api/savingroom/${route.params.id}/`)
  room.value = res.data

  try {
    await axios.post(`/api/savingroom/${route.params.id}/join/`)
    joined.value = true
  } catch (err) {
    if (err.response?.status === 400 && err.response?.data?.detail === '이미 참가한 방입니다.') {
      joined.value = true
    }
  }

  const ws = new WebSocket(`ws://localhost:8000/ws/savings/${route.params.id}/`)
  ws.onmessage = (e) => {
    const data = JSON.parse(e.data)
    logList.value.unshift(data)
  }
  socket.value = ws
})

onBeforeUnmount(() => {
  if (socket.value) socket.value.close()
})

const joinRoom = async () => {
  try {
    await axios.post(`/api/savingroom/${room.value.id}/join/`)
    joined.value = true
  } catch (err) {
    alert('참가 실패')
    console.error(err)
  }
}
</script>

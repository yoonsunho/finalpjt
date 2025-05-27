<template>
  <div>
    <h1>공동 저축방 리스트</h1>
    <button @click="goToCreate">➕ 방 만들기</button>
    <div v-for="room in rooms" :key="room.id">
      <SharedSavingRoomCard :room="room" @click="goToRoom(room.id)" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import SharedSavingRoomCard from '@/components/savingroom/SharedSavingRoomCard.vue'
import axios from 'axios'

const rooms = ref([])
const router = useRouter()

const goToRoom = (id) => {
  router.push({ name: 'SharedSavingRoomDetailView', params: { id } })
}

const goToCreate = () => {
  router.push({ name: 'SharedSavingRoomCreateView' })
}

onMounted(async () => {
  const res = await axios.get('/api/savingroom/')
  rooms.value = res.data
})
</script>

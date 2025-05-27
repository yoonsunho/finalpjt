<template>
  <div class="create-room">
    <h1>공동 저축방 만들기</h1>
    <form @submit.prevent="createRoom">
      <input v-model="name" placeholder="방 이름" required />
      <textarea v-model="description" placeholder="설명" />
      <input v-model.number="goalAmount" type="number" placeholder="목표 금액 (원)" required />
      <input v-model="deadline" type="date" required />
      <button type="submit">생성하기</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const name = ref('')
const description = ref('')
const goalAmount = ref(null)
const deadline = ref('')
const router = useRouter()

const createRoom = async () => {
  try {
    const res = await axios.post('/savingroom/', {
      name: name.value,
      description: description.value,
      goal_amount: goalAmount.value,
      deadline: deadline.value,
    })
    router.push({ name: 'SharedSavingRoomDetailView', params: { id: res.data.id } })
  } catch (err) {
    alert('생성 실패 ㅠㅠ')
    console.error(err)
  }
}
</script>

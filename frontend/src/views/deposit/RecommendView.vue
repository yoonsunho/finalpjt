<template>
  <h1>맞춤추천받기</h1>
  <button @click="getRecommend">맞춤추천받기</button>
  <div></div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import { useAccountStore } from '@/stores/user'

const accountStore = useAccountStore()
const API_URL = 'http://127.0.0.1:8000'

const getRecommend = async () => {
  const userId = accountStore.user_id
  console.log('유저:', accountStore.userInfo)
  console.log('ID:', userId)

  if (!userId) {
    console.warn('로그인이 필요합니다!')
    return
  }

  try {
    const res = await axios.get(`${API_URL}/recommend/${userId}/`, {
      headers: {
        Authorization: `Token ${accountStore.token}`,
      },
    })
    console.log(res.data)
  } catch (error) {
    console.error('추천 요청 실패:', error)
  }
}
</script>

<style scoped></style>

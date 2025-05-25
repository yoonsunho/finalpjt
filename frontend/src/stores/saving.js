import axios from 'axios'
import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { useAccountStore } from './user'

export const useSavingStore = defineStore('saving', () => {
  const accountStore = useAccountStore()
  const API_URL = 'http://127.0.0.1:8000'

  const savingProducts = ref([])
  const likedProducts = ref([])
  const joinedProducts = ref([])
  const joinedSavingDetails = ref([])

  const isLiked = (id) => likedProducts.value.includes(id)
  const isJoined = (id) => joinedProducts.value.includes(id)

  const toggleLike = async (id) => {
    try {
      const headers = { Authorization: `Token ${accountStore.token}` }
      const response = await axios.post(
        `${API_URL}/finlife/saving/${id}/interest/`,
        {},
        { headers },
      )

      if (response.data.action === 'added') likedProducts.value.push(id)
      else likedProducts.value = likedProducts.value.filter((pid) => pid !== id)

      return response.data.action
    } catch (err) {
      console.error('찜 토글 실패:', err)
      throw err
    }
  }

  const toggleJoin = async (id) => {
    try {
      const headers = { Authorization: `Token ${accountStore.token}` }
      const response = await axios.post(`${API_URL}/finlife/saving/${id}/join/`, {}, { headers })

      if (response.data.action === 'joined') joinedProducts.value.push(id)
      else joinedProducts.value = joinedProducts.value.filter((pid) => pid !== id)

      return response.data.action
    } catch (err) {
      console.error('가입 토글 실패:', err)
      throw err
    }
  }

  const getSavingProducts = () => {
    axios
      .get(`${API_URL}/finlife/saving/`)
      .then((res) => {
        savingProducts.value = res.data
      })
      .catch((err) => console.error(err))
  }

  const fetchSavingInterests = () => {
    axios
      .get(`${API_URL}/finlife/my-interests/`, {
        headers: { Authorization: `Token ${accountStore.token}` },
      })
      .then((res) => {
        likedProducts.value = res.data.savings.map((item) => item.product?.id ?? item.product)
      })
      .catch((err) => console.error('찜 목록 조회 실패:', err))
  }

  const fetchSavingJoins = () => {
    axios
      .get(`${API_URL}/finlife/my-joins/`, {
        headers: { Authorization: `Token ${accountStore.token}` },
      })
      .then((res) => {
        joinedSavingDetails.value = res.data.savings || []
        joinedProducts.value = joinedSavingDetails.value.map(
          (item) => item.product?.id ?? item.product,
        )
      })
      .catch((err) => console.error('가입 목록 조회 실패:', err))
  }

  return {
    savingProducts,
    likedProducts,
    joinedProducts,
    joinedSavingDetails,
    isLiked,
    isJoined,
    toggleLike,
    toggleJoin,
    getSavingProducts,
    fetchSavingInterests,
    fetchSavingJoins,
  }
})

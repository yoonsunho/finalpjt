import axios from 'axios'
import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { useAccountStore } from './user'

export const useDepositStore = defineStore('deposit', () => {
  const accountStore = useAccountStore()
  const API_URL = 'http://127.0.0.1:8000'

  const depositProducts = ref([])
  const likedProducts = ref([])
  const joinedProducts = ref([])
  const joinedDepositDetails = ref([])

  const isLiked = (id) => likedProducts.value.includes(id)
  const isJoined = (id) => joinedProducts.value.includes(id)

  const toggleLike = async (id) => {
    try {
      const headers = { Authorization: `Token ${accountStore.token}` }
      const response = await axios.post(
        `${API_URL}/finlife/deposit/${id}/interest/`,
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
      const response = await axios.post(`${API_URL}/finlife/deposit/${id}/join/`, {}, { headers })

      if (response.data.action === 'joined') joinedProducts.value.push(id)
      else joinedProducts.value = joinedProducts.value.filter((pid) => pid !== id)

      return response.data.action
    } catch (err) {
      console.error('가입 토글 실패:', err)
      throw err
    }
  }

  const getDepositProducts = () => {
    axios
      .get(`${API_URL}/finlife/deposit/`)
      .then((res) => {
        depositProducts.value = res.data
      })
      .catch((err) => console.error(err))
  }

  const fetchDepositInterests = () => {
    axios
      .get(`${API_URL}/finlife/my-interests/`, {
        headers: { Authorization: `Token ${accountStore.token}` },
      })
      .then((res) => {
        likedProducts.value = res.data.deposits.map((item) => item.product?.id ?? item.product)
      })
      .catch((err) => console.error('찜 목록 조회 실패:', err))
  }

  const fetchDepositJoins = () => {
    axios
      .get(`${API_URL}/finlife/my-joins/`, {
        headers: { Authorization: `Token ${accountStore.token}` },
      })
      .then((res) => {
        joinedDepositDetails.value = res.data.deposits || []
        joinedProducts.value = joinedDepositDetails.value.map(
          (item) => item.product?.id ?? item.product,
        )
      })
      .catch((err) => console.error('가입 목록 조회 실패:', err))
  }

  return {
    depositProducts,
    likedProducts,
    joinedProducts,
    joinedDepositDetails,
    isLiked,
    isJoined,
    toggleLike,
    toggleJoin,
    getDepositProducts,
    fetchDepositInterests,
    fetchDepositJoins,
  }
})

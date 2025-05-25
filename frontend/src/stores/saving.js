import axios from 'axios'
import { ref } from 'vue'
import { defineStore } from 'pinia'
import { useAccountStore } from './user'

export const useSavingStore = defineStore(
  'saving',
  () => {
    const accountStore = useAccountStore()
    const API_URL = 'http://127.0.0.1:8000'

    const savingProducts = ref([])

    // 찜한 상품 목록
    const likedProducts = ref([])
    // 가입한 상품 목록
    const joinedProducts = ref([])

    // 찜한상품목록에서 id찾고
    const isLiked = (id) => likedProducts.value.includes(id)
    const isJoined = (id) => joinedProducts.value.includes(id)

    const toggleLike = (id) => {
      const headers = {
        Authorization: `Token ${accountStore.token}`,
      }

      axios({
        method: 'post', // DELETE가 아닌 POST 사용
        url: `${API_URL}/finlife/saving/${id}/interest/`,
        headers: headers,
        data: {},
      })
        .then((response) => {
          if (response.data.action === 'added') {
            likedProducts.value.push(id)
          } else if (response.data.action === 'removed') {
            likedProducts.value = likedProducts.value.filter((productId) => productId !== id)
          }
        })
        .catch((err) => {
          console.error('찜 토글 실패:', err)
        })
    }

    // 가입하기 토글 (Django에서 POST 토글 방식으로 처리)
    const toggleJoin = (id) => {
      const headers = {
        Authorization: `Token ${accountStore.token}`,
      }

      axios({
        method: 'post', // DELETE가 아닌 POST 사용
        url: `${API_URL}/finlife/saving/${id}/join/`,
        headers: headers,
        data: {},
      })
        .then((response) => {
          // Django에서 반환하는 action 값에 따라 처리
          if (response.data.action === 'joined') {
            joinedProducts.value.push(id)
          } else if (response.data.action === 'canceled') {
            joinedProducts.value = joinedProducts.value.filter((productId) => productId !== id)
          }
        })
        .catch((err) => {
          console.error('가입 토글 실패:', err)
        })
    }

    // 적금 상품 가져오기
    const getSavingProducts = function () {
      axios({
        method: 'GET',
        url: `${API_URL}/finlife/saving/`,
      })
        .then((res) => {
          savingProducts.value = res.data
        })
        .catch((err) => console.log(err))
    }

    // 찜한 적금 목록 가져오기
    const getSavingInterests = function () {
      const headers = {
        Authorization: `Token ${accountStore.token}`,
      }

      axios({
        method: 'GET',
        url: `${API_URL}/finlife/my-interests/`,
        headers: headers,
      })
        .then((res) => {
          likedProducts.value = res.data.savings.map((item) => item.product.id)
        })
        .catch((err) => console.log('찜 목록 조회 실패:', err))
    }

    // 가입한 적금 목록 가져오기
    const getSavingJoins = function () {
      const headers = {
        Authorization: `Token ${accountStore.token}`,
      }

      axios({
        method: 'GET',
        url: `${API_URL}/finlife/my-joins/`,
        headers: headers,
      })
        .then((res) => {
          joinedProducts.value = res.data.savings.map((item) => item.product.id)
        })
        .catch((err) => console.log('가입 목록 조회 실패:', err))
    }

    return {
      savingProducts,
      getSavingProducts,
      API_URL,
      likedProducts,
      joinedProducts,
      isLiked,
      isJoined,
      toggleLike,
      toggleJoin,
      getSavingInterests,
      getSavingJoins,
    }
  },
  { persist: true },
)

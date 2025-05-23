import axios from 'axios'
import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useSavingStore = defineStore(
  'saving',
  () => {
    const API_URL = 'http://127.0.0.1:8000'

    const savingProducts = ref([])

    // 찜한 상품 목록
    const likedProducts = ref([])
    // 가입한 상품 목록
    const joinedProducts = ref([])
    // 찜한상품목록에서 id찾고
    const isLiked = (id) => likedProducts.value.includes(id)
    const isJoined = (id) => joinedProducts.value.includes(id)
    // isLiked이면 찜해제 !isLiked이면 찜
    const toggleLike = (id) => {
      if (isLiked(id)) {
        likedProducts.value = likedProducts.value.filter((productId) => productId !== id)
      } else {
        likedProducts.value.push(id)
      }
    }
    const toggleJoin = (id) => {
      if (isJoined(id)) {
        joinedProducts.value = joinedProducts.value.filter((productId) => productId !== id)
      } else {
        joinedProducts.value.push(id)
      }
    }

    // 예금 상품 가져오기
    const getSavingProducts = function () {
      axios({
        method: 'GET',
        url: `${API_URL}/finlife/saving/`,
      })
        .then((res) => {
          // console.log(res)
          // console.log(res.data)
          savingProducts.value = res.data
        })
        .catch((err) => console.log(err))
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
    }
  },
  { persist: true },
)

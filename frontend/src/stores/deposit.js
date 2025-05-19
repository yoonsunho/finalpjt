import axios from 'axios'
import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useDepositStore = defineStore('deposit', () => {
  
  const API_URL = 'http://127.0.0.1:8000'

  const DepositProductData = ref([])
  const getDepositDetail = ref({})

  // 예금 상품 가져오기
  const getDepositProducts = function(){
    axios({
      method:'GET',
      url: `${API_URL}/finlife/deposit_product_list/`
    })
    .then(res => {
      console.log(res)
      console.log(res.dat)
    })
    .catch(err => console.log(err))
  }

  // 예금 상품 가져오기
  return {  }
})

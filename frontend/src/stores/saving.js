import axios from 'axios'
import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useSavingStore = defineStore('saving', () => {
  
  const API_URL = 'http://127.0.0.1:8000'

  const savingProducts  = ref([])
  // const depositDetail  = ref({})

  // 예금 상품 가져오기
  const getSavingProducts  = function(){
    axios({
      method:'GET',
      url: `${API_URL}/finlife/saving/`
    })
    .then(res => {
      // console.log(res)
      // console.log(res.data)
      savingProducts.value = res.data
    })
    .catch(err => console.log(err))
  }

  return { 
    savingProducts, 
    getSavingProducts, 
    API_URL 
  }
}, {persist :true})

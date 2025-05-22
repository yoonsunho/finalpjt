import axios from 'axios'
import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useDepositStore = defineStore('deposit', () => {
  
  const API_URL = 'http://127.0.0.1:8000'

  const depositProducts  = ref([])
  // const depositDetail  = ref({})

  // 예금 상품 가져오기
  const getDepositProducts  = function(){
    axios({
      method:'GET',
      url: `${API_URL}/finlife/deposit/`
    })
    .then(res => {
      // console.log(res)
      console.log(res.data)
      depositProducts.value = res.data
    })
    .catch(err => console.log(err))
  }

  // // 예금 detail가져오기
  // const getDepositDetail = function(id) {
  //   axios({
  //     method: 'GET',
  //     url: `${API_URL}/finlife/deposit/${id}/`
  //   })
  //   .then(res => {
  //     console.log(res)
  //     console.log(res.data)
  //     depositDetail.value = res.data
  //   })
  //   .catch(err => console.log(err))
  // }

  return { 
    depositProducts, 
    // depositDetail, 
    getDepositProducts, 
    // getDepositDetail,
    API_URL 
  }
}, {persist :true})

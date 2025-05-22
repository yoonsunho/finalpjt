<template>
    <div v-if="product && product.saving_product">
        <h1>Saving Detail</h1>
        <h5>{{ product.id }}</h5>
        <h3>{{ product.saving_product.fin_prdt_nm }}({{ product.saving_product.fin_prdt_cd }})</h3>
        <strong>
            <ul>
                저축 금리 유형 :{{ product.intr_rate_nm }}({{ product.intr_rate_type }})
                저축 기간 : {{ product.save_trm }}개월,
                저축 금리 :{{ product.intr_rate }},
                최고 우대 금리: {{ product.intr_rate2 }}
            </ul>
        </strong>
        <p>금융회사 명: {{ product.saving_product.kor_co_nm }}</p>
        <p>공시 제출월[YYYYMM]: {{ product.saving_product.dcls_month }}</p>
        <p>가입 방법 : {{ product.saving_product.join_way }}</p>
        <p>만기 후 이자율 : {{ product.saving_product.mtrt_int }}</p>
        <p>우대 조건: {{ product.saving_product.spcl_cnd }}</p>
        <p>기타 유의 사항:{{ product.saving_product.etc_note }}</p>
    </div>
</template>

<script setup>
// 준비물
  // 1. AXIOS
  import axios from 'axios';
  // 2. 게시글 상세 조회 요청 경로: 출처가 이미 스토어에 이씅ㅁ
  import { useSavingStore } from '@/stores/saving';
  // 3. 조회 하고자 하는 게시글 id: route
  import { useRoute } from 'vue-router';
  // 4. 응답 받은 게시글을 저장할 위치
  import {ref, onMounted} from 'vue'

  const product = ref(null)
  const store =useSavingStore()
  const route = useRoute()

  const getSavingDetail = function(){
    axios({
        method:'GET',
        url:`${store.API_URL}/finlife/saving/${route.params.id}/`
    })
    .then(res=>{
        console.log(res)
        console.log(res.data)
        product.value = res.data
    })
    .catch(err=> console.log(err))
  }
  onMounted(()=>{
    getSavingDetail()
  })
</script>
    
<style scoped>

</style>
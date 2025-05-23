<template>
 <div v-if="product">
  <h1 class="saving_product_name">{{ product.fin_prdt_nm }}</h1>
  <h5>id: {{ product.id }}</h5>
  <p>금융회사 명: {{ product.kor_co_nm }}</p>
  <p>가입 방법: {{ product.join_way }}</p>
  <p>만기 후 이자율: {{ product.mtrt_int }}</p>
  <p>우대 조건: {{ product.spcl_cnd }}</p>
  <p>가입 제한: {{ product.join_deny }}</p>
  <p>기타 유의 사항: {{ product.etc_note }}</p>
  <p v-if="product.max_limit">최고한도: {{ product.max_limit }}</p>
  <div v-if="product && product.options">
  <h2>옵션 목록</h2>
  <div v-for="(option, index) in product.options" :key="option.id" class="option-box">
    <h3>옵션 {{ index + 1 }}</h3>
    <p>금리 유형: {{ option.intr_rate_type_nm }} </p>
    <p>적립 유형: {{ option.rsrv_type_nm }}개월</p>
    <p>저축 기간: {{ option.save_trm }}개월</p>
    <p>저축 금리: {{ option.intr_rate }}%</p>
    <p>최고 우대 금리: {{ option.intr_rate2 }}%</p>
  </div>
</div>
</div>

<div class="button">
  <div class="likebutton">
    <button class="like" v-if="!isLiked" @click="toggleLike">찜하기</button>
    <button class="liked" v-else @click="toggleLike">찜 완료</button>
  </div>
  <div class="signupbutton">
    <button class="join" v-if="!isJoined" @click="toggleJoin">가입하기</button>
    <button class="joined" v-else @click="toggleJoin">가입 완료</button>
  </div>
</div>

</template>

<script setup>
import axios from 'axios';
// 2. 게시글 상세 조회 요청 경로: 출처가 이미 스토어에 이씅ㅁ
import { useSavingStore } from '@/stores/saving.js';
// 3. 조회 하고자 하는 게시글 id: route
import { useRoute } from 'vue-router';
// 4. 응답 받은 게시글을 저장할 위치
import { ref, onMounted, computed, watch } from 'vue'

const product = ref(null)
const store = useSavingStore()
const route = useRoute()
const productId = route.params.id // 현재상품id

const isLiked = computed(() => store.isLiked(productId))
const isJoined = computed(() => store.isJoined(productId))

const toggleLike = () => store.toggleLike(productId)
const toggleJoin = () => store.toggleJoin(productId)

const getSavingDetail = function(){
    // console.log('요청 URL:', `${store.API_URL}/finlife/saving/${route.params.id}/`)
    
    axios({
        method: 'GET',
        url: `${store.API_URL}/finlife/saving/${route.params.id}/`
    })
    .then(res => {
        // console.log(res)
        console.log(res.data)
        product.value = res.data
        console.log('product.value 설정 후:', product.value)
    })
    .catch(err => {
        console.error('API 오류:', err)
    })
}

onMounted(() => {
    console.log('route.params.id:', route.params.id)
    getSavingDetail()
})

watch(isLiked, (newVal) => {
  console.log('찜 여부:', newVal);
}, { immediate: true });
watch(isJoined, (newVal) => {
  console.log('가입 여부:', newVal);
}, { immediate: true });

</script>
    
<style scoped>
.product-detail {
  max-width: 720px;
  margin: 2rem auto;
  padding: 1.5rem;
  border: 1px solid #ddd;
  border-radius: 10px;
  background-color: #fafafa;
  font-family: 'Pretendard', sans-serif;
}

.product-name {
  text-align: center;
  font-size: 1.75rem;
  margin-bottom: 1rem;
}

.section {
  margin-top: 1.5rem;
}

.section-title {
  margin-bottom: 1rem;
  font-size: 1.25rem;
  border-bottom: 1px solid #ccc;
  padding-bottom: 0.5rem;
}

.option-box {
  margin-bottom: 1rem;
  padding: 1rem;
  border: 1px solid #eee;
  border-radius: 6px;
  background-color: #fff;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}

.button {
  display: flex;
  flex-direction: row;
}

.like, .liked {
  color: black;
  border: 2px solid black;
  padding: 5px;
  border-radius: 20px;
}

.join, .joined {
  background-color: dodgerblue;
  border-radius: 20px;
  padding: 5px;
  color: white;
}

</style>
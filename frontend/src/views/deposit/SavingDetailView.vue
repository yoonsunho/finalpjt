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
        <p>금리 유형: {{ option.intr_rate_type_nm }}</p>
        <p>적립 유형: {{ option.rsrv_type_nm }}개월</p>
        <p>저축 기간: {{ option.save_trm }}개월</p>
        <p>저축 금리: {{ option.intr_rate }}%</p>
        <p>최고 우대 금리: {{ option.intr_rate2 }}%</p>
      </div>
    </div>
  </div>

  <div class="button" v-if="isLogin">
    <div class="likebutton">
      <button class="like" v-if="!isLiked" @click="toggleLike">찜하기</button>
      <button class="liked" v-else @click="toggleLike">찜 완료</button>
    </div>
    <div class="signupbutton">
      <button class="join" v-if="!isJoined" @click="confirmJoin">가입하기</button>
      <button class="joined" v-else @click="confirmCancelJoin">가입 완료</button>
    </div>
  </div>
  <ConfirmModal
    :show="showJoinModal"
    title="가입하시겠습니까?"
    @confirm="doJoin"
    @close="showJoinModal = false"
  />
  <ConfirmModal
    :show="showCancelModal"
    title="가입을 취소하시겠습니까?"
    @confirm="doCancel"
    @close="showCancelModal = false"
  />
</template>

<script setup>
import axios from 'axios'
import { useSavingStore } from '@/stores/saving.js'
import { useAccountStore } from '@/stores/user.js'
import { useRoute } from 'vue-router'
import { ref, onMounted, computed, watch } from 'vue'
import ConfirmModal from '@/components/ConfirmModal.vue'

const product = ref(null)
const store = useSavingStore()
const accountStore = useAccountStore()
const route = useRoute()
const productId = route.params.id // 현재상품id

const isLiked = computed(() => store.isLiked(productId))
const isJoined = computed(() => store.isJoined(productId))
const isLogin = computed(() => !!accountStore.token)

const showJoinModal = ref(false)
const showCancelModal = ref(false)

const confirmJoin = () => (showJoinModal.value = true)
const confirmCancelJoin = () => (showCancelModal.value = true)
const doJoin = async () => {
  try {
    const result = await store.toggleJoin(productId)
    console.log('적금 가입 결과:', result)
    showJoinModal.value = false
  } catch (err) {
    alert('가입 처리 중 오류 발생!')
  }
}

const doCancel = async () => {
  try {
    const result = await store.toggleJoin(productId)
    console.log('적금 가입 취소 결과:', result)
    showCancelModal.value = false
  } catch (err) {
    alert('가입 취소 처리 중 오류 발생!')
  }
}

const toggleLike = async () => {
  try {
    const result = await store.toggleLike(productId)
    console.log('적금 찜 처리:', result)
  } catch (err) {
    alert('찜 처리 중 오류 발생!')
  }
}

const getSavingDetail = function () {
  axios({
    method: 'GET',
    url: `${store.API_URL}/finlife/saving/${route.params.id}/`,
  })
    .then((res) => {
      product.value = res.data
    })
    .catch((err) => {
      console.error('API 오류:', err)
    })
}

onMounted(() => {
  getSavingDetail()
})

watch(
  isLiked,
  (newVal) => {
    console.log('찜 여부:', newVal)
  },
  { immediate: true },
)
watch(
  isJoined,
  (newVal) => {
    console.log('가입 여부:', newVal)
  },
  { immediate: true },
)
</script>

<style scoped>
.product-detail {
  max-width: 720px;
  margin: 3rem auto;
  padding: 2rem;
  border: none;
  border-radius: 16px;
  background-color: #ffffff;
  font-family: 'Pretendard', 'Apple SD Gothic Neo', sans-serif;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
}

.saving_product_name {
  text-align: center;
  font-size: 2rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  color: #1e1e1e;
}

p {
  font-size: 1rem;
  color: #444;
  margin: 0.4rem 0;
  line-height: 1.6;
}

h2 {
  margin-top: 2rem;
  margin-bottom: 1rem;
  font-size: 1.2rem;
  font-weight: 600;
  color: #222;
  border-bottom: 1px solid #e5e5e5;
  padding-bottom: 0.5rem;
}

.option-box {
  margin-bottom: 1rem;
  padding: 1.2rem;
  border-radius: 12px;
  background-color: #f9fafb;
  border: 1px solid #eaeaea;
  transition: box-shadow 0.2s ease;
}
.option-box:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.button {
  display: flex;
  gap: 12px;
  justify-content: center;
  margin-top: 2rem;
}

.likebutton,
.signupbutton {
  flex: 1;
  display: flex;
  justify-content: center;
}

.like,
.liked,
.join,
.joined {
  width: 100%;
  max-width: 160px;
  padding: 0.75rem 1rem;
  font-size: 0.95rem;
  font-weight: 500;
  border-radius: 9999px;
  border: 1.5px solid #d1d5db;
  background-color: white;
  color: #1f2937;
  cursor: pointer;
  transition: all 0.2s ease-in-out;
}

.like:hover,
.liked:hover,
.join:hover,
.joined:hover {
  background-color: #f3f4f6;
}

.liked {
  background-color: #f0f0f0;
  border-color: #999;
  color: #111;
}

.join {
  background-color: #2563eb;
  color: white;
  border: none;
}

.join:hover {
  background-color: #1d4ed8;
}

.joined {
  background-color: #e0f2fe;
  color: #0369a1;
  border: 1.5px solid #38bdf8;
}

.joined:hover {
  background-color: #bae6fd;
}
</style>

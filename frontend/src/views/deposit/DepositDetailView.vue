<template>
  <div v-if="product">
    <h1 class="deposit_product_name">{{ product.fin_prdt_nm }}</h1>
    <!-- <h5>id: {{ product.id }}</h5> -->
    <p>금융회사 명: {{ product.kor_co_nm }}</p>
    <p>가입 방법: {{ product.join_way }}</p>
    <p>만기 후 이자율: {{ product.mtrt_int }}</p>
    <p>우대 조건: {{ product.spcl_cnd }}</p>
    <p>가입 제한: {{ product.join_deny }}</p>
    <p>기타 유의 사항: {{ product.etc_note }}</p>
    <p>최고한도: {{ product.max_limit }}</p>

    <div v-if="product.options">
      <h2>옵션 목록</h2>
      <div v-for="(option, index) in product.options" :key="option.id" class="option-box">
        <h3>옵션 {{ index + 1 }}</h3>
        <p>금리 유형: {{ option.intr_rate_type_nm }}</p>
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
import { useDepositStore } from '@/stores/deposit.js'
import { useAccountStore } from '@/stores/user.js'
import { useRoute } from 'vue-router'
import { watch, ref, onMounted, computed } from 'vue'
import ConfirmModal from '@/components/ConfirmModal.vue'

const product = ref(null)
const depositStore = useDepositStore()
const accountStore = useAccountStore()
const route = useRoute()
const productId = route.params.id

const isLiked = computed(() => {
  return depositStore.isLiked(productId)
})
const isJoined = computed(() => {
  return depositStore.isJoined(productId)
})
const isLogin = computed(() => !!accountStore.token)

const showJoinModal = ref(false)
const showCancelModal = ref(false)

const confirmJoin = () => (showJoinModal.value = true)
const confirmCancelJoin = () => (showCancelModal.value = true)
const doJoin = async () => {
  try {
    const result = await depositStore.toggleJoin(productId)
    console.log('가입 처리:', result)
    showJoinModal.value = false
  } catch (err) {
    alert('가입 처리 중 오류 발생!')
  }
}

const doCancel = async () => {
  try {
    const result = await depositStore.toggleJoin(productId)
    console.log('가입 취소 처리:', result)
    showCancelModal.value = false
  } catch (err) {
    alert('가입 취소 처리 중 오류 발생!')
  }
}

const toggleLike = async () => {
  try {
    const result = await depositStore.toggleLike(productId)
    console.log('찜 처리:', result)
  } catch (err) {
    alert('찜 처리 중 오류 발생!')
  }
}

const getDepositDetail = () => {
  axios
    .get(`${depositStore.API_URL}/finlife/deposit/${productId}/`)
    .then((res) => {
      product.value = res.data
    })
    .catch((err) => {
      console.error('API 오류:', err)
    })
}

onMounted(() => {
  depositStore.getDepositInterests()
  depositStore.getDepositJoins()
  getDepositDetail()
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
* {
  font-family: 'Pretendard', sans-serif;
  box-sizing: border-box;
}

.product-detail {
  max-width: 760px;
  margin: 3rem auto;
  padding: 2.5rem;
  border-radius: 20px;
  background-color: #ffffff;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.05);
}

.deposit_product_name {
  text-align: center;
  font-size: 28px;
  font-weight: 700;
  color: #111827;
  margin-bottom: 2rem;
}

h5 {
  text-align: center;
  color: #6b7280;
  margin-bottom: 1.5rem;
}

p {
  font-size: 15px;
  color: #374151;
  margin: 0.5rem 0;
  line-height: 1.6;
}

h2 {
  margin-top: 2rem;
  font-size: 18px;
  font-weight: 600;
  color: #1f2937;
  border-bottom: 1px solid #e5e7eb;
  padding-bottom: 0.4rem;
  margin-bottom: 1rem;
}

.option-box {
  margin-bottom: 1rem;
  padding: 1.25rem 1.5rem;
  background-color: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 16px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.03);
}

.option-box h3 {
  font-size: 16px;
  font-weight: 600;
  color: #2563eb;
  margin-bottom: 0.5rem;
}

.button {
  display: flex;
  gap: 12px;
  justify-content: center;
  margin-top: 2.5rem;
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
  padding: 0.75rem 1.25rem;
  font-size: 15px;
  font-weight: 600;
  border-radius: 9999px;
  border: 1px solid transparent;
  cursor: pointer;
  transition: all 0.2s ease;
}

.like {
  background-color: white;
  border: 1.5px solid #d1d5db;
  color: #374151;
}

.like:hover {
  background-color: #f3f4f6;
}

.liked {
  background-color: #f3f4f6;
  border: 1.5px solid #9ca3af;
  color: #1f2937;
}

.liked:hover {
  background-color: #e5e7eb;
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

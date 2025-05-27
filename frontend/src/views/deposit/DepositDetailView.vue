<template>
  <!-- <h1>예금 상품 목록</h1> -->
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
  margin: 0;
  padding: 0;
}

.deposit_product_name {
  font-size: 24px;
  font-weight: 700;
  color: #191f28;
  text-align: center;
  margin-bottom: 24px;
}

.product-detail {
  max-width: 700px;
  margin: 32px auto;
  padding: 24px;
  background: #ffffff;
  border-radius: 16px;
  border: 1px solid #f2f4f6;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
}

p {
  font-size: 14px;
  color: #4e5968;
  margin-bottom: 10px;
  line-height: 1.5;
}

h2 {
  font-size: 18px;
  font-weight: 600;
  color: #191f28;
  border-bottom: 1px solid #e5e8eb;
  padding-bottom: 8px;
  margin-top: 32px;
  margin-bottom: 16px;
}

.option-box {
  background: #f9fafb;
  border: 1px solid #e5e8eb;
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 12px;
}

.option-box h3 {
  font-size: 15px;
  font-weight: 600;
  color: #3182f6;
  margin-bottom: 8px;
}

.button {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 12px;
  margin-top: 28px;
}

.likebutton,
.signupbutton {
  flex: 1;
  max-width: 180px;
}

.like,
.liked,
.join,
.joined {
  width: 100%;
  padding: 12px;
  font-size: 14px;
  font-weight: 600;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.like {
  background: #ffffff;
  border: 1px solid #d1d6db;
  color: #4e5968;
}

.like:hover {
  border-color: #3182f6;
  color: #3182f6;
  background: #f0f4f8;
}

.liked {
  background: #f2f4f6;
  border: 1px solid #d1d6db;
  color: #191f28;
}

.join {
  background: #3182f6;
  border: none;
  color: #ffffff;
}

.join:hover {
  background: #1b64da;
}

.joined {
  background: #e8f3ff;
  color: #0369a1;
  border: 1px solid #a4d8ff;
}

.joined:hover {
  background: #d3ecff;
}

/* 반응형 */
@media (max-width: 768px) {
  .product-detail {
    margin: 24px 16px;
    padding: 20px;
  }

  .deposit_product_name {
    font-size: 20px;
  }

  .button {
    flex-direction: column;
    align-items: center;
  }

  .likebutton,
  .signupbutton {
    max-width: none;
    width: 100%;
  }
}
</style>

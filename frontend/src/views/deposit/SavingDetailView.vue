<template>
  <!-- <h1>적금 상품 목록</h1> -->
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

const savingStore = useSavingStore()
const product = ref(null)
const accountStore = useAccountStore()
const route = useRoute()
const productId = route.params.id

const isLiked = computed(() => {
  return savingStore.isLiked(productId)
})
const isJoined = computed(() => {
  return savingStore.isJoined(productId)
})
const isLogin = computed(() => !!accountStore.token)

const showJoinModal = ref(false)
const showCancelModal = ref(false)

const confirmJoin = () => (showJoinModal.value = true)
const confirmCancelJoin = () => (showCancelModal.value = true)
const doJoin = async () => {
  try {
    const result = await savingStore.toggleJoin(productId)
    console.log('적금 가입 결과:', result)
    showJoinModal.value = false
  } catch (err) {
    alert('가입 처리 중 오류 발생!')
  }
}

const doCancel = async () => {
  try {
    const result = await savingStore.toggleJoin(productId)
    console.log('적금 가입 취소 결과:', result)
    showCancelModal.value = false
  } catch (err) {
    alert('가입 취소 처리 중 오류 발생!')
  }
}

const toggleLike = async () => {
  try {
    const result = await savingStore.toggleLike(productId)
    console.log('적금 찜 처리:', result)
  } catch (err) {
    alert('찜 처리 중 오류 발생!')
  }
}

const getSavingDetail = function () {
  axios({
    method: 'GET',
    url: `${savingStore.API_URL}/finlife/saving/${route.params.id}/`,
  })
    .then((res) => {
      product.value = res.data
    })
    .catch((err) => {
      console.error('API 오류:', err)
    })
}

onMounted(() => {
  savingStore.getSavingInterests()
  savingStore.getSavingJoins()
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
.saving-log {
  max-height: 400px;
  overflow-y: auto;
  padding: 0 8px;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: #6b7684;
}

.empty-icon {
  font-size: 48px;
  margin-bottom: 16px;
  opacity: 0.6;
}

.empty-state h3 {
  font-size: 18px;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 8px 0;
}

.empty-state p {
  font-size: 14px;
  color: #6b7684;
  margin: 0;
}

.log-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.log-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 16px;
  background: #ffffff;
  border-radius: 12px;
  transition: background-color 0.2s ease;
  border: 1px solid #e2e8f0;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.03);
}

.log-item:hover {
  background: #f9fafb;
}

.log-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: 600;
  flex-shrink: 0;
}

.log-content {
  flex: 1;
  min-width: 0;
}

.log-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
}

.log-name {
  font-size: 15px;
  font-weight: 600;
  color: #1f2937;
}

.log-amount {
  font-size: 15px;
  font-weight: 700;
  color: #22c55e;
}

.log-details {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 8px;
}

.log-memo {
  font-size: 13px;
  color: #475569;
  flex: 1;
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.log-memo.placeholder {
  font-style: italic;
  opacity: 0.6;
}

.log-time {
  font-size: 12px;
  color: #94a3b8;
  font-weight: 500;
  white-space: nowrap;
}

.saving-log::-webkit-scrollbar {
  width: 4px;
}

.saving-log::-webkit-scrollbar-track {
  background: transparent;
}

.saving-log::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 2px;
}

.saving-log::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}

@media (max-width: 480px) {
  .log-item {
    padding: 12px;
  }

  .log-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 4px;
  }

  .log-details {
    flex-direction: column;
    align-items: flex-start;
    gap: 4px;
  }

  .log-memo {
    white-space: normal;
    line-height: 1.4;
  }
}
</style>

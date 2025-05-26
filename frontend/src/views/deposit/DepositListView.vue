<template>
  <div>
    <!-- 🔍 필터 섹션 -->
    <div class="filter-bar">
      <form @submit.prevent="filterDeposits" class="filter-form">
        <input v-model="searchBank" placeholder="은행검색" @input="fetchFilteredProducts" />

        <select v-model="selectedRateType" @change="fetchFilteredProducts">
          <option value="">이율 유형 전체</option>
          <option value="단리">단리</option>
          <option value="복리">복리</option>
        </select>

        <select v-model="selectedOrdering" @change="fetchFilteredProducts">
          <option value="">기본 정렬</option>
          <option value="interest_count">찜 많은 순</option>
          <option value="-interest_count">찜 적은 순</option>
          <option value="joined_count">가입 많은 순</option>
          <option value="-joined_count">가입 적은 순</option>
        </select>
        <button type="submit">검색</button>
      </form>
      <!-- 추천받기 버튼 -->
      <button class="cta" @click="handleRecommendClick">추천받기</button>

      <!-- 로그인 필요 모달 -->
      <ConfirmModal
        :show="showLoginModal"
        title="로그인이 필요한 기능입니다. 로그인 하시겠습니까?"
        @confirm="goToLogin"
        @close="showLoginModal = false"
      />
    </div>

    <!-- 📝 예금 리스트 -->
    <div v-for="product in store.depositProducts" :key="product.id">
      <DepositItem :product="product" />
    </div>
  </div>
  <div class="table-wrapper">
    <fwb-table hoverable>
      <fwb-table-head>
        <fwb-table-head-cell>id</fwb-table-head-cell>
        <fwb-table-head-cell>금융 상품명</fwb-table-head-cell>
        <fwb-table-head-cell>은행</fwb-table-head-cell>
        <fwb-table-head-cell>최고 우대 금리</fwb-table-head-cell>
        <fwb-table-head-cell>금리 유형</fwb-table-head-cell>
      </fwb-table-head>
      <fwb-table-body>
        <fwb-table-row
          v-for="(product, index) in store.depositProducts"
          :key="index"
          class="hover:cursor-pointer hover:bg-blue-100"
          @click="$router.push({ name: 'DepositDetailView', params: { id: product.id } })"
        >
          <fwb-table-cell>{{ product.id }}</fwb-table-cell>
          <fwb-table-cell>{{ product.fin_prdt_nm }}</fwb-table-cell>
          <fwb-table-cell>{{ product.kor_co_nm }}</fwb-table-cell>
          <fwb-table-cell>{{ product.max_intr_rate2 }}</fwb-table-cell>
          <fwb-table-cell>{{ product.intr_rate_type_nm }}</fwb-table-cell>
        </fwb-table-row>
      </fwb-table-body>
    </fwb-table>
  </div>
</template>

<script setup>
import {
  FwbTable,
  FwbTableBody,
  FwbTableCell,
  FwbTableHead,
  FwbTableHeadCell,
  FwbTableRow,
} from 'flowbite-vue'
import ConfirmModal from '@/components/ConfirmModal.vue'
import { useDepositStore } from '@/stores/deposit'
import { ref, onMounted } from 'vue'
import { useAccountStore } from '@/stores/user'
import axios from 'axios'
const store = useDepositStore()
const accountStore = useAccountStore()

const searchBank = ref('')
const selectedRateType = ref('')
const selectedOrdering = ref('')
import { useRouter } from 'vue-router'
// import { useAccountStore } from '@/stores/user'
const router = useRouter()
const showLoginModal = ref(false)
const handleRecommendClick = () => {
  if (accountStore.isLogin) {
    router.push({ name: 'RecommendView' })
  } else {
    showLoginModal.value = true
  }
}

const goToLogin = () => {
  showLoginModal.value = false
  router.push({ name: 'LoginView' })
}

const filterDeposits = function () {
  const params = {}

  if (searchBank.value) params.kor_co_nm = searchBank.value
  if (selectedOrdering.value) params.ordering = selectedOrdering.value
  if (selectedRateType.value) params.intr_rate_type_nm = selectedRateType.value

  axios
    .get(`${store.API_URL}/finlife/deposit/`, {
      params: params,
    })
    .then((res) => {
      store.depositProducts = res.data
    })
    .catch((err) => {
      console.error('필터링 실패:', err)
    })
}

onMounted(() => {
  // store.getDepositProducts()
  filterDeposits()
})
</script>
<style scoped>
/* 전체 레이아웃 정리 */
.table-wrapper {
  max-width: 900px;
  width: 100%;
  margin: 0 auto;
  overflow-x: auto;
  border-radius: 12px;
  border: 1px solid #e5e7eb;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  background-color: #ffffff;
}

/* 필터 바 */
.filter-bar {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 1rem;
  margin: 2rem auto;
  padding: 1rem;
  max-width: 900px;
  background-color: #ffffff;
  border-radius: 12px;
  border: 1px solid #e5e7eb;
  box-shadow: 0 1px 6px rgba(0, 0, 0, 0.03);
}

/* 인풋과 셀렉트 요소 스타일 */
input,
select {
  padding: 0.6rem 1rem;
  font-size: 0.9rem;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  background-color: #f9fafb;
  color: #111827;
  transition:
    border 0.2s ease,
    background-color 0.2s ease;
}

input:focus,
select:focus {
  outline: none;
  border-color: #60a5fa;
  background-color: #fff;
}

/* 버튼 스타일 */
button[type='submit'] {
  padding: 0.6rem 1.2rem;
  background-color: #2563eb;
  color: white;
  font-weight: 500;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

button[type='submit']:hover {
  background-color: #1d4ed8;
}

/* 테이블 hover 효과 */
.hover\:bg-blue-100:hover {
  background-color: #f0f9ff !important;
}

/* 테이블 내부 폰트 및 간격 */
fwb-table-cell,
fwb-table-head-cell {
  font-size: 0.9rem;
  padding: 1rem;
  color: #111827;
}

fwb-table-head-cell {
  font-weight: 600;
  background-color: #f3f4f6;
  border-bottom: 1px solid #e5e7eb;
}
</style>

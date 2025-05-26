<template>
  <div>
    <!-- 🔍 필터 섹션 -->
    <div class="filter-bar">
      <form @submit.prevent="filterDeposits" class="filter-form">
        <input v-model="searchDeposits" placeholder="예금 이름 검색" />
        <input v-model="searchBank" placeholder="은행검색" />

        <select v-model="selectedRateType">
          <option value="">이율 유형 전체</option>
          <option value="단리">단리</option>
          <option value="복리">복리</option>
        </select>

        <select v-model="selectedOrdering">
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
const searchDeposits = ref('')
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

  if (searchDeposits.value) params.search = searchDeposits.value
  if (searchBank.value) params.kor_co_nm = searchBank.value
  if (selectedOrdering.value) params.ordering = selectedOrdering.value
  if (selectedRateType.value) params.intr_rate_type_nm = selectedRateType.value

  axios
    .get(`${store.API_URL}/finlife/deposit/`, {
      params: params,
    })
    .then((res) => {
      store.depositProducts = res.data
      console.log(res.data)
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
* {
  font-family: 'Pretendard', sans-serif;
  box-sizing: border-box;
}

.table-wrapper {
  max-width: 900px;
  margin: 2rem auto;
  overflow-x: auto;
  background: #ffffff;
  border-radius: 20px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.04);
  padding: 1rem;
}

.filter-bar {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  align-items: center;
  justify-content: space-between;
  max-width: 900px;
  margin: 2rem auto;
  padding: 1.5rem;
  border-radius: 20px;
  background: #ffffff;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
  border: 1px solid #e5e7eb;
}

.filter-form {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  align-items: center;
}

input,
select {
  padding: 0.6rem 1rem;
  font-size: 0.9rem;
  border-radius: 12px;
  border: 1px solid #d1d5db;
  background-color: #f9fafb;
  color: #111827;
  transition: border-color 0.2s ease;
  min-width: 150px;
}

input:focus,
select:focus {
  outline: none;
  background-color: #fff;
  border-color: #3b82f6;
}

button[type='submit'] {
  padding: 0.6rem 1.2rem;
  background-color: #3b82f6;
  color: white;
  border: none;
  border-radius: 9999px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

button[type='submit']:hover {
  background-color: #2563eb;
}

/* 추천 버튼 */
.cta {
  padding: 0.6rem 1.2rem;
  background-color: #111827;
  color: #ffffff;
  border-radius: 9999px;
  font-size: 14px;
  font-weight: 600;
  border: none;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.cta:hover {
  background-color: #374151;
}

/* Flowbite Table 커스텀 */
fwb-table-head-cell {
  background-color: #f3f4f6 !important;
  font-size: 13px !important;
  font-weight: 600 !important;
  padding: 1rem !important;
  color: #6b7280 !important;
  border-bottom: 1px solid #e5e7eb !important;
}

fwb-table-cell {
  font-size: 14px !important;
  padding: 1rem !important;
  color: #111827 !important;
  white-space: nowrap;
}

fwb-table-row {
  transition: background-color 0.2s ease;
  cursor: pointer;
}

.hover\:bg-blue-100:hover {
  background-color: #eef6ff !important;
}
</style>

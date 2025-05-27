<template>
  <div>
    <div class="header-content">
      <h1 class="title">적금 상품 목록</h1>
      <p class="subtext">적금 상품을 한눈에 비교해요.</p>
      <!-- <br /><br /> -->
      <!-- <hr /> -->
    </div>
  </div>
  <div class="section">
    <div class="filter-bar">
      <form @submit.prevent="filterSavings" class="filter-form">
        <input v-model="searchSavings" placeholder="적금 이름 검색" />
        <input v-model="searchBank" placeholder="은행검색" />

        <select v-model="selectedRateType">
          <option value="">이율 유형 전체</option>
          <option value="단리">단리</option>
          <option value="복리">복리</option>
        </select>

        <select v-model="selectedOrdering">
          <option value="">기본 정렬</option>
          <option value="-interest_count">찜 많은 순</option>
          <option value="interest_count">찜 적은 순</option>
          <option value="-joined_count">가입 많은 순</option>
          <option value="joined_count">가입 적은 순</option>
        </select>
        <button type="submit">검색</button>
      </form>
      <!-- 추천받기 버튼 -->
      <button class="cta" @click="handleRecommendClick">맞춤 상품<br />추천받기</button>

      <!-- 로그인 필요 모달 -->
      <ConfirmModal
        :show="showLoginModal"
        title="로그인이 필요한 기능입니다. 로그인 하시겠습니까?"
        @confirm="goToLogin"
        @close="showLoginModal = false"
      />
    </div>
    <div class="table-wrapper">
      <fwb-table hoverable>
        <fwb-table-head>
          <!-- <fwb-table-head-cell>id</fwb-table-head-cell> -->
          <fwb-table-head-cell>금융 상품명</fwb-table-head-cell>
          <fwb-table-head-cell>은행</fwb-table-head-cell>
          <fwb-table-head-cell>최고 우대 금리</fwb-table-head-cell>
          <fwb-table-head-cell>금리 유형</fwb-table-head-cell>

          <fwb-table-head-cell>찜한 사람 수</fwb-table-head-cell>
          <fwb-table-head-cell>가입자 수</fwb-table-head-cell>
        </fwb-table-head>
        <fwb-table-body>
          <fwb-table-row
            v-for="(product, index) in store.savingProducts"
            :key="index"
            class="hover:cursor-pointer hover:bg-blue-100"
            @click="$router.push({ name: 'SavingDetailView', params: { id: product.id } })"
          >
            <!-- <fwb-table-cell>{{ product.id }}</fwb-table-cell> -->
            <fwb-table-cell>{{ product.fin_prdt_nm }}</fwb-table-cell>
            <fwb-table-cell>{{ product.kor_co_nm }}</fwb-table-cell>
            <fwb-table-cell>{{ product.max_intr_rate2 }}</fwb-table-cell>
            <fwb-table-cell>{{ product.intr_rate_type_nm }}</fwb-table-cell>
            <fwb-table-cell>{{ product.interest_count }}</fwb-table-cell>
            <fwb-table-cell>{{ product.joined_count }}</fwb-table-cell>
          </fwb-table-row>
        </fwb-table-body>
      </fwb-table>
    </div>
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
import { useSavingStore } from '@/stores/saving'
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useAccountStore } from '@/stores/user'

const searchSavings = ref('')
const searchBank = ref('')
const selectedRateType = ref('')
const selectedOrdering = ref('')
const store = useSavingStore()
const accountStore = useAccountStore()
import { useRouter } from 'vue-router'
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
const filterSavings = function () {
  const params = {}
  console.log(params)
  if (searchSavings.value) params.search = searchSavings.value
  if (searchBank.value) params.kor_co_nm = searchBank.value
  if (selectedOrdering.value) params.ordering = selectedOrdering.value
  if (selectedRateType.value) params.intr_rate_type_nm = selectedRateType.value

  axios
    .get(`${store.API_URL}/finlife/saving/`, {
      params: params,
    })
    .then((res) => {
      store.savingProducts = res.data
      console.log(res.data)
    })
    .catch((err) => {
      console.error('필터링 실패:', err)
    })
}

onMounted(() => {
  // store.getSavingProducts()
  filterSavings()
})
</script>
<style scoped>
* {
  font-family: 'Pretendard', sans-serif;
  box-sizing: border-box;
}

.filter-bar {
  /* max-width: 1200px; */
  width: 100%;
  margin: 0 auto 24px;
  padding: 24px;
  background: #ffffff;
  border: 1px solid #f2f4f6;
  border-radius: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  align-items: center;
  justify-content: space-between;
}

.filter-form {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  align-items: center;
  flex: 1;
}

input,
select {
  padding: 12px 14px;
  font-size: 14px;
  font-weight: 500;
  color: #191f28;
  background: #ffffff;
  border: 1px solid #e5e8eb;
  border-radius: 12px;
  min-width: 140px;
  transition: border-color 0.2s ease;
  outline: none;
}

input:focus,
select:focus {
  border-color: #3182f6;
  box-shadow: 0 0 0 3px rgba(49, 130, 246, 0.08);
}

input::placeholder {
  color: #b0b8c1;
  font-weight: 400;
}

button[type='submit'],
.cta {
  padding: 12px 20px;
  font-size: 14px;
  font-weight: 600;
  border: none;
  border-radius: 12px;
  min-height: 44px;
  cursor: pointer;
  transition: background-color 0.2s ease;
  white-space: nowrap;
}

button[type='submit'] {
  background: #3182f6;
  color: #ffffff;
}

button[type='submit']:hover {
  background: #1b64da;
}

.cta {
  background: #191f28;
  color: #ffffff;
}

.cta:hover {
  background: #2a3441;
}
.title {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 8px;
  text-align: center;
}
.subtext {
  font-size: 1.1rem;
  text-align: center;
  color: black;
  margin: 0;
}
.table-wrapper {
  /* max-width: 1200px;
  margin: 0 auto; */
  min-height: 100vh;
  background: #ffffff;
  border: 1px solid #f2f4f6;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
}

.section {
  background: white;
  border-radius: 20px;
  padding-top: 32px;
}
/* Flowbite 커스터마이징 */
:deep(.fwb-table th) {
  background: #f9fafb !important;
  font-size: 13px !important;
  font-weight: 600 !important;
  color: #8b95a1 !important;
  padding: 16px !important;
  border-bottom: 1px solid #e5e8eb !important;
  letter-spacing: 0.3px !important;
}

:deep(.fwb-table td) {
  font-size: 14px !important;
  font-weight: 500 !important;
  color: #191f28 !important;
  padding: 16px !important;
  border-bottom: 1px solid #f2f4f6 !important;
}

:deep(.fwb-table tr:hover) {
  background: rgba(49, 130, 246, 0.04) !important;
  cursor: pointer;
}

:deep(.fwb-table tr:last-child td) {
  border-bottom: none !important;
}
.header {
  text-align: center;
  margin-top: 10px;
  /* margin-bottom: 10px; */
  /* padding-bottom: 50px; */
}

hr {
  color: #eeeeee;
  font-weight: bold;
}
.header-content h1 {
  font-size: 2.5rem;
  font-weight: 700;
  /* margin-bottom: 8px; */
}

.subtitle {
  font-size: 1.1rem;
  color: black;
  /* margin-bottom: 30px; */
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .filter-bar {
    flex-direction: column;
    align-items: stretch;
    padding: 20px;
    margin: 0 16px 20px;
  }

  .filter-form {
    width: 100%;
    gap: 10px;
    flex-direction: column;
  }

  input,
  select,
  button {
    width: 100%;
    min-width: unset;
  }

  .cta {
    margin-top: 12px;
  }

  .table-wrapper {
    margin: 0 16px;
    overflow-x: auto;
  }
}
</style>

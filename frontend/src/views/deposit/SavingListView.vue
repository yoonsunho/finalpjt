<template>
  <div class="filter-bar">
    <form @submit.prevent="filterSavings" class="filter-form">
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
          v-for="(product, index) in store.savingProducts"
          :key="index"
          class="hover:cursor-pointer hover:bg-blue-100"
          @click="$router.push({ name: 'SavingDetailView', params: { id: product.id } })"
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
import { useSavingStore } from '@/stores/saving'
import { ref, onMounted } from 'vue'
import axios from 'axios'
const searchBank = ref('')
const selectedRateType = ref('')
const selectedOrdering = ref('')
const store = useSavingStore()

const filterSavings = function () {
  const params = {}

  if (searchBank.value) params.kor_co_nm = searchBank.value
  if (selectedOrdering.value) params.ordering = selectedOrdering.value
  if (selectedRateType.value) params.intr_rate_type_nm = selectedRateType.value

  axios
    .get(`${store.API_URL}/finlife/saving/`, {
      params: params,
    })
    .then((res) => {
      store.savingProducts = res.data
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
.table-wrapper {
  max-width: 800px;
  width: 100%;
  overflow-x: auto;
  margin: 0 auto;
  /* box-shadow: inset 0 0 3px dodgerblue; */
  border: 2px solid dodgerblue;
}

.filter-bar {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
}
input,
select {
  padding: 0.5rem;
  font-size: 0.9rem;
}
</style>

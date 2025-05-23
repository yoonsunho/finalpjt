<template>
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
import SavingList from '@/components/product/SavingList.vue';
import { useSavingStore } from '@/stores/saving';
import { onMounted } from 'vue'

const store = useSavingStore()
onMounted(()=>{
store.getSavingProducts()

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
.deposit_product_name {
    font-weight: bold;
    width: 300px;
}
</style>




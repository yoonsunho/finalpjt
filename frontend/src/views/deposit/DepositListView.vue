<template>
  <div class="table-wrapper">
    <fwb-table hoverable>
      <fwb-table-head>
        <fwb-table-head-cell>id</fwb-table-head-cell>
        <fwb-table-head-cell>예금이름</fwb-table-head-cell>
        <fwb-table-head-cell>은행</fwb-table-head-cell>
        <fwb-table-head-cell>금리</fwb-table-head-cell>
      </fwb-table-head>
      <fwb-table-body>
        <fwb-table-row
            v-for="(option, index) in store.depositProducts"
            :key="index"
            class="hover:cursor-pointer hover:bg-blue-100"
            @click="$router.push({ name: 'DepositDetailView', params: { id: option.id } })"
            >
            <fwb-table-cell>{{ option.id }}</fwb-table-cell>
            <fwb-table-cell>{{ option.deposit_product.fin_prdt_nm }}</fwb-table-cell>
            <fwb-table-cell>{{ option.deposit_product.kor_co_nm }}</fwb-table-cell>
            <fwb-table-cell>{{ option.deposit_product.mtrt_int }}</fwb-table-cell>
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

import { useDepositStore } from '@/stores/deposit'
import { onMounted } from 'vue'

const store = useDepositStore()
onMounted(() => {
  store.getDepositProducts()
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

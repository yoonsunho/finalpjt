<template>
  <fwb-table hoverable>
    <fwb-table-head>
      <fwb-table-head-cell>예적금이름</fwb-table-head-cell>
      <fwb-table-head-cell>은행</fwb-table-head-cell>
      <fwb-table-head-cell>금리</fwb-table-head-cell>
      <fwb-table-head-cell>기간</fwb-table-head-cell>
    </fwb-table-head>
    <fwb-table-body>
      <fwb-table-row>
        <fwb-table-cell>어쩌구여행적금</fwb-table-cell>
        <fwb-table-cell>신한은행</fwb-table-cell>
        <fwb-table-cell>연 2.4%</fwb-table-cell>
        <fwb-table-cell>6개월 이상</fwb-table-cell>
      </fwb-table-row>
      <fwb-table-row>
        <fwb-table-cell>어쩌구가족적금</fwb-table-cell>
        <fwb-table-cell>기업은행</fwb-table-cell>
        <fwb-table-cell>연 3.2%</fwb-table-cell>
        <fwb-table-cell>1년 이상</fwb-table-cell>
      </fwb-table-row>
      <fwb-table-row>
        <fwb-table-cell>백만원적금</fwb-table-cell>
        <fwb-table-cell>국민은행</fwb-table-cell>
        <fwb-table-cell>연 1%</fwb-table-cell>
        <fwb-table-cell>1년 이상 2년 미만</fwb-table-cell>
      </fwb-table-row>
    </fwb-table-body>
  </fwb-table>
</template>

<script setup>
import {
  FwbA,
  FwbTable,
  FwbTableBody,
  FwbTableCell,
  FwbTableHead,
  FwbTableHeadCell,
  FwbTableRow,
} from 'flowbite-vue'
</script>
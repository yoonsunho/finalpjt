<template>
  <div class="deposit-list-container">
    <h1>어떤 적금을 찾고 계신가요?</h1>
    <h2>나에게 맞는 예적금 찾아보기</h2>
    <!-- 예적금 받아오기 -->
    <!-- 근데 예금메뉴와 적금메뉴를 분리할것인가 ?? -->
    <TableComponent />
    <!-- <RouterLink :to="{ name: 'depositdetail' }">예시적금입니다..</RouterLink> -->
  </div>
</template>

<script setup>
import { ref } from 'vue'
import TableComponent from '@/components/TableComponent.vue'
// Table컴포넌트에 예적금이름 routerlink설정하기
</script>

<style scoped>
.deposit-list-container {
  display: flex;
  flex-direction: column;
  /* justify-content: center; */
  align-items: center;
}
h1 {
  font-size: 2.5rem;
}
h2 {
  font-size: 1.25rem;
}
</style>

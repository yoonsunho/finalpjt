<template>
  <div class="exchange-container">
    <h1>환율계산기</h1>
    <p>2025-10-30 기준 현재 환율은 1300원 입니다.</p>
    <fwb-select v-model="selected" :options="countries_from" label="countries-from" />
    <fwb-select v-model="selected" :options="countries_to" label="countries-to" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { FwbSelect } from 'flowbite-vue'

const selected = ref('')

const countries_from = [
  { value: 'us', name: '미국' },
  { value: 'ca', name: '일본' },
  { value: 'fr', name: '중국' },
]
const countries_to = [
  { value: 'us', name: '미국' },
  { value: 'ca', name: '일본' },
  { value: 'fr', name: '중국' },
]
</script>
<style scoped>
.exchange-container {
  padding: 0px 20rem;
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  border-radius: 1rem;
  font-family: Pretendard, sans-serif;
}
</style>

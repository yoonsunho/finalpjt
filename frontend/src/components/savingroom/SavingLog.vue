<template>
  <div>
    <h3>입금 내역</h3>
    <ul>
      <li v-for="(log, idx) in logList" :key="idx">
        <strong>{{ log.nickname }}</strong
        >님이 {{ log.amount }}원 입금함 ({{ log.memo || '메모 없음' }})
      </li>
    </ul>
  </div>
</template>

<script setup>
defineProps({ logList: Array })
</script>

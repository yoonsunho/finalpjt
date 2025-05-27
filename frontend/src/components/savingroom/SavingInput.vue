<template>
  <form @submit.prevent="submitDeposit">
    <input type="number" v-model="amount" placeholder="금액" required />
    <input type="text" v-model="memo" placeholder="메모 (선택)" />
    <button type="submit">입금</button>
  </form>
</template>

<script setup>
import { ref } from 'vue'
const props = defineProps(['roomId', 'socket'])

const amount = ref('')
const memo = ref('')

const submitDeposit = () => {
  if (!props.socket || props.socket.readyState !== 1) return alert('웹소켓 연결 안됨 ㅠㅠ')

  props.socket.send(
    JSON.stringify({
      amount: parseInt(amount.value),
      memo: memo.value,
    }),
  )

  amount.value = ''
  memo.value = ''
}
</script>

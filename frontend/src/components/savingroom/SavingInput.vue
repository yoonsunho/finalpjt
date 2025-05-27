<template>
  <form @submit.prevent="submitDeposit">
    <input type="number" v-model="amount" placeholder="금액" required />
    <input type="text" v-model="memo" placeholder="메모 (선택)" />
    <button type="submit" :disabled="isSubmitting">
      {{ isSubmitting ? '입금 중...' : '입금' }}
    </button>
  </form>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps(['roomId', 'socket'])
const emit = defineEmits(['saving-completed'])

const amount = ref('')
const memo = ref('')
const isSubmitting = ref(false)

const submitDeposit = async () => {
  if (!props.socket || props.socket.readyState !== 1) {
    return alert('웹소켓 연결 안됨 ㅠㅠ')
  }

  if (isSubmitting.value) return

  try {
    isSubmitting.value = true

    props.socket.send(
      JSON.stringify({
        amount: parseInt(amount.value),
        memo: memo.value,
      }),
    )

    // 입력 필드 초기화
    amount.value = ''
    memo.value = ''

    // 저축 완료 이벤트 emit
    setTimeout(() => {
      emit('saving-completed')
      console.log('Saving completed event emitted')
    }, 500) // WebSocket 메시지 처리 시간을 고려한 지연
  } catch (error) {
    console.error('저축 입력 오류:', error)
    alert('저축 입력 중 오류가 발생했습니다.')
  } finally {
    isSubmitting.value = false
  }
}
</script>

<style scoped>
form {
  display: flex;
  flex-direction: column;
  gap: 16px;
  max-width: 400px;
}

input {
  padding: 12px 16px;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  font-size: 16px;
  transition: border-color 0.3s ease;
}

input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

button {
  background: linear-gradient(135deg, #10b981, #059669);
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

button:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
}

button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
}
</style>

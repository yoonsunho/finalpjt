<template>
  <form @submit.prevent="submitDeposit">
    <input
      type="number"
      v-model="amount"
      placeholder="금액"
      required
      :disabled="isSubmitting || achievementRate >= 100"
    />
    <input
      type="text"
      v-model="memo"
      placeholder="메모 (선택)"
      :disabled="isSubmitting || achievementRate >= 100"
    />
    <button type="submit" :disabled="isSubmitting || achievementRate >= 100">
      {{ achievementRate >= 100 ? '입금 불가 (목표 달성!)' : isSubmitting ? '입금 중...' : '입금' }}
    </button>
  </form>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps(['roomId', 'socket', 'achievementRate'])

const amount = ref('')
const memo = ref('')
const isSubmitting = ref(false)

const submitDeposit = async () => {
  if (!props.socket || props.socket.readyState !== 1) {
    return alert('웹소켓 연결 안됨 ㅠㅠ')
  }

  if (isSubmitting.value || props.achievementRate >= 100) return

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
  } catch (error) {
    console.error('저축 입력 오류:', error)
    alert('저축 입력 중 오류가 발생했습니다.')
  } finally {
    isSubmitting.value = false
  }
}
</script>
<style scoped>
.goal-complete {
  background: linear-gradient(135deg, #d1fae5, #a7f3d0);
  border: 2px solid #10b981;
  text-align: center;
  border-radius: 20px;
  padding: 32px;
  box-shadow: 0 4px 20px rgba(16, 185, 129, 0.15);
}

.goal-complete .section-header svg {
  color: #059669;
}

.goal-complete h2 {
  font-size: 24px;
  color: #065f46;
  margin-bottom: 12px;
}

.complete-message {
  font-size: 16px;
  font-weight: 500;
  color: #065f46;
}
</style>

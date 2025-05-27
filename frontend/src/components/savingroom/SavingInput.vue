<template>
  <div>
    <!-- 달성률 100% 이상일 때 축하 메시지 -->
    <div v-if="achievementRate >= 100" class="goal-complete">
      <div class="section-header"></div>
      <h2>🎉 축하합니다! 🎉</h2>
      <p class="complete-message">목표 저축액을 달성했어요!</p>
      <!-- <div class="achievement-badge">달성률: {{ Math.round(achievementRate) }}%</div> -->
    </div>

    <!-- 입금 폼 -->
    <form @submit.prevent="submitDeposit" class="deposit-form">
      <div class="input-group">
        <input
          type="number"
          v-model="amount"
          placeholder="금액을 입력하세요"
          required
          min="1"
          :disabled="isSubmitting || achievementRate >= 100"
          :class="{ disabled: achievementRate >= 100 }"
        />
        <input
          type="text"
          v-model="memo"
          placeholder="메모 (선택사항)"
          maxlength="50"
          :disabled="isSubmitting || achievementRate >= 100"
          :class="{ disabled: achievementRate >= 100 }"
        />
      </div>

      <button
        type="submit"
        :disabled="isSubmitting || achievementRate >= 100 || !amount"
        :class="{
          'goal-achieved': achievementRate >= 100,
          submitting: isSubmitting,
        }"
      >
        <span v-if="achievementRate >= 100"> 🏆 목표 달성! 입금 완료 </span>
        <span v-else-if="isSubmitting"> 💰 입금 처리 중... </span>
        <span v-else> 💸 입금하기 </span>
      </button>

      <!-- 목표 달성 시 안내 메시지 -->
      <div v-if="achievementRate >= 100" class="achievement-notice">
        목표를 달성하여 더 이상 입금할 수 없습니다.
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  roomId: String,
  socket: Object,
  achievementRate: {
    type: Number,
    default: 0,
  },
})

const amount = ref('')
const memo = ref('')
const isSubmitting = ref(false)

// 입금 가능 여부 계산
const canDeposit = computed(() => {
  return props.achievementRate < 100 && !isSubmitting.value && amount.value > 0
})

const submitDeposit = async () => {
  // 목표 달성 시 입금 차단
  if (props.achievementRate >= 100) {
    alert('🎉 이미 목표를 달성했습니다! 축하드려요!')
    return
  }

  if (!props.socket || props.socket.readyState !== WebSocket.OPEN) {
    alert('⚠️ 연결이 불안정합니다. 잠시 후 다시 시도해주세요.')
    return
  }

  if (isSubmitting.value || !amount.value || amount.value <= 0) {
    return
  }

  try {
    isSubmitting.value = true

    props.socket.send(
      JSON.stringify({
        type: 'deposit', // 메시지 타입 명시
        amount: parseInt(amount.value),
        memo: memo.value.trim(),
        timestamp: new Date().toISOString(),
      }),
    )

    // 성공 시 폼 초기화
    amount.value = ''
    memo.value = ''
  } catch (error) {
    console.error('저축 입력 오류:', error)
    alert('💥 저축 입력 중 오류가 발생했습니다. 다시 시도해주세요.')
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
  margin-bottom: 24px;
  box-shadow: 0 8px 32px rgba(16, 185, 129, 0.2);
  animation: celebration 0.6s ease-out;
}

@keyframes celebration {
  0% {
    transform: scale(0.9);
    opacity: 0;
  }
  50% {
    transform: scale(1.05);
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
}

.goal-complete h2 {
  font-size: 28px;
  color: #065f46;
  margin-bottom: 12px;
  font-weight: bold;
}

.complete-message {
  font-size: 18px;
  font-weight: 600;
  color: #065f46;
  margin-bottom: 16px;
}

.achievement-badge {
  display: inline-block;
  background: #059669;
  color: white;
  padding: 8px 16px;
  border-radius: 20px;
  font-weight: bold;
  font-size: 14px;
}

.deposit-form {
  background: #f8fafc;
  padding: 24px;
  border-radius: 16px;
  border: 1px solid #e2e8f0;
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 16px;
}

input {
  padding: 12px 16px;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  font-size: 16px;
  transition: all 0.3s ease;
}

input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

input.disabled {
  background-color: #f1f5f9;
  color: #94a3b8;
  cursor: not-allowed;
  border-color: #cbd5e1;
}

button {
  width: 100%;
  padding: 14px 20px;
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-bottom: 12px;
}

button:hover:not(:disabled) {
  background: linear-gradient(135deg, #2563eb, #1e40af);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
}

button:disabled {
  cursor: not-allowed;
  opacity: 0.6;
  transform: none;
  box-shadow: none;
}

button.goal-achieved {
  background: linear-gradient(135deg, #10b981, #059669);
  cursor: not-allowed;
}

button.submitting {
  background: linear-gradient(135deg, #f59e0b, #d97706);
}

.achievement-notice {
  text-align: center;
  color: #059669;
  font-weight: 600;
  font-size: 14px;
  padding: 8px;
  background: #d1fae5;
  border-radius: 8px;
  border: 1px solid #a7f3d0;
}

/* 반응형 디자인 */
@media (max-width: 480px) {
  .goal-complete {
    padding: 24px 16px;
  }

  .goal-complete h2 {
    font-size: 24px;
  }

  .complete-message {
    font-size: 16px;
  }

  .deposit-form {
    padding: 20px 16px;
  }
}
</style>

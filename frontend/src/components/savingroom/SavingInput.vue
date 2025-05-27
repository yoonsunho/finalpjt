<template>
  <div>
    <!-- 달성률 100% 이상일 때 축하 메시지 -->
    <div v-if="achievementRate >= 100" class="goal-complete">
      <div class="celebration-icon">🎉</div>
      <h3>목표 달성 완료!</h3>
      <p>축하드려요! 저축 목표를 달성했어요</p>
    </div>

    <!-- 목표 초과 입금 시 안내 메시지 -->
    <div v-if="exceedsGoal && amount && achievementRate < 100" class="warning-message">
      <div class="warning-icon">⚠️</div>
      <span>목표 금액을 초과할 수 없어요</span>
    </div>

    <!-- 입금 폼 -->
    <form @submit.prevent="submitDeposit" class="deposit-form">
      <div class="input-section">
        <div class="amount-input-wrapper">
          <input
            type="number"
            v-model.number="amount"
            placeholder="입금할 금액을 입력하세요"
            required
            min="1"
            :disabled="isSubmitting || achievementRate >= 100"
            :class="{
              disabled: achievementRate >= 100,
              error: exceedsGoal && amount,
            }"
            class="amount-input"
          />
          <span class="currency">원</span>
        </div>

        <input
          type="text"
          v-model="memo"
          placeholder="메모 (선택사항)"
          maxlength="50"
          :disabled="isSubmitting || achievementRate >= 100"
          :class="{ disabled: achievementRate >= 100 }"
          class="memo-input"
        />
      </div>

      <div v-if="amount && achievementRate < 100 && !exceedsGoal" class="amount-preview">
        <div class="preview-item">
          <span class="preview-label">입금 후 누적 금액</span>
          <span class="preview-value">{{ (totalSaved + (amount || 0)).toLocaleString() }}원</span>
        </div>
        <div class="preview-item">
          <span class="preview-label">달성률</span>
          <span class="preview-value achievement"
            >{{ Math.round(((totalSaved + (amount || 0)) / goalAmount) * 100) }}%</span
          >
        </div>
      </div>

      <button
        type="submit"
        :disabled="!canDeposit"
        :class="{
          'goal-achieved': achievementRate >= 100,
          submitting: isSubmitting,
          error: exceedsGoal && amount,
        }"
        class="submit-btn"
      >
        <div class="btn-content">
          <div v-if="achievementRate >= 100" class="btn-icon">🏆</div>
          <div v-else-if="exceedsGoal && amount" class="btn-icon">⚠️</div>
          <div v-else-if="isSubmitting" class="spinner-icon"></div>
          <div v-else class="btn-icon">💰</div>

          <span v-if="achievementRate >= 100">목표 달성 완료</span>
          <span v-else-if="exceedsGoal && amount">입금 금액 초과</span>
          <span v-else-if="isSubmitting">입금 처리 중...</span>
          <span v-else>입금하기</span>
        </div>
      </button>

      <div v-if="remainingAmount > 0 && achievementRate < 100" class="remaining-info">
        목표까지 <strong>{{ remainingAmount.toLocaleString() }}원</strong> 남았어요
      </div>

      <div v-if="achievementRate >= 100" class="completion-message">
        🎯 목표를 달성하여 더 이상 입금할 수 없습니다
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  roomId: [String, Number],
  socket: Object,
  achievementRate: { type: Number, default: 0 },
  totalSaved: { type: Number, default: 0 },
  goalAmount: { type: Number, default: 0 },
})

const amount = ref(0)
const memo = ref('')
const isSubmitting = ref(false)

const remainingAmount = computed(() => {
  return Math.max(0, props.goalAmount - props.totalSaved)
})

const exceedsGoal = computed(() => {
  const deposit = parseInt(amount.value)

  if (!deposit || isNaN(deposit) || deposit <= 0) {
    return false
  }

  if (props.achievementRate >= 100) {
    return false
  }

  return props.totalSaved + deposit > props.goalAmount
})

const canDeposit = computed(() => {
  const deposit = parseInt(amount.value)
  return props.achievementRate < 100 && !isSubmitting.value && deposit > 0 && !exceedsGoal.value
})

const submitDeposit = async () => {
  if (props.achievementRate >= 100) {
    return
  }

  if (exceedsGoal.value) {
    return
  }

  if (!props.socket || props.socket.readyState !== WebSocket.OPEN) {
    alert('연결이 불안정합니다. 잠시 후 다시 시도해주세요.')
    return
  }

  if (isSubmitting.value || !amount.value || amount.value <= 0) return

  try {
    isSubmitting.value = true

    props.socket.send(
      JSON.stringify({
        type: 'deposit',
        amount: parseInt(amount.value),
        memo: memo.value.trim(),
        timestamp: new Date().toISOString(),
      }),
    )

    amount.value = ''
    memo.value = ''
  } catch (error) {
    console.error('저축 입력 오류:', error)
    alert('저축 입력 중 오류가 발생했습니다. 다시 시도해주세요.')
  } finally {
    isSubmitting.value = false
  }
}
</script>

<style scoped>
.goal-complete {
  background: linear-gradient(135deg, #e8f5e8, #d4edda);
  border: 1px solid #c3e6cb;
  text-align: center;
  border-radius: 16px;
  padding: 32px 24px;
  margin-bottom: 20px;
  animation: slideIn 0.4s ease-out;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.celebration-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.goal-complete h3 {
  color: #155724;
  font-size: 20px;
  font-weight: 700;
  margin: 0 0 8px 0;
}

.goal-complete p {
  color: #155724;
  font-size: 15px;
  margin: 0;
  opacity: 0.8;
}

.warning-message {
  display: flex;
  align-items: center;
  gap: 8px;
  background: #fff3cd;
  border: 1px solid #ffeaa7;
  border-radius: 12px;
  padding: 12px 16px;
  margin-bottom: 16px;
  color: #856404;
  font-size: 14px;
  font-weight: 500;
}

.warning-icon {
  font-size: 16px;
}

.deposit-form {
  background: #f8f9fa;
  border-radius: 16px;
  padding: 24px;
  border: 1px solid #f1f3f4;
}

.input-section {
  margin-bottom: 20px;
}

.amount-input-wrapper {
  position: relative;
  margin-bottom: 12px;
}

.amount-input {
  width: 100%;
  padding: 16px 40px 16px 16px;
  border: 2px solid #e8eaed;
  border-radius: 12px;
  font-size: 18px;
  font-weight: 600;
  background: white;
  transition: all 0.2s ease;
  box-sizing: border-box;
}

.amount-input:focus {
  outline: none;
  border-color: #4285f4;
  box-shadow: 0 0 0 3px rgba(66, 133, 244, 0.1);
}

.amount-input.error {
  border-color: #ea4335;
  box-shadow: 0 0 0 3px rgba(234, 67, 53, 0.1);
}

.amount-input.disabled {
  background: #f8f9fa;
  color: #9aa0a6;
  cursor: not-allowed;
  border-color: #e8eaed;
}

.currency {
  position: absolute;
  right: 16px;
  top: 50%;
  transform: translateY(-50%);
  color: #6b7684;
  font-size: 16px;
  font-weight: 500;
  pointer-events: none;
}

.memo-input {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid #e8eaed;
  border-radius: 12px;
  font-size: 15px;
  background: white;
  transition: all 0.2s ease;
  box-sizing: border-box;
}

.memo-input:focus {
  outline: none;
  border-color: #4285f4;
  box-shadow: 0 0 0 3px rgba(66, 133, 244, 0.1);
}

.memo-input.disabled {
  background: #f8f9fa;
  color: #9aa0a6;
  cursor: not-allowed;
  border-color: #e8eaed;
}

.amount-preview {
  background: white;
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 20px;
  border: 1px solid #e8eaed;
}

.preview-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.preview-item:last-child {
  margin-bottom: 0;
}

.preview-label {
  font-size: 14px;
  color: #6b7684;
  font-weight: 500;
}

.preview-value {
  font-size: 15px;
  color: #191f28;
  font-weight: 600;
}

.preview-value.achievement {
  color: #4285f4;
}

.submit-btn {
  width: 100%;
  padding: 16px;
  border: none;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  margin-bottom: 16px;
  background: #4285f4;
  color: white;
}

.submit-btn:hover:not(:disabled) {
  background: #3367d6;
  transform: translateY(-1px);
}

.submit-btn:disabled {
  cursor: not-allowed;
  opacity: 0.6;
  transform: none;
}

.submit-btn.goal-achieved {
  background: #34a853;
}

.submit-btn.submitting {
  background: #fbbc04;
  color: #1a1a1a;
}

.submit-btn.error {
  background: #ea4335;
}

.btn-content {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.btn-icon {
  font-size: 18px;
}

.spinner-icon {
  width: 18px;
  height: 18px;
  border: 2px solid rgba(26, 26, 26, 0.3);
  border-top: 2px solid #1a1a1a;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.remaining-info {
  text-align: center;
  color: #6b7684;
  font-size: 14px;
  padding: 12px;
  background: white;
  border-radius: 8px;
  border: 1px solid #e8eaed;
}

.completion-message {
  text-align: center;
  color: #34a853;
  font-size: 14px;
  font-weight: 500;
  padding: 12px;
  background: #e8f5e8;
  border-radius: 8px;
  border: 1px solid #c3e6cb;
}

/* 반응형 */
@media (max-width: 480px) {
  .deposit-form {
    padding: 20px;
  }

  .goal-complete {
    padding: 24px 20px;
  }

  .celebration-icon {
    font-size: 40px;
  }

  .amount-input {
    font-size: 16px;
  }
}
</style>

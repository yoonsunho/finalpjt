<template>
  <div class="create-room">
    <div class="header">
      <button @click="goBack" class="btn-back">
        <svg
          width="20"
          height="20"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
        >
          <path d="M19 12H5M12 19l-7-7 7-7" />
        </svg>
      </button>
      <div class="header-content">
        <h1>공동 저축방 만들기</h1>
        <p class="subtitle">친구들과 함께할 저축방을 만들어보세요</p>
      </div>
    </div>

    <div class="form-container">
      <form @submit.prevent="createRoom" class="create-form">
        <div class="form-section">
          <h2>기본 정보</h2>

          <div class="form-group">
            <label for="name">
              <svg
                width="20"
                height="20"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
              >
                <path d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2H5a2 2 0 00-2-2z" />
                <path d="M8 21v-4a2 2 0 012-2h4a2 2 0 012 2v4" />
              </svg>
              방 이름
            </label>
            <input
              id="name"
              v-model="name"
              placeholder="저축방 이름을 입력하세요"
              required
              class="form-input"
            />
          </div>

          <div class="form-group">
            <label for="description">
              <svg
                width="20"
                height="20"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
              >
                <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z" />
                <polyline points="14,2 14,8 20,8" />
                <line x1="16" y1="13" x2="8" y2="13" />
                <line x1="16" y1="17" x2="8" y2="17" />
                <polyline points="10,9 9,9 8,9" />
              </svg>
              설명
            </label>
            <textarea
              id="description"
              v-model="description"
              placeholder="저축방에 대한 설명을 입력하세요"
              rows="4"
              class="form-textarea"
            />
          </div>
        </div>

        <div class="form-section">
          <h2>목표 설정</h2>

          <div class="form-group">
            <label for="goalAmount">
              <svg
                width="20"
                height="20"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
              >
                <line x1="12" y1="1" x2="12" y2="23" />
                <path d="M17 5H9.5a3.5 3.5 0 000 7h5a3.5 3.5 0 010 7H6" />
              </svg>
              목표 금액
            </label>
            <div class="input-with-unit">
              <input
                id="goalAmount"
                v-model.number="goalAmount"
                type="number"
                placeholder="목표 금액을 입력하세요"
                required
                min="1"
                class="form-input"
              />
              <span class="unit">원</span>
            </div>
            <div v-if="goalAmount" class="amount-display">
              {{ goalAmount?.toLocaleString?.() }}원
            </div>
          </div>

          <div class="form-group">
            <label for="deadline">
              <svg
                width="20"
                height="20"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
              >
                <rect x="3" y="4" width="18" height="18" rx="2" ry="2" />
                <line x1="16" y1="2" x2="16" y2="6" />
                <line x1="8" y1="2" x2="8" y2="6" />
                <line x1="3" y1="10" x2="21" y2="10" />
              </svg>
              마감일
            </label>
            <input
              id="deadline"
              v-model="deadline"
              type="date"
              required
              :min="today"
              class="form-input"
            />
          </div>
        </div>

        <div class="form-actions">
          <button type="button" @click="goBack" class="btn-cancel">취소</button>
          <button type="submit" :disabled="isSubmitting" class="btn-submit">
            <svg
              v-if="isSubmitting"
              width="20"
              height="20"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              class="spinner"
            >
              <path d="M21 12a9 9 0 11-6.219-8.56" />
            </svg>
            <svg
              v-else
              width="20"
              height="20"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
            >
              <path d="M12 5v14M5 12h14" />
            </svg>
            {{ isSubmitting ? '생성 중...' : '저축방 생성하기' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { useAccountStore } from '@/stores/user'

const accountStore = useAccountStore()
const name = ref('')
const description = ref('')
const goalAmount = ref(null)
const deadline = ref('')
const isSubmitting = ref(false)
const router = useRouter()

const API_URL = 'http://127.0.0.1:8000'

// 오늘 날짜를 YYYY-MM-DD 형식으로 반환
const today = computed(() => {
  return new Date().toISOString().split('T')[0]
})

const createRoom = async () => {
  if (isSubmitting.value) return

  try {
    isSubmitting.value = true

    const res = await axios.post(
      `${API_URL}/savingroom/`,
      {
        name: name.value,
        description: description.value,
        goal_amount: goalAmount.value,
        deadline: deadline.value,
      },
      {
        headers: {
          Authorization: `Token ${accountStore.token}`,
        },
      },
    )

    // 성공 시 상세 페이지로 이동
    router.push({
      name: 'SharedSavingRoomDetailView',
      params: { id: res.data.id },
    })
  } catch (err) {
    console.error('Room creation error:', err)

    let errorMessage = '생성에 실패했습니다.'

    if (err.response) {
      // 서버에서 응답이 온 경우
      if (err.response.status === 400) {
        errorMessage = '입력 정보를 확인해주세요.'
      } else if (err.response.status === 401) {
        errorMessage = '로그인이 필요합니다.'
      } else if (err.response.status === 500) {
        errorMessage = '서버 오류가 발생했습니다.'
      }
    } else if (err.request) {
      // 네트워크 오류
      errorMessage = '네트워크 연결을 확인해주세요.'
    }

    alert(errorMessage)
  } finally {
    isSubmitting.value = false
  }
}

const goBack = () => {
  router.back()
}
</script>

<style scoped>
.create-room {
  max-width: 800px;
  margin: 0 auto;
  padding: 32px 24px;
  min-height: 100vh;
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
}

.header {
  display: flex;
  align-items: flex-start;
  gap: 20px;
  margin-bottom: 40px;
}

.btn-back {
  background: white;
  border: none;
  padding: 12px;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  color: #64748b;
}

.btn-back:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
  color: #3b82f6;
}

.header-content h1 {
  color: #1e293b;
  margin: 0 0 8px 0;
  font-size: 32px;
  font-weight: 700;
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.subtitle {
  color: #64748b;
  margin: 0;
  font-size: 16px;
  font-weight: 400;
}

.form-container {
  background: white;
  border-radius: 20px;
  padding: 40px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.create-form {
  display: flex;
  flex-direction: column;
  gap: 32px;
}

.form-section {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.form-section h2 {
  color: #1e293b;
  font-size: 20px;
  font-weight: 600;
  margin: 0;
  padding-bottom: 8px;
  border-bottom: 2px solid #e2e8f0;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  color: #374151;
  font-size: 14px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.form-group label svg {
  color: #3b82f6;
}

.form-input,
.form-textarea {
  width: 100%;
  padding: 16px;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  font-size: 16px;
  box-sizing: border-box;
  transition: all 0.3s ease;
  background: #fafbfc;
}

.form-input:focus,
.form-textarea:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1);
  background: white;
}

.form-textarea {
  resize: vertical;
  min-height: 120px;
  font-family: inherit;
}

.input-with-unit {
  position: relative;
  display: flex;
  align-items: center;
}

.input-with-unit .form-input {
  padding-right: 50px;
}

.unit {
  position: absolute;
  right: 16px;
  color: #64748b;
  font-weight: 600;
}

.amount-display {
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  color: white;
  padding: 12px 16px;
  border-radius: 8px;
  text-align: center;
  font-weight: 600;
  font-size: 18px;
}

.form-actions {
  display: flex;
  gap: 16px;
  justify-content: flex-end;
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #e2e8f0;
}

.btn-cancel,
.btn-submit {
  padding: 16px 24px;
  border: none;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 8px;
}

.btn-cancel {
  background: #f1f5f9;
  color: #64748b;
  border: 2px solid #e2e8f0;
}

.btn-cancel:hover {
  background: #e2e8f0;
  transform: translateY(-1px);
}

.btn-submit {
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  color: white;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

.btn-submit:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(59, 130, 246, 0.4);
}

.btn-submit:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
}

.spinner {
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

/* 반응형 디자인 */
@media (max-width: 768px) {
  .create-room {
    padding: 16px;
  }

  .header {
    flex-direction: column;
    gap: 16px;
  }

  .header-content h1 {
    font-size: 24px;
  }

  .form-container {
    padding: 24px;
  }

  .form-actions {
    flex-direction: column-reverse;
  }

  .btn-cancel,
  .btn-submit {
    width: 100%;
    justify-content: center;
  }
}
</style>

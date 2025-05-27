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
  max-width: 720px;
  margin: 0 auto;
  padding: 24px 16px;
  background: #ffffff;
}

.header {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  margin-bottom: 32px;
}

.btn-back {
  background: none;
  border: none;
  padding: 8px;
  border-radius: 8px;
  cursor: pointer;
  color: #4b5563;
}

.btn-back:hover {
  background: #f1f5f9;
}

.header-content h1 {
  font-size: 24px;
  font-weight: 600;
  color: #1f2937;
}

.subtitle {
  font-size: 14px;
  color: #6b7280;
}

.form-container {
  background: #f9fafb;
  border-radius: 12px;
  padding: 24px;
  border: 1px solid #e5e7eb;
}

.form-section {
  margin-bottom: 24px;
}

.form-section h2 {
  font-size: 16px;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 16px;
  border-bottom: 1px solid #e5e7eb;
  padding-bottom: 8px;
}

.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  font-weight: 500;
  color: #374151;
  margin-bottom: 6px;
}

.form-input,
.form-textarea {
  width: 100%;
  padding: 12px;
  border-radius: 8px;
  font-size: 14px;
  border: 1px solid #e5e7eb;
  background: #ffffff;
}

.form-input:focus,
.form-textarea:focus {
  outline: none;
  border-color: #3182f6;
  box-shadow: 0 0 0 2px rgba(49, 130, 246, 0.15);
}

.form-textarea {
  resize: vertical;
  min-height: 100px;
  font-family: inherit;
}

.input-with-unit {
  position: relative;
  display: flex;
  align-items: center;
}

.input-with-unit .unit {
  position: absolute;
  right: 16px;
  font-size: 14px;
  color: #6b7280;
}

.amount-display {
  margin-top: 8px;
  text-align: right;
  font-weight: 600;
  color: #1f2937;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 24px;
}

.btn-cancel,
.btn-submit {
  padding: 12px 20px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  border: none;
  transition: 0.2s;
}

.btn-cancel {
  background: #f3f4f6;
  color: #374151;
}

.btn-cancel:hover {
  background: #e5e7eb;
}

.btn-submit {
  background: #3182f6;
  color: white;
}

.btn-submit:disabled {
  background: #9ca3af;
  cursor: not-allowed;
}

@media (max-width: 768px) {
  .create-room {
    padding: 16px;
  }
  .header {
    flex-direction: column;
    gap: 12px;
  }
  .form-container {
    padding: 20px;
  }
  .form-actions {
    flex-direction: column-reverse;
    align-items: stretch;
  }
  .btn-cancel,
  .btn-submit {
    width: 100%;
  }
}
</style>

<template>
  <div class="create-room">
    <h1>공동 저축방 만들기</h1>
    <form @submit.prevent="createRoom">
      <div class="form-group">
        <label for="name">방 이름</label>
        <input id="name" v-model="name" placeholder="방 이름을 입력하세요" required />
      </div>

      <div class="form-group">
        <label for="description">설명</label>
        <textarea
          id="description"
          v-model="description"
          placeholder="저축방에 대한 설명을 입력하세요"
          rows="4"
        />
      </div>

      <div class="form-group">
        <label for="goalAmount">목표 금액 (원)</label>
        <input
          id="goalAmount"
          v-model.number="goalAmount"
          type="number"
          placeholder="목표 금액을 입력하세요"
          required
          min="1"
        />
      </div>

      <div class="form-group">
        <label for="deadline">마감일</label>
        <input id="deadline" v-model="deadline" type="date" required :min="today" />
      </div>

      <div class="form-actions">
        <button type="button" @click="goBack" class="btn-cancel">취소</button>
        <button type="submit" :disabled="isSubmitting" class="btn-submit">
          {{ isSubmitting ? '생성 중...' : '생성하기' }}
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const name = ref('')
const description = ref('')
const goalAmount = ref(null)
const deadline = ref('')
const isSubmitting = ref(false)
const router = useRouter()

// 오늘 날짜를 YYYY-MM-DD 형식으로 반환
const today = computed(() => {
  return new Date().toISOString().split('T')[0]
})

const createRoom = async () => {
  if (isSubmitting.value) return

  try {
    isSubmitting.value = true

    const res = await axios.post('/savingroom/', {
      name: name.value,
      description: description.value,
      goal_amount: goalAmount.value,
      deadline: deadline.value,
    })

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
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
}

.create-room h1 {
  text-align: center;
  margin-bottom: 30px;
  color: #333;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
  color: #555;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 16px;
  box-sizing: border-box;
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.25);
}

.form-group textarea {
  resize: vertical;
  min-height: 100px;
}

.form-actions {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
  margin-top: 30px;
}

.btn-cancel,
.btn-submit {
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-cancel {
  background-color: #6c757d;
  color: white;
}

.btn-cancel:hover {
  background-color: #545b62;
}

.btn-submit {
  background-color: #007bff;
  color: white;
}

.btn-submit:hover:not(:disabled) {
  background-color: #0056b3;
}

.btn-submit:disabled {
  background-color: #6c757d;
  cursor: not-allowed;
}
</style>

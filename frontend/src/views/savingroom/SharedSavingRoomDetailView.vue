<template>
  <div class="room-detail">
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
        <h1 v-if="room">{{ room.name }}</h1>
        <p v-if="room" class="subtitle">{{ room.description }}</p>
      </div>
    </div>

    <div v-if="loading" class="loading">
      <div class="spinner"></div>
      <p>저축방 정보를 불러오는 중...</p>
    </div>

    <div v-else-if="error" class="error">
      <div class="error-icon">⚠️</div>
      <h3>오류가 발생했습니다</h3>
      <p>{{ error }}</p>
      <button @click="fetchRoomDetail" class="btn-retry">다시 시도</button>
    </div>

    <div v-else-if="room" class="content">
      <!-- 목표 정보 섹션 -->
      <div class="goal-section">
        <div class="goal-card">
          <div class="goal-header">
            <svg
              width="24"
              height="24"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
            >
              <circle cx="12" cy="12" r="10" />
              <path d="M12 6v6l4 2" />
            </svg>
            <h2>목표 정보</h2>
          </div>
          <div class="goal-details">
            <div class="goal-item">
              <span class="label">목표 금액</span>
              <span class="value">{{ room.goal_amount?.toLocaleString?.() }}원</span>
            </div>
            <div class="goal-item">
              <span class="label">현재 달성률</span>
              <span class="value achievement-rate">{{ room.achievement_rate }}%</span>
            </div>
            <div class="goal-item">
              <span class="label">마감일</span>
              <span class="value">{{ formatDate(room.deadline) }}</span>
            </div>
          </div>
          <div class="progress-bar">
            <div
              class="progress-fill"
              :style="{ width: `${Math.min(room.achievement_rate, 100)}%` }"
            ></div>
          </div>
        </div>
      </div>

      <!-- 참가 버튼 -->
      <div v-if="!joined" class="join-section">
        <button @click="joinRoom" :disabled="isJoining" class="btn-join">
          <svg
            v-if="isJoining"
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
            <path d="M16 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2" />
            <circle cx="8.5" cy="7" r="4" />
            <line x1="20" y1="8" x2="20" y2="14" />
            <line x1="23" y1="11" x2="17" y2="11" />
          </svg>
          {{ isJoining ? '참가 중...' : '저축방 참가하기' }}
        </button>
      </div>

      <!-- 저축 입력 섹션 -->
      <div v-if="joined" class="saving-section">
        <div class="section-header">
          <svg
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
          >
            <line x1="12" y1="1" x2="12" y2="23" />
            <path d="M17 5H9.5a3.5 3.5 0 000 7h5a3.5 3.5 0 010 7H6" />
          </svg>
          <h2>저축하기</h2>
        </div>
        <SavingInput :roomId="room.id" :socket="socket" @saving-completed="refreshLogs" />
      </div>

      <!-- 참가자 목록 섹션 -->
      <div class="participants-section">
        <div class="section-header">
          <svg
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
          >
            <path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2" />
            <circle cx="9" cy="7" r="4" />
            <path d="M23 21v-2a4 4 0 00-3-3.87" />
            <path d="M16 3.13a4 4 0 010 7.75" />
          </svg>
          <h2>참가자 목록 ({{ room.participants?.length || 0 }}명)</h2>
        </div>
        <div class="participants-grid">
          <div
            v-for="participant in room.participants"
            :key="participant.id"
            class="participant-card"
          >
            <div class="participant-avatar">
              {{ participant.user.nickname.charAt(0).toUpperCase() }}
            </div>
            <div class="participant-info">
              <h3>{{ participant.user.nickname }}</h3>
              <p class="participant-amount">{{ participant.total_saved?.toLocaleString?.() }}원</p>
            </div>
          </div>
        </div>
      </div>

      <!-- 저축 로그 섹션 -->
      <div v-if="joined" class="log-section">
        <div class="section-header">
          <svg
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
          >
            <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z" />
            <polyline points="14,2 14,8 20,8" />
            <line x1="16" y1="13" x2="8" y2="13" />
            <line x1="16" y1="17" x2="8" y2="17" />
          </svg>
          <h2>저축 기록</h2>
          <button @click="refreshLogs" class="btn-refresh">
            <svg
              width="16"
              height="16"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
            >
              <polyline points="23 4 23 10 17 10"></polyline>
              <polyline points="1 20 1 14 7 14"></polyline>
              <path d="M20.49 9A9 9 0 0 0 5.64 5.64L1 10m22 4l-4.64 4.36A9 9 0 0 1 3.51 15"></path>
            </svg>
          </button>
        </div>
        <SavingLog :logList="logList" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAccountStore } from '@/stores/user'
import axios from 'axios'
import SavingInput from '@/components/savingroom/SavingInput.vue'
import SavingLog from '@/components/savingroom/SavingLog.vue'

const API_URL = 'http://127.0.0.1:8000'
const route = useRoute()
const router = useRouter()
const accountStore = useAccountStore()

const room = ref(null)
const socket = ref(null)
const logList = ref([])
const joined = ref(false)
const loading = ref(false)
const error = ref('')
const isJoining = ref(false)

const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('ko-KR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  })
}

// 현재 사용자가 이미 참가자인지 확인하는 함수
const checkIfUserJoined = () => {
  if (!room.value?.participants || !accountStore.user?.id) return

  const isParticipant = room.value.participants.some(
    (participant) => participant.user.id === accountStore.user.id,
  )

  if (isParticipant) {
    joined.value = true
  }
}

// 방 데이터만 업데이트하는 함수 (참가 로직 없음)
const updateRoomData = async () => {
  try {
    const res = await axios.get(`${API_URL}/savingroom/${route.params.id}/`, {
      headers: {
        Authorization: `Token ${accountStore.token}`,
      },
    })
    room.value = res.data
    console.log('Room data updated:', res.data)

    // 참가 상태 재확인
    checkIfUserJoined()
  } catch (err) {
    console.error('Failed to update room data:', err)
  }
}

const fetchRoomDetail = async () => {
  try {
    loading.value = true
    error.value = ''

    // API 엔드포인트 통일 - /savingroom/ 사용
    const res = await axios.get(`${API_URL}/savingroom/${route.params.id}/`, {
      headers: {
        Authorization: `Token ${accountStore.token}`,
      },
    })
    room.value = res.data
    console.log('room data:', res.data)

    // 사용자가 이미 참가자인지 확인
    checkIfUserJoined()

    // 참가하지 않은 경우에만 참가 시도
    if (!joined.value) {
      await tryJoinRoom()
    } else if (!socket.value) {
      // 이미 참가했지만 WebSocket이 연결되지 않은 경우 연결
      setupWebSocket()
    }
  } catch (err) {
    console.error('Failed to fetch room detail:', err)

    if (err.response) {
      if (err.response.status === 401) {
        error.value = '로그인이 필요합니다.'
      } else if (err.response.status === 404) {
        error.value = '존재하지 않는 저축방입니다.'
      } else if (err.response.status === 500) {
        error.value = '서버에 일시적인 문제가 발생했습니다.'
      } else {
        error.value = '저축방 정보를 불러오는데 실패했습니다.'
      }
    } else if (err.request) {
      error.value = '네트워크 연결을 확인해주세요.'
    } else {
      error.value = '알 수 없는 오류가 발생했습니다.'
    }
  } finally {
    loading.value = false
  }
}

const fetchSavingLogs = async () => {
  try {
    const res = await axios.get(`${API_URL}/savingroom/${route.params.id}/logs/`, {
      headers: {
        Authorization: `Token ${accountStore.token}`,
      },
    })
    logList.value = res.data
    console.log('Saving logs fetched:', res.data)
  } catch (err) {
    console.error('저축 기록 불러오기 실패:', err)
    // 권한 문제가 아닌 경우에만 에러 처리
    if (err.response?.status !== 403) {
      console.error('Failed to fetch saving logs:', err)
    }
  }
}

// 로그 새로고침 함수
const refreshLogs = async () => {
  console.log('Refreshing logs...')
  await fetchSavingLogs()
}

const tryJoinRoom = async () => {
  try {
    await axios.post(
      `${API_URL}/savingroom/${route.params.id}/join/`,
      {},
      {
        headers: {
          Authorization: `Token ${accountStore.token}`,
        },
      },
    )
    joined.value = true
    setupWebSocket()
  } catch (err) {
    console.error('tryJoinRoom error:', err.response?.data)
    if (err.response?.status === 400 && err.response?.data?.detail === '이미 참가한 방입니다.') {
      joined.value = true
      setupWebSocket()
    }
  }
}

const joinRoom = async () => {
  if (isJoining.value) return

  try {
    isJoining.value = true
    await axios.post(
      `${API_URL}/savingroom/${room.value.id}/join/`,
      {},
      {
        headers: {
          Authorization: `Token ${accountStore.token}`,
        },
      },
    )
    joined.value = true

    // 참가 후 순차적으로 데이터 업데이트
    await updateRoomData()
    await fetchSavingLogs()

    // WebSocket 연결
    setupWebSocket()
  } catch (err) {
    console.error('Join room error:', err)

    let errorMessage = '참가에 실패했습니다.'
    if (err.response?.status === 400) {
      errorMessage = '이미 참가한 방입니다.'
      joined.value = true
      // 이미 참가한 경우에도 데이터 다시 로드
      await updateRoomData()
      await fetchSavingLogs()
      setupWebSocket()
    } else if (err.response?.status === 401) {
      errorMessage = '로그인이 필요합니다.'
    }

    if (err.response?.status !== 400) {
      alert(errorMessage)
    }
  } finally {
    isJoining.value = false
  }
}

const setupWebSocket = () => {
  // 중복 연결 방지
  if (socket.value || !joined.value) return

  const token = accountStore.token
  const ws = new WebSocket(`ws://localhost:8000/ws/savings/${route.params.id}/?token=${token}`)

  ws.onopen = () => {
    console.log('WebSocket connected')
  }

  ws.onmessage = async (e) => {
    const data = JSON.parse(e.data)
    console.log('WebSocket message received:', data)

    // 로그 데이터 업데이트 (중복 체크 개선)
    if (data.id && !logList.value.some((log) => log.id === data.id)) {
      logList.value = [data, ...logList.value]
      console.log('New log added to list:', data)
    }

    // 방 데이터 업데이트 (약간의 지연을 두어 서버 업데이트 완료 후 호출)
    setTimeout(async () => {
      await updateRoomData()
    }, 100)
  }

  ws.onclose = () => {
    console.log('WebSocket disconnected')
    socket.value = null
  }

  ws.onerror = (error) => {
    console.error('WebSocket error:', error)
  }

  socket.value = ws
}

const goBack = () => {
  router.back()
}

// 추가: 저축 입력 후 수동으로 로그 새로고침하는 함수
defineExpose({
  refreshLogs,
})

onMounted(async () => {
  await fetchRoomDetail()
  // 참가 여부와 관계없이 로그 조회 시도
  await fetchSavingLogs()
})

onBeforeUnmount(() => {
  if (socket.value) {
    socket.value.close()
    socket.value = null
  }
})
</script>

<style scoped>
.room-detail {
  max-width: 1200px;
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
  line-height: 1.6;
}

.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 20px;
  background: white;
  border-radius: 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #e2e8f0;
  border-top: 3px solid #3b82f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 16px;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.loading p {
  color: #64748b;
  font-size: 16px;
  margin: 0;
}

.error {
  text-align: center;
  padding: 60px 40px;
  background: white;
  border-radius: 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  border-left: 4px solid #ef4444;
}

.error-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.error h3 {
  color: #1e293b;
  margin: 0 0 12px 0;
  font-size: 24px;
  font-weight: 600;
}

.error p {
  color: #64748b;
  margin: 0 0 24px 0;
  font-size: 16px;
}

.btn-retry {
  background: linear-gradient(135deg, #ef4444, #dc2626);
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-retry:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
}

.content {
  display: flex;
  flex-direction: column;
  gap: 32px;
}

.goal-section {
  background: white;
  border-radius: 20px;
  padding: 32px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.goal-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 24px;
}

.goal-header svg {
  color: #3b82f6;
}

.goal-header h2 {
  color: #1e293b;
  font-size: 24px;
  font-weight: 600;
  margin: 0;
}

.goal-details {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 24px;
  margin-bottom: 24px;
}

.goal-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.goal-item .label {
  color: #64748b;
  font-size: 14px;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.goal-item .value {
  color: #1e293b;
  font-size: 20px;
  font-weight: 700;
}

.achievement-rate {
  color: #10b981;
}

.progress-bar {
  width: 100%;
  height: 12px;
  background: #e2e8f0;
  border-radius: 6px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(135deg, #10b981, #059669);
  border-radius: 6px;
  transition: width 0.3s ease;
}

.join-section {
  text-align: center;
  padding: 40px;
  background: white;
  border-radius: 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.btn-join {
  background: linear-gradient(135deg, #10b981, #059669);
  color: white;
  border: none;
  padding: 16px 32px;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
}

.btn-join:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(16, 185, 129, 0.4);
}

.btn-join:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
}

.saving-section,
.participants-section,
.log-section {
  background: white;
  border-radius: 20px;
  padding: 32px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.section-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 2px solid #e2e8f0;
}

.section-header svg {
  color: #3b82f6;
}

.section-header h2 {
  color: #1e293b;
  font-size: 20px;
  font-weight: 600;
  margin: 0;
  flex: 1;
}

.btn-refresh {
  background: #f1f5f9;
  border: 1px solid #e2e8f0;
  padding: 8px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  color: #64748b;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-refresh:hover {
  background: #e2e8f0;
  color: #3b82f6;
  transform: rotate(90deg);
}

.participants-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 16px;
}

.participant-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
  background: #f8fafc;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
  transition: all 0.3s ease;
}

.participant-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.participant-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 18px;
}

.participant-info h3 {
  color: #1e293b;
  font-size: 16px;
  font-weight: 600;
  margin: 0 0 4px 0;
}

.participant-amount {
  color: #10b981;
  font-size: 14px;
  font-weight: 600;
  margin: 0;
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .room-detail {
    padding: 16px;
  }

  .header {
    flex-direction: column;
    gap: 16px;
  }

  .header-content h1 {
    font-size: 24px;
  }

  .goal-section,
  .saving-section,
  .participants-section,
  .log-section {
    padding: 24px;
  }

  .goal-details {
    grid-template-columns: 1fr;
  }

  .participants-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 480px) {
  .header-content h1 {
    font-size: 20px;
  }

  .btn-join {
    padding: 12px 24px;
    font-size: 14px;
  }
}
</style>

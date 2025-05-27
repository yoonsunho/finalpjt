<template>
  <div v-if="room" class="room-detail">
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

      <div class="header-text">
        <h1 class="room-title">{{ room.name }}</h1>
        <p class="room-description">{{ room.description }}</p>
        <p class="room-owner">by {{ room.created_by.nickname }}</p>
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

    <div v-else class="content">
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
          <ul class="goal-list">
            <li class="goal-item">
              <span class="label">목표 금액</span>
              <span class="value highlight">{{ room.goal_amount?.toLocaleString?.() }}원</span>
            </li>
            <li class="goal-item">
              <span class="label">현재 모은 금액</span>
              <span class="value">{{ room.total_saved?.toLocaleString?.() }}원</span>
            </li>
            <li class="goal-item">
              <span class="label">현재 달성률</span>
              <span class="value achievement-rate">{{ room.achievement_rate }}%</span>
            </li>
            <li class="goal-item">
              <span class="label">마감일</span>
              <span class="value">{{ formatDate(room.deadline) }}</span>
            </li>
          </ul>
          <div class="progress-bar">
            <div
              class="progress-fill"
              :style="{ width: `${Math.min(room.achievement_rate, 100)}%` }"
            ></div>
          </div>
        </div>
      </div>

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
        <SavingInput
          :roomId="room.id"
          :socket="socket"
          :achievementRate="room.achievement_rate"
          :totalSaved="room.total_saved"
          :goalAmount="room.goal_amount"
        />
      </div>

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
            :key="participant.user.nickname"
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
        </div>
        <SavingLog :logList="logList" />
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
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
const toastMessage = ref('')
const showToast = ref(false)

const triggerToast = (message) => {
  toastMessage.value = message
  showToast.value = true
  setTimeout(() => {
    showToast.value = false
  }, 5000)
}
const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('ko-KR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  })
}

const checkIfUserJoined = () => {
  if (!room.value?.participants || !accountStore.userInfo?.nickname) return
  const isParticipant = room.value.participants.some(
    (participant) => participant.user.nickname === accountStore.userInfo?.nickname,
  )
  if (isParticipant) joined.value = true
}
const buildLogListFromParticipants = () => {
  const logs = []

  if (!room.value?.participants) return

  for (const participant of room.value.participants) {
    if (!participant.deposits) continue // <- deposits 없으면 패스
    for (const deposit of participant.deposits) {
      logs.push({
        ...deposit,
        nickname: participant.user.nickname,
      })
    }
  }

  logList.value = logs.sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
}

const updateRoomData = async () => {
  try {
    const res = await axios.get(`${API_URL}/savingroom/${route.params.id}/`, {
      headers: { Authorization: `Token ${accountStore.token}` },
    })
    room.value = res.data
    checkIfUserJoined()
    buildLogListFromParticipants()
  } catch (err) {
    console.error('Failed to update room data:', err)
  }
}

const fetchRoomDetail = async () => {
  try {
    loading.value = true
    error.value = ''
    const res = await axios.get(`${API_URL}/savingroom/${route.params.id}/`, {
      headers: { Authorization: `Token ${accountStore.token}` },
    })
    room.value = res.data
    checkIfUserJoined()
    buildLogListFromParticipants()
    if (!joined.value) {
      await tryJoinRoom()
    } else if (!socket.value) {
      setupWebSocket()
    }
  } catch (err) {
    console.error('Failed to fetch room detail:', err)
    if (err.response) {
      if (err.response.status === 401) error.value = '로그인이 필요합니다.'
      else if (err.response.status === 404) error.value = '존재하지 않는 저축방입니다.'
      else if (err.response.status === 500) error.value = '서버에 일시적인 문제가 발생했습니다.'
      else error.value = '저축방 정보를 불러오는데 실패했습니다.'
    } else if (err.request) error.value = '네트워크 연결을 확인해주세요.'
    else error.value = '알 수 없는 오류가 발생했습니다.'
  } finally {
    loading.value = false
  }
}

const tryJoinRoom = async () => {
  try {
    await axios.post(
      `${API_URL}/savingroom/${route.params.id}/join/`,
      {},
      {
        headers: { Authorization: `Token ${accountStore.token}` },
      },
    )
    joined.value = true
    setupWebSocket()
  } catch (err) {
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
        headers: { Authorization: `Token ${accountStore.token}` },
      },
    )
    joined.value = true
    await updateRoomData()
    setupWebSocket()
  } catch (err) {
    let errorMessage = '참가에 실패했습니다.'
    if (err.response?.status === 400) {
      errorMessage = '이미 참가한 방입니다.'
      joined.value = true
      await updateRoomData()
      setupWebSocket()
    } else if (err.response?.status === 401) {
      errorMessage = '로그인이 필요합니다.'
    }
    if (err.response?.status !== 400) alert(errorMessage)
  } finally {
    isJoining.value = false
  }
}

const setupWebSocket = () => {
  if (socket.value || !joined.value) return
  const token = accountStore.token
  const ws = new WebSocket(`ws://localhost:8000/ws/savings/${route.params.id}/?token=${token}`)
  ws.onopen = () => console.log('WebSocket connected')
  ws.onmessage = (e) => {
    const data = JSON.parse(e.data)
    const exists = logList.value.some((log) => log.id === data.id)
    if (!exists) {
      updateRoomData()
    }
  }
  ws.onclose = () => {
    console.log('WebSocket disconnected')
    socket.value = null
  }
  ws.onerror = (error) => console.error('WebSocket error:', error)
  socket.value = ws
}

const goBack = () => router.back()

onMounted(fetchRoomDetail)

onBeforeUnmount(() => {
  if (socket.value) socket.value.close()
  socket.value = null
})
</script>
<style scoped>
.room-detail {
  /* max-width: 720px; */
  width: 100%;
  margin: 0 auto;
  padding: 24px 16px;
  background: #fff;
}
.header {
  display: flex;
  align-items: flex-start; /* center → flex-start */
  flex-direction: column; /* 모바일에서도 자연스럽게 유지되도록 */
  gap: 8px;
  margin-bottom: 24px;
}

.btn-back {
  background: none;
  border: none;
  padding: 8px;
  border-radius: 8px;
  cursor: pointer;
  color: #4b5563;
  flex-shrink: 0;
}
.btn-back:hover {
  background: #f1f5f9;
}

.header-text {
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.header-content h1 {
  font-size: 24px;
  font-weight: 600;
  color: #1f2937;
}
.subtitle,
.owner {
  font-size: 14px;
  color: #6b7280;
}
.room-title {
  font-size: 22px;
  font-weight: 700;
  color: #111827;
}

.room-description {
  font-size: 14px;
  color: #6b7280;
}

.room-owner {
  font-size: 13px;
  color: #9ca3af;
  font-style: italic;
}
.loading,
.error {
  text-align: center;
  padding: 32px;
  background: #f9fafb;
  border-radius: 12px;
  border: 1px solid #e5e7eb;
}
.error-icon {
  font-size: 32px;
  color: #ef4444;
}
.btn-retry {
  background: #ef4444;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 8px;
  margin-top: 16px;
}

.content {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.goal-section,
.saving-section,
.participants-section,
.log-section {
  background: #f9fafb;
  border-radius: 12px;
  padding: 20px;
  border: 1px solid #e5e7eb;
}

.goal-details {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  font-size: 14px;
  color: #374151;
  row-gap: 12px;
  column-gap: 32px; /* 기존 16px보다 넉넉하게 */
}
.goal-card {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.goal-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 18px;
  font-weight: 600;
  color: #1f2937;
}

.goal-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.goal-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid #e5e7eb;
}
.goal-item:last-child {
  border-bottom: none;
}

.goal-item .label {
  color: #6b7280;
  font-size: 14px;
  font-weight: 500;
}
.goal-item .value {
  font-size: 15px;
  font-weight: 600;
  color: #1f2937;
}
.goal-item .value.highlight {
  color: #3b82f6;
}
.goal-item .value.achievement-rate {
  color: #10b981;
}

.achievement-rate {
  color: #10b981;
}

.progress-bar {
  margin-top: 16px;
  height: 8px;
  background: #e5e7eb;
  border-radius: 4px;
  overflow: hidden;
}
.progress-fill {
  height: 100%;
  background: #10b981;
  transition: width 0.3s ease;
}

.btn-join {
  background: #3b82f6;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  font-weight: 600;
  font-size: 14px;
  transition: background 0.2s ease;
}
.btn-join:disabled {
  background: #9ca3af;
}
.btn-join:hover:not(:disabled) {
  background: #2563eb; /* 살짝 어두운 파랑으로 반응 */
}
.section-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 16px;
  color: #1f2937;
}

.participants-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 12px;
}

.participant-card {
  display: flex;
  align-items: center;
  padding: 12px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  min-height: 60px; /* 일정 높이 확보 */
  justify-content: flex-start; /* center → flex-start */
  gap: 12px; /* 간격 살짝 더 넓게 */
  background: white;
}

.participant-avatar {
  width: 40px;
  height: 40px;
  border-radius: 20px;
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: 600;
  flex-shrink: 0;
}

.participant-info h3 {
  font-size: 14px;
  font-weight: 600;
  color: #1f2937;
  margin: 0;
}
.participant-amount {
  font-size: 13px;
  color: #10b981;
  font-weight: 500;
}

@media (max-width: 768px) {
  .goal-details {
    grid-template-columns: 1fr;
  }
  .participants-grid {
    grid-template-columns: 1fr 1fr;
  }
  .header {
    flex-direction: column;
  }
  .header-content h1 {
    font-size: 20px;
  }
  .btn-join {
    width: 100%;
  }
}
</style>

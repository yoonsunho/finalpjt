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
      <div class="header-content">
        <h1>{{ room.name }}</h1>
        <p class="subtitle">{{ room.description }}</p>
        <p class="owner">{{ room.created_by.nickname }}</p>
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
          <div class="goal-details">
            <div class="goal-item">
              <span class="label">목표 금액</span>
              <span class="value">{{ room.goal_amount?.toLocaleString?.() }}원</span>
            </div>
            <div class="goal-item">
              <span class="label">현재 모은 금액</span>
              <span class="value">{{ room.total_saved?.toLocaleString?.() }}원</span>
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
const checkIfUserJoined = async () => {
  console.log('=== checkIfUserJoined 시작 ===')

  if (!accountStore.userInfo) {
    console.log('사용자 정보가 없어서 가져오는 중...')
    try {
      await accountStore.fetchUserInfo()
    } catch (err) {
      console.error('사용자 정보를 가져올 수 없습니다:', err)
      joined.value = false
      return
    }
  }

  const myNickname = accountStore.userInfo?.nickname
  if (!room.value?.participants || !myNickname) {
    console.warn('참가자 목록이 없거나 닉네임 없음')
    joined.value = false
    return
  }

  const isUserParticipant = room.value.participants.some((participant, index) => {
    const participantNickname = participant.user?.nickname
    console.log(`비교 ${index}:`, participantNickname, 'vs', myNickname)
    return participantNickname === myNickname
  })

  joined.value = isUserParticipant
  console.log('✅ 최종 joined.value 결과:', joined.value)

  if (joined.value && !socket.value) {
    console.log('WebSocket 설정 시작...')
    setupWebSocket()
  }

  console.log('=== checkIfUserJoined 종료 ===')
}

const buildLogListFromParticipants = () => {
  const logs = []

  if (!room.value?.participants) return

  for (const participant of room.value.participants) {
    if (!participant.deposits) continue
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
    buildLogListFromParticipants()
    await checkIfUserJoined()
  } catch (err) {
    console.error('Failed to update room data:', err)
  }
}
const fetchRoomDetail = async () => {
  try {
    loading.value = true
    error.value = ''

    // ✅ 유저 정보 먼저 불러오기
    await accountStore.fetchUserInfo()

    const res = await axios.get(`${API_URL}/savingroom/${route.params.id}/`, {
      headers: { Authorization: `Token ${accountStore.token}` },
    })

    room.value = res.data
    buildLogListFromParticipants()

    // ✅ 이제 참가 여부 확인
    await checkIfUserJoined()
    console.log('현재 유저 ID:', accountStore.userInfo?.id)
    console.log('최종 joined 상태:', joined.value)
  } catch (err) {
    error.value = '방 정보를 불러오지 못했어요!'
    console.error(err)
  } finally {
    loading.value = false
  }
}

// WebSocket 연결 상태를 확인하는 함수 추가
const checkWebSocketConnection = () => {
  if (socket.value && socket.value.readyState === WebSocket.OPEN) {
    return true
  }
  return false
}

// 개선된 setupWebSocket 함수
const setupWebSocket = () => {
  // 이미 연결되어 있거나 참가하지 않은 경우 건너뛰기
  if ((socket.value && socket.value.readyState === WebSocket.OPEN) || !joined.value) {
    console.log('WebSocket 설정 건너뛰기:', {
      hasActiveSocket: checkWebSocketConnection(),
      joined: joined.value,
    })
    return
  }

  // 기존 연결이 있으면 정리
  if (socket.value) {
    socket.value.close()
    socket.value = null
  }

  const token = accountStore.token
  const ws = new WebSocket(`ws://localhost:8000/ws/savings/${route.params.id}/?token=${token}`)

  ws.onopen = () => {
    console.log('WebSocket connected successfully')
  }

  ws.onmessage = (e) => {
    const data = JSON.parse(e.data)
    console.log('WebSocket message received:', data)

    // 중복 방지를 위해 기존 로그와 비교
    const exists = logList.value.some((log) => log.id === data.id)
    if (!exists) {
      updateRoomData()
    }
  }

  ws.onclose = (e) => {
    console.log('WebSocket disconnected', e.code, e.reason)
    socket.value = null

    // 연결이 예기치 않게 끊어진 경우 재연결 시도
    if (joined.value && e.code !== 1000) {
      setTimeout(() => {
        console.log('WebSocket 재연결 시도...')
        setupWebSocket()
      }, 3000)
    }
  }

  ws.onerror = (error) => {
    console.error('WebSocket error:', error)
  }

  socket.value = ws
}

// 개선된 joinRoom 함수
const joinRoom = async () => {
  console.log('joinRoom() 호출됨')
  console.log('joined.value:', joined.value)
  console.log('isJoining.value:', isJoining.value)

  if (isJoining.value || joined.value) {
    console.log('joinRoom() 실행 안 함 - 이미 참가중이거나 처리중')
    return
  }

  try {
    isJoining.value = true

    const res = await axios.post(
      `${API_URL}/savingroom/${room.value.id}/join/`,
      {},
      {
        headers: { Authorization: `Token ${accountStore.token}` },
      },
    )

    console.log('참가 성공!', res.data)

    // 참가 성공 후 즉시 상태 업데이트
    joined.value = true

    // 방 데이터 새로고침
    await updateRoomData()

    // WebSocket 연결 설정
    setupWebSocket()

    triggerToast('저축방에 참가했습니다!')
  } catch (err) {
    console.log('joinRoom error:', err.response?.data)

    // 이미 참가한 방인 경우 처리
    if (
      err.response?.status === 400 &&
      (err.response?.data?.detail === '이미 참가한 방입니다.' ||
        err.response?.data?.error === '이미 참가한 방입니다.')
    ) {
      console.log('이미 참가한 방 - joined를 true로 설정')
      joined.value = true
      await updateRoomData()
      setupWebSocket()
      triggerToast('이미 참가한 방입니다.')
    } else {
      triggerToast('참가에 실패했습니다. 다시 시도해주세요.')
    }
  } finally {
    isJoining.value = false
  }
}

const goBack = () => router.back()

onMounted(() => {
  fetchRoomDetail()
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

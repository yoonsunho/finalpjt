<template>
  <div class="saving-log">
    <div v-if="!logList || logList.length === 0" class="empty-state">
      <div class="empty-icon">💰</div>
      <h3>아직 입금 내역이 없어요</h3>
      <p>첫 번째 입금을 시작해보세요!</p>
    </div>

    <div v-else class="log-list">
      <div v-for="log in logList" :key="log.id" class="log-item">
        <div class="log-avatar">
          {{ (log.nickname || '?').charAt(0).toUpperCase() }}
        </div>

        <div class="log-content">
          <div class="log-header">
            <span class="log-name">{{ log.nickname }}</span>
            <span class="log-amount">+{{ (log.amount || 0).toLocaleString() }}원</span>
          </div>

          <div class="log-details">
            <span v-if="log.memo" class="log-memo">{{ log.memo }}</span>
            <span v-else class="log-memo placeholder">메모 없음</span>
            <span class="log-time">{{ formatTime(log.created_at) }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  logList: {
    type: Array,
    default: () => [],
  },
})

const formatTime = (dateString) => {
  if (!dateString) return ''

  const date = new Date(dateString)
  const now = new Date()
  const diff = now - date

  // 1분 미만
  if (diff < 60000) {
    return '방금 전'
  }

  // 1시간 미만
  if (diff < 3600000) {
    const minutes = Math.floor(diff / 60000)
    return `${minutes}분 전`
  }

  // 1일 미만
  if (diff < 86400000) {
    const hours = Math.floor(diff / 3600000)
    return `${hours}시간 전`
  }

  // 그 외는 날짜 표시
  return date.toLocaleDateString('ko-KR', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}
</script>

<style scoped>
.saving-log {
  max-height: 400px;
  overflow-y: auto;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: #6b7684;
}

.empty-icon {
  font-size: 48px;
  margin-bottom: 16px;
  opacity: 0.6;
}

.empty-state h3 {
  font-size: 18px;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 8px 0;
}

.empty-state p {
  font-size: 14px;
  color: #6b7684;
  margin: 0;
}

.log-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.log-item {
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

.log-item:hover {
  background: #f1f5f9;
}

.log-avatar {
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

.log-content {
  flex: 1;
  min-width: 0;
}

.log-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 4px;
}

.log-name {
  font-size: 15px;
  font-weight: 600;
  color: #1f2937;
}

.log-amount {
  font-size: 15px;
  font-weight: 700;
  color: #22c55e;
}

.log-details {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 8px;
}

.log-memo {
  font-size: 13px;
  color: #475569;
  flex: 1;
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.log-memo.placeholder {
  font-style: italic;
  opacity: 0.6;
}

.log-time {
  font-size: 12px;
  color: #94a3b8;
  font-weight: 500;
  white-space: nowrap;
}

.saving-log::-webkit-scrollbar {
  width: 4px;
}

.saving-log::-webkit-scrollbar-track {
  background: transparent;
}

.saving-log::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 2px;
}

.saving-log::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}

@media (max-width: 480px) {
  .log-item {
    padding: 12px;
  }

  .log-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 4px;
  }

  .log-details {
    flex-direction: column;
    align-items: flex-start;
    gap: 4px;
  }

  .log-memo {
    white-space: normal;
    line-height: 1.4;
  }
}
</style>

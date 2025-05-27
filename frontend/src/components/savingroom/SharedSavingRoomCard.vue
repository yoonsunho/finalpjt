<template>
  <div class="room-card">
    <h3>{{ room.name }}</h3>
    <p>
      목표: <strong>{{ room.goal_amount.toLocaleString() }}원</strong>
    </p>
    <p>달성률: {{ room.achievement_rate }}%</p>
    <p class="creator">방장: {{ room.created_by.nickname }}</p>
  </div>
</template>

<script setup>
defineProps({
  room: {
    type: Object,
    default: () => ({}),
  },
})
</script>

<style scoped>
.room-card {
  padding: 24px;
  border-radius: 20px;
  background-color: #ffffff;
  border: 1px solid #e2e8f0;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  transition: all 0.2s ease;
  cursor: pointer;
}

.room-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.06);
  background-color: #f8fafc;
}

.room-card h3 {
  font-size: 20px;
  font-weight: 700;
  color: #212529;
  margin-bottom: 16px;
}

.room-card p {
  font-size: 15px;
  color: #495057;
  margin: 6px 0;
  line-height: 1.5;
}

.room-card p strong {
  font-weight: 600;
  color: #4e4e4e;
}

.creator {
  margin-top: 20px;
  font-size: 14px;
  color: #868e96;
}
</style>

<template>
  <div class="room-card">
    <h3>{{ room.name }}</h3>
    <p>목표: {{ room.goal_amount.toLocaleString() }}원</p>
    <p>달성률: {{ room.achievement_rate }}%</p>
    <p class="creator">
      <!-- 방장: <strong>{{ room.created_by?.nickname }}</strong> -->
    </p>
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
  border: 1px solid #ddd;
  padding: 1rem;
  border-radius: 10px;
  cursor: pointer;
  transition: 0.2s;
  background: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.room-card:hover {
  background-color: #f9f9f9;
  transform: scale(1.01);
}

.creator {
  margin-top: 0.5rem;
  color: #64748b;
  font-size: 14px;
}
</style>

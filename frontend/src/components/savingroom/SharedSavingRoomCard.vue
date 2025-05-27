<template>
  <div class="room-card">
    <h3>{{ room.name }}</h3>
    <p>목표: {{ room.goal_amount.toLocaleString() }}원</p>
    <p>달성률: {{ room.achievement_rate }}%</p>
    <p class="creator">
      방장: <strong>{{ room.created_by }}</strong>
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
  padding: 24px;
  border-radius: 16px;
  background: white;
  border: 1px solid #e2e8f0;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
  transition: all 0.3s ease;
}

.room-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
  background-color: #f9fafb;
}

.room-card h3 {
  font-size: 18px;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 12px;
}

.room-card p {
  font-size: 14px;
  color: #475569;
  margin: 4px 0;
  line-height: 1.4;
}

.creator {
  margin-top: 12px;
  font-size: 13px;
  color: #64748b;
}
</style>

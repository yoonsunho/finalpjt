<template>
  <div class="room-card" @click="$emit('click')">
    <h3>{{ room.name }}</h3>
    <p>목표: {{ room.goal_amount.toLocaleString() }}원</p>
    <p>달성률: {{ room.achievement_rate }}%</p>
  </div>
</template>

<script setup>
defineProps({ room: Object })
</script>

<style scoped>
.room-card {
  border: 1px solid #ddd;
  padding: 1rem;
  border-radius: 10px;
  cursor: pointer;
  transition: 0.2s;
}
.room-card:hover {
  background-color: #f9f9f9;
  transform: scale(1.01);
}
</style>

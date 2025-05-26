<template>
  <div class="spot-page">
    <div class="controls">
      <button @click="asset = 'gold'">금</button>
      <button @click="asset = 'silver'">은</button>

      <input type="date" v-model="startDate" />
      <input type="date" v-model="endDate" />
      <button @click="getSpotData">조회</button>
    </div>

    <div class="chart-container">
      <LineChart :chart-data="chartData" v-if="chartData" />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import SpotChart from '@/components/SpotChart.vue'

const asset = ref('gold')
const startDate = ref('')
const endDate = ref('')
const chartData = ref(null)
const getSpotData = ''
</script>
<style scoped>
.spot-page {
  padding: 20px;
  font-family: 'Pretendard', sans-serif;
  max-width: 800px;
  margin: 0 auto;
}

.controls {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  align-items: center;
  margin-bottom: 20px;
}

.controls button {
  padding: 8px 16px;
  border: 1px solid #ddd;
  background-color: #f9f9f9;
  border-radius: 6px;
  cursor: pointer;
  font-weight: bold;
  transition: background-color 0.2s ease;
}

.controls button:hover {
  background-color: #eee;
}

.controls button.active {
  background-color: #333;
  color: #fff;
}

.controls input[type='date'] {
  padding: 6px 12px;
  border: 1px solid #ccc;
  border-radius: 6px;
}

.chart-container {
  background: #fff;
  padding: 20px;
  border: 1px solid #eee;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}
</style>

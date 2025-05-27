<template>
  <div>
    <div class="header-content">
      <h1 class="title">현물 시세 비교</h1>
      <p class="subtext">기간에 따른 현물 자산의 시세 변화를 확인해요.</p>
      <br /><br />
      <hr />
    </div>
  </div>
  <div class="spot-page">
    <div class="controls">
      <button :class="{ active: asset === 'gold' }" @click="selectAsset('gold')">금</button>
      <button :class="{ active: asset === 'silver' }" @click="selectAsset('silver')">은</button>
      <input type="date" v-model="startDate" placeholder="시작일" />
      <input type="date" v-model="endDate" placeholder="종료일" />
      <button @click="getSpotData" :disabled="!startDate || !endDate">조회</button>
    </div>

    <!-- 에러 메시지 -->
    <div v-if="errorMessage" class="error">
      {{ errorMessage }}
    </div>

    <!-- 차트 영역 -->
    <div class="chart-container">
      <SpotChart v-if="chartData && chartData.length" :chart-data="chartData" :asset="asset" />
      <div v-else class="no-data">데이터가 없습니다.</div>
    </div>
  </div>
</template>
<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import SpotChart from '@/components/SpotChart.vue'

const asset = ref('gold') // 선택된 자산 (gold or silver)
const startDate = ref('') // 시작일
const endDate = ref('') // 종료일
const chartData = ref([]) // 차트에 사용할 데이터 배열
const errorMessage = ref('') // 에러 메시지

// 자산 선택 함수
const selectAsset = (selectedAsset) => {
  asset.value = selectedAsset
  getSpotData()
}

// API 호출하여 데이터 가져오기
const getSpotData = async () => {
  errorMessage.value = ''
  try {
    const params = {
      asset: asset.value,
      ...(startDate.value && { start_date: startDate.value }),
      ...(endDate.value && { end_date: endDate.value }),
    }

    const response = await axios.get('http://127.0.0.1:8000/spot/commodity_price/', { params })

    if (response.data.data && response.data.data.length > 0) {
      // API에서 받은 데이터를 차트용으로 가공
      chartData.value = response.data.data.map((item) => ({
        date: item.date,
        price: parseFloat(item.close_last),
      }))
    } else {
      chartData.value = []
      errorMessage.value = '선택한 기간에 데이터가 없습니다.'
    }
  } catch (error) {
    errorMessage.value = '데이터를 불러오는데 실패했습니다.'
    console.error(error)
  }
}

// 컴포넌트 마운트 시 초기 데이터 로드
onMounted(() => {
  getSpotData()
})
</script>
<style scoped>
.spot-page {
  padding: 24px;
  font-family: 'Pretendard', sans-serif;
  /* max-width: 800px; */
  width: 100%;
  margin: 0 auto;
}

.header {
  text-align: center;
  margin-top: 10px;
  /* margin-bottom: 10px; */
  /* padding-bottom: 50px; */
}

hr {
  color: #eeeeee;
  font-weight: bold;
}
.header-content h1 {
  text-align: center;
  font-size: 2.5rem;
  font-weight: 700;
  /* margin-bottom: 8px; */
}

.subtext {
  text-align: center;
  font-size: 1.1rem;
  color: black;
  /* margin-bottom: 30px; */
}

.controls {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 24px;
  align-items: center;
}

.controls button {
  padding: 10px 16px;
  font-size: 14px;
  font-weight: 600;
  border-radius: 8px;
  border: 1px solid #d1d5db;
  background-color: #f9fafb;
  color: #374151;
  transition:
    background-color 0.2s ease,
    color 0.2s ease;
  cursor: pointer;
}

.controls button:hover {
  background-color: #f3f4f6;
}

.controls button.active {
  background-color: #2563eb;
  color: white;
  border-color: #2563eb;
}

.controls button:disabled {
  background-color: #e5e7eb;
  color: #9ca3af;
  cursor: not-allowed;
}

.controls input[type='date'] {
  padding: 8px 12px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 14px;
  color: #374151;
  background-color: white;
}

.error {
  color: #ef4444;
  font-size: 14px;
  margin-bottom: 16px;
}

.chart-container {
  background: #ffffff;
  padding: 24px;
  border-radius: 16px;
  border: 1px solid #e5e7eb;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
}

.no-data {
  font-size: 14px;
  color: #6b7280;
  text-align: center;
  padding: 40px 0;
}
</style>

<template>
  <div class="spot-page">
    <div class="controls">
      <!-- 자산 선택 버튼 -->
      <button 
        :class="{ active: asset === 'gold' }" 
        @click="selectAsset('gold')"
      >
        금
      </button>
      <button 
        :class="{ active: asset === 'silver' }" 
        @click="selectAsset('silver')"
      >
        은
      </button>

      <!-- 날짜 선택 -->
      <input 
        type="date" 
        v-model="startDate" 
        placeholder="시작일"
      />
      <input 
        type="date" 
        v-model="endDate" 
        placeholder="종료일"
      />
      <button @click="getSpotData">조회</button>
    </div>

    <!-- 에러 메시지 -->
    <div v-if="errorMessage" class="error">
      {{ errorMessage }}
    </div>

    <!-- 차트 영역 -->
    <div class="chart-container">
      <SpotChart 
        v-if="chartData && chartData.length" 
        :chart-data="chartData" 
        :asset="asset" 
      />
      <div v-else class="no-data">데이터가 없습니다.</div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import SpotChart from '@/components/SpotChart.vue'

const asset = ref('gold')       // 선택된 자산 (gold or silver)
const startDate = ref('')       // 시작일
const endDate = ref('')         // 종료일
const chartData = ref([])       // 차트에 사용할 데이터 배열
const errorMessage = ref('')    // 에러 메시지

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

    // 백엔드 API 주소에 맞게 수정하세요
    const response = await axios.get('http://127.0.0.1:8000/spot/commodity_price/', { params })

    if (response.data.data && response.data.data.length > 0) {
      // API에서 받은 데이터를 차트용으로 가공
      chartData.value = response.data.data.map(item => ({
        date: item.date,
        price: parseFloat(item.close_last)
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

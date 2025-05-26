<template>
  <div>
    <canvas ref="canvasRef"></canvas>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import {
  Chart,
  LineController,
  LineElement,
  PointElement,
  LinearScale,
  Title,
  CategoryScale,
  Tooltip,
  Legend,
} from 'chart.js'

Chart.register(
  LineController,
  LineElement,
  PointElement,
  LinearScale,
  Title,
  CategoryScale,
  Tooltip,
  Legend,
)

// props 선언 (chartData: Array, asset: String)
const props = defineProps({
  chartData: {
    type: Array,
    required: true,
  },
  asset: {
    type: String,
    required: true,
  }
})

const canvasRef = ref(null)
let chartInstance = null

// 차트 그리기 함수
const renderChart = () => {
  if (!props.chartData || props.chartData.length === 0) return

  // 기존 차트가 있으면 파괴
  if (chartInstance) {
    chartInstance.destroy()
  }

  const ctx = canvasRef.value.getContext('2d')
  chartInstance = new Chart(ctx, {
    type: 'line',
    data: {
      labels: props.chartData.map(d => d.date),
      datasets: [{
        label: props.asset === 'gold' ? '금 가격' : '은 가격',
        data: props.chartData.map(d => d.price),
        borderColor: props.asset === 'gold' ? '#FFD700' : '#C0C0C0',
        backgroundColor: props.asset === 'gold' ? 'rgba(255,215,0,0.1)' : 'rgba(192,192,192,0.1)',
        tension: 0.1,
        pointBackgroundColor: props.asset === 'gold' ? '#FFD700' : '#C0C0C0',
        pointBorderColor: '#fff',
        pointRadius: 3,
      }]
    },
    options: {
      responsive: true,
      plugins: {
        title: {
          display: true,
          text: props.asset === 'gold' ? '금 가격 변동' : '은 가격 변동',
        },
        legend: {
          display: true,
        }
      },
      scales: {
        x: {
          title: {
            display: true,
            text: '날짜',
          }
        },
        y: {
          title: {
            display: true,
            text: '가격(USD)',
          }
        }
      }
    }
  })
}

// chartData나 asset이 바뀔 때마다 차트 다시 그림
watch(
  () => [props.chartData, props.asset],
  () => {
    renderChart()
  },
  { deep: true }
)

onMounted(() => {
  renderChart()
})

</script>

<style scoped>
canvas {
  max-width: 100%;
  height: 400px;
}
</style>

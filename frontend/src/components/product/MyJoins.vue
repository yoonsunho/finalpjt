<template>
  <div class="my-joins">
    <h1>내 가입 목록</h1>
    <!-- 예금 가입 목록 -->
    <div class="section" v-if="depositJoins.length > 0">
      <h2>예금 상품</h2>
      <div class="products-list">
        <div v-for="item in depositJoins" :key="item.id" class="product-item">
          <div class="product-info">
            <h3>{{ item.product.fin_prdt_nm }}</h3>
            <p>{{ item.product.kor_co_nm }}</p>
            <small>가입일: {{ formatDate(item.joined_at) }}</small>
          </div>
          <button @click="cancelJoin('deposit', item.product.id)" class="btn-cancel">
            가입 취소
          </button>
        </div>
      </div>

      <!-- 적금 가입 목록 -->
      <div class="section" v-if="savingJoins.length > 0">
        <h2>적금 상품</h2>
        <div class="products-list">
          <div v-for="item in savingJoins" :key="item.id" class="product-item">
            <div class="product-info">
              <h3>{{ item.product.fin_prdt_nm }}</h3>
              <p>{{ item.product.kor_co_nm }}</p>
              <small>가입일: {{ formatDate(item.joined_at) }}</small>
            </div>
            <button @click="cancelJoin('saving', item.product.id)" class="btn-cancel">
              가입 취소
            </button>
          </div>
        </div>
      </div>

      <!-- 가입한 상품이 없을 때 -->
      <div v-if="depositJoins.length === 0 && savingJoins.length === 0" class="no-data">
        <p>가입한 상품이 없습니다.</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useAccountStore } from '@/stores/user'

const accountStore = useAccountStore()
const API_URL = 'http://127.0.0.1:8000'

const isLoading = ref(true)
const depositJoins = ref([])
const savingJoins = ref([])

// 가입한 상품 목록 가져오기
const getMyJoins = async () => {
  try {
    const response = await axios.get(`${API_URL}/finlife/my-joins/`, {
      headers: {
        Authorization: `Token ${accountStore.token}`,
      },
    })
    
    depositJoins.value = response.data.deposits || []
    savingJoins.value = response.data.savings || []
  } catch (error) {
    console.error('가입 목록 조회 실패:', error)
  } finally {
    isLoading.value = false
  }
}

// 가입 취소
const cancelJoin = async (type, productId) => {
  if (!confirm('정말 가입을 취소하시겠습니까?')) {
    return
  }

  try {
    const url =
      type === 'deposit'
        ? `${API_URL}/finlife/deposit/${productId}/join/`
        : `${API_URL}/finlife/saving/${productId}/join/`

    await axios.post(
      url,
      {},
      {
        headers: {
          Authorization: `Token ${accountStore.token}`,
        },
      },
    )

    // 목록에서 제거
    if (type === 'deposit') {
      depositJoins.value = depositJoins.value.filter((item) => item.product.id !== productId)
    } else {
      savingJoins.value = savingJoins.value.filter((item) => item.product.id !== productId)
    }
  } catch (error) {
    console.error('가입 취소 실패:', error)
    alert('가입 취소에 실패했습니다.')
  }
}

// 날짜 포맷팅
const formatDate = (dateString) => {
  if (!dateString) return '정보 없음'

  const date = new Date(dateString)
  return date.toLocaleDateString('ko-KR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  })
}

onMounted(() => {
  getMyJoins()
})
</script>

<style scoped>
.my-joins {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

h1 {
  font-size: 2rem;
  margin-bottom: 30px;
  text-align: center;
}

.loading {
  text-align: center;
  padding: 50px;
  font-size: 1.1rem;
  color: #191f28;
}

.section {
  margin-bottom: 40px;
}

.section h2 {
  font-size: 1.5rem;
  margin-bottom: 20px;
  color: #2c3e50;
  border-bottom: 2px solid #27ae60;
  padding-bottom: 10px;
}

.products-list {
  display: grid;
  gap: 15px;
}

.product-item {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 20px;
  background: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.product-info h3 {
  font-size: 1.2rem;
  margin-bottom: 5px;
  color: #2c3e50;
}

.product-info p {
  color: #191f28;
  margin: 5px 0;
}

.product-info small {
  color: #191f28;
  font-size: 0.85rem;
}

.btn-cancel {
  background-color: #f39c12;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-cancel:hover {
  background-color: #e67e22;
}

.no-data {
  text-align: center;
  padding: 50px;
  color: #191f28;
}

.no-data p {
  font-size: 1.1rem;
}
</style>

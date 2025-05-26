<template>
  <div class="my-interests">
    <h1>찜한 상품</h1>

    <!-- 예금 섹션 -->
    <div class="section" v-if="depositInterests.length > 0">
      <h2>예금 상품</h2>
      <div class="products-list">
        <div v-for="item in depositInterests" :key="item.id" class="product-item">
          <h3>{{ item.product_name }}</h3>
          <p>{{ item.company_name }}</p>
          <small>가입일: {{ formatDate(item.joined_at) }}</small>
          <button @click="removeLike('deposit', item.product)" class="btn-remove">찜 해제</button>
        </div>
      </div>
    </div>

    <!-- 적금 섹션 -->
    <div class="section" v-if="savingInterests.length > 0">
      <h2>적금 상품</h2>
      <div class="products-list">
        <div v-for="item in savingInterests" :key="item.id" class="product-item">
          <h3>{{ item.product_name }}</h3>
          <p>{{ item.company_name }}</p>
          <small>가입일: {{ formatDate(item.joined_at) }}</small>
          <button @click="removeLike('saving', item.product)" class="btn-remove">찜 해제</button>
        </div>
      </div>
    </div>

    <!-- 아무것도 없을 때 -->
    <div v-if="depositInterests.length === 0 && savingInterests.length === 0" class="no-data">
      <p>찜한 상품이 없습니다.</p>
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
const depositInterests = ref([])
const savingInterests = ref([])

// 찜한 상품 목록 가져오기
const getMyInterests = async () => {
  try {
    const response = await axios.get(`${API_URL}/finlife/my-interests/`, {
      headers: {
        Authorization: `Token ${accountStore.token}`,
      },
    })

    depositInterests.value = response.data.deposits || []
    savingInterests.value = response.data.savings || []
  } catch (error) {
    console.error('찜 목록 조회 실패:', error)
  } finally {
    isLoading.value = false
  }
}

// 찜 해제
const removeLike = async (type, productId) => {
  try {
    const url =
      type === 'deposit'
        ? `${API_URL}/finlife/deposit/${productId}/interest/`
        : `${API_URL}/finlife/saving/${productId}/interest/`

    await axios.post(
      url,
      {},
      {
        headers: {
          Authorization: `Token ${accountStore.token}`,
        },
      },
    )
    if (type === 'deposit') {
      depositInterests.value = depositInterests.value.filter(
        (item) => item.product.id !== productId,
      )
    } else {
      savingInterests.value = savingInterests.value.filter((item) => item.product.id !== productId)
    }
  } catch (error) {
    console.error('찜 해제 실패:', error)
    alert('찜 해제에 실패했습니다.')
  }
}

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
  getMyInterests()
})
</script>

<style scoped>
.my-joins,
.my-interests {
  max-width: 720px;
  margin: 0 auto;
  padding: 32px 20px;
  background-color: #f8f9fa;
  font-family: 'Pretendard', sans-serif;
}

h1 {
  font-size: 1.8rem;
  font-weight: 600;
  color: #212529;
  text-align: center;
  margin-bottom: 24px;
}

.section h2 {
  font-size: 1.25rem;
  font-weight: 500;
  border-left: 4px solid #00aaff;
  padding-left: 12px;
  margin-bottom: 16px;
  color: #343a40;
}

.products-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.product-item {
  background-color: #ffffff;
  border-radius: 16px;
  padding: 20px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
  border: 1px solid #dee2e6;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.product-item h3 {
  font-size: 1.1rem;
  margin-bottom: 6px;
  font-weight: 500;
  color: #212529;
}

.product-item p {
  font-size: 0.95rem;
  color: #495057;
  margin-bottom: 4px;
}

.product-item small {
  font-size: 0.85rem;
  color: #868e96;
}

.btn-remove {
  background-color: transparent;
  color: #ff4d4f;
  border: 1px solid #ff4d4f;
  padding: 6px 14px;
  font-size: 0.9rem;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease-in-out;
}

.btn-remove:hover {
  background-color: #ff4d4f;
  color: white;
}

.no-data {
  text-align: center;
  padding: 40px;
  color: #868e96;
  font-size: 1rem;
}
</style>

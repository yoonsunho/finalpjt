<template>
  <div class="my-interests">
    <h1>내 찜 목록</h1>
    <div class="section" v-if="depositInterests.length > 0">
      <h2>예금 상품</h2>
      <div class="products-list">
        <div v-for="item in depositInterests" :key="item.id" class="product-item">
          <h3>{{ item.product.fin_prdt_nm }}</h3>
          <p>{{ item.product.kor_co_nm }}</p>
          <button @click="removeLike('deposit', item.product.id)" class="btn-remove">
            찜 해제
          </button>
        </div>
      </div>

      <!-- 적금 찜 목록 -->
      <div class="section" v-if="savingInterests.length > 0">
        <h2>적금 상품</h2>
        <div class="products-list">
          <div v-for="item in savingInterests" :key="item.id" class="product-item">
            <h3>{{ item.product.fin_prdt_nm }}</h3>
            <p>{{ item.product.kor_co_nm }}</p>
            <button @click="removeLike('saving', item.product.id)" class="btn-remove">
              찜 해제
            </button>
          </div>
        </div>
      </div>

      <!-- 찜한 상품이 없을 때 -->
      <div v-if="depositInterests.length === 0 && savingInterests.length === 0" class="no-data">
        <p>찜한 상품이 없습니다.</p>
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

    // 목록에서 제거
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

onMounted(() => {
  getMyInterests()
})
</script>

<style scoped>
.my-interests {
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
  border-bottom: 2px solid #3498db;
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

.product-item h3 {
  font-size: 1.2rem;
  margin-bottom: 5px;
  color: #2c3e50;
}

.product-item p {
  color: #191f28;
  margin: 0;
}

.btn-remove {
  background-color: #e74c3c;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-remove:hover {
  background-color: #c0392b;
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

<template>
  <div class="recommend-container">
    <h1>고객님께 맞는 금융 상품을<br />추천해 드립니다.</h1>

    <div v-if="recommendations">
      <h2>추천 예금 상품</h2>
      <div v-for="deposit in recommendations.deposits" :key="deposit.id" class="product-card">
        <img :src="getBankImage(deposit.kor_co_nm)" class="bank-logo" alt="bank logo" />
        <div class="product-info">
          <RouterLink
            :to="{ name: 'DepositDetailView', params: { id: deposit.id } }"
            class="product-name"
          >
            <h3>{{ deposit.fin_prdt_nm }}</h3>
          </RouterLink>
          <h3>{{ deposit.kor_co_nm }}</h3>
          <p>최고 우대 금리: {{ deposit.max_intr_rate2 }}%</p>
          <small>추천 이유: {{ deposit.recommend_reason }}</small>
        </div>
      </div>

      <h2>추천 적금 상품</h2>
      <div v-for="saving in recommendations.savings" :key="saving.id" class="product-card">
        <img :src="getBankImage(saving.kor_co_nm)" class="bank-logo" alt="bank logo" />
        <div class="product-info">
          <RouterLink
            :to="{ name: 'SavingDetailView', params: { id: saving.id } }"
            class="product-name"
          >
            <h3>{{ saving.fin_prdt_nm }}</h3>
          </RouterLink>
          <h3>{{ saving.kor_co_nm }}</h3>
          <p>최고 우대 금리: {{ saving.max_intr_rate2 }}%</p>
          <small>추천 이유: {{ saving.recommend_reason }}</small>
        </div>
      </div>
    </div>
    <p v-else-if="error">{{ error }}</p>
    <div v-else class="loading-box">
      <div class="spinner"></div>
      <p>고객님의 정보를 바탕으로<br />맞춤 예적금을 추천해 드릴게요.<br />조금만 기다려주세요!</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAccountStore } from '@/stores/user'
import axios from 'axios'

const accountStore = useAccountStore()
const recommendations = ref(null)
const error = ref(null)

const API_URL = 'http://127.0.0.1:8000'

onMounted(async () => {
  if (!accountStore.isLogin) {
    error.value = '로그인이 필요합니다.'
    console.log('로그인되지 않음')
    return
  }

  try {
    if (!accountStore.userInfo) {
      await accountStore.fetchUserInfo()
    }

    const userEmail = accountStore.userInfo?.email
    const token = accountStore.token
    const startTime = performance.now() // 시작 시간
    console.log('추천 데이터 요청 중...')
    const res = await axios.get(`${API_URL}/recommend/${userEmail}/`, {
      headers: {
        Authorization: `Token ${token}`,
      },
    })

    console.log('추천 데이터 받음:', res.data)
    const endTime = performance.now() // 끝 시간
    const duration = (endTime - startTime).toFixed(2)

    console.log(`추천 데이터 받음:`, res.data)
    console.log(`걸린 시간: ${duration}ms`)
    recommendations.value = res.data
  } catch (err) {
    console.error('추천 불러오기 실패:', err)

    if (err.response?.status === 401) {
      accountStore.token = null
      accountStore.userInfo = null
    } else if (err.response?.status === 404) {
      error.value = '추천 데이터를 찾을 수 없습니다.'
    } else {
      error.value = '추천 데이터를 불러오는데 실패했습니다.'
    }
  }
})
const imageExtensions = ['.svg', '.png', '.jpg']
const getBankImage = (bankName) => {
  const formatted = bankName.replace(/\s/g, '').replace(/\(.+?\)/g, '')

  console.log('찾는 은행명:', formatted)

  for (const ext of imageExtensions) {
    try {
      const imageUrl = new URL(`/src/assets/images/${formatted}${ext}`, import.meta.url).href
      console.log('시도하는 파일:', `${formatted}${ext}`)
      return imageUrl
    } catch (e) {
      console.log('파일 없음:', `${formatted}${ext}`)
      continue
    }
  }

  return '' //fallback
}
</script>
<style scoped>
* {
  font-family: 'Pretendard', sans-serif;
  box-sizing: border-box;
}

.recommend-container {
  max-width: 960px;
  margin: 32px auto;
  padding: 0 16px;
}

h1 {
  font-size: 24px;
  font-weight: 700;
  text-align: center;
  color: #191f28;
  margin-bottom: 32px;
  line-height: 1.5;
}

h2 {
  font-size: 18px;
  font-weight: 600;
  color: #191f28;
  margin: 24px 0 12px;
  border-bottom: 1px solid #f2f4f6;
  padding-bottom: 4px;
}

.product-card {
  display: flex;
  align-items: center;
  background: #ffffff;
  border: 1px solid #f2f4f6;
  border-radius: 16px;
  padding: 16px;
  margin-bottom: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
  transition: box-shadow 0.2s ease;
}

.product-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
}

.bank-logo {
  width: 64px;
  height: 64px;
  object-fit: contain;
  margin-right: 20px;
  flex-shrink: 0;
}

.product-info {
  flex: 1;
}

.product-name h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #191f28;
}

.product-name:hover h3 {
  color: #3182f6;
}

.product-info h3 {
  font-size: 14px;
  font-weight: 500;
  color: #4e5968;
  margin: 4px 0;
}

.product-info p {
  font-size: 14px;
  color: #3182f6;
  font-weight: 500;
  margin: 4px 0;
}

.product-info small {
  font-size: 13px;
  color: #8b95a1;
}

.loading-box {
  display: flex;
  flex-direction: column;
  align-items: center;
  color: #6b7280;
  padding: 40px 0;
  text-align: center;
}

.spinner {
  width: 36px;
  height: 36px;
  margin-bottom: 16px;
  border: 4px solid #f1f3f5;
  border-top: 4px solid #3182f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* 반응형 */
@media (max-width: 640px) {
  .product-card {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }

  .bank-logo {
    margin: 0 0 8px 0;
  }

  h1 {
    font-size: 20px;
  }

  h2 {
    font-size: 16px;
  }

  .product-info p,
  .product-info h3,
  .product-info small {
    font-size: 13px;
  }
}
</style>

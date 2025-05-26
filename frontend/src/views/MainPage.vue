<template>
  <div class="landing-wrapper">
    <section ref="hero" class="section hero">
      <h1 class="hero-title">금융생활을 보다 더 편리하게</h1>
      <p class="hero-subtitle">예적금 비교, 추천받기, 현물 시세 확인, 커뮤니티까지 한 번에</p>
      <button class="cta">지금 시작하기</button>
    </section>

    <!-- 예적금 상품 리스트 -->
    <section ref="products" class="section products">
      <div class="products-text">
        <h2>다양한 금융 상품을 한 눈에 비교해요.</h2>
        <p>예적금 상품을 모아 볼 수 있어요.</p>
      </div>

      <div class="cards-section">
        <div class="cards-row">
          <div class="card" v-for="deposit in topDeposits" :key="'deposit-' + deposit.id">
            <h3>{{ deposit.fin_prdt_nm }}</h3>
            <p>{{ deposit.kor_co_nm }}</p>
            <p>금리: {{ deposit.max_intr_rate2 }}%</p>
          </div>
        </div>

        <div class="cards-row">
          <div class="card" v-for="saving in topSavings" :key="'saving-' + saving.id">
            <h3>{{ saving.fin_prdt_nm }}</h3>
            <p>{{ saving.kor_co_nm }}</p>
            <p>금리: {{ saving.max_intr_rate2 }}%</p>
          </div>
        </div>
      </div>
    </section>

    <!-- 맞춤 추천 -->
    <section ref="recommend" class="section recommend">
      <RouterLink :to="{ name: 'RecommendView' }">
        <button class="cta">추천받기</button>
      </RouterLink>
      <h2>나에게 맞는 예적금을 추천 받아요.</h2>
      <p>몇 가지 질문에만 답하면 끝!</p>
    </section>

    <!-- 커뮤니티 -->
    <section ref="community" class="section community">
      <h2>혼자보다 함께 더 똑똑한 금융 생활!</h2>
      <div class="community-container">
        <div class="community-card">
          <div class="community-title">안녕하세요</div>
          <div class="community-tags">
            <span class="community-tag">#자유게시판</span>
          </div>
          <div class="community-extra">뚱인데요</div>
        </div>
        <div class="community-card">
          <div class="community-title">등촌칼국수를 드셔 보신 적이 있으신가요?</div>
          <div class="community-tags">
            <span class="community-tag">#절약 꿀팁</span>
          </div>
          <div class="community-extra">와 진짜 너무 맛있던데요??</div>
        </div>
        <div class="community-card">
          <div class="community-title">뼈찜이 먹고싶은 하루네요..</div>
          <div class="community-tags">
            <span class="community-tag">#적금 후기</span>
          </div>
          <div class="community-extra">
            뼈찜이 너무 인기가 많아서 아쉽습니다<br />
            언제쯤 먹어볼 수 있을까요?
          </div>
        </div>
      </div>
    </section>

    <!-- 금/은 시세 -->
    <section ref="market" class="section market">
      <h2>실시간 금/은 시세 비교</h2>
      <div class="graph">📈 실시간 그래프 자리</div>
    </section>

    <!-- 지도 -->
    <section ref="map" class="section map">
      <h2>지금 나와 가까운 은행을 검색해요.</h2>
      <div class="map-container">지도 컴포넌트</div>
    </section>

    <!-- CTA -->
    <section class="section final-cta">
      <h2>지금, 당신의 금융생활을 바꿔보세요</h2>
      <div class="cta-buttons">
        <button>회원가입 하러가기</button>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import gsap from 'gsap'
import ScrollTrigger from 'gsap/ScrollTrigger'
import { RouterLink } from 'vue-router'

gsap.registerPlugin(ScrollTrigger)

const hero = ref(null)
const products = ref(null)
const recommend = ref(null)
const community = ref(null)
const market = ref(null)
const map = ref(null)
const API_URL = 'http://127.0.0.1:8000'
const topDeposits = ref([])
const topSavings = ref([])

onMounted(async () => {
  // 1. 인기 예금/적금 불러오기
  try {
    const [depositRes, savingRes] = await Promise.all([
      axios.get(`${API_URL}/finlife/deposit/`, { params: { ordering: '-joined_count' } }),
      axios.get(`${API_URL}/finlife/saving/`, { params: { ordering: '-joined_count' } }),
    ])

    topDeposits.value = depositRes.data.slice(0, 3)
    topSavings.value = savingRes.data.slice(0, 3)
  } catch (err) {
    console.error('인기 상품 불러오기 실패:', err)
  }

  // 2. gsap
  const sections = [products, recommend, community, market, map]

  sections.forEach((sectionRef, i) => {
    gsap.fromTo(
      sectionRef.value,
      { opacity: 0, y: 100, scale: 0.95 },
      {
        scrollTrigger: {
          trigger: sectionRef.value,
          start: 'top 80%',
          toggleActions: 'play none none none',
        },
        opacity: 1,
        y: 0,
        scale: 1,
        duration: 0.8,
        ease: 'power3.out',
        delay: i * 0.15,
      },
    )
  })
})
</script>

<style scoped>
html,
body {
  scroll-behavior: smooth;
  margin: 0;
  padding: 0;
  font-family: 'Pretendard', sans-serif;
  background: #f9fafb;
}

.section {
  min-height: 100vh;
  padding: 6rem 2rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  scroll-snap-align: start;
}

.hero {
  background: linear-gradient(to bottom, #e0f2fe, #ffffff);
  background-attachment: fixed;
  text-align: center;
}
.hero-title {
  font-weight: 600;
  font-size: 4rem;
  color: #191f28;
}
.hero-subtitle {
  font-size: 2rem;
  color: #4e5968;
}

.products {
  display: flex;
  flex-direction: row;
  background: #fef3c7;
}
.products-text {
  flex-direction: column;
}
.recommend {
  display: flex;
  flex-direction: row;
  background: #bae6fd;
}
.community {
  background: #d1fae5;
}
.market {
  background: #f3e8ff;
}
.map {
  background: #fff7ed;
}

.final-cta {
  background-color: #2563eb;
  color: white;
  text-align: center;
}

.cards.products {
  display: flex;
  flex-wrap: wrap;
  gap: 2rem;
  justify-content: center;
  margin-top: 2rem;
}
.card,
.graph,
.map-container {
  background-color: #e5e7eb;
  padding: 2rem;
  border-radius: 0.75rem;
  width: 100%;
  max-width: 420px;
  text-align: center;
  transition: transform 0.3s ease;
}

.cta,
.cta-buttons button {
  margin-top: 2rem;
  padding: 0.8rem 1.8rem;
  background-color: #2563eb;
  color: white;
  border: none;
  border-radius: 0.5rem;
  font-weight: bold;
  cursor: pointer;
  transition: background 0.2s ease;
}
.cta:hover,
.cta-buttons button:hover {
  background-color: #1e40af;
}

.cta-buttons {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  justify-content: center;
  margin-top: 1.5rem;
}

.tags {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
  flex-wrap: wrap;
}
.tags span {
  background: white;
  padding: 0.4rem 1rem;
  border-radius: 9999px;
  font-size: 0.9rem;
  font-weight: 500;
  color: #2563eb;
}

.community-container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  flex-wrap: wrap;
  justify-content: flex-start;
}

.community-card {
  width: 280px;
  border-radius: 20px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.06);
  background-color: #ffffff;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  padding: 1.2rem;
  font-family: 'Pretendard', 'Apple SD Gothic Neo', sans-serif;
}

.community-title {
  font-size: 1rem;
  font-weight: 600;
  color: #111827;
  line-height: 1.4;
  margin-bottom: 0.8rem;
}

.community-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.3rem;
  font-size: 0.75rem;
  color: #9ca3af;
  margin-bottom: 1rem;
}

.community-tag {
  background-color: #f3f4f6;
  padding: 0.2rem 0.6rem;
  border-radius: 9999px;
}

.community-extra {
  font-size: 0.85rem;
  line-height: 1.4;
  color: #374151;
  background-color: #f9fafb;
  padding: 0.8rem;
  border-radius: 12px;
  margin-top: auto;
}

.cards-section {
  display: flex;
  flex-direction: column;
  gap: 2rem;
  margin-top: 2rem;
  width: 100%;
  align-items: center;
}

.cards-row {
  display: flex;
  gap: 2rem;
  justify-content: center;
  flex-wrap: wrap;
}

.card {
  flex: 0 0 calc(33.33% - 2rem);
  max-width: 300px;
}
</style>

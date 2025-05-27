<template>
  <div class="landing-wrapper">
    <section ref="hero" class="section hero">
      <h1 class="hero-title">금융생활을 보다 더 편리하게</h1>
      <p class="hero-subtitle">당신의 금융,<br />선호하는 것을 지원해 드립니다.</p>
      <button class="cta">지금 시작하기</button>
    </section>

    <section ref="products" class="section products">
      <div class="products-text">
        <br />
        <br />
        <h2>다양한 금융 상품을 한 눈에 비교해요.</h2>
        <!-- <br /> -->
        <p>여러 은행의 예적금 상품을 모아 볼 수 있어요.</p>
      </div>

      <div class="carousel-row-wrapper">
        <h3 class="carousel-row-title">예금 TOP10</h3>
        <div ref="depositCarousel" class="carousel-row-track">
          <div class="carousel-card" v-for="deposit in topDeposits" :key="'deposit-' + deposit.id">
            <div class="carousel-card-header">
              <img
                class="bankimage"
                v-if="getBankImage(deposit.kor_co_nm)"
                :src="getBankImage(deposit.kor_co_nm)"
                alt="은행 로고"
              />
            </div>
            <div class="carousel-card-content">
              <h3>{{ deposit.fin_prdt_nm }}</h3>
              <h4>{{ deposit.kor_co_nm }}</h4>
              <h5>금리: {{ deposit.max_intr_rate2 }}%</h5>
            </div>
          </div>

          <div class="carousel-card" v-for="deposit in topDeposits" :key="'deposit-' + deposit.id">
            <div class="carousel-card-header">
              <img
                class="bankimage"
                v-if="getBankImage(deposit.kor_co_nm)"
                :src="getBankImage(deposit.kor_co_nm)"
                alt="은행 로고"
              />
            </div>
            <div class="carousel-card-content">
              <h3>{{ deposit.fin_prdt_nm }}</h3>
              <h4>{{ deposit.kor_co_nm }}</h4>
              <h5>금리: {{ deposit.max_intr_rate2 }}%</h5>
            </div>
          </div>
        </div>
        <div class="gradient-overlay gradient-overlay-left"></div>
        <div class="gradient-overlay gradient-overlay-right"></div>
      </div>

      <div class="carousel-row-wrapper">
        <h3 class="carousel-row-title">적금 TOP10</h3>
        <div ref="savingCarousel" class="carousel-row-track">
          <div class="carousel-card" v-for="saving in topSavings" :key="'saving-' + saving.id">
            <div class="carousel-card-header">
              <img
                class="bankimage"
                v-if="getBankImage(saving.kor_co_nm)"
                :src="getBankImage(saving.kor_co_nm)"
                alt="은행 로고"
              />
            </div>
            <div class="carousel-card-content">
              <h3>{{ saving.fin_prdt_nm }}</h3>
              <h4>{{ saving.kor_co_nm }}</h4>
              <h5>금리: {{ saving.max_intr_rate2 }}%</h5>
            </div>
          </div>
          <div class="carousel-card" v-for="saving in topSavings" :key="'saving-' + saving.id">
            <div class="carousel-card-header">
              <img
                class="bankimage"
                v-if="getBankImage(saving.kor_co_nm)"
                :src="getBankImage(saving.kor_co_nm)"
                alt="은행 로고"
              />
            </div>
            <div class="carousel-card-content">
              <h3>{{ saving.fin_prdt_nm }}</h3>
              <h4>{{ saving.kor_co_nm }}</h4>
              <h5>금리: {{ saving.max_intr_rate2 }}%</h5>
            </div>
          </div>
        </div>
        <div class="gradient-overlay gradient-overlay-left"></div>
        <div class="gradient-overlay gradient-overlay-right"></div>
      </div>
    </section>

    <!-- 커뮤니티 -->
    <section ref="community" class="section community">
      <h2 class="community-title1">혼자보다 함께 더 똑똑한 금융 생활!</h2>
      <p class="community-title2">금융 고민, 함께 나눠요</p>
      <div
        v-for="(articles, category) in store.popularArticlesByCategory"
        :key="category"
        class="category-block"
      >
        <h3 class="category-header"># {{ categoryLabels[category] || category }}</h3>
        <div class="community-container">
          <div v-for="article in articles.slice(0, 3)" :key="article.id" class="community-card">
            <div class="community-title">{{ article.title }}</div>
            <div class="community-tags">
              <span class="community-tag"
                >#{{ categoryLabels[article.category] || article.category }}</span
              >
            </div>
            <div class="community-extra">
              <strong>{{ article.user }}</strong
              ><br />
              {{ truncateContent(article.content, 3) }}
            </div>
          </div>
        </div>
      </div>
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
import { ref, onMounted, nextTick } from 'vue'
import axios from 'axios'
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'
import { RouterLink } from 'vue-router'
import { useArticleStore } from '@/stores/article'
import SpotChart from '@/components/SpotChart.vue'
const bankImages = import.meta.glob('@/assets/images/*', { eager: true, import: 'default' })
const store = useArticleStore()

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

const mapContainerRef = ref(null)

const initLandingMap = () => {
  const { kakao } = window
  const options = {
    center: new kakao.maps.LatLng(37.566826, 126.9786567),
    level: 3,
  }
  const kakaoMap = new kakao.maps.Map(mapContainerRef.value, options)
  map.value = kakaoMap
}
const depositCarousel = ref(null)
const savingCarousel = ref(null)

const categoryLabels = {
  REVIEW: '예적금 후기',
  TIP: '절약 꿀팁',
  FREE: '자유게시판',
}

function truncateContent(text, lines = 3) {
  const words = text.split('\n')
  if (words.length <= lines) return text
  return words.slice(0, lines).join('\n') + '...'
}

function getBankImage(bankName) {
  const entry = Object.entries(bankImages).find(([path, _]) => path.includes(`/${bankName}.`))
  return entry ? entry[1] : null
}

// onMounted 1: 인기 글 불러오기
onMounted(() => {
  store.getPopularArticlesByCategory()
})

// onMounted 2: 예/적금 불러오기 + carousel 애니메이션
onMounted(async () => {
  try {
    const [depositRes, savingRes] = await Promise.all([
      axios.get(`${API_URL}/finlife/deposit/`, { params: { ordering: '-joined_count' } }),
      axios.get(`${API_URL}/finlife/saving/`, { params: { ordering: '-joined_count' } }),
    ])
    topDeposits.value = depositRes.data.slice(0, 10)
    topSavings.value = savingRes.data.slice(0, 10)
  } catch (err) {
    console.error('인기 상품 불러오기 실패:', err)
  }

  await nextTick()

  const sections = [products, recommend, community, market, map]
  // sections.forEach((sectionRef, i) => {
  //   gsap.fromTo(
  //     sectionRef.value,
  //     { opacity: 0, y: 100, scale: 0.95 },
  //     {
  //       scrollTrigger: {
  //         trigger: sectionRef.value,
  //         start: 'top 80%',
  //         toggleActions: 'play none none none',
  //       },
  //       opacity: 1,
  //       y: 0,
  //       scale: 1,
  //       duration: 0.8,
  //       ease: 'power3.out',
  //       delay: i * 0.15,
  //     },
  //   )
  // })

  if (depositCarousel.value) {
    const width = depositCarousel.value.scrollWidth
    gsap.to(depositCarousel.value, {
      x: `-50%`,
      ease: 'none',
      duration: 60,
      repeat: -1,
      modifiers: {
        x: gsap.utils.unitize((x) => parseFloat(x) % width),
      },
    })
  }

  if (savingCarousel.value) {
    const width = savingCarousel.value.scrollWidth
    gsap.to(savingCarousel.value, {
      x: `-50%`,
      ease: 'none',
      duration: 60,
      repeat: -1,
      modifiers: {
        x: gsap.utils.unitize((x) => parseFloat(x) % width),
      },
    })
  }
})
onMounted(async () => {
  const waitForKakao = () =>
    new Promise((resolve) => {
      const check = () => {
        if (window.kakao && kakao.maps && typeof kakao.maps.Map === 'function') {
          resolve()
        } else setTimeout(check, 100)
      }
      check()
    })

  await waitForKakao()
  await nextTick()
  initLandingMap()
})
</script>

<style scoped>
* {
  font-family: Pretendard;
}

html,
body {
  scroll-behavior: smooth;
  margin: 0;
  padding: 0;
  background: #f9fafb;

  /* box-shadow: inset 0 0 3px dodgerblue; */
}
h2 {
  text-align: center;
}
.section {
  min-height: 100vh;
  /* padding: 6rem 2rem; */
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  scroll-snap-align: start;
  /* padding: 200px; */
  /* box-shadow: inset 0 0 3px dodgerblue; */
}
.section.products {
  flex-direction: column;
  box-sizing: border-box;
  margin-bottom: 150px;
  /* padding: none !important; */
}
.section.community {
  background-color: black;
}

.section.community::after {
}
.section.recommend {
  font-size: 2rem;
  font-weight: 600;
}
.section.market {
  background: #f3f4f6; /* 연한 그레이 */
  padding: 5rem 2rem;
  text-align: center;
}

.section.market h2 {
  font-size: 2.5rem;
  font-weight: 700;
  color: #0f172a;
  margin-bottom: 2rem;
}

.graph {
  width: 100%;
  height: 400px;
  background-color: white;
  border-radius: 16px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.06);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  color: #94a3b8;
}

.section.recommend p {
  font-size: 1.5rem;
  font-weight: 600;
}
.hero {
  /* 기존 배경 그대로 유지하고 */
  position: relative;
  background:
    linear-gradient(to bottom, rgba(0, 0, 0, 0.8), rgba(0, 0, 0, 0.3)),
    url('@/assets/images/image10.jpg');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  text-align: center;
  color: white;
}
.community-title1 {
  color: white;
}

.hero::after {
  content: '';
  position: absolute;
  bottom: -1px;
  left: 0;
  width: 100%;
  height: 200px;
  background: linear-gradient(to bottom, transparent, #ffffff);
  z-index: 1;
}
.community-title2 {
  color: white;
  font-size: 1.5rem;
}
.hero-title {
  display: block;
  word-break: keep-all;
  white-space: normal;
  text-align: center;
  font-weight: 600;
  font-size: 4rem;
  /* color: #191f28; */
}
.hero-subtitle {
  font-size: 2rem;
  /* color: #4e5968; */
}

.products {
  display: flex;
  flex-direction: row;
  background: #fff;
}
.products-text {
  font-size: 2rem;
  font-weight: 600;
  flex-direction: column;
  word-break: keep-all;
  white-space: normal;
  text-align: center;
}
.products-text p {
  font-size: 1.5rem;
  margin-top: 10px;
  font-weight: 500;
  word-break: keep-all;
  white-space: normal;
}

.recommend {
  display: flex;
  flex-direction: column;
  background: #bae6fd;
  word-break: keep-all;
  white-space: normal;
}
.community {
  background: #d1fae5;
  word-break: keep-all;
  white-space: normal;
}
.market {
  background: #f3e8ff;
  word-break: keep-all;
  white-space: normal;
}
.map {
  background: #fff7ed;
  word-break: keep-all;
  white-space: normal;
}
.bankimage {
  background-color: white;
}

.section .final-cta {
  background-color: #2563eb;
  color: white;
  text-align: center;
  /* height: 100px; */
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
  /* flex-direction: column; */
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
  text-align: start;
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
  text-align: start;
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
.carousel-row-wrapper {
  width: 100%;
  overflow: hidden;
  position: relative;
  padding: 2rem 0;
  background-color: #fff;
}

.carousel-row-track {
  display: flex;
  gap: 2.5rem;
  width: max-content;
  flex-wrap: nowrap;
}

.carousel-card {
  width: 250px;
  height: 250px; /* 고정 높이 */
  background-color: #e5e7eb;
  border-radius: 0.75rem;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.08);
  flex-shrink: 0;
  word-break: keep-all;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  white-space: normal;
}

.carousel-card-header {
  flex: 0 0 40%; /* 높이의 45% */
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: white;
}

.carousel-card-header img {
  max-height: 100px;
  max-width: 100%;
  object-fit: cover;
  padding: 1rem;
}

.carousel-card-content {
  flex: 1; /* 나머지 55% */
  padding: 1rem;
  text-align: center;
  display: flex;
  gap: 5px;
  flex-direction: column;
  justify-content: center;
  /* align-self: center; */
  font-size: 0.95rem;
}

.carousel-card-content h3 {
  font-size: 1.1rem;
  font-weight: 500;
}
.carousel-card-content h4 {
  font-size: 1rem;
  font-weight: 400;
}
.carousel-card-content h5 {
  font-size: 0.8rem;
  font-color: #4e5968;
  font-weight: 400;
}

.carousel-row-title {
  text-align: center;
  font-size: 1.5rem;
  font-weight: 500;
  margin-bottom: 60px;
}
.gradient-overlay {
  position: absolute;
  top: 0;
  bottom: 0;
  width: 100px; /* 더 넓게 */
  z-index: 999;
  pointer-events: none;
}

.gradient-overlay-left {
  left: 0;
  background: linear-gradient(to right, #ffffff, rgba(255, 255, 255, 0));
}

.gradient-overlay-right {
  right: 0;
  background: linear-gradient(to left, #ffffff, rgba(255, 255, 255, 0));
}
.category-header {
  font-size: 1.25rem;
  font-weight: bold;
  margin: 2rem 0 1rem;
}
.section.recommend {
  background: #e0f2fe;
  padding: 5rem 2rem;
  text-align: center;
}

.section.recommend h2 {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 1rem;
  color: #0f172a;
}

.section.recommend p {
  font-size: 1.3rem;
  color: #334155;
  margin-bottom: 2rem;
}

/* 커뮤니티 섹션 */
.section.community {
  /* background: #ecfdf5; */
  padding: 5rem 2rem;
  text-align: center;
}

.section.community h2 {
  font-size: 2.5rem;
  font-weight: 700;
  color: white;
  margin-bottom: 2rem;
}

.category-header {
  font-size: 1.2rem;
  font-weight: 600;
  color: white;
  margin-bottom: 1rem;
  text-align: left;
}

.community-container {
  display: flex;
  gap: 1.5rem;
  flex-wrap: wrap;
  /* justify-content: center; */
}

/* 마지막 CTA */
.section.final-cta {
  padding: 6rem 2rem;
  background-color: rgb(1, 112, 223);
  color: white;
  text-align: center;
  min-height: 30vh;
}

.section.final-cta h2 {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 2rem;
}

.cta-buttons button {
  padding: 1rem 2rem;
  background-color: #ffffff;
  color: #2563eb;
  font-size: 1rem;
  font-weight: 600;
  border-radius: 0.5rem;
  transition: background 0.3s ease;
  border: none;
}

.cta-buttons button:hover {
  background-color: #e0e7ff;
}
</style>

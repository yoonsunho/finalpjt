<template>
  <swiper
    class="mySwiper"
    :modules="modules"
    :pagination="{ clickable: true }"
    :navigation="true"
    :loop="true"
    :autoplay="{ delay: 4000, disableOnInteraction: false }"
  >
    <swiper-slide v-for="(slide, index) in slides" :key="index">
      <div class="slide-container">
        <img
          :src="slide.src"
          :alt="slide.text.replace(/<br\s*\/?>/g, ' ')"
          :style="slide.positionStyle"
        />
        <div class="overlay"></div>

        <div class="content-wrapper">
          <div class="slide-text">
            <div class="text" v-html="slide.text"></div>
          </div>
          <div class="slide-subtext">
            <div class="subtext" v-html="slide.subtext"></div>
          </div>
          <button class="cta-button">바로가기</button>
        </div>
      </div>
    </swiper-slide>
  </swiper>
</template>

<script setup>
import { Swiper, SwiperSlide } from 'swiper/vue'
import 'swiper/css'
import { Autoplay } from 'swiper/modules'

// Swiper 모듈들을 등록
const modules = [Autoplay]

const slides = [
  {
    src: new URL('@/assets/images/image1.png', import.meta.url).href,
    text: '여러 가지 예금 상품을 한눈에 비교해요!',
    subtext: '금리, 조건 비교하고 가입까지 한 번에',
    positionStyle: 'object-position: 10% center;',
  },
  {
    src: new URL('@/assets/images/image2.png', import.meta.url).href,
    text: '내게 맞는 적금 상품 찾아봐요!',
    subtext: '맞춤 금융상품 추천으로 쉬운 상품 선택',
    positionStyle: 'object-position: 21% center;',
  },
  {
    src: new URL('@/assets/images/image3.png', import.meta.url).href,
    text: '실시간으로 현물 시세를 확인해요.',
    subtext: '금, 은 시세의 변동을 확인할 수 있어요',
    positionStyle: 'object-position: top center;',
  },
  {
    src: new URL('@/assets/images/image4.png', import.meta.url).href,
    text: '혼자보다 함께 더 똑똑한 금융 생활',
    subtext: '다른 사람들과 금융 팁을 나누고 함께 성장해요',
    positionStyle: 'object-position: 44% center;',
  },
  {
    src: new URL('@/assets/images/image5.png', import.meta.url).href,
    text: '내 근처 은행을 검색해요',
    subtext: '지금 나와 가까운 은행 검색으로 편리한 금융생활',
    positionStyle: 'object-position: 1% center;',
  },
]
</script>

<style scoped>
* {
  font-family: Pretendard;
}
.mySwiper {
  width: 100%;
  padding: 0 !important;
  margin: 0 !important;
}

.swiper-slide {
  display: flex;
  justify-content: center;
  align-items: center;
}

.slide-container {
  position: relative;
  width: 100%;
  height: 580px;
  overflow: hidden;
}

@media (max-width: 768px) {
  .slide-container {
    height: 400px;
  }
}

@media (max-width: 480px) {
  .slide-container {
    height: 300px;
  }
}

.slide-container img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: top center;
}

.overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(to bottom, rgba(0, 0, 0, 0), rgba(0, 0, 0, 0.45));
  z-index: 1;
}

.content-wrapper {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  padding: 0rem 8% 6rem;
  z-index: 2;
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
}

@media (max-width: 768px) {
  .content-wrapper {
    padding: 1.5rem 8% 2rem;
  }
}

@media (max-width: 480px) {
  .content-wrapper {
    padding: 1rem 5% 1.5rem;
  }
}

.cta-button {
  background-color: white;
  color: #191f28;
  padding: 0.5rem 1.4rem;
  border: none;
  border-radius: 9999px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.3s ease;
  align-self: flex-start;
  margin-top: 0.5rem;
}

.cta-button:hover {
  background-color: #f0f0f0;
}

.slide-subtext {
  color: white;
  max-width: 100%;
  line-height: 1.4;
  text-align: left;
}

.slide-subtext .subtext {
  font-size: 1rem;
  word-break: keep-all;
}

@media (max-width: 480px) {
  .slide-subtext .subtext {
    font-size: 0.875rem;
  }
}

.slide-text {
  color: white;
  max-width: 100%;
  line-height: 1.4;
  text-align: left;
}

.slide-text .text {
  font-size: 2.5rem;
  font-weight: bold;
  word-break: keep-all;
}

@media (max-width: 768px) {
  .slide-text .text {
    font-size: 2rem;
  }
}

@media (max-width: 480px) {
  .slide-text .text {
    font-size: 1.5rem;
  }
}
</style>

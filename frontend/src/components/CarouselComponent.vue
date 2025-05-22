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
        <img :src="slide.src" :alt="slide.text.replace(/<br\s*\/?>/g, ' ')" />
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
    src: new URL('@/assets/images/image1.jpg', import.meta.url).href,
    text: '당신에게 딱 맞는<br>점심 메뉴를<br>추천해드립니다..바로!',
    subtext: '부가설명을 넣는 서브텍스트입니다.',
  },
  {
    src: new URL('@/assets/images/image2.jpg', import.meta.url).href,
    text: '집가고싶은사람 손',
    subtext: '부가설명을 넣는 서브<br>텍스트입니다.부가설명을 넣는 서브텍스트입니다.',
  },
  {
    src: new URL('@/assets/images/image3.jpg', import.meta.url).href,
    text: '덥고배고프고졸립니다..',
    subtext: '부가설명을 넣는 서브텍스트입니다.부가설<br>명을 넣는 서브텍스트입니다.부',
  },
  {
    src: new URL('@/assets/images/image4.jpg', import.meta.url).href,
    text: '당신에게 딱 맞는 금융상품을 추천해 드립니다. 저축을 열심히 해보세염. 지금 당장 시작해볼까요? 아자아자!',
    subtext:
      '부가설명을 넣는 서브부가설명을 넣는 서브텍스트입니다.부가설명을 넣는 서브텍스트입니다.부.',
  },
]
</script>

<style scoped>
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
  height: 500px;
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
}

.overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(to bottom, rgba(0, 0, 0, 0.2), rgba(0, 0, 0, 0.95));
  z-index: 1;
}

.content-wrapper {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  padding: 2rem 10% 3rem;
  z-index: 2;
  display: flex;
  flex-direction: column;
  gap: 1rem;
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
  color: black;
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

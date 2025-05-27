<template>
<div v-if="video" class="detail-container">
    
    <h2>{{ video.snippet.title }}</h2>
    <p>업로드 날짜: {{ video.snippet.publishedAt.slice(0, 10) }}</p>
    <iframe
      width="640"
      height="360"
      :src="`https://www.youtube.com/embed/${videoId}`"
      frameborder="0"
      allowfullscreen
    ></iframe>
    <p class="description">{{ video.snippet.description }}</p>

  </div>
  <div v-else class="loading">동영상 정보를 불러오는 중입니다...</div>
</template>

<script setup>
 import {ref} from 'vue'
    import {useRoute,useRouter} from 'vue-router'
    const API_KEY = import.meta.env.VITE_YOUTUBE_API_KEY

    const route = useRoute()
    const router = useRouter()
    const videoId = route.params.id

    const video = ref(null)


    // 유튜브 API로 상세 정보 가져오기
    const fetchVideoDetail = () => {
    const params = new URLSearchParams({
        part: 'snippet',
        id: videoId,
        key: API_KEY
    })
    fetch(`https://www.googleapis.com/youtube/v3/videos?${params}`)
        .then(res => res.json())
        .then(data => {
        video.value = data.items[0]
        })
    }

    // 컴포넌트 마운트 시 데이터 불러오기
    fetchVideoDetail()


</script>

<style scoped>

</style>
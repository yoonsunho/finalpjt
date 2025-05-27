<template>
    <div class="search-container">
        <input type="text"
        v-model="searchQuery"
        placeholder="검색어를 입력하세요."
        @keyup.enter = 'searchVideos'>
        <button @click="searchVideos">검색</button>
    </div>
    
    <!-- 검색 결과 표시 -->
    <div v-if="loading" class="loading">검색 중..</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else class="results">
        <div v-for="video in videos">
            <RouterLink :to="{name:'StockInfoDetailView', params:{id:video.id.videoId}}">
                <img :src="video.snippet.thumbnails.medium.url" :alt="video.snippet.title">
                <div class="video-info">
                    <h4>{{ video.snippet.title }}</h4>
                    <p>{{ video.snippet.channelTitle }}</p>
                </div>
            </RouterLink>
        </div>
    </div>
</template>

<script setup>
    import {ref, onMounted} from 'vue'
    import { useRoute ,RouterLink} from 'vue-router'
    
    const API_KEY = import.meta.env.VITE_YOUTUBE_API_KEY
    const searchQuery = ref('')
    const videos = ref([])
    const loading = ref(false)
    const error = ref(null)

    //동영상 검색
    const searchVideos  = () => {
    if (!searchQuery.value.trim()) return;

    loading.value = true;
    error.value = null;

    const params = new URLSearchParams({
        part: 'snippet',
        maxResults: 10,
        q: searchQuery.value,
        type: 'video',
        key: API_KEY
    })

    fetch(`https://www.googleapis.com/youtube/v3/search?${params}`)
        .then(response => {
            if (!response.ok) throw new Error('API 요청 실패');
            return response.json();
        })
        .then(data => {
            videos.value = data.items;
            loading.value = false;
        })
        .catch(err => {
            console.error('API 요청 오류:', err);
            error.value = '동영상을 불러오는 중 오류가 발생했습니다.';
            loading.value = false;
        });
    }
    
</script>

<style scoped>

.search-container {
    margin-bottom: 20px;
    display: flex;
}

input {
    padding: 8px;
    width: 300px;
    margin-right: 10px;
    border: 1px solid #ddd;
    border-radius: 4px;
}

button {
    padding: 8px 16px;
    background-color: #FF0000;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

button:hover {
    background-color: #CC0000;
}


.results {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 20px;
}

.video-item {
    border: 1px solid #eee;
    border-radius: 4px;
    overflow: hidden;
}

.video-item img {
    width: 100%;
    height: auto;
}

.video-info {
    padding: 10px;
}

.video-info h4 {
    margin: 0 0 8px 0;
    font-size: 16px;
}

.video-info p {
    margin: 0;
    color: #666;
    font-size: 14px;
}

.loading, .error {
    text-align: center;
    padding: 20px;
}

.error {
    color: red;
}
</style>
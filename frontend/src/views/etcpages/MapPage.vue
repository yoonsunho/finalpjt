<template>
  <div class="bank-finder-app">
    <div class="header">
      <div class="header-content">
        <h1>내 주변 은행 찾기</h1>
        <p class="subtitle">원하는 지역과 은행을 선택하여 가까운 지점을 찾아보세요</p>
      </div>
    </div>

    <div class="search-bank">
      <div class="search-section">
        <div class="search-header">
          <h2>검색 조건</h2>
        </div>

        <div class="selectors" :class="{ disabled: !isKakaoReady }">
          <div class="selector-group">
            <label>📍 시/도</label>
            <select v-model="selectedName" @change="onNameChange" :disabled="!isKakaoReady">
              <option disabled value="">시/도를 선택해주세요</option>
              <option v-for="item in mapInfo" :key="item.name" :value="item.name">
                {{ item.name }}
              </option>
            </select>
          </div>

          <div class="selector-group">
            <label>🏘️ 시/군/구</label>
            <select v-model="selectedCountry" :disabled="!selectedName || !isKakaoReady">
              <option disabled value="">
                {{ selectedName ? '시/군/구를 선택해주세요' : '먼저 시/도를 선택해주세요' }}
              </option>
              <option v-for="country in countries" :key="country" :value="country">
                {{ country }}
              </option>
            </select>
          </div>

          <div class="selector-group">
            <label>🏛️ 은행</label>
            <select v-model="selectedBank" :disabled="!isKakaoReady">
              <option disabled value="">은행을 선택해주세요</option>
              <option v-for="bank in bankInfo" :key="bank" :value="bank">{{ bank }}</option>
            </select>
          </div>

          <button
            class="search-button"
            @click="combineSelection"
            :disabled="
              !isKakaoReady ||
              isSearching ||
              !map ||
              !selectedName ||
              !selectedCountry ||
              !selectedBank
            "
          >
            <span v-if="isSearching" class="loading-spinner"></span>
            <span class="button-text">
              {{ isSearching ? '검색중...' : '🔍 검색하기' }}
            </span>
          </button>
        </div>
      </div>

      <div class="result-area">
        <div class="map-section">
          <div class="section-header">
            <h3>지도</h3>
            <div class="result-count" v-if="searchResults.length > 0">
              {{ searchResults.length }}개 지점 발견
            </div>
          </div>
          <div class="kakao-map-container" ref="mapContainerRef">
            <div v-if="!isKakaoReady" class="map-loading">
              <div class="loading-spinner large"></div>
              <p>지도를 불러오는 중...</p>
            </div>
          </div>
        </div>

        <div class="list-section">
          <div class="section-header">
            <h3>검색 결과</h3>
            <button v-if="searchResults.length > 0" class="clear-button" @click="clearResults">
              초기화
            </button>
          </div>

          <div class="result-list">
            <div v-if="searchResults.length === 0" class="empty-state">
              <div class="empty-icon">🔍</div>
              <h4>검색 결과가 없습니다</h4>
              <p>위에서 조건을 선택하고 검색해보세요</p>
            </div>

            <div
              v-for="place in searchResults"
              :key="place.id"
              class="result-card"
              @click="focusMarker(place.id)"
            >
              <div class="card-header">
                <h4>{{ place.place_name }}</h4>
                <span class="distance" v-if="place.distance">{{ place.distance }}m</span>
              </div>
              <div class="card-content">
                <p class="address">📍 {{ place.address_name }}</p>
                <p v-if="place.phone" class="phone">📞 {{ place.phone }}</p>
                <p v-if="place.category_name" class="category">🏷️ {{ place.category_name }}</p>
              </div>
              <div class="card-actions">
                <!-- <span class="click-hint">클릭하여 지도에서 보기</span> -->
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, nextTick } from 'vue'
import jsonData from '@/assets/data.json'

const mapInfo = ref(jsonData.mapInfo)
const bankInfo = ref(jsonData.bankInfo)

const selectedName = ref('')
const selectedCountry = ref('')
const selectedBank = ref('')
const countries = ref([])

const isKakaoReady = ref(false)
const isSearching = ref(false)
const mapContainerRef = ref(null)
const map = ref(null)
const markerList = ref([])
const searchResults = ref([])
const mapCenter = ref({
  lat: 37.566826,
  lng: 126.9786567,
})

const getCurrentLocation = () => {
  return new Promise((resolve, reject) => {
    if (!navigator.geolocation) {
      reject(new Error('브라우저가 위치 정보를 지원하지 않아요!'))
    } else {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          resolve({
            lat: position.coords.latitude,
            lng: position.coords.longitude,
          })
        },
        (err) => {
          reject(new Error('위치 정보 접근 실패'))
        },
      )
    }
  })
}

const onNameChange = () => {
  const selected = mapInfo.value.find((item) => item.name === selectedName.value)
  countries.value = selected ? selected.countries : []
  selectedCountry.value = ''
}

watch(selectedName, onNameChange)

const checkKakaoReady = (timeout = 10000) => {
  return new Promise((resolve, reject) => {
    const start = Date.now()
    const check = () => {
      if (window.kakao && kakao.maps && typeof kakao.maps.Map === 'function') {
        resolve(true)
      } else if (Date.now() - start > timeout) {
        reject(new Error('카카오맵 SDK 로딩 타임아웃'))
      } else {
        setTimeout(check, 100)
      }
    }
    check()
  })
}

const initMap = () => {
  const { kakao } = window
  const options = {
    center: new kakao.maps.LatLng(mapCenter.value.lat, mapCenter.value.lng),
    level: 3,
  }

  const kakaoMap = new kakao.maps.Map(mapContainerRef.value, options)

  const zoomControl = new kakao.maps.ZoomControl()
  kakaoMap.addControl(zoomControl, kakao.maps.ControlPosition.RIGHT)

  kakao.maps.event.addListener(kakaoMap, 'dragend', () => {
    const center = kakaoMap.getCenter()
    mapCenter.value = { lat: center.getLat(), lng: center.getLng() }
  })

  map.value = kakaoMap
}

const combineSelection = async () => {
  if (!selectedName.value || !selectedCountry.value || !selectedBank.value) {
    alert('모든 항목을 선택해주세요.')
    return
  }

  if (!map.value) {
    alert('지도가 아직 준비되지 않았습니다.')
    return
  }

  const keyword = `${selectedName.value} ${selectedCountry.value} ${selectedBank.value}`
  await searchPlace(keyword)
}

const searchPlace = async (keyword) => {
  const { kakao } = window
  if (!keyword || !map.value || !kakao?.maps?.services?.Places) return

  isSearching.value = true

  markerList.value.forEach((markerObj) => markerObj.marker.setMap(null))
  markerList.value = []

  try {
    const ps = new kakao.maps.services.Places()
    const data = await new Promise((resolve) => {
      ps.keywordSearch(keyword, (res, status) => {
        resolve(status === kakao.maps.services.Status.OK ? res : [])
      })
    })

    searchResults.value = data
    if (data.length === 0) {
      alert('검색 결과가 없습니다. 다른 조건으로 검색해보세요.')
      return
    }

    const bounds = new kakao.maps.LatLngBounds()

    for (const place of data) {
      const position = new kakao.maps.LatLng(place.y, place.x)
      const marker = new kakao.maps.Marker({
        position,
        map: map.value,
      })
      const infoWindow = new kakao.maps.InfoWindow({
        content: `
          <div style="padding: 12px 16px; min-width: 220px; font-family: Pretendard;">
            <h4 style="margin: 0 0 8px 0; font-size: 16px; font-weight: 600; color: #1f2937;">${place.place_name}</h4>
            <p style="margin: 0 0 4px 0; font-size: 13px; color: #6b7280; line-height: 1.4;">📍 ${place.address_name}</p>
            ${place.phone ? `<p style="margin: 0 0 4px 0; font-size: 13px; color: #3b82f6;">📞 ${place.phone}</p>` : ''}
            ${place.category_name ? `<p style="margin: 0; font-size: 12px; color: #9ca3af;">🏷️ ${place.category_name}</p>` : ''}
          </div>
        `,
      })
      kakao.maps.event.addListener(marker, 'click', () => {
        markerList.value.forEach(({ infoWindow }) => infoWindow.close())
        infoWindow.open(map.value, marker)
      })
      markerList.value.push({ marker, infoWindow, id: place.id })
      bounds.extend(position)
    }

    map.value.setBounds(bounds)
  } finally {
    isSearching.value = false
  }
}

const focusMarker = (placeId) => {
  const markerObj = markerList.value.find((item) => item.id === placeId)
  if (markerObj) {
    map.value.panTo(markerObj.marker.getPosition())
    map.value.setCenter(markerObj.marker.getPosition())
    markerList.value.forEach(({ infoWindow }) => infoWindow.close())
    markerObj.infoWindow.open(map.value, markerObj.marker)
  }
}

const clearResults = () => {
  searchResults.value = []
  markerList.value.forEach((markerObj) => markerObj.marker.setMap(null))
  markerList.value = []
}

onMounted(async () => {
  try {
    await checkKakaoReady()
    const location = await getCurrentLocation()
    mapCenter.value = location
  } catch (err) {
    mapCenter.value = { lat: 37.566826, lng: 126.9786567 }
  }

  await nextTick()
  initMap()
  isKakaoReady.value = true
})
</script>

<style scoped>
* {
  font-family: Pretendard;
}

/* 전체 앱 컨테이너 */
.bank-finder-app {
  min-height: 100vh;
  /* padding: 20px 0; */
}

/* 헤더 */
.header {
  text-align: center;
  margin-bottom: 40px;
}

.header-content h1 {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 8px;
}

.subtitle {
  font-size: 1.1rem;
  color: rgba(255, 255, 255, 0.9);
  margin: 0;
}

/* 메인 검색 영역 */
.search-bank {
  width: 100%;
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  flex-direction: column;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
  border-radius: 20px;
  /* gap: 32px; */
}

/* 검색 섹션 */
.search-section {
  background: white;
  border-radius: 20px;
  padding: 32px;
}

.search-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.search-header h2 {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0;
}

@keyframes pulse {
  0%,
  100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

/* 셀렉터 영역 */
.selectors {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  transition: opacity 0.3s ease;
}

.selector-group {
  flex: 1;
  min-width: 200px;
}

.selectors.disabled {
  opacity: 0.5;
  pointer-events: none;
}

.selector-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.selector-group label {
  font-size: 14px;
  font-weight: 600;
  color: #374151;
}

select {
  width: 100%;
  padding: 16px;
  font-size: 16px;
  border-radius: 12px;
  border: 2px solid #e5e7eb;
  background-color: #ffffff;
  transition: all 0.2s ease;
  cursor: pointer;
}

select:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

select:disabled {
  background-color: #f9fafb;
  color: #9ca3af;
  cursor: not-allowed;
}

.search-button {
  width: 100%;
  padding: 18px;
  font-size: 18px;
  font-weight: 600;
  border-radius: 16px;
  border: none;
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  color: white;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  margin-top: 12px;
}

.search-button:hover:not(:disabled) {
  background: linear-gradient(135deg, #2563eb, #1e40af);
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(59, 130, 246, 0.3);
}

.search-button:disabled {
  background: #cbd5e1;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}
/* 결과 영역 */
.result-area {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 32px;
}

.map-section,
.list-section {
  background: white;
  border-radius: 20px;
  padding: 24px;
  /* box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1); */
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.section-header h3 {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0;
}

.result-count {
  background: #dbeafe;
  color: #1e40af;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 500;
}

.clear-button {
  background: #fee2e2;
  color: #dc2626;
  border: none;
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.clear-button:hover {
  background: #fecaca;
}

/* 지도 */
.kakao-map-container {
  width: 100%;
  height: 520px;
  border-radius: 16px;
  overflow: hidden;
  position: relative;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
}

.map-loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #6b7280;
}

.result-list {
  max-height: 520px;
  padding-right: 7px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.result-list::-webkit-scrollbar {
  width: 6px;
}

.result-list::-webkit-scrollbar-track {
  background: #f1f5f9;
  border-radius: 3px;
}

.result-list::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 3px;
}

.result-list::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}

.result-card {
  background: #f8fafc;
  padding: 20px;
  border-radius: 16px;
  border: 1px solid #e2e8f0;
  cursor: pointer;
  transition: all 0.3s ease;
}

.result-card:hover {
  background: #f1f5f9;
  border-color: #3b82f6;
  transform: translateY(-2px);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
}

.card-header h4 {
  font-size: 16px;
  font-weight: 600;
  color: #1f2937;
  margin: 0;
  line-height: 1.4;
}

.distance {
  background: #dbeafe;
  color: #1e40af;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
}

.card-content {
  margin-bottom: 12px;
}

.card-content p {
  font-size: 14px;
  margin: 6px 0;
  line-height: 1.4;
}

.address {
  color: #4b5563;
}

.phone {
  color: #3b82f6;
  font-weight: 500;
}

.category {
  color: #6b7280;
  font-size: 13px;
}

.click-hint {
  font-size: 12px;
  color: #9ca3af;
  font-style: italic;
}

/* 빈 상태 */
.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: #6b7280;
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: 16px;
}

.empty-state h4 {
  font-size: 18px;
  font-weight: 600;
  color: #374151;
  margin: 0 0 8px 0;
}

.empty-state p {
  font-size: 14px;
  margin: 0;
}

/* 로딩 스피너 */
.loading-spinner {
  width: 16px;
  height: 16px;
  border: 2px solid transparent;
  border-top: 2px solid currentColor;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.loading-spinner.large {
  width: 24px;
  height: 24px;
  border-width: 3px;
  margin-bottom: 12px;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* 반응형 */
@media (max-width: 1024px) {
  .result-area {
    grid-template-columns: 1fr;
  }

  .list-section {
    order: -1;
  }

  .result-list {
    max-height: 300px;
  }
}

@media (max-width: 768px) {
  .header-content h1 {
    font-size: 2rem;
  }

  .selectors {
    grid-template-columns: 1fr;
  }

  .search-section {
    padding: 24px;
  }

  .kakao-map-container {
    height: 400px;
  }
}
</style>

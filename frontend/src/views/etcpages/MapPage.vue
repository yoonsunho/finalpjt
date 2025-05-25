<template>
  <div class="search-bank">
    <select v-model="selectedName" @change="onNameChange">
      <option disabled value="">시/도 선택</option>
      <option v-for="item in mapInfo" :key="item.name" :value="item.name">{{ item.name }}</option>
    </select>

    <select v-model="selectedCountry" :disabled="!selectedName">
      <option disabled value="">시/군/구 선택</option>
      <option v-for="country in countries" :key="country">{{ country }}</option>
    </select>

    <select v-model="selectedBank">
      <option disabled value="">은행 선택</option>
      <option v-for="bank in bankInfo" :key="bank">{{ bank }}</option>
    </select>

    <button @click="combineSelection">검색</button>
  </div>

  <KakaoMap
    class="kakao-map-container"
    :lat="37.566826"
    :lng="126.9786567"
    @onLoadKakaoMap="onLoadKakaoMap"
  >
    <KakaoMapMarker
      v-for="(marker, index) in markerList"
      :key="marker.key === undefined ? index : marker.key"
      :lat="marker.lat"
      :lng="marker.lng"
      :infoWindow="marker.infoWindow"
      :clickable="true"
      @onClickKakaoMapMarker="onClickMapMarker(marker)"
    />
  </KakaoMap>
</template>
<script setup>
import { KakaoMap, KakaoMapMarker } from 'vue3-kakao-maps'
import { ref, watch, onMounted } from 'vue'
import jsonData from '@/assets/data.json'
const isKakaoReady = ref(false)

const map = ref(null)
const markerList = ref([])

const mapInfo = ref(jsonData.mapInfo)
const bankInfo = ref(jsonData.bankInfo)

const selectedName = ref('') // 선택한 도
const selectedCountry = ref('') // 선택한 시군구
const selectedBank = ref('') // 선택한 은행

const countries = ref([])

watch(selectedName, (newVal) => {
  const nameData = mapInfo.value.find((item) => item.name === newVal)
  countries.value = nameData ? nameData.countries : []
  selectedCountry.value = ''
})

const onLoadKakaoMap = (mapRef) => {
  map.value = mapRef
  // searchPlace()
}

const combineSelection = () => {
  if (!selectedName.value || !selectedCountry.value || !selectedBank.value) {
    alert('항목을 모두 선택해주세요.')
    return
  }

  if (!isKakaoReady.value) {
    alert('지도가 아직 준비 중이에요! 조금만 기다려주세요!')
    return
  }

  const combined = `${selectedName.value} ${selectedCountry.value} ${selectedBank.value}`
  searchPlace(combined)
}

const searchPlace = (keyword) => {
  if (!keyword || !map.value) {
    console.warn('지도 또는 키워드가 비어 있어요!')
    return
  }

  if (typeof kakao === 'undefined' || !kakao.maps?.services) {
    console.warn('카카오 객체 또는 services가 아직 준비되지 않았어요!')
    alert('지도가 아직 준비 중이에요! 잠시 후 다시 시도해주세요!')
    console.error()
    return
  }
  markerList.value = []

  const ps = new kakao.maps.services.Places()
  ps.keywordSearch(keyword, (data, status) => {
    if (status === kakao.maps.services.Status.OK) {
      const bounds = new kakao.maps.LatLngBounds()

      for (let marker of data) {
        const markerItem = {
          lat: marker.y,
          lng: marker.x,
          infoWindow: {
            content: `<div style="padding:4px 10px">${marker.place_name}</div>`,
            visible: false,
          },
        }
        markerList.value.push(markerItem)
        bounds.extend(new kakao.maps.LatLng(Number(marker.y), Number(marker.x)))
      }

      map.value.setBounds(bounds)
    } else {
      alert('검색 결과가 없습니다.')
    }
  })
}

const onClickMapMarker = (markerItem) => {
  markerItem.infoWindow.visible = !markerItem.infoWindow.visible
}
onMounted(() => {
  const checkKakaoReady = setInterval(() => {
    if (window.kakao && kakao.maps && kakao.maps.services) {
      isKakaoReady.value = true
      clearInterval(checkKakaoReady)
      console.log('카카오맵 SDK 로딩 완료!')
    }
  }, 300)
})
</script>
<style scoped>
.search-bank {
  display: flex;
  flex-direction: column;
  gap: 24px;
  max-width: 600px;
  margin: 0 auto;
  padding: 40px 20px;
  background: white;
  border-radius: 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
}

.selectors {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

select {
  padding: 12px 16px;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  font-size: 16px;
  background-color: #f9fafb;
  transition: all 0.2s ease;
}

select:focus {
  outline: none;
  border-color: #3b82f6;
  background-color: white;
}

button {
  padding: 12px;
  font-size: 16px;
  background-color: #3b82f6;
  color: white;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

button:hover {
  background-color: #2563eb;
}

.kakao-map-container {
  width: 100%;
  height: 500px;
  border-radius: 20px;
  overflow: hidden;
  margin-top: 24px;
}
</style>

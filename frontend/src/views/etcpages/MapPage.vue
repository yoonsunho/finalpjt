<template>
  <div class="search-bank">
    <div class="selectors" :class="{ disabled: !isKakaoReady }">
      <select v-model="selectedName" @change="onNameChange" :disabled="!isKakaoReady">
        <option disabled value="">시/도 선택</option>
        <option v-for="item in mapInfo" :key="item.name" :value="item.name">{{ item.name }}</option>
      </select>

      <select v-model="selectedCountry" :disabled="!selectedName || !isKakaoReady">
        <option disabled value="">시/군/구 선택</option>
        <option v-for="country in countries" :key="country" :value="country">{{ country }}</option>
      </select>

      <select v-model="selectedBank" :disabled="!isKakaoReady">
        <option disabled value="">은행 선택</option>
        <option v-for="bank in bankInfo" :key="bank" :value="bank">{{ bank }}</option>
      </select>

      <button @click="combineSelection" :disabled="!isKakaoReady || isSearching || !map">
        {{ isSearching ? '검색 중' : '검색' }}
      </button>
    </div>

    <div class="kakao-map-container" ref="mapContainerRef"></div>
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
watch(selectedName, (newVal) => {
  const selected = mapInfo.value.find((item) => item.name === newVal)
  countries.value = selected ? selected.countries : []
  selectedCountry.value = ''
})

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
    alert('항목을 모두 선택해주세요.')
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

    if (data.length === 0) {
      alert('검색 결과가 없습니다.')
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
          <div style="padding: 8px 12px; min-width: 200px;">
            <h4 style="margin: 0 0 4px 0; font-size: 14px; font-weight: bold;">${place.place_name}</h4>
            <p style="margin: 0; font-size: 12px; color: #666;">${place.address_name}</p>
            ${place.phone ? `<p style="margin: 2px 0 0 0; font-size: 12px; color: #0066cc;">${place.phone}</p>` : ''}
          </div>
        `,
      })
      kakao.maps.event.addListener(marker, 'click', () => {
        markerList.value.forEach(({ infoWindow }) => infoWindow.close()) // 기존 창 닫기
        infoWindow.open(map.value, marker)
      })
      markerList.value.push({ marker, infoWindow })
      bounds.extend(position)
    }

    map.value.setBounds(bounds)
  } finally {
    isSearching.value = false
  }
}

// 컴포넌트 마운트 후 지도 준비
onMounted(async () => {
  try {
    await checkKakaoReady() // 카카오 sdk를 준비
    const location = await getCurrentLocation() // 현재 사용자의 좌표를 받아옴
    mapCenter.value = location
  } catch (err) {
    mapCenter.value = { lat: 37.566826, lng: 126.9786567 } // fallback
  }

  await nextTick()
  initMap()
  isKakaoReady.value = true
})
</script>
<style scoped>
.search-bank {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 40px 20px;
  /* max-width: 640px; */
  width: 100%;
  margin: 100px;
  background-color: #ffffff;
  border-radius: 24px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.05);
}

.selectors {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-bottom: 32px;
}

.selectors.disabled {
  opacity: 0.6;
  pointer-events: none;
}

select {
  width: 100%;
  padding: 14px 16px;
  font-size: 16px;
  border: 1px solid #d1d5db;
  border-radius: 14px;
  background-color: #f9fafb;
  color: #111827;
  transition:
    border-color 0.2s ease,
    background-color 0.2s ease;
}

select:focus {
  outline: none;
  border-color: #3b82f6;
  background-color: #ffffff;
}

button {
  width: 100%;
  padding: 14px;
  font-size: 16px;
  font-weight: 500;
  border: none;
  border-radius: 14px;
  background-color: #3b82f6;
  color: #ffffff;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

button:hover:not(:disabled) {
  background-color: #2563eb;
}

button:disabled {
  background-color: #cbd5e1;
  cursor: not-allowed;
}

.kakao-map-container {
  width: 700px;
  height: 480px;
  border-radius: 20px;
  background-color: #f1f5f9;
  overflow: hidden;
  border: 1px solid #e5e7eb;
}
</style>

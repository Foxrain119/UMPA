<template>
  <div class="map-wrapper">
    <div id="kakao-map" ref="mapContainer"></div>
    <div v-if="isLoading" class="loading-overlay">
      <div class="loading-spinner"></div>
    </div>
    <!-- 검색 결과 목록 -->
    <div class="search-result-list">
      <div v-if="searchResults.meta?.total_count === 0" class="no-result">
        검색 결과가 없습니다.
      </div>
      <template v-else-if="searchResults.places?.length">
        <div class="result-count">
          총 {{ searchResults.meta.total_count }}개의 결과가 있습니다.
        </div>
        <div v-for="place in searchResults.places" 
             :key="place.id" 
             class="result-item" 
             @click="moveToPlace(place)"
             :class="{ active: selectedPlaceId === place.id }">
          <h4>{{ place.name }}</h4>
          <p class="address">
            <span class="road-address">{{ place.road_address || place.address }}</span>
            <span v-if="place.road_address && place.address" class="jibun-address">
              (지번) {{ place.address }}
            </span>
          </p>
          <p v-if="place.phone" class="phone">📞 {{ place.phone }}</p>
          <p v-if="place.distance" class="distance">
            🚶‍♂️ {{ formatDistance(place.distance) }}
          </p>
          <a :href="place.place_url" 
             target="_blank" 
             class="detail-link"
             @click.stop>
            상세보기 →
          </a>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';

const props = defineProps({
  searchResults: {
    type: Object,
    default: () => ({ places: [] })
  },
  isLoading: {
    type: Boolean,
    default: false
  }
});

const mapContainer = ref(null);
const map = ref(null);
const markers = ref([]);
const infowindows = ref([]);

// 선택된 장소 ID 상태 추가
const selectedPlaceId = ref(null);

// 지도 초기화
const initMap = () => {
  if (window.kakao && window.kakao.maps) {
    const options = {
      center: new window.kakao.maps.LatLng(37.498095, 127.027610),
      level: 3
    };
    map.value = new window.kakao.maps.Map(mapContainer.value, options);
  }
};

// 마커와 인포윈도우 생성
const displayMarkers = () => {
  // 기존 마커와 인포윈도우 제거
  markers.value.forEach(marker => marker.setMap(null));
  infowindows.value.forEach(infowindow => infowindow.close());
  markers.value = [];
  infowindows.value = [];

  // 검색 결과 표시
  props.searchResults.places.forEach((place, index) => {
    const position = new window.kakao.maps.LatLng(place.lat, place.lng);
    
    // 마커 생성
    const marker = new window.kakao.maps.Marker({
      position: position,
      map: map.value
    });

    // 인포윈도우 내용
    const content = `
      <div class="infowindow" style="padding:10px;width:200px;">
        <h5 style="margin:0 0 5px;font-size:14px;">${place.name}</h5>
        <p style="margin:0;font-size:12px;">${place.road_address || place.address}</p>
        ${place.phone ? `<p style="margin:5px 0 0;font-size:12px;">📞 ${place.phone}</p>` : ''}
        <a href="${place.place_url}" target="_blank" style="font-size:12px;color:#0f89ff;">상세보기</a>
      </div>
    `;

    // 인포윈도우 생성
    const infowindow = new window.kakao.maps.InfoWindow({
      content: content,
      removable: true
    });

    // 마커 클릭 이벤트
    window.kakao.maps.event.addListener(marker, 'click', () => {
      infowindows.value.forEach(info => info.close());
      infowindow.open(map.value, marker);
    });

    markers.value.push(marker);
    infowindows.value.push(infowindow);

    // 첫 번째 결과에 대한 인포윈도우 자동 표시
    if (index === 0) {
      infowindow.open(map.value, marker);
      map.value.setCenter(position);
    }
  });

  // 모든 마커가 보이도록 지도 범위 재설정
  if (markers.value.length > 0) {
    const bounds = new window.kakao.maps.LatLngBounds();
    markers.value.forEach(marker => bounds.extend(marker.getPosition()));
    map.value.setBounds(bounds);
  }
};

// 특정 장소로 이동
const moveToPlace = (place) => {
  selectedPlaceId.value = place.id;
  const position = new window.kakao.maps.LatLng(place.lat, place.lng);
  map.value.setCenter(position);
  
  // 해당 마커의 인포윈도우 열기
  const index = props.searchResults.places.findIndex(p => p.id === place.id);
  if (index !== -1) {
    infowindows.value.forEach(info => info.close());
    infowindows.value[index].open(map.value, markers.value[index]);
  }
};

// 거리 포맷팅
const formatDistance = (distance) => {
  const dist = parseInt(distance);
  if (dist < 1000) {
    return `${dist}m`;
  }
  return `${(dist / 1000).toFixed(1)}km`;
};

// 검색 결과 변경 감지
watch(() => props.searchResults, (newResults) => {
  if (newResults.places?.length > 0) {
    displayMarkers();
  }
}, { deep: true });

onMounted(() => {
  // 카카오맵 API가 완전히 로드될 때까지 대기
  const initializeMap = () => {
    if (window.kakao && window.kakao.maps) {
      initMap();
    } else {
      setTimeout(initializeMap, 100);
    }
  };

  initializeMap();
});

defineExpose({
  setCenter: (lat, lng) => {
    if (map.value) {
      const moveLatLon = new window.kakao.maps.LatLng(lat, lng);
      map.value.setCenter(moveLatLon);
    }
  }
});
</script>

<style scoped>
.map-wrapper {
  flex: 1;
  min-height: 600px;
  position: relative;
  display: flex;
}

#kakao-map {
  width: 70%;
  height: 600px;
  border-radius: 8px;
}

.search-result-list {
  width: 30%;
  height: 600px;
  overflow-y: auto;
  padding: 10px;
  background: white;
  border-left: 1px solid #eee;
}

.no-result {
  padding: 20px;
  text-align: center;
  color: #666;
}

.result-count {
  padding: 10px;
  background: #f8f9fa;
  border-bottom: 1px solid #eee;
  font-weight: bold;
}

.result-item {
  padding: 15px;
  border-bottom: 1px solid #eee;
  cursor: pointer;
  transition: background-color 0.2s;
}

.result-item:hover,
.result-item.active {
  background: #f0f7ff;
}

.result-item h4 {
  margin: 0 0 8px;
  font-size: 16px;
  color: #333;
}

.address {
  margin: 0 0 5px;
  font-size: 14px;
  color: #666;
}

.jibun-address {
  display: block;
  font-size: 13px;
  color: #888;
}

.phone {
  margin: 5px 0;
  font-size: 14px;
  color: #444;
}

.distance {
  margin: 5px 0;
  font-size: 14px;
  color: #0f89ff;
}

.detail-link {
  display: inline-block;
  margin-top: 5px;
  color: #0f89ff;
  text-decoration: none;
  font-size: 13px;
}

.detail-link:hover {
  text-decoration: underline;
}

/* 기존 스타일 유지 */
.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.loading-spinner {
  width: 50px;
  height: 50px;
  border: 5px solid #f3f3f3;
  border-top: 5px solid #0f89ff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style> 
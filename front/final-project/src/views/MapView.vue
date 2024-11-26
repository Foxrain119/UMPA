<template>
  <div class="page-container">
    <div class="title-container">
      <h1>주변 은행</h1>
    </div>
    <div class="content-container">
      <div class="map-content">
        <div class="search-section">
          <BankSearchForm 
            @search-banks="searchNearbyBanks"
            :provinces="provinces"
            :districts="districts"
            :banks="banks"
          />
        </div>
        
        <div class="map-section">
          <KakaoMap 
            v-if="isMapReady"
            ref="kakaoMapRef"
            :searchResults="searchResults"
            :isLoading="isLoading"
          />
          <div v-else class="map-loading">
            지도를 불러오는 중...
          </div>
        </div>
      </div>
    </div>
    <br><br><br>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import BankSearchForm from '@/components/map/BankSearchForm.vue';
import KakaoMap from '@/components/map/KakaoMap.vue';

const API_URL = 'http://127.0.0.1:8000'

const provinces = ref([]);
const districts = ref({});
const banks = ref([]);
const kakaoMapRef = ref(null);
const searchResults = ref({ places: [] });
const isLoading = ref(false);
const isMapReady = ref(false);

// 위치 및 은행 정보 가져오기
const fetchLocations = async () => {
  try {
    const response = await axios.get(`${API_URL}/maps/locations/`);
    provinces.value = response.data.provinces;
    districts.value = response.data.districts;
    banks.value = response.data.banks;
  } catch (error) {
    console.error('위치 정보 로드 실패:', error);
  }
};

onMounted(async () => {
  // 위치 및 은행 정보 로드
  await fetchLocations();
  
  // 카카오맵 API가 로드되었는지 확인
  const checkMapLoad = () => {
    if (window.kakao && window.kakao.maps) {
      isMapReady.value = true;
    } else {
      setTimeout(checkMapLoad, 100);
    }
  };
  
  checkMapLoad();
});

// 주변 은행 검색 함수
const searchNearbyBanks = async (searchParams) => {
  try {
    isLoading.value = true;
    const response = await axios({
      method: 'get',
      url: `${API_URL}/maps/search/`,
      params: {
        province: searchParams.province,
        district: searchParams.district,
        bank: searchParams.bank
      }
    });

    searchResults.value = response.data;
  } catch (error) {
    console.error('은행 검색 중 오류 발생:', error);
    window.alert('은행 검색 중 오류가 발생했습니다.');
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped>
.page-container {
  width: 100%;
}

.title-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  justify-content: center;
}

h1 {
  font-size: 2.5rem;
  color: #333;
  font-family: 'S-CoreDream-6Bold';
  position: relative;
  margin: 2rem 0;
  text-align: center;
}

/* h1::after {
  content: '';
  position: absolute;
  bottom: -10px;
  left: 50%;
  transform: translateX(-50%);
  width: 100%;
  height: 3px;
  background-color: #007bff;
} */

.content-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
  border-radius: 15px;
  box-shadow: 5px 5px 10px rgba(109, 106, 106, 0.5);
}

.map-content {
  display: flex;
  gap: 0;
  margin-top: 20px;
  background-color: #fff;
  border-radius: 8px;
  padding: 2rem 0;
}

.search-section {
  flex: 0 0 300px; /* 검색창 너비 고정 */
  background-color: #f8f9fa;
  border-radius: 8px;
  padding: 1.5rem;
  /* margin-right: 2rem; */
}

.map-section {
  flex: 1; /* 남은 공간 모두 차지 */
  min-height: 600px;
  border-radius: 8px;
  overflow: hidden;
}

.map-loading {
  width: 100%;
  height: 100%;
  min-height: 600px;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f8f9fa;
  border-radius: 8px;
  font-size: 1.2rem;
  color: #666;
}

/* 반응형 디자인 */
@media (max-width: 992px) {
  .map-content {
    flex-direction: column;
  }

  .search-section {
    flex: none;
    width: 100%;
  }

  .map-section {
    width: 100%;
  }
}
</style>
<template>
  <div class="map-container">
    <h1>주변 은행 찾기</h1>
    <div class="map-content">
      <BankSearchForm 
        @search-banks="searchNearbyBanks"
        :provinces="provinces"
        :districts="districts"
        :banks="banks"
      />
      
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
.map-container {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.map-content {
  display: flex;
  gap: 20px;
  margin-top: 20px;
}

h1 {
  margin-bottom: 20px;
  color: #333;
}

.map-loading {
  flex: 1;
  min-height: 600px;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f8f9fa;
  border-radius: 8px;
  font-size: 1.2rem;
  color: #666;
}
</style>
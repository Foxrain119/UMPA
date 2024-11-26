<template>
  <div class="search-form">
    <h3>은행 찾기</h3>
    <form @submit.prevent="handleSubmit">
      <!-- 시/도 선택 -->
      <div class="form-group">
        <label for="province">광역시 / 도</label>
        <select 
          id="province" 
          v-model="selectedProvince"
          class="form-select"
        >
          <option value="">선택하세요</option>
          <option v-for="province in provinces" :key="province" :value="province">
            {{ province }}
          </option>
        </select>
      </div>

      <!-- 구/군 선택 -->
      <div class="form-group">
        <label for="district">시 / 군 / 구</label>
        <select 
          id="district" 
          v-model="selectedDistrict"
          class="form-select"
          :disabled="!selectedProvince"
        >
          <option value="">선택하세요</option>
          <option 
            v-for="district in availableDistricts" 
            :key="district" 
            :value="district"
          >
            {{ district }}
          </option>
        </select>
      </div>

      <!-- 은행 선택 -->
      <div class="form-group">
        <label for="bank">은행</label>
        <select 
          id="bank" 
          v-model="selectedBank"
          class="form-select"
        >
          <option value="">전체</option>
          <option 
            v-for="bank in banks" 
            :key="bank.name" 
            :value="bank.name"
          >
            {{ bank.name }}
          </option>
        </select>
      </div>

      <button type="submit" class="search-button">찾기</button>
    </form>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue';

const props = defineProps({
  provinces: {
    type: Array,
    required: true,
    default: () => []
  },
  districts: {
    type: Object,
    required: true,
    default: () => ({})
  },
  banks: {
    type: Array,
    required: true,
    default: () => []
  }
});

const emit = defineEmits(['search-banks']);

const selectedProvince = ref('');
const selectedDistrict = ref('');
const selectedBank = ref('');

const availableDistricts = computed(() => {
  return selectedProvince.value ? props.districts[selectedProvince.value] || [] : [];
});

const handleSubmit = () => {
  // 필수 입력값 검증
  if (!selectedProvince.value) {
    alert('시/도를 선택해주세요.');
    return;
  }
  if (!selectedDistrict.value) {
    alert('시/군/구를 선택해주세요.');
    return;
  }

  emit('search-banks', {
    province: selectedProvince.value,
    district: selectedDistrict.value,
    bank: selectedBank.value
  });
};

// 시/도 선택 시 구/군 초기화
watch(selectedProvince, () => {
  selectedDistrict.value = '';
});

// 디버깅을 위한 props 감시
watch(() => props.provinces, (newVal) => {
  console.log('Provinces updated:', newVal);
}, { immediate: true });

watch(() => props.districts, (newVal) => {
  console.log('Districts updated:', newVal);
}, { immediate: true });

watch(() => props.banks, (newVal) => {
  console.log('Banks updated:', newVal);
}, { immediate: true });
</script>

<style scoped>
.search-form {
  width: 300px;
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 8px;
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
  color: #495057;
}

.form-select {
  width: 100%;
  padding: 8px;
  border: 1px solid #ced4da;
  border-radius: 4px;
  background-color: white;
}

.search-button {
  width: 100%;
  padding: 10px;
  background-color: #0f89ff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
}

.search-button:hover {
  background-color: #0056b3;
}
</style> 
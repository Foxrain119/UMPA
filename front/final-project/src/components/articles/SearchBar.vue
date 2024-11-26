<template>
  <div class="search-container">
    <select v-model="searchType" class="search-select">
      <option value="title">제목</option>
      <option value="title_content">제목+내용</option>
      <option value="user">작성자</option>
    </select>
    <input 
      type="text" 
      v-model="searchKeyword"
      placeholder="검색어를 입력하세요"
      class="search-input"
      @keyup.enter="handleSearch"
    >
    <button @click="handleSearch" class="search-btn">검색</button>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const searchType = ref('title');
const searchKeyword = ref('');

const emit = defineEmits(['search']);

const handleSearch = () => {
  emit('search', {
    type: searchType.value,
    keyword: searchKeyword.value
  });
};
</script>

<style scoped>
.search-container {
  display: flex;
  gap: 10px;
  justify-content: center;
  margin: 20px 0;
}

.search-select {
  padding: 8px;
  border-radius: 4px;
  border: 1px solid #ddd;
}

.search-input {
  padding: 8px;
  width: 300px;
  border-radius: 4px;
  border: 1px solid #ddd;
}

.search-btn {
  padding: 8px 16px;
  background-color: #0f89ff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
</style> 
<template>
  <div class="pagination">
    <button 
      :disabled="currentPage === 1"
      @click="$emit('page-change', currentPage - 1)"
      class="page-btn"
    >
      이전
    </button>
    
    <span class="page-info">
      {{ currentPage }} / {{ totalPages }}
    </span>
    
    <button 
      :disabled="currentPage === totalPages"
      @click="$emit('page-change', currentPage + 1)"
      class="page-btn"
    >
      다음
    </button>
  </div>
</template>

<script setup>
defineProps({
  currentPage: {
    type: Number,
    required: true
  },
  totalPages: {
    type: Number,
    required: true
  }
});

defineEmits(['page-change']);
</script>

<style scoped>
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
  margin: 20px 0;
}

.page-btn {
  padding: 8px 16px;
  border: 1px solid #ddd;
  background-color: white;
  border-radius: 4px;
  cursor: pointer;
}

.page-btn:disabled {
  background-color: #f5f5f5;
  cursor: not-allowed;
}

.page-info {
  font-size: 1rem;
}
</style> 
<template>
  <div class="article-form-overlay">
    <div class="article-form">
      <h3>{{ isEdit ? '글 수정' : '새 글 작성' }}</h3>
      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label for="title">제목</label>
          <input 
            type="text" 
            id="title" 
            v-model="form.title" 
            required
            class="form-control"
          >
        </div>
        
        <div class="form-group">
          <label for="content">내용</label>
          <textarea 
            id="content" 
            v-model="form.content" 
            required
            class="form-control"
            rows="5"
          ></textarea>
        </div>

        <div class="button-group">
          <button type="submit" class="submit-btn">
            {{ isEdit ? '수정' : '작성' }}
          </button>
          <button type="button" @click="$emit('close')" class="cancel-btn">
            취소
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, defineProps, defineEmits } from 'vue';

const props = defineProps({
  article: {
    type: Object,
    default: () => ({})
  },
  isEdit: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['submit', 'close']);

const form = ref({
  title: props.article.title || '',
  content: props.article.content || ''
});

const handleSubmit = () => {
  emit('submit', { ...form.value });
};
</script>

<style scoped>
.article-form-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.article-form {
  max-width: 800px;
  width: 90%;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: white;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
}

.form-control {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.button-group {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
}

.submit-btn, .cancel-btn {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.submit-btn {
  background-color: #0f89ff;
  color: white;
}

.cancel-btn {
  background-color: #6c757d;
  color: white;
}

.submit-btn:hover {
  background-color: #0066cc;
}

.cancel-btn:hover {
  background-color: #5a6268;
}
</style> 
<template>
  <div class="article-detail-overlay">
    <div class="article-detail">
      <div class="detail-header">
        <h3>{{ article.title }}</h3>
        <button @click="$emit('close')" class="close-btn">&times;</button>
      </div>

      <div class="article-info">
        <span>작성자: {{ article.user }}</span>
        <span>작성일: {{ formatDate(article.created_at) }}</span>
      </div>

      <div v-if="!isEditing" class="article-content">
        {{ article.content }}
      </div>

      <div v-else class="article-edit">
        <ArticleForm 
          :article="article"
          :isEdit="true"
          @submit="handleEdit"
          @close="isEditing = false"
        />
      </div>

      <div v-if="isOwner && !isEditing" class="article-actions">
        <button @click="isEditing = true" class="edit-btn">수정</button>
        <button @click="$emit('delete', article.id)" class="delete-btn">삭제</button>
      </div>

      <div class="comments-section">
        <h4>댓글 ({{ article.comment_count || 0 }})</h4>
        <CommentList 
          :comments="article.comment_set"
          :articleId="article.id"
          @refresh="handleRefresh"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue';
import { useAccountStore } from '@/stores/account';
import CommentList from './CommentList.vue';
import ArticleForm from './ArticleForm.vue';
import axios from 'axios';

const props = defineProps({
  article: {
    type: Object,
    required: true
  }
});

const store2 = useAccountStore();

const isOwner = computed(() => {
  return store2.token && store2.profile?.username === props.article.user;
});

const formatDate = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleString('ko-KR', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  });
};

const handleRefresh = async () => {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/articles/${props.article.id}/`);
    if (response.data) {
      console.log('Article detail data:', response.data);
      Object.assign(props.article, response.data);
    }
  } catch (error) {
    console.error('게시글 새로고침 실패:', error);
  }
};

const emit = defineEmits(['close', 'delete', 'refresh']);

const isEditing = ref(false);

const handleEdit = async (formData) => {
  try {
    if (!isOwner.value) {
      alert('본인이 작성한 게시글만 수정할 수 있습니다.');
      return;
    }

    await axios.put(`http://127.0.0.1:8000/articles/${props.article.id}/`, 
      formData,
      {
        headers: { Authorization: `Token ${store2.token}` }
      }
    );
    isEditing.value = false;
    await handleRefresh();
  } catch (error) {
    console.error('게시글 수정 실패:', error);
    if (error.response?.status === 403) {
      alert('본인이 작성한 게시글만 수정할 수 있습니다.');
    } else {
      alert('게시글 수정에 실패했습니다.');
    }
  }
};

onMounted(() => {
  handleRefresh();
});
</script>

<style scoped>
.article-detail-overlay {
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

.article-detail {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  width: 80%;
  max-width: 800px;
  max-height: 80vh;
  overflow-y: auto;
}

.detail-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
}

.article-info {
  color: #666;
  margin-bottom: 20px;
}

.article-info span {
  margin-right: 20px;
}

.article-content {
  margin-bottom: 20px;
  line-height: 1.6;
}

.article-actions {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 20px;
}

.delete-btn {
  background-color: #dc3545;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
}

.edit-btn {
  background-color: #6c757d;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  margin-right: 8px;
}

.edit-btn:hover {
  background-color: #5a6268;
}

.comments-section {
  border-top: 1px solid #ddd;
  padding-top: 20px;
}
</style> 
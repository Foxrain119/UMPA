<template>
  <div class="comment-list">
    <div v-if="store2.token" class="comment-form">
      <textarea 
        v-model="newComment" 
        placeholder="댓글을 입력하세요..."
        class="comment-input"
      ></textarea>
      <button @click="addComment" class="submit-btn">댓글 작성</button>
    </div>
    
    <div v-else class="login-message">
      댓글을 작성하려면 로그인이 필요합니다.
    </div>

    <div v-if="comments && comments.length > 0" class="comments">
      <CommentItem
        v-for="comment in comments"
        :key="comment.id"
        :comment="comment"
        @delete="deleteComment"
        @update="updateComment"
      />
    </div>
    <div v-else class="no-comments">
      작성된 댓글이 없습니다.
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';
import { useAccountStore } from '@/stores/account';
import axios from 'axios';
import CommentItem from './CommentItem.vue';

const props = defineProps({
  comments: {
    type: Array,
    default: () => []
  },
  articleId: {
    type: Number,
    required: true
  }
});

const emit = defineEmits(['refresh']);
const store2 = useAccountStore();
const newComment = ref('');

// comments prop 변경 감지
watch(() => props.comments, (newComments) => {
  console.log('Comments data:', newComments);
}, { immediate: true });

const addComment = async () => {
  if (!newComment.value.trim()) return;
  
  try {
    if (!store2.token) {
      alert('로그인이 필요합니다.');
      return;
    }

    await axios.post(`http://127.0.0.1:8000/articles/${props.articleId}/comments/`, {
      content: newComment.value
    }, {
      headers: { Authorization: `Token ${store2.token}` }
    });
    newComment.value = '';
    emit('refresh');
  } catch (error) {
    console.error('댓글 작성 실패:', error.response?.data || error);
  }
};

const deleteComment = async (commentId) => {
  try {
    if (!store2.token) {
      alert('로그인이 필요합니다.');
      return;
    }

    const comment = props.comments.find(c => c.id === commentId);
    if (comment.user !== store2.profile?.username) {
      alert('본인이 작성한 댓글만 삭제할 수 있습니다.');
      return;
    }

    await axios.delete(`http://127.0.0.1:8000/articles/comments/${commentId}/`, {
      headers: { Authorization: `Token ${store2.token}` }
    });
    emit('refresh');
  } catch (error) {
    if (error.response?.status === 403) {
      alert('본인이 작성한 댓글만 삭제할 수 있습니다.');
    } else {
      alert('댓글 삭제에 실패했습니다.');
    }
    console.error('댓글 삭제 실패:', error);
  }
};

const updateComment = async (commentId, content) => {
  try {
    if (!store2.token) {
      alert('로그인이 필요합니다.');
      return;
    }

    const comment = props.comments.find(c => c.id === commentId);
    if (comment.user !== store2.profile?.username) {
      alert('본인이 작성한 댓글만 수정할 수 있습니다.');
      return;
    }

    await axios.put(`http://127.0.0.1:8000/articles/comments/${commentId}/`, {
      content
    }, {
      headers: { Authorization: `Token ${store2.token}` }
    });
    emit('refresh');
  } catch (error) {
    if (error.response?.status === 403) {
      alert('본인이 작성한 댓글만 수정할 수 있습니다.');
    } else {
      alert('댓글 수정에 실패했습니다.');
    }
    console.error('댓글 수정 실패:', error);
  }
};
</script>

<style scoped>
.comment-list {
  margin-top: 20px;
}

.comment-form {
  margin-bottom: 20px;
}

.comment-input {
  width: 100%;
  min-height: 60px;
  padding: 8px;
  margin-bottom: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  resize: vertical;
}

.submit-btn {
  background-color: #0f89ff;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
}

.submit-btn:hover {
  background-color: #0066cc;
}

.login-message {
  text-align: center;
  color: #666;
  padding: 10px;
  background-color: #f8f9fa;
  border-radius: 4px;
  margin-bottom: 20px;
}

.comments {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.no-comments {
  text-align: center;
  color: #666;
  padding: 20px;
}
</style> 
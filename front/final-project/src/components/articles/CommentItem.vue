<template>
  <div class="comment-item">
    <div class="comment-header">
      <span class="comment-author">{{ comment.user }}</span>
      <span class="comment-date">{{ formatDate(comment.created_at) }}</span>
    </div>

    <div v-if="!isEditing" class="comment-content">
      {{ comment.content }}
    </div>
    
    <div v-else class="comment-edit">
      <textarea 
        v-model="editedContent"
        class="edit-input"
      ></textarea>
    </div>

    <div v-if="isOwner" class="comment-actions">
      <template v-if="!isEditing">
        <button @click="startEdit" class="edit-btn">수정</button>
        <button @click="$emit('delete', comment.id)" class="delete-btn">삭제</button>
      </template>
      <template v-else>
        <button @click="saveEdit" class="save-btn">저장</button>
        <button @click="cancelEdit" class="cancel-btn">취소</button>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useAccountStore } from '@/stores/account';

const props = defineProps({
  comment: {
    type: Object,
    required: true
  }
});

const emit = defineEmits(['delete', 'update']);
const store2 = useAccountStore();

const isEditing = ref(false);
const editedContent = ref(props.comment.content);

const isOwner = computed(() => {
  return store2.token && store2.profile?.username === props.comment.user;
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

const startEdit = () => {
  isEditing.value = true;
  editedContent.value = props.comment.content;
};

const saveEdit = async () => {
  if (!isOwner.value) {
    alert('본인이 작성한 댓글만 수정할 수 있습니다.');
    return;
  }

  if (editedContent.value.trim() !== props.comment.content) {
    emit('update', props.comment.id, editedContent.value);
  }
  isEditing.value = false;
};

const cancelEdit = () => {
  isEditing.value = false;
  editedContent.value = props.comment.content;
};
</script>

<style scoped>
.comment-item {
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: #fff;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
}

.comment-author {
  font-weight: bold;
}

.comment-date {
  color: #666;
  font-size: 0.9em;
}

.comment-content {
  margin-bottom: 8px;
  line-height: 1.4;
}

.comment-edit {
  margin-bottom: 8px;
}

.edit-input {
  width: 100%;
  min-height: 60px;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  resize: vertical;
}

.comment-actions {
  display: flex;
  gap: 8px;
  justify-content: flex-end;
}

.edit-btn, .delete-btn, .save-btn, .cancel-btn {
  padding: 4px 8px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9em;
}

.edit-btn {
  background-color: #6c757d;
  color: white;
}

.delete-btn {
  background-color: #dc3545;
  color: white;
}

.save-btn {
  background-color: #28a745;
  color: white;
}

.cancel-btn {
  background-color: #6c757d;
  color: white;
}

.edit-btn:hover, .save-btn:hover {
  opacity: 0.9;
}

.delete-btn:hover, .cancel-btn:hover {
  opacity: 0.9;
}
</style> 
<template>
  <tr class="article-item">
    <td>{{ index + 1 }}</td>
    <td>
      <a href="#" @click.prevent="$emit('show-detail', article)">
        {{ article.title }}
      </a>
    </td>
    <td>{{ article.user }}</td>
    <td>{{ formatDate(article.created_at) }}</td>
    <td>
      <button 
        @click="$emit('like', article.id)"
        :class="['like-btn', { 'liked': isLiked }]"
      >
        ❤️ {{ article.like_users?.length || 0 }}
      </button>
    </td>
    <td>{{ article.comment_count }}</td>
  </tr>
</template>

<script setup>
import { computed } from 'vue';
import { useAccountStore } from '@/stores/account';

const props = defineProps({
  article: {
    type: Object,
    required: true
  },
  index: {
    type: Number,
    required: true
  }
});

const emit = defineEmits(['show-detail', 'delete', 'like']);
const store2 = useAccountStore();

const isOwner = computed(() => {
  return props.article.user === store2.profile?.username;
});

const isLiked = computed(() => {
  return props.article.like_users?.some(user => user.id === store2.profile?.id);
});

const formatDate = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleDateString('ko-KR', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  });
};
</script>

<style scoped>
.article-item td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

.like-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 5px;
}

.like-btn.liked {
  color: red;
}

.delete-btn {
  background-color: #dc3545;
  color: white;
  border: none;
  padding: 5px 10px;
  border-radius: 4px;
  cursor: pointer;
}

.delete-btn:hover {
  background-color: #c82333;
}

a {
  color: #0f89ff;
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}
</style> 
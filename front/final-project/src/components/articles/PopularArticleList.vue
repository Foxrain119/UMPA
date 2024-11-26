<template>
  <div class="popular-articles" v-if="popularArticles.length">
    <h3 class="popular-title">🔥 금주의 인기 게시글 🔥</h3>
    <div class="popular-list">
      <div v-for="(article, index) in popularArticles" 
           :key="article.id" 
           class="popular-item"
           @click="handleArticleClick(article)"
      >
        <span class="rank">{{ index + 1 }}</span>
        <div class="article-info">
          <span class="article-title">
            {{ article.title }}
          </span>
          <div class="article-meta">
            <span>👤 {{ article.user }}</span>
            <span>❤️ {{ article.like_users?.length || 0 }}</span>
            <span>📅 {{ formatDate(article.created_at) }}</span>
          </div>
        </div>
      </div>
    </div>

    <ArticleDetail
      v-if="selectedArticle"
      :article="selectedArticle"
      @close="selectedArticle = null"
      @delete="handleDelete"
      @refresh="$emit('refresh')"
    />
  </div>
</template>

<script setup>
import { computed, ref } from 'vue';
import ArticleDetail from './ArticleDetail.vue';

const props = defineProps({
  articles: {
    type: Array,
    required: true
  }
});

const emit = defineEmits(['refresh']);

const selectedArticle = ref(null);

const popularArticles = computed(() => {
  const sevenDaysAgo = new Date();
  sevenDaysAgo.setDate(sevenDaysAgo.getDate() - 7);

  return props.articles
    .filter(article => new Date(article.created_at) >= sevenDaysAgo)
    .sort((a, b) => (b.like_users?.length || 0) - (a.like_users?.length || 0))
    .slice(0, 5);
});

const handleArticleClick = (article) => {
  selectedArticle.value = article;
};

const handleDelete = () => {
  selectedArticle.value = null;
  emit('refresh');
};

const formatDate = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleDateString('ko-KR', {
    month: 'short',
    day: 'numeric'
  });
};
</script>

<style scoped>
.popular-articles {
  background-color: #f8f9fa;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 24px;
}

.popular-title {
  font-size: 1.2rem;
  margin-bottom: 12px;
  color: #343a40;
}

.popular-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.popular-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px;
  background-color: white;
  border-radius: 4px;
  transition: transform 0.2s;
  cursor: pointer;
}

.popular-item:hover {
  transform: translateX(4px);
  background-color: #f1f3f5;
}

.rank {
  font-size: 1.2rem;
  font-weight: bold;
  color: #0f89ff;
  min-width: 24px;
}

.article-info {
  flex: 1;
}

.article-title {
  color: #343a40;
  font-weight: 500;
  display: block;
  margin-bottom: 4px;
}

.article-meta {
  display: flex;
  gap: 12px;
  font-size: 0.9rem;
  color: #6c757d;
}
</style> 
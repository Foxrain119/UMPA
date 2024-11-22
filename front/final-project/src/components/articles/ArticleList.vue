<template>
  <div class="article-list">
    <table class="table">
      <thead>
        <tr>
          <th>번호</th>
          <th>제목</th>
          <th>작성자</th>
          <th>작성일</th>
          <th>좋아요</th>
          <th>댓글</th>
          <th>관리</th>
        </tr>
      </thead>
      <tbody>
        <ArticleItem
          v-for="article in articles"
          :key="article.id"
          :article="article"
          @show-detail="showDetail"
          @delete="$emit('delete', $event)"
          @like="$emit('like', $event)"
        />
      </tbody>
    </table>

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
import { ref } from 'vue';
import ArticleItem from './ArticleItem.vue';
import ArticleDetail from './ArticleDetail.vue';

const props = defineProps({
  articles: {
    type: Array,
    required: true
  }
});

const emit = defineEmits(['delete', 'like', 'refresh']);
const selectedArticle = ref(null);

const showDetail = (article) => {
  selectedArticle.value = article;
};

const handleDelete = (articleId) => {
  selectedArticle.value = null;
  emit('delete', articleId);
};
</script>

<style scoped>
.article-list {
  width: 100%;
  margin-top: 20px;
}

.table {
  width: 100%;
  border-collapse: collapse;
}

.table th {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #ddd;
  background-color: #f8f9fa;
  font-weight: bold;
}
</style> 
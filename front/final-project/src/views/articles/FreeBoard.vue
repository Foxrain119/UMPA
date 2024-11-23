<template>
  <div class="free-board">
    <div class="board-header">
      <h2>자유게시판</h2>
      <button v-if="store2.token" @click="showWriteForm = true" class="write-btn">
        글쓰기
      </button>
    </div>

    <ArticleForm 
      v-if="showWriteForm" 
      @close="showWriteForm = false"
      @submit="handleSubmit"
    />

    <ArticleList 
      v-if="articles.length > 0"
      :articles="articles" 
      @delete="handleDelete"
      @like="handleLike"
      @refresh="fetchArticles"
    />
    <div v-else-if="!isLoading" class="no-articles">
      게시글이 없습니다.
    </div>
    <div v-else class="loading">
      로딩 중...
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useAccountStore } from '@/stores/account';
import ArticleForm from '@/components/articles/ArticleForm.vue';
import ArticleList from '@/components/articles/ArticleList.vue';
import axios from 'axios';

const store2 = useAccountStore();
const articles = ref([]);
const showWriteForm = ref(false);
const isLoading = ref(false);

const fetchArticles = async () => {
  try {
    isLoading.value = true;
    const response = await axios.get('http://127.0.0.1:8000/articles/');
    console.log('Article data:', response.data);
    articles.value = response.data;
  } catch (error) {
    console.error('게시글 로딩 실패:', error);
  } finally {
    isLoading.value = false;
  }
};

const handleSubmit = async (articleData) => {
  try {
    const { title, content } = articleData;
    
    const response = await axios.post('http://127.0.0.1:8000/articles/', 
      { title, content }, 
      {
        headers: { 
          Authorization: `Token ${store2.token}`
        }
      }
    );
    
    if (response.status === 201) {  // 성공적으로 생성됨
      showWriteForm.value = false;
      await fetchArticles();
    }
  } catch (error) {
    console.error('게시글 작성 실패:', error.response?.data || error);
    if (error.response?.status === 401) {
      alert('로그인이 필요합니다.');
    } else {
      alert('게시글 작성에 실패했습니다.');
    }
  }
};

const handleDelete = async (articleId) => {
  try {
    if (!store2.token) {
      alert('로그인이 필요합니다.');
      return;
    }

    await axios.delete(`http://127.0.0.1:8000/articles/${articleId}/`, {
      headers: { Authorization: `Token ${store2.token}` }
    });
    await fetchArticles();
  } catch (error) {
    if (error.response?.status === 403) {
      alert('본인이 작성한 게시글만 삭제할 수 있습니다.');
    } else {
      alert('게시글 삭제에 실패했습니다.');
    }
    console.error('게시글 삭제 실패:', error);
  }
};

const handleLike = async (articleId) => {
  try {
    if (!store2.token) {
      alert('로그인이 필요합니다.');
      return;
    }
    
    await axios.post(`http://127.0.0.1:8000/articles/${articleId}/likes/`, null, {
      headers: { Authorization: `Token ${store2.token}` }
    });
    await fetchArticles();  // 게시글 목록 새로고침
  } catch (error) {
    console.error('좋아요 실패:', error.response?.data || error);
  }
};

onMounted(fetchArticles);
</script>

<style scoped>
.free-board {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.board-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.write-btn {
  background-color: #0f89ff;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
}

.write-btn:hover {
  background-color: #0066cc;
}
</style> 
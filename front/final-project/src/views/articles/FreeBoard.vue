<template>
  <div class="free-board">
    <div class="board-header">
      <h2>금융 팁이 있다면 공유해보세요!</h2>
      <button v-if="store2.token" @click="showArticleForm" class="write-btn">
        글쓰기
      </button>
    </div>

    <PopularArticleList 
      :articles="articles" 
      @refresh="fetchArticles"
    />

    <div class="article-list">
      <ArticleList 
        :articles="paginatedArticles" 
        @delete="handleDelete"
        @like="handleLike"
      />
    </div>

    <Pagination 
      :current-page="currentPage"
      :total-pages="totalPages"
      @page-change="handlePageChange"
    />

    <SearchBar @search="handleSearch" />

    <!-- ArticleForm 조건부 렌더링 -->
    <ArticleForm
      v-if="isWriting"
      :article="{}"
      :isEdit="false"
      @submit="handleSubmit"
      @close="isWriting = false"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAccountStore } from '@/stores/account';
import axios from 'axios';
import ArticleList from '@/components/articles/ArticleList.vue';
import Pagination from '@/components/articles/Pagination.vue';
import SearchBar from '@/components/articles/SearchBar.vue';
import ArticleForm from '@/components/articles/ArticleForm.vue';
import PopularArticleList from '@/components/articles/PopularArticleList.vue';

const router = useRouter();
const store2 = useAccountStore();

const articles = ref([]);
const currentPage = ref(1);
const itemsPerPage = 10;
const searchResults = ref(null);
const isWriting = ref(false);

// 검색 결과나 전체 게시글 중 표시할 데이터 선택
const displayedArticles = computed(() => {
  return searchResults.value || articles.value;
});

// 현재 페이지에 표시할 게시글
const paginatedArticles = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage;
  const end = start + itemsPerPage;
  return displayedArticles.value.slice(start, end);
});

// 전체 페이지 수 계산
const totalPages = computed(() => {
  return Math.ceil(displayedArticles.value.length / itemsPerPage);
});

const fetchArticles = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/articles/');
    articles.value = response.data;
  } catch (error) {
    console.error('게시글 목록 조회 실패:', error);
  }
};

// 글쓰기 버튼 클릭 핸들러 수정
const showArticleForm = () => {
  if (!store2.token) {
    alert('로그인이 필요합니다.');
    return;
  }
  isWriting.value = true;
};

// 글 작성 제출 핸들러 추가
const handleSubmit = async (formData) => {
  try {
    await axios.post('http://127.0.0.1:8000/articles/', formData, {
      headers: { Authorization: `Token ${store2.token}` }
    });
    isWriting.value = false;
    await fetchArticles();
  } catch (error) {
    console.error('게시글 작성 실패:', error);
    alert('게시글 작성에 실패했습니다.');
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
    await fetchArticles();
  } catch (error) {
    console.error('좋아요 실패:', error.response?.data || error);
  }
};

const handlePageChange = (page) => {
  currentPage.value = page;
};

const handleSearch = async ({ type, keyword }) => {
  if (!keyword.trim()) {
    searchResults.value = null;
    currentPage.value = 1;
    await fetchArticles();
    return;
  }

  try {
    const response = await axios.get(`http://127.0.0.1:8000/articles/search/`, {
      params: {
        type,
        keyword
      }
    });
    searchResults.value = response.data;
    currentPage.value = 1; // 검색 시 첫 페이지로 이동
  } catch (error) {
    console.error('검색 실패:', error);
    alert('검색에 실패했습니다.');
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

.article-list {
  margin-bottom: 20px;
}
</style> 
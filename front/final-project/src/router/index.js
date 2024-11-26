import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import FinanceView from '@/views/FinanceView.vue'
import ExchangeView from '@/views/ExchangeView.vue'
import MapView from '@/views/MapView.vue'
import ArticleView from '@/views/ArticleView.vue'
import ProfileView from '@/views/ProfileView.vue'
import SignUpView from '@/views/SignUpView.vue'
import LoginView from '@/views/LoginView.vue'
import SearchProductsView from '@/views/finance/SearchProductsView.vue'
import SearchDepositsView from '@/views/finance/SearchDepositsView.vue'
import SearchSavingView from '@/views/finance/SearchSavingView.vue'
import CommendProductsView from '@/views/finance/RecommendProductsView.vue'
import RecommendProductsView from '@/views/finance/RecommendProductsView.vue'
import ProductDetailView from '@/views/finance/ProductDetailView.vue'
import RecommendProductsAlgo1View from '@/views/finance/RecommendProductsAlgo1View.vue'
import RecommendProductsAlgo2View from '@/views/finance/RecommendProductsAlgo2View.vue'
import FreeBoard from '@/views/articles/FreeBoard.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignUpView,
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
    },
    {
      path: '/finance',
      name: 'finance',
      component: FinanceView,
      children: [
        {
          path: '/search_products',
          name: 'search_products',
          component: SearchProductsView,
          children: [
            {
              path: '/deposit',
              name: 'deposit',
              component: SearchDepositsView,
            },
            {
              path: '/saving',
              name: 'saving',
              component: SearchSavingView,
            }
          ],
          redirect: '/deposit'
        },
        {
          path: '/detail',
          name: 'detail',
          component: ProductDetailView,
        },
        {
          path: '/recommend_products',
          name: 'recommend_products',
          component: RecommendProductsView,
          children: [
            {
              path: '/algo1',
              name: 'algo1',
              component: RecommendProductsAlgo1View,
            },
            {
              path: '/algo2',
              name: 'algo2',
              component: RecommendProductsAlgo2View
            },
          ]
        },
      ]
    },
    {
      path: '/exchange',
      name: 'exchange',
      component: ExchangeView,
    },
    {
      path: '/map',
      name: 'map',
      component: MapView,
    },
    {
      path: '/articles',
      name: 'articles',
      component: ArticleView,
      children: [
        {
          path: 'free',
          name: 'free-board',
          component: FreeBoard
        }
        // 추후 다른 게시판 추가 가능
      ]
    },
    {
      path: '/profile',
      name: 'profile',
      component: ProfileView,
    },

    // Finance
    
    
  ],
})

export default router

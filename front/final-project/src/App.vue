<template>
  <div class="nav-container">
    <nav class="navbar">
      <div>
        <router-link :to="{ name: 'home' }">home</router-link> |
        <router-link :to="{ name: 'deposit' }">예적금 비교</router-link> |
        <router-link :to="{ name: 'exchange' }">환율 계산</router-link> |
        <router-link :to="{ name: 'map' }">주변 은행</router-link> |
        <router-link :to="{ name: 'articles' }">커뮤니티</router-link>
      </div>
      <div class="user-bar">
        <router-link :to="{ name: 'login' }" v-show="!store2.token">
          <button class="login-btn">로그인</button>
        </router-link>
        <router-link :to="{ name: 'signup' }" v-show="!store2.token">
          <button class="signup-btn">회원가입</button>
        </router-link>
        <router-link :to="{ name: 'profile' }" v-show="store2.token">
          <button class="">프로필</button>
        </router-link>
        <button v-show="store2.token" @click.prevent="logOut">로그아웃</button>
      </div>
    </nav>
  </div>
  <router-view></router-view>
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router';
import { useAccountStore } from './stores/account';
import { useFinanceStore } from '@/stores/finance';
import { onMounted } from 'vue';

const store = useFinanceStore()
const store2 = useAccountStore(0)

const logOut = function () {
  store2.logOut()
}

onMounted(() => {
  store.getProducts()
  store.getExchages()
  store2.getUserInfo()
})
</script>

<style scoped>
a {
  text-decoration: none;
  color: black;
}
button {
  margin: 0px 3px;
  border: 1px solid rgb(15, 137, 255);
  border-radius: 8%;
  font-size: 15px;
}
.login-btn {
  background-color: white;
  color: rgb(15, 137, 255);
}
.signup-btn {
  background-color: rgb(15, 137, 255);
  color: white;
}
.nav-container {
  border: 0px;
  border-bottom: 5px solid rgb(15, 137, 255);
  padding: 20px;
  position: sticky;
}
.navbar {
  display: flex;
  justify-content: space-between;
}
.user-bar {
  display: inline-block;
}
</style>
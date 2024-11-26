<template>
  <div class="nav-container">
    <nav class="navbar">
      <div>
        <router-link :to="{ name: 'home' }">
          <img class="logo" :src="logo" alt="logo">
        </router-link>
        <router-link class="menu" :to="{ name: 'deposit' }">예적금 상품</router-link>
        <router-link class="menu" :to="{ name: 'exchange' }">환율 계산</router-link>
        <router-link class="menu" :to="{ name: 'map' }">주변 은행</router-link>
        <router-link class="menu" :to="{ name: 'free-board' }">커뮤니티</router-link>
      </div>
      <div class="user-bar">
        <span v-show="store2.token && store2.profile">
          {{ store2.profile?.nickname }}님, 환영합니다! &nbsp;
        </span>
        <router-link :to="{ name: 'login' }" v-show="!store2.token">
          <button class="login-btn">로그인</button>
        </router-link>
        <router-link :to="{ name: 'signup' }" v-show="!store2.token">
          <button>회원가입</button>
        </router-link>
        <router-link :to="{ name: 'profile' }" v-show="store2.token">
          <button class="profile-btn">프로필</button>
        </router-link>
        <button class="signup-btn" v-show="store2.token" @click.prevent="logOut">로그아웃</button>
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
const store2 = useAccountStore()

const logo = store2.images.logo

const logOut = function () {
  store2.logOut()
}

onMounted(() => {
  store.getProducts()
  store.getExchages()
  store2.getUserInfo()
  store2.getStaticFiles()
})

</script>

<style scoped>
a {
  text-decoration: none;
  color: black;
  font-size: 18px;
}
button {
  width: 80px;
  height: 30px;
  margin: 0px 3px;
  padding: 0;
  border: 1px solid rgb(15, 137, 255);
  border-radius: 8%;
  font-size: 15px;
  background-color: rgb(15, 137, 255);
  color: white;
}
.logo {
  width: 100px;
  margin: 0 25px;
}
.menu {
  font-size: 18px;
  padding-right: 20px;
}
.login-btn {
  background-color: white;
  color: rgb(15, 137, 255);
}

.profile-btn {
  /* border: 1px solid rgb(192, 224, 255); */
  background-color: white;
  color: black;
}
.nav-container {
  min-width: 900px;
  border: 0px;
  /* border-bottom: 5px solid rgb(12, 190, 245); */
  /* border-bottom: 5px solid rgb(82, 82, 82); */
  padding: 5px 0px;
  position: sticky;
}
.navbar {
  display: flex;
  justify-content: space-between;
  padding: 0;
}
.user-bar {
  display: inline-block;
}
</style>
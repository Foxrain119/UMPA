<template>
  <div>
    <h1>로그인 페이지</h1>
    <form @submit.prevent="logIn">
      <label for="email">이메일 : </label>
      <input type="text" id="email" v-model="email"><br>

      <label for="password">비밀번호 : </label>
      <input type="password" id="password" v-model="password"><br>

      <input type="submit" value="logIn">
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAccountStore } from '@/stores/account';

const email = ref(null)
const password = ref(null)

const store2 = useAccountStore()

const logIn = function () {
  const payload = {
    email: email.value,
    password: password.value
  }
  store2.logIn(payload)
}
</script>

<style scoped>

</style>
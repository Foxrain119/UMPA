<template>
  <div>
    <h1>회원 가입 페이지</h1>
    <form @submit.prevent="signUp">
      <label for="username">아이디 : </label>
      <input type="text" id="username" v-model.trim="username"><br>

      <label for="password1">비밀번호 : </label>
      <input type="password" id="password1" v-model.trim="password1"><br>

      <label for="password2">비밀번호 확인 : </label>
      <input type="password" id="password2" v-model.trim="password2"><br>
      
      <input type="submit" value="SignUp">
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useFinanceStore } from '@/stores/finance';

const username = ref(null)
const password1 = ref(null)
const password2 = ref(null)

const store = useFinanceStore()

const signUp = function () {
  const payload = {
    username: username.value,
    password1: password1.value,
    password2: password2.value
  }
  store.signUp(payload)
}
</script>

<style scoped>

</style>
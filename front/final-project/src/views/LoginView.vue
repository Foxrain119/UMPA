<template>
  <div class="login-box">
    <h1>로그인</h1>
    <form @submit.prevent="logIn">
      <label for="email">이메일 : </label>
      <input type="text" id="email" v-model="email"><br>

      <label for="password">비밀번호 : </label>
      <input type="password" id="password" v-model="password"><br>

      <input type="submit" value="logIn" class="login">
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
h1 {
  font-family: 'Freesentation-7Bold';
}
label {
  width: 120px;
}
input {
  width: 500px;
  margin: 10px 0;
  border: 1px solid rgb(240, 240, 240);
  border-radius: 8px;
  box-shadow: 3px 3px 4px rgba(192, 192, 192, 0.5);
}

.login-box {
  margin: 40px 100px;
}
.login {
  width:  620px;
  background-color: antiquewhite;
}
.login:hover {
  background-color: rgb(218, 184, 139);
}
</style>
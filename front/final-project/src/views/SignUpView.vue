<template>
  <div class="signup-box">
    <h1>회원 가입</h1>
    <br>
    <form @submit.prevent="signUp">
      <label for="username">이름 : </label>
      <input type="text" id="username" v-model.trim="username"><br>
      
      <label for="nickname">닉네임 : </label>
      <input type="text" id="nickname" v-model.trim="nickname"><br>
      
      <label for="email">이메일 : </label>
      <input type="text" id="email" v-model.trim="email"><br>

      <label for="password1">비밀번호 : </label>
      <input type="password" id="password1" v-model.trim="password1"><br>

      <label for="password2">비밀번호 확인 : </label>
      <input type="password" id="password2" v-model.trim="password2"><br>

      <label for="phone">연락처 : </label>
      <input type="text" id="phone" v-model.trim="phone"><br>
      
      <label for="age">나이 : </label>
      <input type="number" id="age" v-model.trim="age"><br>
      <br>
      <input type="submit" value="SignUp" class="signup">
    </form>
    <!-- <form @submit.prevent="signUp">
      <label for="username">아이디 : </label>
      <input type="text" id="username" v-model.trim="username"><br>

      <label for="password1">비밀번호 : </label>
      <input type="password" id="password1" v-model.trim="password1"><br>

      <label for="password2">비밀번호 확인 : </label>
      <input type="password" id="password2" v-model.trim="password2"><br>
      
      <input type="submit" value="SignUp">
    </form> -->
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAccountStore } from '@/stores/account';

const username = ref(null)
const password1 = ref(null)
const password2 = ref(null)
const email = ref(null)
const phone = ref(null)
const age = ref(null)
const nickname = ref(null)

const store2 = useAccountStore()

const signUp = function () {
  const payload = {
    username: username.value,
    password1: password1.value,
    password2: password2.value,
    email: email.value,
    phone: phone.value,
    age: age.value,
    nickname: nickname.value
  }
  store2.signUp(payload)
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
.signup-box {
  width: 700px;
  margin: 40px 100px;
}
.signup {
  width:  620px;
  background-color: antiquewhite;
}
.signup:hover {
  background-color: rgb(218, 184, 139);
}
</style>
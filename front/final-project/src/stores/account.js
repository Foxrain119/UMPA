import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useAccountStore = defineStore('account', () => {
  const API_URL = 'http://127.0.0.1:8000'
  const token = ref(null)
  const router = useRouter()

  const userInfo = ref([])

  const getUserInfo = function () {
    axios({
      method: 'get',
      url: `${API_URL}/profile/user_info/`,
      headers: {
        Authorization: `Token ${token}`
      }
    })
    .then(res => {
      console.log(res.data)
      userInfo.value = res.data
    })
    .catch(err => console.log(err))
  }

  const signUp = function (payload) {
    const { username, password1, password2, nickname, age } = payload

    axios({
      method: 'post',
      url: `${API_URL}/accounts/signup/`,
      data: {
        username, password1, password2, nickname, age
      }
    })
      .then(res => {
        console.log('회원가입이 완료되었습니다.')
        const password = password1
        logIn({ username, password })
        router.push({ name: 'home' })
      })
      .catch(err => console.log(err))
  }

  const logIn = function (payload) {
    const username = payload.username
    const password = payload.password
    axios({
      method: 'post',
      url: `${API_URL}/accounts/login/`,
      data: {
        username, password
      }
    })
     .then(res => {
      console.log('로그인이 완료되었습니다.')
      console.log(res.data)
      token.value = res.data.key
      router.push({ name: 'home' })
     })
     .catch(err => console.log(err))
  }

  const isLogin = computed(() => {
    if (token.value === null) {
      return false
    } else {
      return true
    }
  })

  const logOut = function () {
    token.value = null
    router.push({ name: 'home' })
  }

  return { token, userInfo, getUserInfo, signUp, logIn, isLogin, logOut }
}, { persist: true })
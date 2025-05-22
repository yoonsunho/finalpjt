import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

export const useAccountStore = defineStore(
  'account',
  () => {
    const ACCOUNT_API_URL = 'http://127.0.0.1:8000/accounts'
    const router = useRouter()
    const token = ref('')

    const isLogin = computed(() => {
      return token.value ? true : false
    })

    // 회원가입
    const signUp = function (payload) {
      console.log(payload)
      const {
        email,
        nickname,
        password1,
        password2,
        gender,
        salary,
        wealth,
        tendency,
        deposit_amount,
        deposit_period,
      } = payload
      axios({
        method: 'POST',
        url: `${ACCOUNT_API_URL}/signup/`,
        data: {
          email,
          nickname,
          password1,
          password2,
          gender,
          salary,
          wealth,
          tendency,
          deposit_amount,
          deposit_period,
        },
      })
        .then((res) => {
          console.log('✅ 회원가입 성공:', res.data)
          router.push({ name: 'LoginView' })
          // loginUser({ email, password: payload.password1 });
        })
        .catch((err) => {
          console.error('❌ 회원가입 실패:', err.response?.data || err)

          throw err
        })
    }

    // 로그인
    const logIn = function ({ email, password }) {
      axios({
        method: 'POST',
        url: `${ACCOUNT_API_URL}/login/`,
        data: {
          email,
          password,
        },
      })
        .then((res) => {
          console.log(res.data)
          console.log('로그인 성공')
          token.value = res.data.key
          router.push({ name: 'MainPage' })
        })
        .catch((err) => {
          console.error('❌ 로그인 실패:', err.response?.data || err)

          throw err
        })
    }

    //  로그아웃
    const logOut = function () {
      token.value = ''
      console.log('로그아웃 되었습니다.')
      router.push({ name: 'MainPage' })
    }

    // 현재 유저 정보
    const userInfo = ref(null)

    const fetchUserInfo = function () {
      axios({
        method: 'GET',
        url: `${ACCOUNT_API_URL}/user/`,
        headers: {
          Authorization: `Token ${token.value}`,
        },
      })
        .then((res) => {
          userInfo.value = res.data
          console.log('✅ 유저 정보:', res.data)
        })
        .catch((err) => {
          console.error('유저 정보를 불러오지 못했습니다', err)
        })
    }

    return {
      signUp,
      logIn,
      logOut,
      token,
      isLogin,
      userInfo,
      fetchUserInfo,
    }
  },
  { persist: true },
)

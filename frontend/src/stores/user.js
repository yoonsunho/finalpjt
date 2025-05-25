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
        })
        .catch((err) => {
          console.error('❌ 회원가입 실패:', err.response?.data || err)
        })
    }

    const logIn = async function ({ email, password }) {
      try {
        const res = await axios({
          method: 'POST',
          url: `${ACCOUNT_API_URL}/login/`,
          data: { email, password },
        })
        console.log(res.data)
        token.value = res.data.key
        await fetchUserInfo() // 로그인 성공 후 사용자 정보 가져오기
        router.push({ name: 'MainPage' })
      } catch (err) {
        console.error('❌ 로그인 실패:', err.response?.data || err)
        throw err
      }
    }

    const logOut = function () {
      axios({
        method: 'POST',
        url: `${ACCOUNT_API_URL}/logout/`,
      })
        .then((res) => {
          token.value = null
          router.push({ name: 'MainPage' })
        })
        .catch((err) => console.log(err))
    }

    const userInfo = ref(null)

    const fetchUserInfo = async function () {
      try {
        const res = await axios({
          method: 'GET',
          url: `${ACCOUNT_API_URL}/myprofile/`,
          headers: {
            Authorization: `Token ${token.value}`,
          },
        })
        console.log('사용자 정보 응답:', res.data)
        userInfo.value = res.data
        return res.data
      } catch (err) {
        console.error('유저 정보를 불러오지 못했습니다', err.response?.data || err)
        throw err
      }
    }

    return {
      signUp,
      logIn,
      logOut,
      token,
      isLogin,
      ACCOUNT_API_URL,
      userInfo,
      fetchUserInfo,
    }
  },
  { persist: true },
)

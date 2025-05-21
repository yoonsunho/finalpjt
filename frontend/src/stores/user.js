import { defineStore } from "pinia";
import { ref, computed } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";

export const useAccountStore = defineStore("account", () => {
    const ACCOUNT_API_URL = "http://127.0.0.1:8000/accounts";
    const router = useRouter();
    const token = ref('');

    const isLogin = computed(()=>{
      return token.value ? true : false
    })

    const signUp = function (payload) {
      console.log(payload)
      const {
        email, nickname, password1, password2,
        gender, salary, wealth, tendency,
        deposit_amount, deposit_period
      } = payload
      axios({
        method: "POST",
        url: `${ACCOUNT_API_URL}/signup/`,
        data: {
          email, nickname, password1, password2,
          gender, salary, wealth, tendency,
          deposit_amount, deposit_period,
        }
      })
      .then((res) => {
        console.log("✅ 회원가입 성공:", res.data);
        // loginUser({ email, password: payload.password1 });
      })
      .catch((err) => {
        console.error("❌ 회원가입 실패:", err.response?.data || err);
        
        throw err;
      });
    };

   const logIn = function ({email,password}){
    axios({
      method: 'POST',
      url: `${ACCOUNT_API_URL}/login/`,
      data:{
        email, password
      }
    })
    .then(res=>{
      console.log(res.data)
      token.value = res.data.key
      router.push({name:'MainPage'})
    })
    .catch(err => console.log(err))
   }

    return {
      signUp, logIn,
      token, isLogin
    };
  },
  { persist: true }
);

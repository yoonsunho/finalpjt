import { defineStore } from "pinia";
import { ref, computed } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";

export const useUserStore = defineStore(
  "user",
  () => {
    const API_URL = "http://127.0.0.1:8000/api";
    const router = useRouter();
    const token = ref(null);

    const createUser = function (payload) {
      const {
        username, email, nickname, password1, password2,
        gender, salary, wealth, tendency,
        deposit_amount, deposit_period
      } = payload;

      return axios({
        method: "post",
        url: `${API_URL}/dj-rest-auth/registration/`,
        data: {
          username, email, nickname, password1, password2,
          gender, salary, wealth, tendency,
          deposit_amount, deposit_period,
        },
      })
        .then((res) => {
          console.log("✅ 회원가입 성공:", res.data);
          loginUser({ email, password: payload.password1 });
        })
        .catch((err) => {
          console.error("❌ 회원가입 실패:", err.response?.data || err);
          throw err;
        });
    };

   

    return {
      createUser, 
      token,
    };
  },
  { persist: true }
);

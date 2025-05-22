<template>
  <div class="login-wrapper">
    <div class="login-container">
      <h2>로그인</h2>
      <!-- <div v-if="successMessage" class="success-message">
        {{ successMessage }}
      </div> -->
      <form @submit.prevent="onLogIn">
        <div class="form-group">
          <label for="email">이메일</label>
          <input type="email" id="email" v-model="email" required>
          <!-- <div v-if="errors.email" class="error">{{ errors.email }}</div> -->
        </div>

        <div class="form-group">
          <label for="password">비밀번호</label>
          <input type="password" id="password" v-model="password" required>
          <!-- <div v-if="errors.password" class="error">{{ errors.password }}</div> -->
        </div>

        <button type="submit">로그인</button>
        <!-- <div v-if="errors.non_field_errors" class="error general-error">
          {{ errors.non_field_errors }}
        </div> -->
      </form>
      
      <!-- <div class="signup-link">
        계정이 없으신가요? <router-link :to="{name:'SignUpView'}">회원가입</router-link>
      </div>
      -->
      <!-- <div v-if="tokenInfo" class="token-info">
        <h3>토큰 정보</h3>
        <pre>{{ tokenInfo }}</pre>
      </div> -->
    </div>
  </div>
</template>

<script setup>
  import { ref } from 'vue';
  import { useAccountStore } from '@/stores/user';

  const accountStore = useAccountStore()

  const email = ref('')
  const password = ref('')
  const onLogIn = function(){
    const userInfo ={
      email: email.value,
      password  : password.value
    }
    accountStore.logIn(userInfo)
  }

// import axios from 'axios';

// export default {
//   name: 'Login',
//   data() {
//     return {
//       formData: {
//         email: '',
//         password: ''
//       },
//       errors: {},
//       isSubmitting: false,
//       tokenInfo: null,
//       successMessage: ''
//     };
//   },
//   created() {
//     const params = new URLSearchParams(window.location.search);
//     this.successMessage = params.get('message') || '';
//   },
//   methods: {
//     async submitForm() {
//       this.isSubmitting = true;
//       this.errors = {};
//       this.tokenInfo = null;
      
//       try {
//         const response = await axios.post('/api/dj-rest-auth/login/', {
//           email: this.formData.email,
//           password: this.formData.password
//         });
        
//         console.log('로그인 성공:', response.data);
//         localStorage.setItem('token', response.data.key);
        
//         this.tokenInfo = {
//           token: response.data.key,
//           timestamp: new Date().toLocaleString()
//         };
//         axios.defaults.headers.common['Authorization'] = `Token ${response.data.key}`;
//         this.getUserInfo();
        
//         this.successMessage = '로그인에 성공했습니다.';
//       } catch (error) {
//         console.error('로그인 실패:', error);
        
//         if (error.response && error.response.data) {
//           this.errors = error.response.data;
//         } else {
//           this.errors = { non_field_errors: ['로그인 중 오류가 발생했습니다. 다시 시도해주세요.'] };
//         }
//       } finally {
//         this.isSubmitting = false;
//       }
//     },
//     async getUserInfo() {
//       try {
//         const response = await axios.get('/api/dj-rest-auth/user/');
//         console.log('사용자 정보:', response.data);
//       } catch (error) {
//         console.error('사용자 정보 가져오기 실패:', error);
//       }
//     }
//   }
// };
</script>

<style scoped>
.login-wrapper {

}

.login-container {
  max-width: 400px;
  margin: 0 auto;
  padding: 40px;
  background-color: #ffffff;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

h2 {
  text-align: center;
  margin-bottom: 30px;
  font-size: 24px;
  font-weight: 600;
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #333;
}

input {
  width: 100%;
  padding: 12px 14px;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 14px;
  transition: border 0.2s;
}

input:focus {
  outline: none;
  border-color: #2196F3;
  box-shadow: 0 0 0 2px rgba(33, 150, 243, 0.2);
}

button {
  width: 100%;
  padding: 12px;
  background-color: #2196F3;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
  margin-top: 10px;
}

button:hover {
  background-color: #1976D2;
}

button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.error {
  color: #d32f2f;
  font-size: 13px;
  margin-top: 6px;
}

.general-error {
  margin: 16px 0;
  text-align: center;
}

.success-message {
  background-color: #e0f7e9;
  color: #2e7d32;
  padding: 12px;
  margin-bottom: 24px;
  border-radius: 6px;
  text-align: center;
  font-weight: 500;
}

.signup-link {
  text-align: center;
  margin-top: 24px;
  font-size: 14px;
}

a {
  color: #2196F3;
  text-decoration: none;
  font-weight: 500;
}

a:hover {
  text-decoration: underline;
}

.token-info {
  margin-top: 30px;
  padding: 15px;
  background-color: #f9f9f9;
  border-radius: 6px;
  font-size: 13px;
  color: #555;
}

.token-info pre {
  white-space: pre-wrap;
  word-break: break-word;
}

</style>
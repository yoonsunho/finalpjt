<template>
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
.login-container {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
}

h2 {
  text-align: center;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

input {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

button {
  width: 100%;
  padding: 10px;
  background-color: #2196F3;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  margin-top: 10px;
}

button:hover {
  background-color: #0b7dda;
}

button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.error {
  color: red;
  font-size: 12px;
  margin-top: 5px;
}

.general-error {
  margin: 10px 0;
  text-align: center;
}

.success-message {
  background-color: #dff2bf;
  color: #4F8A10;
  padding: 10px;
  margin-bottom: 20px;
  border-radius: 4px;
  text-align: center;
}

.signup-link {
  text-align: center;
  margin-top: 20px;
}

a {
  color: #2196F3;
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}

.token-info {
  margin-top: 30px;
  padding: 15px;
  background-color: #f5f5f5;
  border-radius: 4px;
}

.token-info pre {
  white-space: pre-wrap;
  word-break: break-all;
}
</style>
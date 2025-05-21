<template>
  <div class="signup-container">
    <h2>회원가입</h2>
    <form @submit.prevent="submitForm">

      <div class="form-group">
        <label for="username">아이디</label>
        <input type="text" id="username" v-model="formData.username" required />
        <div v-if="errors.username" class="error">{{ errors.username }}</div>
      </div>


      <div class="form-group">
        <label for="email">이메일</label>
        <input type="email" id="email" v-model="formData.email" required>
        <div v-if="errors.email" class="error">{{ errors.email }}</div>
      </div>

      <div class="form-group">
        <label for="nickname">닉네임</label>
        <input type="text" id="nickname" v-model="formData.nickname" required>
        <div v-if="errors.nickname" class="error">{{ errors.nickname }}</div>
      </div>

      <div class="form-group">
        <label for="password1">비밀번호</label>
        <input type="password" id="password1" v-model="formData.password1" required>
        <div v-if="errors.password1" class="error">{{ errors.password1 }}</div>
      </div>

      <div class="form-group">
        <label for="password2">비밀번호 확인</label>
        <input type="password" id="password2" v-model="formData.password2" required>
        <div v-if="errors.password2" class="error">{{ errors.password2 }}</div>
      </div>

      <div class="form-group">
        <label for="gender">성별</label>
        <select id="gender" v-model="formData.gender" required>
          <option value="">선택하세요</option>
          <option value="M">남성</option>
          <option value="F">여성</option>
        </select>
        <div v-if="errors.gender" class="error">{{ errors.gender }}</div>
      </div>

      <div class="form-group">
        <label for="salary">연봉</label>
        <select id="salary" v-model.number="formData.salary" required>
          <option value="">선택하세요</option>
          <option value="1">3천만원 미만</option>
          <option value="2">3천만원 - 5천만원</option>
          <option value="3">5천만원 - 1억원</option>
          <option value="4">1억원 초과</option>
        </select>
        <div v-if="errors.salary" class="error">{{ errors.salary }}</div>
      </div>

      <div class="form-group">
        <label for="wealth">자산 범위</label>
        <select id="wealth" v-model.number="formData.wealth" required>
          <option value="">선택하세요</option>
          <option value="1">1천만원 미만</option>
          <option value="2">1천만원 이상 3천만원 미만</option>
          <option value="3">3천만원 이상 5천만원 미만</option>
          <option value="4">5천만원 이상 1억 미만</option>
          <option value="5">1억 이상</option>
        </select>
        <div v-if="errors.wealth" class="error">{{ errors.wealth }}</div>
      </div>

      <div class="form-group">
        <label for="tendency">투자 성향</label>
        <select id="tendency" v-model.number="formData.tendency" required>
          <option value="">선택하세요</option>
          <option value="1">안정형</option>
          <option value="2">중립형</option>
          <option value="3">공격형</option>
        </select>
        <div v-if="errors.tendency" class="error">{{ errors.tendency }}</div>
      </div>

      <div class="form-group">
        <label for="deposit_amount">희망 저축 금액</label>
        <select id="deposit_amount" v-model.number="formData.deposit_amount" required>
          <option value="">선택하세요</option>
          <option value="1">10만원 미만</option>
          <option value="2">10만원 이상 50만원 미만</option>
          <option value="3">50만원 이상 100만원 미만</option>
          <option value="4">100만원 이상</option>
        </select>
        <div v-if="errors.deposit_amount" class="error">{{ errors.deposit_amount }}</div>
      </div>

      <div class="form-group">
        <label for="deposit_period">희망 저축 기간</label>
        <select id="deposit_period" v-model.number="formData.deposit_period" required>
          <option value="">선택하세요</option>
          <option value="1">6개월 미만</option>
          <option value="2">6개월 이상 1년 미만</option>
          <option value="3">1년 이상 2년 미만</option>
          <option value="4">2년 이상</option>
        </select>
        <div v-if="errors.deposit_period" class="error">{{ errors.deposit_period }}</div>
      </div>

      <button type="submit" :disabled="isSubmitting">회원가입</button>
      <div v-if="errors.non_field_errors" class="error general-error">
        {{ errors.non_field_errors }}
      </div>
    </form>
    <div class="login-link">
      이미 계정이 있으신가요? <router-link to="/login">로그인</router-link>
    </div>
  </div>
</template>

<script>
import { useUserStore } from '@/stores/user';

export default {
  name: 'SignUp',
  data() {
    return {
      formData: {
        username: '',
        email: '',
        nickname: '',
        password1: '',
        password2: '',
        gender: '',
        salary: '',
        wealth: '',
        tendency: '',
        deposit_amount: '',
        deposit_period: ''
      },
      errors: {},
      isSubmitting: false
    };
  },
  methods: {
  async submitForm() {
    const userStore = useUserStore();
    try {
      await userStore.createUser(this.formData);
      this.$emit("signup-success", "회원가입 완료");
    } catch (err) {
      console.log('❌ 회원가입 실패: ', err.response?.data);
      this.errors = err.response?.data || { non_field_errors: ["오류"] };
    }
  }
}
};
</script>


<style scoped>
.signup-container {
  max-width: 600px;
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

input, select {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

button {
  width: 100%;
  padding: 10px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  margin-top: 10px;
}

button:hover {
  background-color: #45a049;
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

.login-link {
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
</style>

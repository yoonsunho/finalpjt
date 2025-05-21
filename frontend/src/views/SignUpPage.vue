<template>
    <div class="signup-container">
        <h1>회원가입</h1>
        <form action="">
            <div class="form-group">
                <label for="username">아이디</label>
                <input type="text" v-model="form.username" id="username" required>
            </div>
            <div class="form-group">
                <label for="email">이메일</label>
                <input type="email" v-model="form.email" id="email" required>
            </div>
            <div class="form-group">
                <label for="password">비밀번호</label>
                <input type="password" v-model="form.password" id="password" required>
            </div>
            <div class="form-group">
                <label for="passwordcheck">비밀번호 확인</label>
                <input type="password" v-model="form.passwordcheck" id="passwordcheck" required>
            </div>
            <div class="form-group">
                <label for="salary">연봉</label>
                <input type="text" v-model="form.salary" id="salary" required>
                <!-- <fwb-range v-model="value" :steps="5" label="Steps range" /> -->
            </div>
            <div class="form-group">
                <label for="salary">희망 저축 기간</label>
                <input type="text" v-model="form.salary" id="salary" required>
            </div>
            <button type="submit">가입하기</button>
        </form>

        <h1>회원가입이 완료되었습니다.</h1>

    </div>
</template>

<script setup>
import {ref} from 'vue'

const form = ref({
    username: '',
    email: '',
    password: '',
    passwordcheck: '',
    salary: '',
})
</script>

<style scoped>
.signup-container {
  max-width: 400px;
  margin: 40px auto;
  padding: 2rem;
  /* border: 1px solid #ccc; */
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  border-radius: 1rem;
  font-family: Pretendard, sans-serif;
}

h1 {
  text-align: center;
  margin-bottom: 1rem;
}

.form-group {
  margin-bottom: 1rem;
}

label {
  display: block;
  margin-bottom: 0.25rem;
  font-weight: bold;
}

input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 0.5rem;
}

button {
  width: 100%;
  padding: 0.75rem;
  background-color: #3182f6;
  color: white;
  border: none;
  border-radius: 0.5rem;
  font-weight: bold;
  cursor: pointer;
}

button:hover {
  background-color: #2574e6;
}

.error {
  color: red;
  margin-top: 1rem;
  text-align: center;
}
</style>
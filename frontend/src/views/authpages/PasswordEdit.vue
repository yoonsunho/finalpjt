<template>
  <div class="password-info">
    <form @submit.prevent="save">
      <!-- 현재 비밀번호와 일치하지 않으면 경고 -->
      <label>현재 비밀번호: <input type="password" v-model="form.password" /></label><br />
      <label>새 비밀번호: <input type="password" v-model="form.password1" /></label><br />
      <label>새 비밀번호 확인: <input type="password" v-model="form.password2" /></label><br />
      <div class="btn">
        <button class="button-back" type="button" @click="$router.back()">취소</button>
        <button class="button-save" type="submit">저장</button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAccountStore } from '@/stores/user'
import axios from 'axios'

const router = useRouter()
const ACCOUNT_API_URL = 'http://127.0.0.1:8000/accounts'
const store = useAccountStore()
const form = reactive({
  password: '',
  password1: '',
  password2: '',
})

const save = async () => {
  try {
    if (form.password1 || form.password2) {
      // 비밀번호 필드 중 하나만 입력된 경우
      if (!form.password || !form.password1 || !form.password2) {
        alert(
          '비밀번호를 변경하려면 현재 비밀번호, 새 비밀번호, 새 비밀번호 확인을 모두 입력해주세요.',
        )
        return
      }

      // 현재 비밀번호와 새 비밀번호가 같은 경우
      if (form.password === form.password1) {
        alert('현재 비밀번호와 새 비밀번호가 동일합니다. 다른 비밀번호를 입력해주세요.')
        return
      }

      // 새 비밀번호 확인이 일치하지 않는 경우
      if (form.password1 !== form.password2) {
        alert('새 비밀번호와 새 비밀번호 확인이 일치하지 않습니다.')
        return
      }
      try {
        await axios.put(
          `${ACCOUNT_API_URL}/myprofile/change-password/`,
          {
            old_password: form.password,
            new_password: form.password1,
            confirm_password: form.password2,
          },
          {
            headers: {
              Authorization: `Token ${store.token}`,
            },
          },
        )
      } catch (passwordError) {
        console.error('비밀번호 변경 실패:', passwordError)
        if (passwordError.response?.data) {
          const errors = passwordError.response.data
          if (errors.old_password) {
            alert(`현재 비밀번호가 올바르지 않습니다.`)
          } else if (errors.new_password) {
            alert(`새 비밀번호가 유효하지 않습니다: ${errors.new_password[0]}`)
          } else if (errors.non_field_errors) {
            alert(`비밀번호 변경 오류: ${errors.non_field_errors[0]}`)
          } else {
            alert('비밀번호 변경 중 오류가 발생했습니다.')
          }
        } else {
          alert('현재 비밀번호가 올바르지 않습니다.')
        }
        return
      }
    }

    alert('수정되었습니다!')
    await store.fetchUserInfo() // 수정된 정보로 스토어 업데이트
    router.push({ name: 'ProfilePage' })
  } catch (err) {
    console.error('수정 실패:', err)
    if (err.response?.data) {
      const errors = err.response.data
    } else {
      alert('수정 중 오류가 발생하였습니다')
    }
  }
}
</script>
<style scoped>
* {
  font-family: Pretendard;
}
.password-info {
  background: #fff;
  padding: 40px;
  border-radius: 20px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.06);
  max-width: 600px;
  margin: 40px auto;
}
form label {
  display: block;
  font-weight: 600;
  color: #333;
  margin-bottom: 1.2rem;
}
input {
  border: 1px solid #dcdcdc;
  border-radius: 12px;
  padding: 12px;
  width: 100%;
  max-width: 100%;
  margin-top: 0.4rem;
  font-size: 15px;
  background-color: #fdfdfd;
}
.btn {
  display: flex;
  justify-content: end;
  /* width: 100%; */
  gap: 25px;
}
.button-group {
  margin-top: 2rem;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}
.button-back,
.button-save {
  padding: 10px 20px;
  border: none;
  border-radius: 12px;
  color: white;
  font-weight: bold;
  font-size: 15px;
  cursor: pointer;
  transition: background 0.3s;
}
.button-back {
  background-color: #64748b;
}
.button-save {
  background-color: #191f28;
}
.button-back:hover {
  background-color: #475569;
}
.button-save:hover {
  background-color: #0f172a;
}
</style>

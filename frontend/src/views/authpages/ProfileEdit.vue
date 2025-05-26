<template>
  <div class="profile-category-info">
    <form @submit.prevent="save">
      <label>이메일: <input v-model="form.email" disabled /></label><br />
      <label>닉네임: <input v-model="form.nickname" /></label><br />
      <!-- 현재 비밀번호와 일치하지 않으면 경고 -->
      <label>현재 비밀번호: <input type="password" v-model="form.password" /></label><br />
      <label>새 비밀번호: <input type="password" v-model="form.password1" /></label><br />
      <label>새 비밀번호 확인: <input type="password" v-model="form.password2" /></label><br />
      <label
        >성별:
        <select v-model="form.gender">
          <option value="">선택하세요</option>
          <option value="M">남성</option>
          <option value="F">여성</option>
        </select> </label
      ><br />
      <label
        >연봉:
        <select v-model="form.salary">
          <option value="">선택하세요</option>
          <option value="under_30m">3천만원 미만</option>
          <option value="30m_50m">3천만원~5천만원</option>
          <option value="50m_100m">5천만원~1억원</option>
          <option value="over_100m">1억원 이상</option>
        </select> </label
      ><br /><label
        >자산 범위:
        <select v-model="form.wealth">
          <option value="">선택하세요</option>
          <option value="under_10m">1천만원 미만</option>
          <option value="10m_30m">1천~3천만원</option>
          <option value="30m_50m">3천~5천만원</option>
          <option value="50m_100m">5천~1억원</option>
          <option value="over_100m">1억원 이상</option>
        </select> </label
      ><br /><label
        >투자 성향:
        <select v-model="form.tendency">
          <option value="">선택하세요</option>
          <option value="safe">안정형</option>
          <option value="neutral">중립형</option>
          <option value="aggressive">공격형</option>
        </select> </label
      ><br /><label
        >희망 저축 금액:
        <select v-model="form.deposit_amount">
          <option value="">선택하세요</option>
          <option value="under_100k">10만원 미만</option>
          <option value="100k_500k">10~50만원</option>
          <option value="500k_1m">50~100만원</option>
          <option value="over_1m">100만원 이상</option>
        </select> </label
      ><br /><label
        >희망 저축 기간:
        <select v-model="form.deposit_period">
          <option value="">선택하세요</option>
          <option value="under_6m">6개월 미만</option>
          <option value="6m_12m">6~12개월</option>
          <option value="1y_2y">1~2년</option>
          <option value="over_2y">2년 이상</option>
        </select> </label
      ><br />
      <button class="button-back" type="button" @click="$router.back()">취소</button>
      <button class="button-save" type="submit">저장</button>
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
  email: '',
  nickname: '',
  password: '',
  password1: '',
  password2: '',
  gender: '',
  salary: '',
  wealth: '',
  tendency: '',
  deposit_amount: '',
  deposit_period: '',
})

onMounted(() => {
  const user = store.userInfo
  if (user) {
    form.email = user.email || ''
    form.nickname = user.nickname || ''
    form.gender = user.gender || ''
    form.salary = user.salary || ''
    form.wealth = user.wealth || ''
    form.tendency = user.tendency || ''
    form.deposit_amount = user.deposit_amount || ''
    form.deposit_period = user.deposit_period || ''
  }
})

const save = async () => {
  try {
    // 1. 프로필 정보 업데이트 (백엔드 URL에 맞춤)
    const profilePayload = {
      email: form.email,
      nickname: form.nickname,
      gender: form.gender,
      salary: form.salary,
      wealth: form.wealth,
      tendency: form.tendency,
      deposit_amount: form.deposit_amount,
      deposit_period: form.deposit_period,
    }

    await axios.put(`${ACCOUNT_API_URL}/myprofile/`, profilePayload, {
      headers: {
        Authorization: `Token ${store.token}`,
      },
    })

    // 2. 비밀번호 변경 요청이 있는 경우
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

      // 비밀번호 변경 요청 (백엔드 serializer에 맞춰 confirm_password 사용)
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
      if (errors.nickname) {
        alert(`닉네임 오류: ${errors.nickname[0]}`)
      } else {
        alert('수정 중 오류가 발생하였습니다')
      }
    } else {
      alert('수정 중 오류가 발생하였습니다')
    }
  }
}
</script>

<style>
.button-back {
  background-color: dodgerblue;
}
.button-save {
  background-color: #191f28;
}
input {
  border: 1px solid #191f28;
}
input[disabled] {
  background-color: #f5f5f5;
  color: #666;
}
</style>

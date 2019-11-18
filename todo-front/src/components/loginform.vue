<template>
  <div class="login-div">
    <!-- 로딩일 때 스피너 보여줄 것 -->
    <div v-if="loading" class="spinner-border" role="status">
      <!-- 눈이 보이지 않는 사람들에게 말로써 로딩중임을 알려주는 태그 -->
      <span class="sr-only"></span>
    </div>
    <!-- 로딩 아닐 때 로그인form 화면 보여줌 -->
    <div v-else class="login-form">
      <!-- error가 하나라도 있다면 errors.length > 1 === true -->
      <div v-if="errors.length" class="alert alert-danger">
        <h4>다음 오류를 해결해주세요</h4>
        <hr>
        <div v-for="(error, idx) in errors" v-bind:key="idx">
          {{ error }}
        </div>
      </div>


      <div class="form-group">
        <label for="id">ID</label>
        <input type="text" id="id" class="form-control" placeholder="아이디를 입력해주세요" v-model="credentials.username">
        <!-- 위의 라벨은 input을 위한 라벨임 -->
      </div>
      <div class="form-group">
        <label for="password">PassWord</label>
        <input type="password" id="password" class="form-control" placeholder="비밀번호를 입력해주세요" v-model="credentials.password">
        <!-- 위의 라벨은 input을 위한 라벨임 -->
      </div>
      <button class="btn btn-success" v-on:click="login">Login</button>
    </div>

  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Loginform',
  // 어느 데이터를 양방향 바인딩할지 (v-model)작성
  data() {
    // 항상 오브젝트를 리턴해야함
    return {
      credentials: {
        username: '',
        password: '',
      },
      loading: false,
      errors: [],
    }
  },
  methods: {
    login() {
      if(this.checkForm()) {
        this.loading = true
        const SERVER_IP = process.env.VUE_APP_SERVER_IP

        axios.get(SERVER_IP, this.credentials)
          .then(response => {
            console.log(response)
            this.loading = false
          })
          .catch(error => {
            console.error(error)
            this.loading = false
          })
        console.log('Login Button Clicked!')
      }
    },
    checkForm() {
      this.errors = []
      if (!this.credentials.username) {
        this.errors.push('아이디를 입력해주세요.')
      }
      if (this.credentials.password.length < 8) {
        this.errors.push('비밀번호는 8자 이상 입력해주세요.')
      }
      if (this.errors.length === 0) {
        return true
      }
      // else~ 는 꼭 안적어줘도됨
      // } else {
      //   return false
      }
    }
  }
</script>

<style>

</style>
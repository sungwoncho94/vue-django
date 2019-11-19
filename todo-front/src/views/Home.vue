<template>
  <div class="home">


  </div>
</template>

<script>
import router from '@/router'

export default {
  name: 'home',

  methods: {
    // 로그인 되어있는지 확인하여 로그인되어있지 않을 시, 로그인 페이지로 보내는 함수
    checkLoggedIn() {
      // 1. 세션을 시작해서
      this.$session.start()

      // 2. jwt가 있는지 확인하겠다.
      // 3. if, jwt가 없다면 -> 로그인 페이지로 보내주겠다.
      if(!this.$session.has('jwt')) {
        router.push('/login')
      }
    }
  },
  // vue가 화면에 그려지면 실행하는 함수
  mounted() {
    this.checkLoggedIn()
  }
}
</script>

<style>

</style>
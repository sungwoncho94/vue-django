<template>
  <div id="app">
    <div id="nav">

      <!-- 조건부랜더링 -->
      <div v-if="isLoggedIn">
        <!-- 로그아웃 버튼 만들기 -->
        <!-- 로그아웃은 별도의 페이지가 필요 없이 그냥 기능이기 때문에 a태그 써도 된다 -->
        <!-- @click.prevent -> logout 페이지로 이동하는 것이 아니라, logout기능만 실현 (href로 redirect방지 위해) -->
        <a @click.prevent="logout" href="/logout">Logout</a>
      </div>
      <div v-else>
        <!-- router link : router의 index.js를 참조해서 어떤 페이지를 보여줄지 가르킴 -->
        <router-link to="/">Home</router-link>  |  
        <!-- <router-link to="/about">About</router-link> -->
        <router-link to="/login">Login</router-link>  |
      </div>
      
    </div>
    <div class="container col-6">
      <router-view/>
    </div>
  </div>
</template>

<script>
import router from '@/router'

export default {
  name: 'App',
  data() {
      return {
        // 사용자의 로그인 상태 값, jwt가 있으면 true -> 로그인 해있음
        isLoggedIn: this.$session.has('jwt')
      }
  },
  methods: {
    logout() {
      // 세션에 세션아이디밖에 없기 때문에 세션 자체를 다 날리면 된다
      this.$session.destroy()
      // 로그아웃한 후, 로그인 페이지로 보내준다
      router.push('/login')
    }
  },
  // 데이터의 변화가 일어나는 시점에 실행하는 함수
  updated() {
    this.isLoggedIn = this.$session.has('jwt')
  }
}
</script>>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

#nav {
  padding: 30px;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #42b983;
}
</style>

<template>
  <div class="home">
    <h1>Todo</h1>
    <!-- 3. 사용 -->
    <TodoInput @createTodo="createTodo"/>
    <TodoList :todos="todos"/>
  </div>
</template>

<script>
import axios from 'axios'
import jwtDecode from 'jwt-decode'  // jwt을 해석(decode)해주는 라이브러리
// 1. 호출
import TodoList from '@/components/TodoList'
import router from '@/router'
import TodoInput from '@/components/TodoInput'


export default {
  name: 'home',
  data() {
    return {
      todos: [],
    }
  },

  // 2. 등록
  components: {
    TodoList,
    TodoInput,
  },

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
    },
    
    // 우리가 만든 django API서버로 todos를 달라는 요청을 보낸 뒤, todos data에 할당하는 함수
    getTodo() {
      // 토큰을 꺼내야 디코딩 할 수 있음 (항상 session.start로 시작한다)
      this.$session.start()
      const token = this.$session.get('jwt')  // token 등록한 key값임
      const userId = jwtDecode(token).user_id
      const SERVER_IP = process.env.VUE_APP_SERVER_IP

      const options = {
        headers: {
          Authorization: 'JWT ' + token
        }
      }
      // axios.get은 두번째 인자로 설정값을 넣어줘야한다. -> headers에 우리의 인증키를 보내야함 (authorization)
      axios.get(`${SERVER_IP}/api/v1/users/${userId}/`, options)
        .then(response => {
          console.log(response)
          this.todos = response.data.todo_set
        })
        .catch(error => {
          console.log(error)
        })
    },
    createTodo(title) {
      this.$session.start()
      const token = this.$session.get('jwt')
      const SERVER_IP = process.env.VUE_APP_SERVER_IP
      const userId = jwtDecode(token).user_id

      const options = {
        headers: {
          Authorization: 'JWT ' + token
        }
      }
      
      // 요청 보낼 데이터 작성
      const data = {
        title, 
        user: userId
      }
      axios.post(`${SERVER_IP}/api/v1/todos/`, data, options)
        .then(response => {
          // 우리가 가지고 있는 todo목록에 즉시 추가됨
          this.todos.push(response.data)
        })
        .catch(error => {
          console.error(error)
        })

    },
  },
  // vue가 화면에 그려지면 실행하는 함수
  mounted() {
    this.checkLoggedIn()
    this.getTodo()
  }
}
</script>

<style>

</style>
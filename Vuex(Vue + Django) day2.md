# Vuex(Vue + Django) day2

- 시작하기 (todo-front / todo-back)
  ![1574122950689](C:\Users\student\AppData\Roaming\Typora\typora-user-images\1574122950689.png)

XHR = 페이지 변경 없이 데이터 요청을 보내고 받는 것
현재 로그인을 하려고하면 CORB 오류가 난다.
서로 다른 사이트간에 JS요청으로 리소스를 공유하려 할 때, 정보 보호를 위해 막아둠  -->  우리의 vue를 화이트리스트 처리해줘야함

---------------

- 장고 - 앱 만들어주기  ->  settings에 앱 등록하기
  `$ python manage.py startapp todos`  

  ```python
  INSTALLED_APPS = [
      # local apps
      'todos',
  ```

- 설치

  ```bash
  # django rest framework 설치
  $ pip install djangorestframework
  $ pip install djangorestframework-jwt
  
  # 뷰가 장고로 접근할 수 있게 해주는 모듈
  $ pip install django-cors-headers
  
  # settings에 등록해주기
  INSTALLED_APPS = [
      # local apps
      'todos',
  
      # Third party apps
      'rest_framework',
      'corsheaders',
  ```

- JWT관련 세팅 (웹토큰을 통해서 인증처리 해주는 것)
  `https://jpadilla.github.io/django-rest-framework-jwt/` - usage / Additional Settings

  ```python
  REST_FRAMEWORK = {
      # 로그인 여부를 확인해주는 클래스
      'DEFAULT_PERMISSION_CLASSES': (
          'rest_framework.permissions.IsAuthenticated',
      ),
      # 인증 여부를 확인하는 클래스
      'DEFAULT_AUTHENTICATION_CLASSES': (
          'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
          'rest_framework.authentication.SessionAuthentication',
          'rest_framework.authentication.BasicAuthentication',
      ),
  }
  
  
  JWT_AUTH = {
      # 필수!! => secret_key (settings.py 위쪽에 있음)
      # Token을 서명할 시크릿 키를 등록 (절대 외부 노출 금지)  but, 어차피 default가 settings.py에 있는 secret key이기 때문에 꼭 안해줘도됨
      'JWT_SECRET_KEY': SECRET_KEY,
      # Token을 어떻게 hashing할 것인지 적어놓는 것.
      'JWT_ALGORITHM': 'HS256',
      # Token 새로고침 허용
      'JWT_ALLOW_REFRESH': True,
      # 유효기간 / datetime import해야함  /  default는 5분이지만, 개발할 때에는 7주일정도로 설정
      'JWT_EXPIRATION_DELTA': datetime.timedelta(days=7),
      # 28일 마다 토큰이 갱신 (유효기간 연장시)
      'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=28),
  }
  ```

- 화이트리스트에 추가하기
  `https://github.com/adamchainz/django-cors-headers/#setup`

  ```python
  MIDDLEWARE = [
      'corsheaders.middleware.CorsMiddleware',
      ...
  ]
  
  # vue server 등록 / 우리 서버에서만 접근 가능
  # CORS_ORIGIN_WHITELIST = [
  #     "http://localhost:8080",
  # ]
  
  # 오픈api를 사용해서 데이터를 가져올 때, 전세계 모든 곳에서 접근 가능
  CORS_ORIGIN_ALLOW_ALL = True
  
  ```

  

- 프로젝트폴더 (todoback)의 urls.py
  : 그게 동일한 토큰이 올때만 해당 정보를 보여주겠다는 의미

	```python
  from django.contrib import admin
  from django.urls import path
  from rest_framework_jwt.views import obtain_jwt_token
  
  urlpatterns = [
      path('admin/', admin.site.urls),
      path('api-token-auth/', obtain_jwt_token)
  ]
  ```
  
- todos / models.py

  ```python
  from django.db import models
  # 유저 모델을 새롭게 작성하기 위해 abstractUser 상속받아서 씀
  from django.contrib.auth.models import AbstractUser
  from django.conf import settings
  
  # AbstractUser를 사용할건데, 그대로 상속받아서 쓸 것. (default 유저를 사용하더라도 장고에서는 강력히 커스텀 유저를 사용하라고 권장)
  class User(AbstractUser):
      pass
  
  
  class Todo(models.Model):
      user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
      title = models.CharField(max_length=50)
      completed = models.BooleanField(default=False)
  
      def __str__(self):
          return self.title
      
  
  # todoback / settings.py
  # custom한 유저모델 사용할거라고 등록
  AUTH_USER_MODEL = 'todos.User'
  ```

- `$ python manage.py makemigrations`
  `$ python manage.py makemigrations`

  `$ python manage.py createsuperuser`

-------------------

- `python manage.py runserver` -> `http://127.0.0.1:8000/api-token-auth/`
- JWT의 인증방식 알아보기

![1574128839636](../../AppData/Roaming/Typora/typora-user-images/1574128839636.png)

username / password 입력 후 POST요청 보내면 token이 온다 (get 요청으로는 불가능)

![1574128903994](../../AppData/Roaming/Typora/typora-user-images/1574128903994.png)

토큰 정보 복사해서 jwt.io 에 decoding해보면 나의 정보가 나온다

![1574129267642](../../AppData/Roaming/Typora/typora-user-images/1574129267642.png)

우리의 시크릿키 (settings.py)를 입력하면 Signature Verified 가 된다 -> 인증 받음

![1574129236042](../../AppData/Roaming/Typora/typora-user-images/1574129236042.png)

---------------

- vue-페이지에서 post로 로그인 요청을 보내서 token을 받아보자(?)
  todo-front / loginform.vue
  내가 토큰값을 가지고 있으면 로그인 한 상태임!!

  ```javascript
    methods: {
      login() {
        if(this.checkForm()) {
          this.loading = true
          // http://127.0.0.1:8000
          const SERVER_IP = process.env.VUE_APP_SERVER_IP
  
          // post로만 요청을 보내야 한다
          axios.post(SERVER_IP + '/api-token-auth/', this.credentials)
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
  ```

  - 로그인하면 토큰값이 생김

  ![1574130457689](../../AppData/Roaming/Typora/typora-user-images/1574130457689.png)

------------------

- 저장소에 저장하고 불러오는 `vue-session` install 하기

  todo-fornt/ main.js

  `$ npm i vue-session`

  ```javascript
  // session storage 사용하기 위해 vue-session 임포트해주고, 밑에 사용한다고 알려주기
  import Vuesession from 'vue-session',
  
  Vue.use(VueSession)
  ```

  todo-front / loginform.vue

  ```vue
  <script>
  import axios from 'axios'
  // 사용자가 로그인한 후 홈으로 보내주기 위해 라우터 가져옴
  import router from '@/router'
  
      ...
      
    methods: {
      login() {
        if(this.checkForm()) {
          this.loading = true
          // http://127.0.0.1:8000
          const SERVER_IP = process.env.VUE_APP_SERVER_IP
  
          // post로만 요청을 보내야 한다
          axios.post(SERVER_IP+'/api-token-auth/', this.credentials)
            .then(response => {
  
              // 세션을 초기화, 사용하겠다
              this.$session.start()
  
              // 응답결과를 세션에 저장하겠다.  (this.$session.set(key, token)값 필요)
              this.$session.set('jwt', response.data.token)
  
              // console.log(response)
              this.loading = false
  
              // vue rouwter를 통해 홈으로 이동
              router.push('/')
            })
  ```

  웹 -> 콘솔창 -> 어플리케이션 -> 세션스토리지에 `vue-session-key` 등록되었는지 확인
  ![1574135225665](../../AppData/Roaming/Typora/typora-user-images/1574135225665.png)

----------

- 홈에서 로그인되어있지 않으면, 로그인 페이지로 보내주기
  todo-front / home.vue

  ```vue
  <template>
    <div class="home">
  
  
    </div>
  </template>
  
  <script>
  import router from '@/router'
  
  export default {
    name: 'home',
  
    methods: {
      // 로그인 되어있는지 확인하는 함수
      checkLoggedIn() {
        // 1. 세션을 시작해서
        this.$session.start()
  
        // 2. jwt가 있는지 확인하겠다.
        // jwt가 없다면 -> 로그인 페이지로 보내주겠다.
        if(!this.$session.has('jwt')) {
          router.push('/login')
        }
      }
    },
    // vue가 화면에 그려지면 실행하는 함수
    mounted() {
  
    }
  }
  </script>
  
  <style>
  
  </style>
  ```

- logout = 세션을 지우면 된다

  ```vue
  <!-- todo-front / App.vue -->
  <template>
    <div id="app">
      <div id="nav">
        <!-- router link : router의 index.js를 참조해서 어떤 페이지를 보여줄지 가르킴 -->
        <router-link to="/">Home</router-link>  |  
        <!-- <router-link to="/about">About</router-link> -->
        <router-link to="/login">Login</router-link>  |
        <!-- 로그아웃 버튼 만들기 -->
        <!-- 로그아웃은 별도의 페이지가 필요 없이 그냥 기능이기 때문에 a태그 써도 된다 -->
        <!-- @click.prevent -> logout 페이지로 이동하는 것이 아니라, logout기능만 실현 (href로 redirect방지 위해) -->
        <a @click.prevent="logout" href="/logout">Logout</a>
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
    methods: {
      logout() {
        // 세션에 세션아이디밖에 없기 때문에 세션 자체를 다 날리면 된다
        this.$session.destroy()
        // 로그아웃한 후, 로그인 페이지로 보내준다
        router.push('/login')
      }
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
  
  ```

  로그아웃 눌렀을 때, 세션 키 모두 사라지는지 확인하기!

  

- 조건부랜더링 (로그인 시 -> 홈, 로그아웃 보이기) / (비로그인시 -> 로그인만 보이기)

  ```vue
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
  ```

  ```javascript
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
  ```

  
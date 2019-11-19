# Vuex(Vue + Django)

- 서버의 할 일이 줄어든다
  : 서버는 더 이상 세션을 사용하지 않음

- JWT(Json Web Tocken) - json방식으로 만들어진 토큰
  : 사용자(vue.js) 가 서버에게 로그인 요청을 보냄
  -> 유저 확인함
  -> 원래는 세션id를 받았으나, 지금은 JWT를 받는다
  -> 사용자가 데이터를 요청할 때, JWT를 같이 담아서 보낸다
  -> JWT를 검증해서 결과 알려줌 (기존 사용자의 id가 인증되었는지 아닌지 살펴볼 때 보다 빠르다)

- 보안에 약하지만, 누군가가 나의 컴퓨터를 빼앗지 않는 이상 안전 + 유효기간 짧음

- Authorization

- 

- JWT의 구조
  xxxx.yyyy.zzzz (Header / Payload / Signature)

  - Header : 토큰의 타입과 사용 algorithm
  - Payload : 토큰에 담길 정보가 들어있음 (userID , claim-key:value)
  - Header와 Payload의 값에 비밀키로 hashing  (Header + Payload의 정보를 암호화한 정보 有)

  ![1574045311019](../../AppData/Roaming/Typora/typora-user-images/1574045311019.png)



- vue라우터 : URL에 맞춰서 어떤 컴퍼넌트 랜더링 할건지 결정

  

**실습**

1. 환경설정
   : 3.7버전 / toto-back 까지 들어와서 만들기

   ```bash
   $ python -m venv venv  // 가상환경 만들기
   $ source venv/Scripts/activate    // 가상환경 실행
   $ python -m pip install --upgrade pip
   
   $ pip list
   Package    Version
   ---------- -------
   pip        19.3.1
   setuptools 40.8.0
   
   $ pip insatall django  //  장고 설치
   $ django-admin startproject todoback .  
   			 // 현재 directory에서 프로젝트 시작
   $ deactivate  // 가상환경에서 나옴
   ```

2. 폴더 구조 만들기
   : 다시 todo-back까지 나와서 진행하기

   ```bash
   todo-back
   - todoback
   - venv
   
   todo-front
   $ vue create todo-front  // 옵션 default 선택
   
   // vue 프로젝트로 만든 todo-front는 저절로 깃init까지 해준다
   -> 우리는 상위 폴더에서 깃으로 관리할꺼기 때문에 깃 삭제하기
   $ rm -rf .git
   
   
   .gitignore 만들기
   windows, VScode, vue, vuejs, python, node, venv
   ```

3. vue router 설치 -> 우리 vue project로 가져오기
   : url별로 어떤 component를 사용자에게 rendering할지 결정

   ```bash
   $ vue ui
   // 프로젝트 관리 환경을 goi로 만들어줌
   ```

   `http://localhost:8000/project/select`에서 프로젝트 관리

   (1) 프로젝트 폴더까지 들어와서 `vue ui`실행

   (2) 폴더 만들기 선택

   (3) 플러그인 선택 -> router검색 후, 맨 위 플러그인 설치

   (4) history mode 사용할 것 -> 오른쪽 버튼 클릭해서 켜주기
   	-> 사용자가 어떤 활동을 했는지 알 수 있음

   (5) 라우터 설치 완료

4. 폴더 src -> main.js에서 보면 `import router from './router'`가 새로 생김
   : router에서부터 router를 import해옴

   폴더 router -> index.js 가 있음  ==  기본 파일임
   ex) `import router from './router'` 라고 폴더만 지정하면 index.js를 가져옴
   index.js == url.py 와 비슷한 역할
   이곳에서 우리가 원하는 페이지 보여주는거 설정
   views에 작성되는 파일들을 가져와야함

5. 폴더 todo-front에서 `npm run serve`친 후,
   주소 + / -> home으로, 주소 + /About -> about페이지 보여준다
   (router가 하는 일)

6. About페이지 대신 로그인 페이지 보여주기

   - aoubt.vue연결하는 함수 삭제해주기
   - login페이지 열 수 있도록 함수 만들기

```json
       {
         path: '/login',
         name: 'login',
         component: null
       }
```

- login.vue 파일 만든 후, import 해주기

```js
import Login from '../views'
```

- login 연결해주기

```js
  {
    path: '/login',
    name: 'login',
    component: Login  // import해온 이름으로 연결해줌
  }
```



7. 부트스트랩 설치

   - `$ npm i bootstrap bootstrap-vue`

   - vue에 적용해주기 (main.js)

     ```js
     // app.js
     import BootstrapVue from 'bootstrap-vue'
     import 'bootstrap/dist/css/bootstrap.css'
     import 'bootstrap-vue/dist/bootstrap-vue.css'
     
     Vue.use(BootstrapVue)
     ```

   - css 적용기키기
     (1) app.vue

     ```vue
     <template>
     	...
         </div>
         <div class="container col-6">
           <router-view/>
         </div>
       </div>
     </template>
     ```

     (2) home.vue

     ```vue
     <template>
       <div class="home">
       </div>
     </template>
     
     <script>
     export default {
       name: 'home',
     }
     </script>
     
     <style>
     
     </style>
     ```

     아무 화면도 안켜지면 정상

8. login.vue  /  loginform.vue 만들기

   (1) components -> helloworld 삭제하고, loginform.vue 생성

   ```vue
   <template>
     <div class="login-div">
       <div class="form-group">
         <label for="id">ID</label>
         <input type="text" id="id" class="form-control" placeholder="아이디를 입력해주세요">
         <!-- 위의 라벨은 input을 위한 라벨임 -->
       </div>
       <div class="form-group">
         <label for="password">PassWord</label>
         <input type="password" id="password" class="form-control" placeholder="비밀번호를 입력해주세요">
         <!-- 위의 라벨은 input을 위한 라벨임 -->
       </div>
       <button class="btn btn-success">Login</button>
     </div>
   </template>
   
   <script>
   
   export default {
     name: 'Loginform',
   }
   </script>
   
   <style>
   
   </style>
   ```

   (2) login.vue 에 등록

   ```vue
   <template>
     <div>
       <!-- (3) 컴퍼넌트 사용 -->
       <Loginform />
     </div>
   </template>
   
   <script>
   // (1) 내가 적용하고 싶은 컴퍼넌트 호출
   import Loginform from '@/components/loginform'
   
   export default {
     name: 'login',
     components: {
       // (2) 컴퍼넌트 등록
       Loginform
     }
   }
   </script>
   
   <style>
   
   </style>
   ```

   (3) v-model로 사용자의 id, password 정보 v-model 시키기

   ```vue
   <template>
     <div class="login-div">
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
   </template>
   
   <script>
   
   export default {
     name: 'Loginform',
     // 어느 데이터를 양방향 바인딩할지 (v-model)작성
     data() {
       // 항상 오브젝트를 리턴해야함
       return {
         credentials: {
           username: '',
           password: '',
         }
       }
     },
     methods: {
       login() {
         console.log('Login Button Clicked!')
       },
     },
   }
   </script>
   
   <style>
   
   </style>
   
   ```

   

9. login 에 loading 기능 만들기

   ```vue
   <template>
     <div class="login-div">
       <!-- 로딩일 때 스피너 보여줄 것 -->
       <div v-if="loading" class="spinner-border" role="status">
         <!-- 눈이 보이지 않는 사람들에게 말로써 로딩중임을 알려주는 태그 -->
         <span class="sr-only"></span>
       </div>
       <!-- 로딩 아닐 때 로그인form 화면 보여줌 -->
       <div v-else class="login-form">
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
       }
     },
     methods: {
       login() {
         console.log('Login Button Clicked!')
       },
     },
   }
   </script>
   
   <style>
   
   </style>
   
   ```

   

10. checkForm 기능 만들기

    - id, password입력 시, 오류 반환

    ```vue
    <template>
      <div class="login-div">
        <!-- 로딩일 때 스피너 보여줄 것 -->
        <div v-if="loading" class="spinner-border" role="status">
          <!-- 눈이 보이지 않는 사람들에게 말로써 로딩중임을 알려주는 태그 -->
          <span class="sr-only"></span>
        </div>
        <!-- 로딩 아닐 때 로그인form 화면 보여줌 -->
        <div v-else class="login-form">
    
          <div class="alert alert-danger">
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
    
    ```

11. axios 설치 (todo-front에서!)

    ```bash
    $ npm i axios
    
    ```

    ```javascript
    // script가 시작되는 가장 윗부분에 axios import해주기
    import axios from 'axios'
    
    ```

    - todo-front에 .env.local 파일 만든 후, 우리의 url등록
      우리들이 배포한 서버ip를 손쉽게 바꿔주기 위해

      ```
      VUE_APP_SERVER_IP='http://127.0.0.1:8000'
      
      ```

      ```javascript
        methods: {
          login() {
            if(this.checkForm()) {
              this.loading = true
              const SERVER_IP = process.env.VUE_APP_SERVER_IP
      
      ```

- script 부분

  ```javascript
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
  
  ```

  




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
  CONS_ORIGIN_ALLOW_ALL = True
  
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
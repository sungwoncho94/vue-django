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
- 
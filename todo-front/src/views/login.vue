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
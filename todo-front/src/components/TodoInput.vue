<template>
  <div class="todo-input">
    <!-- 어딘가로 요청 안보낼꺼여서 action 비워둔다 / 요청 보낼필요도 없어서 submit 만들지X-->
    <!-- submit될때마다 onSubmit을 실행시킬거고, privent로 실제 제출은 막을 것 -->
    <form action="" class="input-group mb-3" @submit.prevent="onSubmit">
      <input v-model="title" type="text" class="form-control">
      <button class="btn btn-success">add</button>
    </form>
  </div>
</template>

<script>
export default {
  name: 'TodoInput',
  // 위의 iput data를 가져오기 위해선 data로 v-model양방향 바인딩을 해줘야함
  data() {
    return {
      title: ''
    }
  },
  methods: {
    onSubmit() {
      // 값이 바뀔때마다 createTodo를 실행시키는데, title을 넘겨줌
      // emit은 component가 이벤트를 발생시키게 하는 함수
      this.$emit('createTodo', this.title)
      // 타이틀 값을 넘기면 다시 초기화시켜주기
      this.title = ''
    }
  }
}
</script>

<style>

</style>
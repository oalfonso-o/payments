<template>
  <Promised :promise="accountPromise">
    <template v-slot:pending>
      <p>Loading...</p>
    </template>
    <template v-slot="account">
      <b>Current balance:</b>
      <br/>
      {{ account.balance }} €
    </template>
    <template v-slot:rejected="error">
      <p>Error: {{ error.message }}</p>
      <p>Data: {{ error.data }}</p>
    </template>
  </Promised>
</template>

<script>
  import Api from '@/api'

  export default {
    name: 'CurrentBalance',
    data () {
      return {
        accountPromise: null,
      }
    },
    created() {
      this.accountPromise = Api.get('/account/')
    },
  }
</script>

<template>
  <Promised :promise="usersPromise">
    <template v-slot:pending>
      <p>Loading...</p>
    </template>
    <template v-slot="data">
      <form v-on:submit="pay" action="payments2" method="post">
        <p>
          <b>Send Money</b>
        </p>
        <table align="center">
          <thead>
            <td>
              Receiver
            </td>
            <td>
              Amount
            </td>
          </thead>
          <tr>
            <td>
              <select v-model="receiver" id="receiver" name="receiver" required>
                <option v-for="user in data" v-bind:key="user.id" v-bind:value="user.id">{{ user.username }}</option>
              </select>
            </td>
            <td>
              <input type="number" v-model="amount" id="amount" name="amount" min="0.01" step=".01" required/>
            </td>
          </tr>
          <tr>
            <td colspan="2">
              <button type="submit">Pay</button>
            </td>
          </tr>
        </table>
      </form>
    </template>
    <template v-slot:rejected="error">
      <p>Error: {{ error.message }}</p>
    </template>
  </Promised>
</template>

<script>
  import Api from '@/api'

  export default {
    name: 'PaymentsCreation',
    data () {
      return {
        usersPromise: null,
        receiver: 0,
        amount: 0.01,
      }
    },
    created() {
      this.usersPromise = Api.get('/users/')
    },
    computed: {
      receiver_int () {
        return parseInt(this.receiver)
      },
    },
    methods: {
      pay (event) {
        event.preventDefault()
        let data = {'receiver': this.receiver_int, 'amount': this.amount}
        let paymentCreatedPromise = Api.post('/payments/', data)
        paymentCreatedPromise.then(function(result) {
          if (result.status == 201) {
            location.reload()
          }
        });
      },
    },
  }
</script>

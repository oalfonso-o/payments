<template>
  <Promised :promise="paymentsPromise">
    <template v-slot:pending>
      <p>Loading...</p>
    </template>
    <template v-slot="payments">
      <b> Payments List </b>
      <br/>
      <div class="pane">
        <table align="center">
          <thead>
            <td>
              Sender
            </td>
            <td>
              Receiver
            </td>
            <td colspan="2">
              Amount
            </td>
            <td>
              Datetime
            </td>
          </thead>
          <tr v-for="payment in payments" v-bind:key="payment.id">
            <td v-bind:class="{ outstanding: senderIsLoggedUser(payment) }">
              {{ payment.sender.username }}
            </td>
            <td v-bind:class="{ outstanding: receiverIsLoggedUser(payment) }">
              {{ payment.receiver.username }}
            </td>
            <td v-bind:class="{ negative: senderIsLoggedUser(payment), positive: receiverIsLoggedUser(payment), }">
              <span v-if="senderIsLoggedUser(payment)">-</span>
              <span v-if="receiverIsLoggedUser(payment)">+</span>
            </td>
            <td v-bind:class="{ negative: senderIsLoggedUser(payment), positive: receiverIsLoggedUser(payment), }" class="right_align">
              {{ payment.amount }}
            </td>
            <td>
              {{ payment.created | formatDate }}
            </td>
          </tr>
        </table>
      </div>
    </template>
    <template v-slot:rejected="error">
      <p>Error: {{ error.message }}</p>
    </template>
  </Promised>
</template>

<script>
  import Api from '@/api'

  export default {
    name: 'PaymentsList',
    data () {
      return {
        paymentsPromise: null,
      }
    },
    created() {
      this.paymentsPromise = Api.get('/payments/')
    },
    methods: {
      senderIsLoggedUser(payment) {
        return payment.sender.username == localStorage.getItem('user')
      },
      receiverIsLoggedUser(payment) {
        return payment.receiver.username == localStorage.getItem('user')
      }
    }
  }
</script>

<style lang="scss" scoped>
.pane {
    display: inline-block;
    overflow-y: scroll;
    max-height:500px;
}
table {
    text-align: center;
    margin: auto;
}
.negative {
  color: red;
}
.positive {
  color: green;
}
.outstanding {
  color: rgba(22, 153, 240, 0.712);
}
.right_align {
  text-align: right;
}
</style>

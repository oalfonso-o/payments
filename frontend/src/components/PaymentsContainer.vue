<template>
  <div>
    <hr>
    <CurrentBalance/>
    <hr>
    <PaymentsList/>
    <hr>
    <PaymentsCreation/>
  </div>
</template>

<script>
  import CurrentBalance from '@/components/CurrentBalance.vue'
  import PaymentsList from '@/components/PaymentsList.vue'
  import PaymentsCreation from '@/components/PaymentsCreation.vue'
  export default {
    name: 'PaymentsContainer',
    components : {
      CurrentBalance,
      PaymentsList,
      PaymentsCreation,
    },
  }
</script>
<template>
  <!-- Card -->
  <mdb-container>
  <mdb-row class="justify-content-md-center pt-5">
  <mdb-col xl="6" md="8" sm="10" col="12">
  <mdb-card>
    <mdb-card-body>
        <form @submit.prevent="login">
        <p class="h4 text-center py-4">Sign in</p>
        <div class="grey-text">
            <mdb-input label="Your name" icon="user" group type="text" validate error="wrong" success="right" v-model="username"/>
            <mdb-input label="Your password" icon="lock" group type="password" validate v-model="password"/>
        </div>
        <div class="text-center py-4 mt-3">
            <mdb-btn color="cyan" type="submit">Login</mdb-btn>
        </div>
        </form>
    </mdb-card-body>
  </mdb-card>
  </mdb-col>
  </mdb-row>
  </mdb-container>
</template>
<script>
export default {
  data() {
    return {
        username: "",
        password: "",
    }
  },
  methods: {
    login() {
      let username = this.username
      let password = this.password
      this.$store.dispatch('login', { username, password })
      .then(() => this.$router.push({ name: 'home'}))
      .catch(err => {
        //may need to raise a popup/alert/stuff like that
        this.$bvToast.toast(err.message, {
          title: 'Login Failed',
          autoHideDelay:  15000,
          variant: 'danger',
          appendToast: 'append'
        })
        console.log(err)
      })
    }
  }
}
</script>

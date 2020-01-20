<template>
  <mdb-navbar color="mdb-color" dark class="mb-4" expand="large">
    <mdb-navbar-brand href="/">
      <img src="~/../assets/moviecat.png" style="width: 32px; height: 32px" class="d-inline-block align-top mr-1" alt="Kitten">
      MovieCat
    </mdb-navbar-brand>
    <mdb-navbar-toggler>
      <mdb-navbar-nav>
        <mdb-nav-item href="/" active>List</mdb-nav-item>
        <mdb-nav-item href="#" class="disabled" dibsable>Add</mdb-nav-item>
      </mdb-navbar-nav>
      <mdb-navbar-nav right>
        <form @submit="getMovie" >
          <mdb-input type="text" class="text-white" placeholder="Search" aria-label="Search" label navInput waves waves-fixed v-model="search"/>
        </form>
        <span v-if="isLoggedIn"><mdb-nav-item @click.native="logout" active class="ml-5">Logout</mdb-nav-item></span>
        <span v-else><mdb-nav-item href="/login" active class="ml-5">Login</mdb-nav-item></span>
      </mdb-navbar-nav>
    </mdb-navbar-toggler>
  </mdb-navbar>
</template>
<script>
//import store from '../store'
export default {
  data() {
    return {
      search: "",
    }
  },
  methods: {
    getMovie() {
      this.$router.push({ name: 'search', params: { string: this.search }});
    },
    logout: function () {
      this.$store.dispatch('logout')
      .then(() => {
        this.$router.push('/login')
      })
    }
  },
  computed: {
    isLoggedIn() {
       return this.$store.getters.isLoggedIn;
    }
  }
}
</script>

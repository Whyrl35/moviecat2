<template>
    <div>
      <b-navbar toggleable="lg" type="dark" variant="dark" class="mb-3">
        <b-container fluid>
            <b-navbar-brand href="/">
              <img src="~/../assets/moviecat.png" style="width: 32px; height: 32px" class="d-inline-block align-top" alt="Kitten">
              MovieCat
            </b-navbar-brand>
            <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
            <b-collapse id="nav-collapse" is-nav>
              <b-navbar-nav>
                <b-nav-item href="/">List</b-nav-item>
                <b-nav-item href="#" disabled>Add</b-nav-item>
              </b-navbar-nav>
              <!-- Right aligned nav items -->
              <b-navbar-nav class="ml-auto">
                <b-nav-form>
                  <b-form-input
                    size="sm"
                    class="mr-sm-2"
                    placeholder="Search for a movie"
                    v-model="search"
                    ></b-form-input>
                  <b-button
                    size="sm"
                    class="my-2 my-sm-0"
                    type="submit"
                    variant="success"
                    @click.prevent="getMovie"
                    >Search</b-button>
                </b-nav-form>
                <b-nav-item href="/"  class="pl-4">Login</b-nav-item>
              </b-navbar-nav>
            </b-collapse>
          </b-container>
      </b-navbar>
    </div>
</template>
<script>
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
  }
}
</script>

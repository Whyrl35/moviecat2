<template>
  <div id="app">
    <Navbar/>
    <Result :search_string="search_string"/>
  </div>
</template>
<script>
  import Navbar from '@/components/Navbar.vue';
  import Result from '@/components/Result.vue';
  export default {
    name: 'search',
    components: {
      Navbar,
      Result
    },
    data() {
      return {
        search_string: this.$route.params.string
      };
    },
  }
</script>
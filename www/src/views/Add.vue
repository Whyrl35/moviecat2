<template>
  <div id="app">
    <Navbar />
    <Tmdb />
  </div>
</template>
<script>
  import Navbar from '@/components/Navbar.vue';
  import Tmdb from '@/components/Tmdb.vue';
  export default {
    name: 'movie',
    components: {
      Navbar,
      Tmdb,
    }
  }
</script>
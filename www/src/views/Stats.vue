<template>
  <div id="app">
    <Navbar />
    <Stats />
  </div>
</template>
<script>
  import Navbar from '@/components/Navbar.vue';
  import Stats from '@/components/Stats.vue';
  export default {
    name: 'movie',
    components: {
      Navbar,
      Stats,
    },
    data() {
      return {
      };
    },
  }
</script>
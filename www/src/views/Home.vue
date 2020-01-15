<template>
  <div id="app">
    <Navbar/>
    <Cards/>
  </div>
</template>
<script>
  import Cards from '@/components/Cards.vue'
  import Navbar from '@/components/Navbar.vue';
  export default {
    name: 'home',
    components: {
      Navbar,
      Cards
    },
  }
</script>
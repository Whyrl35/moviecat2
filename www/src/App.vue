<template>
  <div id="app">
    <Navbar />
    <Listcard/>
  </div>
</template>
<script>
 import Listcard from './components/Listcard.vue'
  import Navbar from './components/Navbar.vue';
  export default {
    name: 'navbar',
    components: {
      Navbar,
      Listcard
    }
  }
</script>

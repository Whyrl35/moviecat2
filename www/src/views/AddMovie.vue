<template>
  <div id="app">
    <Navbar />
    <MovieInfo :id="s_id" :type="s_type" :data="s_data" :readonly="s_ro"/>
  </div>
</template>
<script>
  import Navbar from '@/components/Navbar.vue';
  import MovieInfo from '@/components/MovieInfo.vue'
  export default {
    name: 'movie',
    components: {
      Navbar,
      MovieInfo,
    },
    data() {
      return {
        s_id: this.$route.params.id,
        s_type: this.$route.params.type,
        s_data: this.$route.params.data,
        s_ro: this.$route.params.readonly,
      };
    },

  }
</script>
<template>
  <div id="app">
    <router-view/>
  </div>
</template>
<style>
  @import url('https://fonts.googleapis.com/css?family=Roboto:300,400,500,700&display=swap');
</style>
<script>
import store from './store'
import router from './router'
export default {
  created: function () {
    this.$http.interceptors.response.use(undefined, function (err) {
      return new Promise(function () {
        if (err.response.status === 401) {
          /* eslint-disable no-console */
          console.log("401: Token is now invalid");
          store.dispatch('logout')
          //.then(() => {
            router.push({ name: 'login'});
          //})
        }
        throw err;
      });

    });
  }
}
</script>
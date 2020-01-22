<template>
  <mdb-container fluid class="mt-4">
    <mdb-row  class="justify-content-md-center">
      <mdb-col col="12" md="6">
        <mdb-input label="Search on TMDB" placeholder="Movie name" v-model="tmdb_movie" @keyup.native='getResult(tmdb_movie)'/>
      </mdb-col>
    </mdb-row>
    <div v-if="results.length">
      <mdb-row class="justify-content-md-center">
        <mdb-col class="pb-4 col-12 col-sm-6 col-md-4 col-lg-3 col-xl-2"  v-bind:key="data.id" v-for="data in results">
          <mdb-card cascade>
            <mdb-view hover>
							<img style="width: 100%; height: 25rem" :src="'http://image.tmdb.org/t/p/w500/' + data.poster_path" alt="Card image cap" />
              <mdb-mask flex-center waves overlay="white-slight"></mdb-mask>
              <mdb-btn block color="success" size="sm" tag="a" router @click.native="addMovie(data.id, data.title ? 'movie' : 'tv')">Add this movie</mdb-btn>
            </mdb-view>
            <mdb-card-body cascade>
              <mdb-card-title>{{ data.title  || data.name}}</mdb-card-title>
              <span class="grey-text">{{ data.original_title || data.original_name}}</span>
            </mdb-card-body>
          </mdb-card>
        </mdb-col>
      </mdb-row>
    </div>
    <div v-else class="text-center mt-5">
      <h5>No movies available yet 😢</h5>
    </div>
  </mdb-container>
</template>
<script>
export default {
  name: 'search_tmdb',
  data () {
    return {
      tmdb_movie: '',
      results: [],
    }
  },
  methods: {
    getResult(query) {
      this.$http.get('https://api.themoviedb.org/3/search/multi?api_key=6b25c34634150747b40cf03be77fda85&language=fr-FR&query=' + query)
      .then(response => { this.results = response.data.results })
      console.log(query);
    },
    addMovie(id,type) {
      this.$http.get('https://api.themoviedb.org/3/' + type + '/' + id + '?api_key=6b25c34634150747b40cf03be77fda85&language=fr-FR')
      .then(response => {
        this.$router.push({ name: 'add_movie', params: { id: id, type: type, data: response.data, readonly: false}})
      });
    }
  }
}
</script>
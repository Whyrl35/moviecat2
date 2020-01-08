<template>
  <b-container fluid>
    <div v-if="movies.length">
      <b-row>
        <div v-bind:key="data.id" v-for="data in movies">
          <b-col l="4">
            <b-card
              v-bind:title="data.title"
              v-bind:sub-title="data.title_original"
              v-bind:img-src="data.poster"
              img-alt="Image"
              img-top
              tag="movies"
              style="max-width: 20rem;"
              class="mb-2">
              <b-card-text>{{ `${data.synopsis.slice(0,100)}...` }}</b-card-text>
              <b-button href="#" variant="primary">View details</b-button>
            </b-card>
          </b-col>
        </div>
      </b-row>
    </div>
    <div v-else>
      <h5>No movies available yet 😢</h5>
    </div>
  </b-container>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      movies: []
    };
  },
  mounted() {
    axios
      .get("http://localhost:5000/v1/movies")
      .then(response => {
        this.movies = response.data.data.movies;
      })
      .catch(err => {
        this.movies = []
        console.log(err);
      });
  }
};
</script>

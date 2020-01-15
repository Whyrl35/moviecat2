<template>
  <b-container fluid>
    <div v-if="movies.length">
      <b-row class="justify-content-md-center">
        <div v-bind:key="data.id" v-for="data in movies">
          <b-col l="4">
            <b-card
              v-bind:title="data.title"
              v-bind:sub-title="data.title_original"
              v-bind:img-src="data.poster"
              v-bind:rating="data.score"
              img-alt="Image"
              img-top
              style="max-witdh: 20rem; width: 20rem"
              class="mb-2">
              <star-rating v-bind:rating="data.score" :max-rating="rating.max" :star-size="rating.size" class="pb-2" read-only>
              </star-rating>
              <b-button size="sm" :to="{ path: 'movie', params: { id: data.id }}" variant="outline-secondary">View details</b-button>
            </b-card>
          </b-col>
        </div>
      </b-row>
    </div>
    <div v-else>
        <div class="d-flex align-items-center justify-content-center" style="height:90vh">
            <h3>No movies found with this information</h3>
        </div>
    </div>
  </b-container>
</template>

<script>
import axios from "axios";
import StarRating from 'vue-star-rating';
export default {
  props: {
    search_string: { type: String },
  },
  data() {
    return {
      movies: [],
      rating: {
        max: 10,
        size: 15,
      },
    };
  },
  watch: {
      search_string: function(value) {
        axios
        .get(process.env.VUE_APP_API_URL + "/v1/movies/search", {
            params: {
                search_string: value,
                }
            })
        .then(response => {
            this.movies = response.data.data.movies;
        })
        .catch(err => {
            this.movies = []
            console.log(err);
        });
      }
  },
  mounted() {
    axios
    .get(process.env.VUE_APP_API_URL + "/v1/movies/search", {
        params: {
            search_string: this.search_string,
            }
        })
    .then(response => {
        this.movies = response.data.data.movies;
    })
    .catch(err => {
        this.movies = []
        console.log(err);
    });
  },
  components: {
    StarRating
  },
};
</script>

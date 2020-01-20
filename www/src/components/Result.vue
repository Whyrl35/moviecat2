<template>
  <mdb-container fluid>
    <div v-if="movies.length">
      <mdb-row>
        <mdb-col class="pb-4 col-12 col-sm-6 col-md-4 col-lg-3 col-xl-2" v-bind:key="data.id" v-for="data in movies">
          <mdb-card cascade>
            <mdb-view hover>
              <img style="width: 100%; height: 25rem" :src="data.poster" alt="Card image cap" />
              <mdb-mask flex-center waves overlay="white-slight"></mdb-mask>
              <mdb-btn block color="mdb-color" size="sm" tag="a" router @click.native="goMovie">View details</mdb-btn>
            </mdb-view>
            <mdb-card-body cascade>
              <mdb-card-title>{{ data.title }}</mdb-card-title>
              <span class="grey-text">{{ data.title_original}}</span>
            </mdb-card-body>
            <mdb-card-footer class="text-center">
              <star-rating :inline="true" :show-rating="false"  v-bind:rating="data.score" :max-rating="rating.max" :star-size="rating.size" class="" read-only>
              </star-rating>
            </mdb-card-footer>
          </mdb-card>
        </mdb-col>
      </mdb-row>
    </div>
    <div v-else>
        <div class="d-flex align-items-center justify-content-center" style="height:90vh">
            <h3>No movies found with this information</h3>
        </div>
    </div>
  </mdb-container>
</template>

<script>
import axios from "axios";
import StarRating from 'vue-star-rating';
export default {
  methods: {
    goMovie() {
      this.$router.push({ name: 'movie', params: { id: this.movie_id }});
    },
  },

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

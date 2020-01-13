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
              <star-rating v-bind:rating="data.score" :max-rating="max_rating" star-size='15' class="pb-2" read-only=true>
              </star-rating>
              <b-button size="sm" :to="{ path: 'movie', params: { id: data.id }}" variant="outline-secondary">View details</b-button>
            </b-card>
          </b-col>
        </div>
      </b-row>
    </div>
    <div v-else>
      <h5>No movies available yet 😢</h5>
    </div>
    <div style="padding-top: 10px">
      <b-pagination-nav
        :number-of-pages="num_pages"
        :link-gen="linkGen"
        align="center"
      >
      </b-pagination-nav>
    </div>
  </b-container>
</template>

<script>
import axios from "axios";
import StarRating from 'vue-star-rating';
export default {
  methods: {
    linkGen(page) {
      return page === 1 ? '?' : `?page=${page}`
    }
  },
  data() {
    return {
      movies: [],
      max_rating: 10,
      movieCount: 0,
      perPage: 10,
      currentPage: this.$route.query.page === undefined ? 1 : this.$route.query.page
    };
  },
  mounted() {
    axios
      .get("/api/v1/movies?count=" + this.perPage +  "&page=" + this.currentPage)
      .then(response => {
        this.movies = response.data.data.movies;
      })
      .catch(err => {
        this.movies = []
        console.log(err);
      });
    axios
      .get("/api/v1/movies/count")
      .then(response => {
        this.movieCount = response.data.data.count;
      })
      .catch(err => {
        this.movieCount = 0;
        console.log(err);
      });
  },
  computed: {
      num_pages() {
        return this.movieCount / this.perPage + 1;
    }
  },
  components: {
    StarRating
  },
};
</script>

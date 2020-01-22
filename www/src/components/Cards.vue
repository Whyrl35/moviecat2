<template>
  <mdb-container fluid class="mt-4">
    <div v-if="movies.length">
      <mdb-row>
        <mdb-col class="pb-4 col-12 col-sm-6 col-md-4 col-lg-3 col-xl-2"  v-bind:key="data.id" v-for="data in movies">
          <mdb-card cascade>
            <mdb-view hover>
							<img style="width: 100%; height: 25rem" :src="data.poster" alt="Card image cap" />
              <mdb-mask flex-center waves overlay="white-slight"></mdb-mask>
              <mdb-btn block color="mdb-color" size="sm" tag="a" router @click.native="goMovie(data.id)">View details</mdb-btn>
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
      <h5>No movies available yet 😢</h5>
    </div>
    <div class="pt-4">
      <b-pagination-nav
        :number-of-pages="num_pages"
        :link-gen="linkGen"
        align="center"
      >
      </b-pagination-nav>
    </div>
  </mdb-container>
</template>

<script>
import StarRating from 'vue-star-rating';
export default {
  methods: {
    goMovie(id) {
      this.$router.push({ name: 'movie', params: { id: id }});
    },
    linkGen(page) {
      return page === 1 ? '?' : `?page=${page}`
    }
  },
  data() {
    return {
      movies: [],
      rating: {
        max: 10,
        size: 15,
      },
      movie_id: 0,
      movieCount: 0,
      perPage: 12,
      currentPage: this.$route.query.page === undefined ? 1 : this.$route.query.page,
    };
  },
  mounted() {
    this.$http
      .get(process.env.VUE_APP_API_URL + "/v1/movies?count=" + this.perPage +  "&page=" + this.currentPage)
      .then(response => {
        this.movies = response.data.data.movies;
      })
      .catch(err => {
        this.movies = []
        console.log(err);
      });
    this.$http
      .get(process.env.VUE_APP_API_URL + "/v1/movies/count")
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
        return Math.ceil(this.movieCount / this.perPage);
    }
  },
  components: {
    StarRating
  },
};
</script>

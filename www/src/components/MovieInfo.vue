<template>
<div>
  <container class="mt-5">
    <mdb-modal :show="showDeleteModal" @close="showDeleteModal = false">
      <mdb-modal-header>
        <mdb-modal-title>Deleting movie?</mdb-modal-title>
      </mdb-modal-header>
      <mdb-modal-body>Are you sure you want to delete the movie</mdb-modal-body>
      <mdb-modal-footer>
        <mdb-btn color="mdb-color" @click.native="showDeleteModal = false">Close</mdb-btn>
        <mdb-btn color="danger" @click.native="deleteMovie">Deleting</mdb-btn>
      </mdb-modal-footer>
    </mdb-modal>
  </container>
  <div class="backdrop" :style="{ background: computedBackground }">
    <div class="content">
      <mdb-container fluid class="p-5">
        <mdb-row  class="justify-content-md-center">
          <mdb-col col="3" xl="2">
            <img :src="this.poster" class="img-thumbnail zoom w-100" alt="Responsive image">
            <div v-if="this.readonly">
                <mdb-row class="no-gutters">
                  <mdb-col col="12" lg="6">
                    <mdb-btn block color="default" size="sm" tag="a" router @click.native="editMovie">Editing</mdb-btn>
                  </mdb-col>
                  <mdb-col col="12" lg="6">
                    <mdb-btn block color="danger" size="sm" tag="a" router @click.native="showDeleteModal = true">Deleting</mdb-btn>
                  </mdb-col>
                </mdb-row>
            </div>
            <div v-else>
              <mdb-btn block color="success" size="sm" tag="a" router @click.native="addMovie">Adding Movie</mdb-btn>
            </div>
          </mdb-col>
          <mdb-col col="9" xl="5">
          <div v-if="this.readonly">
            <h1><strong>{{title}}</strong></h1>
            <h5 class="grey-text">{{title_original}}</h5>
            <mdb-row class="pt-2">
              <mdb-col col="6">
                <star-rating :show-rating="true"  v-bind:rating="score" :max-rating="10" :star-size="20" class="" read-only/>
              </mdb-col>
              <mdb-col col="6">
                <mdb-icon icon="play" class="green-text mr-2" />play trailer
              </mdb-col>
            </mdb-row>
            <h3 class="pt-5">Synopsis</h3>
            <p>{{ this.synopsis }}</p>
            <h3 class="pt-2">Genres</h3>
            <p>{{ this.genre.replace(/,/g, ', ') }}</p>
          </div>
          <div v-else>
            <mdb-input size="lg" label="Title" v-model="title" bg/>
            <mdb-input size="sm" label="Original Title" v-model="title_original" bg/>
            <mdb-input size="sm" label="Genres" v-model="genre" bg/>
            <mdb-row  class="justify-content-md-center">
              <mdb-col col="4">
                <mdb-input label="Country" v-model="country" bg/>
              </mdb-col>
              <mdb-col col="4">
                <mdb-input label="Duration" v-model="duration" bg/>
              </mdb-col>
              <mdb-col col="4">
                <mdb-input label="Year" v-model="year" bg/>
              </mdb-col>
            </mdb-row>
            <star-rating :show-rating="true"  v-bind:rating="score" :max-rating="10" :star-size="20" class=""/>
            <b-form-checkbox class="pt-3"
              id="checkbox-1"
              v-model="seen"
              name="checkbox-1"
              value="true"
              unchecked-value="false"
            >Movie seen?</b-form-checkbox>
          </div>
          </mdb-col>
        </mdb-row>
      </mdb-container>
    </div>
  </div>
  <div>
      <mdb-container fluid class="p-1">
        <mdb-row  class="justify-content-md-center">
          <mdb-col col="10" xl="6">
          <div v-if="this.readonly">
            <h2 class="pt-3">Casting</h2>
            <p>{{ this.actors.join(', ') }}</p>
            <h2 class="pt-3">Realisators</h2>
            <p>{{ this.realisators.join(', ') }}</p>
            <mdb-row>
              <mdb-col>
                <h2 class="pt-3">Duration</h2>
                <p>{{ this.duration }} minutes</p>
              </mdb-col>
              <mdb-col>
                <h2 class="pt-3">Year</h2>
                <p>{{ this.year }}</p>
              </mdb-col>
              <mdb-col>
                <h2 class="pt-3">Seen</h2>
                <mdb-icon icon="check-circle" class="green-text mr-2" v-if="seen"/>
                <mdb-icon icon="times-circle" class="red-text mr-2" v-else/>
              </mdb-col>
            </mdb-row>
          </div>
          <div v-else>
            <mdb-input label="Actors" v-model="actors" outline/>
            <mdb-input label="Realisators" v-model="realisators" outline/>
            <mdb-input type="textarea" label="Synopsis" v-model="synopsis" :rows="6" outline/>
            <mdb-input label="Poster" v-model="poster" outline/>
            <mdb-input label="Backdrop" v-model="background" outline/>
            <mdb-input label="Trailer" v-model="trailer" outline/>
            <div v-if="is_series">
              <hr/>
              <mdb-input label="Season" v-model="series_season" outline/>
              <mdb-input label="Episodes" v-model="series_episodes" outline/>
              <mdb-input label="Duration" v-model="series_episodes_duration" outline/>
            </div>
          </div>
          </mdb-col>
        </mdb-row>
      </mdb-container>
  </div>
</div>
</template>
<style scoped>
.backdrop {
  width: 100%;
}
.content {
  position: relative;
  top: 0%;
  background: linear-gradient(90deg, rgba(0,0,0,.75) 30%, rgba(69,82,110,.75));
  color: #fff;
}
</style>
<script>
import StarRating from 'vue-star-rating';
export default {
  props: {
    id: { type: Number },
    type: { type: String },
    data: { type: Object },
    readonly: { type: Boolean },
  },
  data() {
    return {
      title: "",
      title_original: "",
      genre: "",
      country: "",
      year: "",
      duration: "",
      score: "",
      synopsis: "",
      actors: "",
      realisators: "",
      seen: false,
      trailer: "",
      poster: "",
      background: "",
      is_series: false,
      series_season: null,
      series_episodes: null,
      series_episodes_duration: null,
      showDeleteModal: false,
    }
  },
  computed: {
    computedBackground() {
      return "rgba(0, 0, 0, 0.75) url('" + this.background + "') no-repeat fixed center center / cover ";
    }
  },
  mounted() {
    if (this.data === null)
    {
      this.$http.get(process.env.VUE_APP_API_URL + "/v1/movie", {
        params: {
          id: this.id
        }
      })
      .then(response => {
        this.title = response.data.data.movie.title;
        this.title_original = response.data.data.movie.title_original;
        this.genre = response.data.data.movie.genre;
        this.country = response.data.data.movie.country;
        this.year = response.data.data.movie.year;
        this.duration = response.data.data.movie.duration;
        this.score = response.data.data.movie.score;
        this.synopsis = response.data.data.movie.synopsis;
        this.actors = response.data.data.movie.actors.map(function(elm) { return elm.first_name + " " + elm.last_name });
        this.realisators = response.data.data.movie.realisators.map(function(elm) { return elm.first_name + " " + elm.last_name });
        this.seen = response.data.data.movie.seen;
        this.trailer = response.data.data.movie.trailer;
        this.poster = response.data.data.movie.poster;
        this.background = response.data.data.movie.background;
        this.is_series = response.data.data.movie.is_series;
        this.series_season = response.data.data.movie.series_season;
        this.series_episodes = response.data.data.movie.series_episodes;
        this.series_episodes_duration = response.data.data.movie.series_episodes_duration;
      });
    }
    else {
      if (this.type === "tv") {
        this.title_original = this.data.original_name;
        this.genre = this.data.genres.map(function(elem){return elem.name}).join();
        this.country = this.data.origin_country.join();
        this.score = this.data.vote_average;
        this.seen = false;
        this.background = 'http://image.tmdb.org/t/p/w500' + this.data.backdrop_path;
        this.is_series = true;
        const date = new Date(this.data.seasons.slice(-1)[0].air_date);
        this.year = date.getFullYear();
        this.series_season = this.data.seasons.slice(-1)[0].season_number;
        this.series_episodes = this.data.seasons.slice(-1)[0].episode_count;
        this.series_episodes_duration = this.data.episode_run_time[0];
        if (this.data.seasons.slice(-1)[0].overview !== "") {
          this.synopsis = this.data.seasons.slice(-1)[0].overview;
        } else {
          this.synopsis = this.data.overview;
        }
        this.duration = this.series_episodes * this.series_episodes_duration;
        this.poster = 'http://image.tmdb.org/t/p/w500' + this.data.seasons.slice(-1)[0].poster_path;

        this.$http.get('https://api.themoviedb.org/3/tv/' + this.id + '/credits?api_key=6b25c34634150747b40cf03be77fda85&language=fr-FR')
        .then(response => {
          this.actors = response.data.cast.slice(0,10).map(function(elem) {return elem.name}).join();
          this.realisators = response.data.crew.filter(function (value) {
            return value.job === "Director";
          }).map(function(elem) {return elem.name}).join();
        })

        this.$http.get('https://api.themoviedb.org/3/tv/' + this.id + '/videos?api_key=6b25c34634150747b40cf03be77fda85&language=fr-FR')
        .then(response => {
          this.trailer = 'https://www.themoviedb.org/video/play?key=' + response.data.results[0].key + '&width=1449&height=814';
        })

        this.title = this.data.name + " - saison " + this.series_season;
      }
      else if (this.type === "movie") {
        const date = new Date(this.data.release_date);

        this.title = this.data.title;
        this.title_original = this.data.original_title;
        this.genre = this.data.genres.map(function(elem){return elem.name}).join();
        this.country = this.data.production_countries[0].iso_3166_1;
        this.year = date.getFullYear();
        this.duration = this.data.runtime;
        this.score = this.data.vote_average;
        this.synopsis = this.data.overview;
        this.seen = false;
        this.poster = 'http://image.tmdb.org/t/p/w500' + this.data.poster_path;
        this.background = 'http://image.tmdb.org/t/p/w500' + this.data.backdrop_path;
        this.is_series = false;
        this.series_season = null;
        this.series_episodes = null;
        this.series_episodes_duration = null;

        this.$http.get('https://api.themoviedb.org/3/movie/' + this.id + '/videos?api_key=6b25c34634150747b40cf03be77fda85&language=fr-FR')
        .then(response => {
          this.trailer = 'https://www.themoviedb.org/video/play?key=' + response.data.results[0].key + '&width=1449&height=814';
        })

        this.$http.get('https://api.themoviedb.org/3/movie/' + this.id + '/credits?api_key=6b25c34634150747b40cf03be77fda85&language=fr-FR')
        .then(response => {
          this.actors = response.data.cast.slice(0,10).map(function(elem) {return elem.name}).join();
          this.realisators = response.data.crew.filter(function (value) {
            return value.job === "Director";
          }).map(function(elem) {return elem.name}).join();
        })
      }
    }
  },
  methods: {
    deleteMovie() {
      this.$http.delete(process.env.VUE_APP_API_URL + "/v1/movie", { params: {id: this.id }})
      .then(() => {
        this.$router.push({ name: 'home'});
      })
      .catch(err => {
        this.$bvToast.toast(err.message, {
          title: 'Error during movie deletion',
          autoHideDelay:  15000,
          variant: 'danger',
          solid: true,
          appendToast: true
        });
      })
    },
    editMovie() {
      alert("not implemented yet")
    },
    addMovie() {
      this.$http.post(process.env.VUE_APP_API_URL + "/v1/movie", {
        title: this.title,
        title_original: this.title_original,
        genre: this.genre,
        country: this.country,
        year: this.year,
        duration: this.duration,
        score: this.score,
        synopsis: this.synopsis,
        actors: this.actors,
        realisators: this.realisators,
        seen: this.seen,
        trailer: this.trailer,
        poster: this.poster,
        background: this.background,
        is_series: this.is_series,
        series_season: this.series_season,
        series_episodes: this.series_episodes,
        series_episodes_duration: this.series_episodes_duration,
      })
      .then(response => {
        this.$bvToast.toast(response.data.message, {
          title: response.data.data.movie.title,
          autoHideDelay:  15000,
          variant: 'success',
          solid: true,
          isStatus: true,
          appendToast: true
        })
      })
      .catch(err => {
        this.$bvToast.toast(err.message, {
          title: 'Error during movie edition',
          autoHideDelay:  15000,
          variant: 'danger',
          solid: true,
          appendToast: true
        })
        console.log(err);
      });
    }
  },
  components: {
    StarRating
  },
}
</script>
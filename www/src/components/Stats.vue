<template>
  <section id="dashboard" class="p-5">
    <section>
      <mdb-row>
        <mdb-col xl="3" md="6" class="mb-r">
          <mdb-card cascade class="cascading-admin-card">
            <div class="admin-up">
              <mdb-icon icon="film" class="primary-color" />
              <div class="data">
                <p>MOVIES</p>
                <h4>
                  <strong>{{movies_count}}</strong>
                </h4>
              </div>
            </div>
            <mdb-card-body>
              <mdb-card-text>Better than last week (25%)</mdb-card-text>
            </mdb-card-body>
          </mdb-card>
        </mdb-col>
        <mdb-col xl="3" md="6" class="mb-r">
          <mdb-card cascade class="cascading-admin-card">
            <div class="admin-up">
              <mdb-icon icon="tv" class="warning-color" />
              <div class="data">
                <p>SERIES / EPISODES</p>
                <h4>
                  <strong>{{series_count}} / {{episodes_count}}</strong>
                </h4>
              </div>
            </div>
            <mdb-card-body>
              <mdb-card-text>Worse than last week (25%)</mdb-card-text>
            </mdb-card-body>
          </mdb-card>
        </mdb-col>
        <mdb-col xl="3" md="6" class="mb-r">
          <mdb-card cascade class="cascading-admin-card">
            <div class="admin-up">
              <mdb-icon icon="chart-pie" class="light-blue lighten-1" />
              <div class="data">
                <p>GENRES</p>
                <h4>
                  <strong>{{genres_count}}</strong>
                </h4>
              </div>
            </div>
            <mdb-card-body class="text-center">
              <mdb-card-text>Top 6 of movie/series genres</mdb-card-text>
              <mdb-horizontal-bar-chart :data="genresChart" :options="genresChartOptions" :height="200" />
            </mdb-card-body>
          </mdb-card>
        </mdb-col>
        <mdb-col xl="3" md="6" class="mb-r">
          <mdb-card cascade class="cascading-admin-card">
            <div class="admin-up">
              <mdb-icon icon="eye" class="red accent-2" />
              <div class="data">
                <p>SEEN</p>
                <h4>
                  <strong>{{seen_count}} on {{ total }}</strong>
                </h4>
              </div>
            </div>
            <mdb-card-body>
              <div>
                <mdb-progress :height="18" :value="progress.seen" />
              </div>
              <mdb-card-text>{{ this.progress.seen }}% of movies/series seen</mdb-card-text>
            </mdb-card-body>
          </mdb-card>
        </mdb-col>
      </mdb-row>
    </section>
  </section>
</template>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.cascading-admin-card {
  margin: 20px 0;
}
.cascading-admin-card .admin-up {
  margin-left: 4%;
  margin-right: 4%;
  margin-top: -20px;
}
.cascading-admin-card .admin-up .fas,
.cascading-admin-card .admin-up .far {
  box-shadow: 0 2px 9px 0 rgba(0, 0, 0, 0.2), 0 2px 13px 0 rgba(0, 0, 0, 0.19);
  padding: 1.7rem;
  font-size: 2rem;
  color: #fff;
  text-align: left;
  margin-right: 1rem;
  border-radius: 3px;
}
.cascading-admin-card .admin-up .data {
  float: right;
  margin-top: 2rem;
  text-align: right;
}
.admin-up .data p {
  color: #999999;
  font-size: 18px;
}
.classic-admin-card .card-body {
  color: #fff;
  margin-bottom: 0;
  padding: 0.9rem;
}
.classic-admin-card .card-body p {
  font-size: 13px;
  opacity: 0.7;
  margin-bottom: 0;
}
.classic-admin-card .card-body h4 {
  margin-top: 10px;
}
</style>

<script>
export default {
  data() {
    return {
      movies_count: 0,
      series_count: 0,
      episodes_count: 0,
      genres_count: 0,
      seen_count: 0,
      total: 0,
      progress: {
        seen: 0
      },
      genresChart: {
        labels: [],
        datasets: [
          {
            data: [],
            label: "",
            backgroundColor: [],
            borderColor: []
          }
        ]
      },
      genresChartOptions: {
        legend: {
          display: false,
        },
        responsive: true,
        maintainAspectRatio: false
      }
    };
  },
  mounted() {
    this.$http
      .get(process.env.VUE_APP_API_URL + "/v1/statistics", {
        params: {
          id: this.id
        }
      })
      .then(response => {
        this.movies_count = response.data.data.movies.count;
        this.series_count = response.data.data.series.count;
        this.episodes_count = response.data.data.series.episodes;
        this.genres_count = response.data.data.genres.count;
        this.total = response.data.data.seen.total;
        this.seen_count = response.data.data.seen.seen;
        this.progress.seen = Math.round(((this.seen_count * 100) / this.total + 0.00001) * 100) / 100;

        let keys = Object.keys(response.data.data.genres.count_by_genres);
        keys.sort(function(a,b) {return response.data.data.genres.count_by_genres[b] - response.data.data.genres.count_by_genres[a]});
        this.genresChart.labels = keys.slice(0,6);
        let data = [];
        keys.forEach(function(k){
          data.push(response.data.data.genres.count_by_genres[k]);
        });
        this.genresChart = Object.assign({});
        this.$set(this.genresChart, 'labels', []);
        this.$set(this.genresChart, 'datasets', []);
        this.genresChart.labels = keys.slice(0,6);
        this.genresChart.datasets.push({
          data: data.slice(0,6),
          label: "number",
          borderColor: ["rgba(255,99,132,1)", "rgba(54, 162, 235, 1)", "rgba(255, 206, 86, 1)",
            "rgba(75, 192, 192, 1)", "rgba(153, 102, 255, 1)", "rgba(255, 159, 64, 1)"],
          backgroundColor: [
            "rgba(255, 99, 132, 0.2)", "rgba(54, 162, 235, 0.2)", "rgba(255, 206, 86, 0.2)",
            "rgba(75, 192, 192, 0.2)", "rgba(153, 102, 255, 0.2)", "rgba(255, 159, 64, 0.2)"],
          borderWidth: 1,
        })
      })
      .catch(err => {
        this.$bvToast.toast(err.message, {
          title: "Error when getting statistics",
          autoHideDelay: 15000,
          variant: "danger",
          solid: true,
          appendToast: true
        });
      });
  }
};
</script>
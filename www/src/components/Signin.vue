<template>
  <!-- Card -->
  <mdb-container>
  <mdb-row class="justify-content-md-center pt-5">
  <mdb-col md="5" col="12">
  <mdb-card>
    <mdb-card-body>
      <form>
        <p class="h4 text-center py-4">Sign in</p>
        <div class="grey-text">
          <mdb-input label="Your name" icon="user" group type="text" validate error="wrong" success="right"/>
          <mdb-input label="Your password" icon="lock" group type="password" validate/>
        </div>
        <div class="text-center py-4 mt-3">
          <mdb-btn color="cyan" type="submit">Login</mdb-btn>
        </div>
      </form>
    </mdb-card-body>
  </mdb-card>
  </mdb-col>
  </mdb-row>
  </mdb-container>
</template>
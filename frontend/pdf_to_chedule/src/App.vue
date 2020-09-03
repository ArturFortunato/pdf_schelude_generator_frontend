<template>
  <v-app>
    <v-app-bar
      app
      color="primary"
      dark
    >
      <div class="d-flex align-center">
        <div>
          <h1>Schedule Generator</h1>
        </div>
      </div>

    </v-app-bar>

    <v-main>
      <Schedules/>
    </v-main>
  </v-app>
</template>

<script>
import Schedules from './components/Schedules';

export default {
  name: 'App',

  components: {
    Schedules,
  },

  data: () => ({
    //
  }),
};
</script>

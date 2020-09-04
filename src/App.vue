<template>
  <v-app>
    <v-app-bar
      app
      color="primary"
      dark
    >
      <div class="d-flex align-center">
        <div>
          <router-link to="/" class="text-white">
            <h1>Schedule Generator</h1>
          </router-link>
        </div>
      </div>

    </v-app-bar>

    <v-main>
      <router-view @updateCourses="updateCourses" :courses="courses" />
    </v-main>
  </v-app>
</template>

<script>
export default {
    name: 'Schedules',
    data: () => ({
        courses: []
    }),
    methods: {
        updateCourses(courses) {
          this.courses = courses
        },
    }
}
</script>

<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

#nav {
  padding: 30px;

  a {
    font-weight: bold;
    color: #2c3e50;

    &.router-link-exact-active {
      color: #42b983;
    }
  }
}

.text-white
{
  color: white !important;
  text-decoration: none;
}
</style>

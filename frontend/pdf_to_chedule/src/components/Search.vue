<template>
  <v-app>
    <v-row>
        <v-col offset-xs="3" offset-sm="3" sm="6" class="max-height-100">
            <div class="vertical-center width-40">
                <v-chip
                    class="ma-2"
                    close
                    color="primary"
                    text-color="white"
                    close-icon="mdi-delete"
                    v-for="course in courses"
                    :key="course"
                    @click:close="deleteCourse(course)"
                >
                    {{ course }}
                </v-chip>
                <v-text-field
                    label="Course..."
                    single-line
                    outlined
                    append-icon="mdi-open-in-new"
                    @keydown="teste"
                    v-model="input"
                >
                </v-text-field>
                <router-link :to=generateLink()>
                    <v-btn color="primary">Generate Schedules!</v-btn>
                </router-link>
            </div>
        </v-col>

    </v-row>
  </v-app>
</template>

<script>
export default {
  name: 'Schedules',
  data: () => ({
    input: '',
    courses: [],
  }),
  methods: {
    teste(event) {
        if (event.code == "Enter") {
            this.courses.push(this.input)
            this.input = ""
            this.$emit('updateCourses',this.courses)
        }
    },
    deleteCourse(course) {
        const index = this.courses.indexOf(course);
        this.courses.splice(index, 1);
    },
    generateLink() {
        return "/schedules/" + this.courses.join("&")
    }
  }
}
</script>

<style lang="scss">
  .border-red {
    border: 2px solid red;
  }

  .vertical-center {
    margin: 0;
    position: fixed;
    left: 50%;
    -ms-transform: translate(-50%, -50%);
    transform: translate(-50%, -50%);
  }

  .max-height-100
  {
    height: 100vh !important;
    max-height: 100vh !important;
  }

  .width-40
  {
      width: 40%;
  }

</style>
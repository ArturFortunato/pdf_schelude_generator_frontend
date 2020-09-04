<template>
  <v-app>
    <v-row>
      <v-col xs="1" sm="1" md="1" lg="1" class="sticky max-height-100">
        <v-btn @click="previous" class="vertical-center left-50">Previous</v-btn>
      </v-col>
      <v-col xs="10" sm="10" md="10" lg="10" offset-xs="1" offset-sm="1" offset-md="1" offset-lg="1" offset-xl="1">          
        <v-calendar
          ref="calendar"
          type="week"
          :now="focus"
          first-time=8
          interval-minutes=30
          interval-count=25
          :events="events"
          :weekdays="weekdays"
        >
          <template v-slot:event="{event}">
              <div :style="{'background-color':event.color,color:'white'}" class="fill-height pl-2">{{ event.name }}</div>
          </template>
        </v-calendar>
      </v-col>
      <v-col xs="1" sm="1" md="1" lg="1" class="sticky max-height-100 right-0">
        <v-btn @click="next" class="vertical-center left-50">Next</v-btn>
      </v-col>

    </v-row>
  </v-app>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Schedules',
  data: () => ({
    weekdays: [1,2,3,4,5],
    focus: '2020-09-01',
    events: [],
    schedules: {},
    current_schedule: 0
  }),
  methods: {
    next() {
      this.events = this.schedules[this.current_schedule == Object.keys(this.schedules).length - 1 ? 0 : this.current_schedule + 1]
      this.current_schedule = this.current_schedule == Object.keys(this.schedules).length - 1 ? 0 : this.current_schedule + 1
    },
    previous() {
      this.events = this.schedules[this.current_schedule == 0 ? Object.keys(this.schedules).length - 1 : this.current_schedule - 1]
      this.current_schedule = this.current_schedule == 0 ? Object.keys(this.schedules).length - 1 : this.current_schedule - 1
    }
  },
  mounted () {
    axios
      .get('http://localhost:5000/schedule')
      .then(response => {
        this.events = response.data[0]
        this.schedules = response.data
      })
  }
}
</script>

<style lang="scss">
  .my-event {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    border-radius: 2px;
    background-color: #1867c0;
    color: #ffffff;
    border: 1px solid #1867c0;
    font-size: 12px;
    padding: 3px;
    cursor: pointer;
    margin-bottom: 1px;
    left: 4px;
    margin-right: 8px;
    position: relative;

    &.with-time {
      position: absolute;
      right: 4px;
      margin-right: 0px;
    }
  }

  .v-calendar-daily_head-day-label {
    //display: none !important;
  }

  .border-red {
    border: 2px solid red;
  }

  .vertical-center {
    margin: 0;
    position: fixed;
    top: 50%;
    -ms-transform: translate(-50%, -50%);
    transform: translate(-50%, -50%);
  }

  .left-50
  {
    left: 50%;
  }

  .right-0
  {
    right: 0;
  }

  .max-height-100
  {
    height: 100vh;
    max-height: 100vh !important;
  }

  .sticky
  {
    position:fixed;
  }
</style>
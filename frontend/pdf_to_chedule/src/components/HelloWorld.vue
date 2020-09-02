<template>
  <v-app>
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
  </v-app>
</template>

<script>
  export default {
    name: 'HelloWorld',
    data: () => ({
      weekdays: [1,2,3,4,5],
      focus: '2020-09-01',
      events:
      [
        {
          name: 'test',
          start: '2020-09-01 10:00:00',
          end: '2020-09-01 11:30:00',
          color: 'red',
        },
        {
          name: 'test',
          start: '2020-09-02 10:00:00',
          end: '2020-09-02 11:30:00',
          color: 'red',
        },
        {
          name: 'test',
          start: '2020-09-03 10:00:00',
          end: '2020-09-03 11:30:00',
          color: 'red',
        },
      ]
    }),
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
</style>
<template>
  <div>
    <h1>List of petrolstations in your surrounding</h1>
    <div v-if="apiCallError">Error contacting server</div>
    <table>
      <tr>
        <th @click="SortStationsAlphabetically">Name</th>
        <th @click="SortStationsByPricePerLiter">Price per liter</th>
        <!-- TODO: Add some kind of icon that shows which column is currently sorted and in which way -->
        <th @click="SortStationsByOverallPrice">Price overall</th>
        <th @click="SortStationsByTravelTime">Estimated travel time</th>
        <th @click="SortStationsByDistance">Distance</th>
      </tr>
      <!-- TODO: Make table sortable by each column -->
      <!-- TODO: Add a popup with details about each station -->
      <tr v-for="station in getStations" :key="station.id">
        <td>{{ station.name }}</td>
        <td>{{ station.price }}</td>
        <td>{{ station.price_overall | formatToTwoDecimals }}</td>
        <td>{{ station.duration.text }}</td>
        <td>{{ station.distance.text }}</td>
      </tr>
    </table>
  </div>
</template>

<script>
import { mapGetters, mapMutations } from 'vuex';
// import store from '../store/index';
export default {
  computed: mapGetters(['apiCallError', 'getStations']),
  methods: {
    ...mapMutations(['SortStationsByPricePerLiter', 'SortStationsByOverallPrice', 'SortStationsByTravelTime', 'SortStationsByDistance', 'SortStationsAlphabetically' ]),
  },
  data: {
    
  },
  filters: {
    formatToTwoDecimals: (value) => {
      const num = parseFloat(value);
      return num.toFixed(2);
    },
  },
};
</script>

<style>
table, th, td {
  border: 1px solid black;
  border-collapse: collapse;
}
</style>

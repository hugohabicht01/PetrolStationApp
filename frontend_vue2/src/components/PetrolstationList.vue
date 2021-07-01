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
      <!-- TODO: Add a popup with details about each station -->
      <tr v-for="station in getStations" :key="station.id" @click="getDetails(station.id)">
        <td>{{ station.name }}</td>
        <td>{{ station.price }}</td>
        <td>{{ station.price_overall | formatToTwoDecimals }}</td>
        <td>{{ station.duration.text }}</td>
        <td>{{ station.distance.text }}</td>
      </tr>
    </table>
    <div>
      <h3>Details</h3>
      <div>ID: {{ detailsID }}</div>
      <div>{{ details.brand }} {{ details.name }}</div>
      <div>
        {{ details.street }} {{ details.houseNumber }}, {{ details.postCode }} {{ details.place }}
      </div>
      <!-- TODO: Colour it green/red -->
      <div>{{ details.isOpen ? 'Open' : 'Closed' }}</div>
      <span>Diesel: {{ details.diesel }} </span>
      <span>Super E5: {{ details.e5 }} </span>
      <span>Super E10: {{ details.e10 }}</span>
    </div>
  </div>
</template>

<script>
import { mapState, mapGetters, mapMutations } from 'vuex';
import store from '../store/index';
export default {
  computed: {
    ...mapGetters(['apiCallError', 'getStations']),
    ...mapState(['detailsID', 'details']),
  },
  methods: {
    ...mapMutations([
      'SortStationsByPricePerLiter',
      'SortStationsByOverallPrice',
      'SortStationsByTravelTime',
      'SortStationsByDistance',
      'SortStationsAlphabetically',
    ]),
    getDetails(id) {
      store.commit('setDetailsID', id);
      store.dispatch('detailsPetrolStation');
    },
  },
  data: {},
  filters: {
    formatToTwoDecimals: (value) => {
      const num = parseFloat(value);
      return num.toFixed(2);
    },
  },
};
</script>

<style>
table,
th,
td {
  border: 1px solid black;
  border-collapse: collapse;
}
</style>

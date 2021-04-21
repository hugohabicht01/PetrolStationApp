<template>
  <div>
    <h1>List of petrolstations in your surrounding</h1>
    <div v-if="!apiCallSuccess">Error contacting server</div>
    <table>
      <tr>
        <th>Name</th>
        <th>Price per liter</th>
        <th>Price overall</th>
        <th>Estimated travel time</th>
        <th>Distance</th>
      </tr>
      <!-- TODO: Make table sortable by each column -->
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
import { mapGetters } from 'vuex';
// import store from '../store/index';
export default {
  computed: mapGetters(['apiCallSuccess', 'getStations']),
  filters: {
    formatToTwoDecimals: (value) => {
      const num = parseFloat(value);
      return num.toFixed(2);
    },
  },
};
</script>

<style></style>

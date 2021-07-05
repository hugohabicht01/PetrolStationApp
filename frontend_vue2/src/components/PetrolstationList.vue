<template>
  <div>
    <h1>{{ $t('PetrolStationList.heading') }}</h1>
    <div v-if="apiCallError">{{ $t('PetrolStationList.apiCallError')}}</div>
    <table>
      <tr>
        <th @click="SortStationsAlphabetically">{{ $t('PetrolStationList.name') }}</th>
        <th @click="SortStationsByPricePerLiter">{{ $t('PetrolStationList.pricePerLiter') }}</th>
        <!-- TODO: Add some kind of icon that shows which column is currently sorted and in which way -->
        <th @click="SortStationsByOverallPrice">{{ $t('PetrolStationList.priceOverall') }}</th>
        <th @click="SortStationsByTravelTime">{{ $t('PetrolStationList.estimatedTime') }}</th>
        <th @click="SortStationsByDistance">{{ $t('PetrolStationList.distance') }}</th>
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
    <!-- TODO: Make this a separate component instead -->
    <!-- 
    TODO: Instead of fetching details about each station on demand,
    just fetch details of all stations in advance to avoid loading delays 
    -->
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
    ...mapGetters(['getStations']),
    ...mapState(['detailsID', 'details', 'apiCallError']),
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

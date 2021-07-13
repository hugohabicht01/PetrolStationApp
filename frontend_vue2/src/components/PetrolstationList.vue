<template>
  <div>
    <h1>{{ $t('PetrolStationList.heading') }}</h1>
    <div v-if="apiCallError">{{ $t('PetrolStationList.apiCallError') }}</div>
    <table>
      <tr>
        <th @click="SortStationsAlphabetically">{{ $t('PetrolStationList.name') }}</th>
        <th @click="SortStationsByPricePerLiter">{{ $t('PetrolStationList.pricePerLiter') }}</th>
        <!-- TODO: Add some kind of icon that shows which column is currently sorted and in which way -->
        <th @click="SortStationsByOverallPrice">{{ $t('PetrolStationList.priceOverall') }}</th>
        <th @click="SortStationsByTravelTime">{{ $t('PetrolStationList.estimatedTime') }}</th>
        <th @click="SortStationsByDistance">{{ $t('PetrolStationList.distance') }}</th>
      </tr>
      <tr v-for="station in getStations" :key="station.id" @click="stationID = station.id">
        <td>{{ station.name }}</td>
        <td>{{ station.price }}</td>
        <td>{{ station.price_overall | formatToTwoDecimals }}</td>
        <td>{{ station.duration.text }}</td>
        <td>{{ station.distance.text }}</td>
      </tr>
    </table>
    <!-- 
    TODO: Instead of fetching details about each station on demand,
    just fetch details of all stations in advance to avoid loading delays 
    -->
    <Details :stationID="stationID" v-if="stationID.length !== 0"></Details>
  </div>
</template>

<script>
import { mapState, mapGetters, mapMutations } from 'vuex';
import Details from '@/components/Details.vue';

export default {
  computed: {
    ...mapGetters(['getStations', 'coords']),
    ...mapState(['apiCallError', 'apiURL', 'place']),
  },
  methods: {
    ...mapMutations([
      'SortStationsByPricePerLiter',
      'SortStationsByOverallPrice',
      'SortStationsByTravelTime',
      'SortStationsByDistance',
      'SortStationsAlphabetically',
    ]),
  },
  data: () => ({
    stationID: ""
  }),
  filters: {
    formatToTwoDecimals: (value) => {
      const num = parseFloat(value);
      return num.toFixed(2);
    },
  },
  components: {
    Details,
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

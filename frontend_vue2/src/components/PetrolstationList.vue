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
      <tr v-for="station in getStations" :key="station.id" @click="getDetails(station.id)">
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
    <Details :details="details" v-if="details !== undefined" :err="detailsError"> </Details>
  </div>
</template>

<script>
import { mapState, mapGetters, mapMutations } from 'vuex';
import store from '../store/index';
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
    getDetails(id) {
      // store.commit('setDetailsID', id);
      // store.dispatch('detailsPetrolStation');
      let url = new URL('details', this.apiURL);
      url.searchParams.append('id', id);

      fetch(url)
        .then((resp) => resp.json())
        .then((data) => (this.details = data.details))
        .then((this.showDetails = true))
        .then(() => {
          // This is only needed once,
          // but the event handler destructs itself after the first time
          // so the event will just go into the void
          const setupDirections = new CustomEvent('setup-directions');
          document.dispatchEvent(setupDirections);

          // Show directions in map
          let self = this;
          const renderDirections = new CustomEvent('render-directions', {
            detail: {
              start: self.place.formatted_address,
              end: `${self.details.place} ${self.details.street} ${self.details.houseNumber}`,
            },
          });
          document.dispatchEvent(renderDirections);
        })
        .catch((err) => {
          console.log(err);
          this.detailsError = 'Failed to fetch details';
        });
    },
  },
  data: () => ({
    details: undefined,
    detailsError: '',
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

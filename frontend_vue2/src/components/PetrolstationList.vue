<template>
  <div v-if="getStations.length" class="lg:flex lg:flex-row lg:items-start">
    <!-- TODO: When no data has been loaded yet, hide Componenent -->
    <!-- <h1>{{ $t('PetrolStationList.heading') }}</h1> -->
    <div v-if="apiCallError">{{ $t('PetrolStationList.apiCallError') }}</div>
    <!-- TODO: Add some kind of icon that shows which column is currently sorted and in which way -->
    <div class="border border-sky-300 rounded-md m-2 overflow-x-auto max-w-max">
      <table class="text-blue-500">
        <tr class="bg-gradient-to-br from-sky-200 to-blue-200 text-left border-sky-300">
          <th @click="SortStationsAlphabetically" class="py-2 px-2">
            {{ $t('PetrolStationList.name') }}
          </th>
          <th @click="SortStationsByPricePerLiter" class="py-2 px-2">
            {{ $t('PetrolStationList.pricePerLiter') }}
          </th>
          <th @click="SortStationsByOverallPrice" class="py-2 px-2">
            {{ $t('PetrolStationList.priceOverall') }}
          </th>
          <th @click="SortStationsByTravelTime" class="py-2 px-2">
            {{ $t('PetrolStationList.estimatedTime') }}
          </th>
          <th @click="SortStationsByDistance" class="py-2 px-2">
            {{ $t('PetrolStationList.distance') }}
          </th>
        </tr>
        <!-- TODO: Highlight the currently selected station -->
        <tr
          v-for="station in getStations"
          :key="station.id"
          @click="setStationID(station.id)"
          class="text-left border-t border-sky-300"
        >
          <td class="p-2 border-t border-sky-300">{{ station.name }}</td>
          <td class="p-2 border-t border-sky-300">{{ station.price }}</td>
          <td class="p-2 border-t border-sky-300">
            {{ station.price_overall | formatToTwoDecimals }}
          </td>
          <td class="p-2 border-t border-sky-300">{{ station.duration.text }}</td>
          <td class="p-2 border-t border-sky-300">{{ station.distance.text }}</td>
        </tr>
      </table>
    </div>
    <Details :stationID="stationID" v-if="stationID.length !== 0" ref="details"></Details>
  </div>
</template>

<script>
import { mapState, mapGetters, mapMutations } from 'vuex';
import Details from '@/components/Details.vue';

export default {
  computed: {
    ...mapGetters(['getStations']),
    ...mapState(['apiCallError']),
  },
  methods: {
    ...mapMutations([
      'SortStationsByPricePerLiter',
      'SortStationsByOverallPrice',
      'SortStationsByTravelTime',
      'SortStationsByDistance',
      'SortStationsAlphabetically',
    ]),
    // TODO: Maybe move this into the Details component
    setStationID(id) {
      this.stationID = id;
      // Wait for the Details component to render
      setTimeout(this.$refs.details.$el.scrollIntoView({behavior: "smooth", block: "center"}), 500);
    }
  },
  data: () => ({
    stationID: '',
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

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
            <div class="flex">
              {{ $t('PetrolStationList.name') }}
              <div v-show="sorting.name !== 'UNSORTED'">
                <arrow-down-icon v-if="sorting.name == 'ASCENDING'" />
                <arrow-up-icon v-if="sorting.name == 'DESCENDING'" />
              </div>
            </div>
          </th>
          <th @click="SortStationsByPricePerLiter" class="py-2 px-2">
            <div class="flex">
              {{ $t('PetrolStationList.pricePerLiter') }}
              <div v-show="sorting.price !== 'UNSORTED'">
                <arrow-down-icon v-if="sorting.price == 'ASCENDING'" />
                <arrow-up-icon v-if="sorting.price == 'DESCENDING'" />
              </div>
            </div>
          </th>
          <th @click="SortStationsByOverallPrice" class="py-2 px-2">
            <div class="flex">
              {{ $t('PetrolStationList.priceOverall') }}
              <div v-show="sorting.price_overall !== 'UNSORTED'">
                <arrow-down-icon v-if="sorting.price_overall == 'ASCENDING'" />
                <arrow-up-icon v-if="sorting.price_overall == 'DESCENDING'" />
              </div>
            </div>
          </th>
          <th @click="SortStationsByTravelTime" class="py-2 px-2">
            <div class="flex">
              {{ $t('PetrolStationList.estimatedTime') }}
              <div v-show="sorting.duration !== 'UNSORTED'">
                <arrow-down-icon v-if="sorting.duration == 'ASCENDING'" />
                <arrow-up-icon v-if="sorting.duration == 'DESCENDING'" />
              </div>
            </div>
          </th>
          <th @click="SortStationsByDistance" class="py-2 px-2">
            <div class="flex">
              {{ $t('PetrolStationList.distance') }}
              <div v-show="sorting.distance !== 'UNSORTED'">
                <arrow-down-icon v-if="sorting.distance == 'ASCENDING'" />
                <arrow-up-icon v-if="sorting.distance == 'DESCENDING'" />
              </div>
            </div>
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
import ArrowUpIcon from 'vue-material-design-icons/ArrowUp.vue';
import ArrowDownIcon from 'vue-material-design-icons/ArrowDown.vue';
import 'vue-material-design-icons/styles.css';

export default {
  computed: {
    ...mapGetters(['getStations']),
    ...mapState(['apiCallError', 'sorting']),
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
      setTimeout(
        this.$refs.details.$el.scrollIntoView({ behavior: 'smooth', block: 'center' }),
        500
      );
    },
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
    ArrowUpIcon,
    ArrowDownIcon,
  },
};
</script>

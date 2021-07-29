<template>
  <div class="petrolstations">
    <!-- <h2>{{ $t('SearchForm.heading') }}</h2> -->
    <form class="flex flex-col w-full p-4">
      <div class="flex flex-row items-center justify-between">
        <label for="petroltypes">{{ $t('SearchForm.petrol') }}:</label>
        <select
          id="petroltypes"
          name="petroltypes"
          v-model="petroltype"
          class="bg-gray-200 rounded-sm"
        >
          <option disabled value="">{{ $t('SearchForm.selectPlaceholder') }}</option>
          <option value="diesel">Diesel</option>
          <option value="e5">Super E5</option>
          <option value="e10">Super E10</option>
        </select>
      </div>
      <br />
      <div class="flex flex-row items-center justify-between">
        <label for="radiusslider" class="flex-grow">{{ $t('SearchForm.radius') }}:</label>
        <input
          type="range"
          name="radiusslider"
          id="radiusslider"
          min="0.5"
          max="20.0"
          step="0.5"
          v-model="radius"
        />
        <label for="radiusslider" class="w-16 text-right"
          >{{ radius | formatToOneDecimal }} km</label
        >
      </div>
      <br />
      <div class="flex flex-row items-center justify-between">
        <label for="tankfillslider" class="flex-grow">{{ $t('SearchForm.tankfill') }}:</label>
        <input
          type="range"
          name="tankfillslider"
          id="tankfillslider"
          min="5"
          max="120"
          step="5"
          v-model="tankfill"
        />
        <label for="tankfillslider" class="w-16 text-right">{{ tankfill }} litre</label>
      </div>
      <button
        @click.prevent="showAdvanced = !showAdvanced"
        class="w-max self-center text-warmgray-600 text-sm flex flex-col"
      >
        {{ showAdvanced ? $t('SearchForm.hideAdvanced') : $t('SearchForm.showAdvanced') }}
        <chevron-down-icon class="self-center" v-if="!showAdvanced" />
        <chevron-up-icon class="self-center" v-if="showAdvanced" />
      </button>
      <div class="advancedOptions" v-show="showAdvanced">
        <div class="flex flex-row items-center justify-between">
          <label for="avgConsumptionCity">{{ $t('SearchForm.avgConsumptionCity') }}</label>
          <input
            type="range"
            name="avgConsumptionCity"
            id="avgConsumptionCity"
            min="3.0"
            max="25.0"
            step="0.2"
            v-model="avgConsumptionCity"
            class="justify-self-end"
          />
          <label for="avgConsumptionCity">
            {{ avgConsumptionCity | formatToOneDecimal }}
          </label>
        </div>
        <div class="flex flex-row items-center justify-between">
          <label for="avgConsumptionMotorway">{{ $t('SearchForm.avgConsumptionMotorway') }}</label>
          <input
            type="range"
            name="avgConsumptionMotorway"
            id="avgConsumptionMotorway"
            min="3.0"
            max="25.0"
            step="0.2"
            v-model="avgConsumptionMotorway"
          />
          <label for="avgConsumptionMotorway">
            {{ avgConsumptionMotorway | formatToOneDecimal }}
          </label>
        </div>
      </div>
      <button
        class="btn btn-primary self-center disabled:opacity-50 disabled:cursor-not-allowed mt-5"
        @click.prevent="searchForStations"
        :disabled="petroltype === '' || !foundCoordinates"
      >
        {{ $t('SearchForm.btnSearch') }}
      </button>
    </form>
  </div>
</template>

<script>
import store from '../store/index';
import { mapGetters } from 'vuex';
import ChevronDownIcon from 'vue-material-design-icons/ChevronDown.vue';
import ChevronUpIcon from 'vue-material-design-icons/ChevronUp.vue'

export default {
  data() {
    return {
      petroltype: '',
      radius: 2.0,
      tankfill: 20,
      showAdvanced: false,
      avgConsumptionCity: 12.0,
      avgConsumptionMotorway: 7.2,
    };
  },
  components: {
    ChevronDownIcon,
    ChevronUpIcon
  },
  methods: {
    searchForStations() {
      store.commit('setFormData', {
        petroltype: this.petroltype,
        radius: this.radius,
        tankfill: this.tankfill,
        avgConsumptionCity: this.avgConsumptionCity,
        avgConsumptionMotorway: this.avgConsumptionMotorway,
      });
      store.dispatch('findPetrolStations');
    },
  },
  computed: {
    ...mapGetters(['foundCoordinates']),
  },
  filters: {
    formatToOneDecimal: (value) => {
      const num = parseFloat(value);
      return num.toFixed(1);
    },
  },
};
</script>

<style lang="scss" scoped>
// TODO: Add some proper CSS,
// this is just temporary styling so that I can see multiple components on the site

// .petrolstations {
//   display: flex;
//   flex-direction: column;
//   width: min-width;
// }
// .form {
//   display: flex;
//   flex-direction: column;
//   width: 100%;
//   max-width:400px;
// }
// .radiusvalue {
//   flex-basis: 80px;
// }
// .flex flex-row items-center justify-between {
//   display: flex;
//   flex-direction: row;
//   justify-content: space-between;
//   align-items: center;
// }
</style>

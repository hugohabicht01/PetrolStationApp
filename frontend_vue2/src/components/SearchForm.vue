<template>
  <div class="petrolstations">
    <h2>{{ $t('SearchForm.heading') }}</h2>
    <form class="form">
      <div class="forminputs">
        <label for="petroltypes">{{ $t('SearchForm.petrol') }}:</label>
        <select id="petroltypes" name="petroltypes" v-model="petroltype">
          <option disabled value="">{{ $t('SearchForm.selectPlaceholder') }}</option>
          <option value="diesel">Diesel</option>
          <option value="e5">Super E5</option>
          <option value="e10">Super E10</option>
        </select>
      </div>
      <br />
      <div class="forminputs">
        <label for="radiusslider">{{ $t('SearchForm.radius') }}:</label>
        <input
          type="range"
          name="radiusslider"
          id="radiusslider"
          min="0.5"
          max="20.0"
          step="0.5"
          v-model="radius"
        />
        <label for="radiusslider" class="radiusvalue">{{ radius | formatToOneDecimal }} km</label>
      </div>
      <br />
      <div class="forminputs">
        <label for="tankfillslider">{{ $t('SearchForm.tankfill') }}:</label>
        <input
          type="range"
          name="tankfillslider"
          id="tankfillslider"
          min="5"
          max="120"
          step="5"
          v-model="tankfill"
        />
        <label for="tankfillslider">{{ tankfill }} litre</label>
      </div>
      <!-- <input
        type="button"
        @click="showAdvanced = !showAdvanced"
        :value="advancedOptionsButtonText"
        id="btnAdvancedOptions"
      /> -->
      <button @click.prevent="showAdvanced = !showAdvanced" id="btnAdvancedOptions">
        {{ showAdvanced ? $t('SearchForm.hideAdvanced') : $t('SearchForm.showAdvanced') }}
      </button>
      <div class="advancedOptions" v-show="showAdvanced">
        <div class="forminputs">
          <label for="avgConsumptionCity">{{ $t('SearchForm.avgConsumptionCity') }}</label>
          <input
            type="range"
            name="avgConsumptionCity"
            id="avgConsumptionCity"
            min="3.0"
            max="25.0"
            step="0.2"
            v-model="avgConsumptionCity"
          />
          <label for="avgConsumptionCity">
            {{ avgConsumptionCity | formatToOneDecimal }}
          </label>
        </div>
        <div class="forminputs">
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
      <div>
        <input
          type="button"
          :value="$t('SearchForm.btnSearch')"
          @click="searchForStations"
          :disabled="petroltype === ''"
        />
      </div>
    </form>
  </div>
</template>

<script>
import store from '../store/index';

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
    // advancedOptionsButtonText() {
    //   return this.showAdvanced ? $t('SearchForm.hideAdvanced') : $t('SearchForm.showAdvanced');
    // },
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
$form-width: 400px;

.petrolstations {
  display: flex;
  flex-direction: column;
  width: min-width;
}
.form {
  display: flex;
  flex-direction: column;
  width: 100%;
  max-width: $form-width;
}
.radiusvalue {
  flex-basis: 80px;
}
.forminputs {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
}
#btnAdvancedOptions {
  justify-self: center;
  width: 50%;
}
</style>

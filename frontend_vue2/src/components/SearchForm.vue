<template>
  <div class="petrolstations">
    <h2>Find petrol stations in your surrounding</h2>
    <form class="form">
      <div class="forminputs">
        <label for="petroltypes">Petrol:</label>
        <select id="petroltypes" name="petroltypes" v-model="petroltype">
          <option disabled value="">Please select one</option>
          <option value="diesel">Diesel</option>
          <option value="e5">Super E5</option>
          <option value="e10">Super E10</option>
        </select>
      </div>
      <br />
      <div class="forminputs">
        <label for="radiusslider">Radius:</label>
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
        <label for="tankfillslider">Fuel:</label>
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
      <input
        type="button"
        @click="showAdvanced = !showAdvanced"
        :value="advancedOptionsButtonText"
      />
      <div class="advancedOptions" v-show="showAdvanced">
        <div class="forminputs">
          <label for="avgConsumptionCity">Average fuelconsumption in city traffic</label>
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
          <label for="avgConsumptionMotorway">Average fuelconsumption on motorway</label>
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
          value="Start the search!"
          @click="searchForStations"
          :disabled="petroltype === ''"
        />
      </div>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      petroltype: '',
      radius: 2.0,
      tankfill: 20,
      showAdvanced: false,
      avgConsumptionCity: 0.0,
      avgConsumptionMotorway: 0.0,
    };
  },
  methods: {
    searchForStations() {
      console.log(`Petrol: ${this.petroltype}, Radius ${this.radius}`);
    },
  },
  computed: {
    advancedOptionsButtonText() {
      return this.showAdvanced ? 'Hide advanced options' : 'Show advanced options';
    },
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
  width: 50vw;
  box-shadow: 0px 8px 40px rgba(128, 128, 128, 0.15);
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
</style>

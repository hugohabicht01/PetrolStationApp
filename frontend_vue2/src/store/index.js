import Vue from 'vue';
import Vuex from 'vuex';
import axios from 'axios';

Vue.use(Vuex);

const store = new Vuex.Store({
  state: {
    currentCoordinates: {
      latitude: undefined,
      longitude: undefined,
      err: false,
    },
    apiData: {
      ok: undefined,
      petrolStations: [],
    },
    apiCallError: false,
    formData: {
      petroltype: '',
      radius: 2.0,
      tankfill: 20,
      showAdvanced: false,
      avgConsumptionCity: 12.0,
      avgConsumptionMotorway: 7.2,
    },
    apiURL: 'https://hugohabicht01-petrolstationapp-gw4w7jq9hj75-8000.githubpreview.dev',
  },
  mutations: {
    setCurrentCoordinates(state, coords) {
      state.currentCoordinates.latitude = coords.latitude;
      state.currentCoordinates.longitude = coords.longitude;
      state.currentCoordinates.err = coords.error;
    },
    setPetrolstations(state, apiData) {
      state.apiData.ok = apiData.ok;
      state.apiData.petrolStations = apiData.petrolStations;
    },
    setFormData(state, data) {
      state.formData = { ...data };
    },
    setAPIData(state, data) {
      state.apiData.ok = data.ok;
      state.apiData.petrolStations = data.petrolStations;
    },
    setAPICallError(state, error) {
      state.apiCallError = error
    },
    // Could possibly add a feature to sort in reverse as well
    // TODO: Refractor all of these methods into one
    SortStationsByPricePerLiter(state) {
      state.apiData.petrolStations.sort((a, b) => {
        return a.price - b.price
      })
    },
    SortStationsByOverallPrice(state) {
      state.apiData.petrolStations.sort((a, b) => {
        return a.price_overall - b.price_overall
      })
    },
    SortStationsByTravelTime(state) {
      state.apiData.petrolStations.sort((a, b) => {
        return a.duration.value - b.duration.value
      })
    },
    SortStationsByDistance(state) {
      state.apiData.petrolStations.sort((a, b) => {
        return a.distance.value - b.distance.value
      })
    },
    SortStationsAlphabetically(state) {
      state.apiData.petrolStations.sort((a, b) => a.name.localeCompare(b.name)
      )
    }
  },
  getters: {
    currentLatitude: (state) => state.currentCoordinates.latitude,
    currentLongitude: (state) => state.currentCoordinates.longitude,
    foundCoordinates(state) {
      return state.currentCoordinates.latitude && state.currentCoordinates.longitude;
    },
    errorWithGPS: (state) => state.currentCoordinates.err,
    formattedCoords: (state) => {
      const lat = state.currentCoordinates.latitude;
      const lng = state.currentCoordinates.longitude;
      return `${lat},${lng}`;
    },
    coords: (state) => ({ lat: state.currentCoordinates.latitude, lng: state.currentCoordinates.longitude }),
    apiCallError: (state) => state.apiCallError,
    getStations: (state) => state.apiData.petrolStations,
  },
  actions: {
    findPetrolStations({ commit, state }) {
      // TODO: Add some validation to make sure that
      // all data is available before sending the request

      // TODO: Add some error handling, in case the API returns errors
      axios
        .get(`${state.apiURL}/find`, {
          params: {
            lat: state.currentCoordinates.latitude,
            lng: state.currentCoordinates.longitude,
            fueltype: state.formData.petroltype,
            rad: state.formData.radius,
            tankfill: state.formData.tankfill,
            avg_city: state.formData.avgConsumptionCity,
            avg_motorway: state.formData.avgConsumptionMotorway,
          },
        })
        .then((response) => {
          commit('setAPIData', response.data);
          commit('setAPICallError', false);
        })
        .catch((error) => {
          console.log(error);
          commit('setAPICallError', error);
        })
        .then(() => console.log('Finished http request'));
    },
  },
  modules: {},
});

export default store;

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
    formData: {
      petroltype: '',
      radius: 2.0,
      tankfill: 20,
      showAdvanced: false,
      avgConsumptionCity: 12.0,
      avgConsumptionMotorway: 7.2,
    },
    apiURL: 'http://localhost:8000',
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
    apiCallSuccess: (state) => state.apiData.ok,
    getStations: (state) => state.apiData.petrolStations,
  },
  actions: {
    findPetrolStations({ commit, state }) {
      // TODO: Add some validation to make sure that
      // all data is available before sending the request
      axios
        .get(`${state.apiURL}/find/`, {
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
        })
        .catch((error) => console.log(error))
        .then(() => console.log('Finished http request'));
    },
  },
  modules: {},
});

export default store;

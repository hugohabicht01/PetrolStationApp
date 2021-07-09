import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

const store = new Vuex.Store({
  state: {
    currentCoordinates: {
      latitude: undefined,
      longitude: undefined,
      err: false,
    },
    place: {},
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
    apiURL: 'https://hugohabicht01-petrolstationapp-qg7gpjqrhgpp-8000.githubpreview.dev',
  },
  mutations: {
    setCurrentCoordinates(state, coords) {
      state.currentCoordinates.latitude = coords.latitude;
      state.currentCoordinates.longitude = coords.longitude;
      state.currentCoordinates.err = coords.error;
    },
    setPlace(state, place) {
      state.place = place
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
      state.apiCallError = false
    },
    setAPICallError(state, error) {
      state.apiCallError = error
    },
    // Could possibly add a feature to sort in reverse as well
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
    },
    setDetailsID(state, data) {
      state.detailsID = data
    },
    setDetails(state, data) {
      state.details = data.details
      state.apiCallError = false
    }
  },
  getters: {
    foundCoordinates(state) {
      return state.currentCoordinates.latitude && state.currentCoordinates.longitude;
    },
    errorWithGPS: (state) => state.currentCoordinates.err,
    coords: (state) => ({ lat: state.currentCoordinates.latitude, lng: state.currentCoordinates.longitude }),
    apiCallError: (state) => state.apiCallError,
    getStations: (state) => state.apiData.petrolStations,
  },
  actions: {
    findPetrolStations({ commit, state }) {
      // TODO: Add some validation to make sure that
      // all data is available before sending the request

      // TODO: Add some error handling, in case the API returns errors
      let url = new URL('find', state.apiURL)

      const params = {
        lat: state.currentCoordinates.latitude,
        lng: state.currentCoordinates.longitude,
        fueltype: state.formData.petroltype,
        rad: state.formData.radius,
        tankfill: state.formData.tankfill,
        avg_city: state.formData.avgConsumptionCity,
        avg_motorway: state.formData.avgConsumptionMotorway,
      }

      for (const key in params) {
        url.searchParams.append(key, params[key])
      }

      fetch(url)
      .then( resp => resp.json())
      .then( data => commit('setAPIData', data))
      .catch( err => commit('setAPICallError', err))
    },
    detailsPetrolStation({ commit, state}) {
      let url = new URL('details', state.apiURL);
      url.searchParams.append("id", state.detailsID);

      fetch(url)
      .then(resp => resp.json())
      .then(data => commit('setDetails', data))
      .catch( err => commit('setAPICallError', err))
    }
  },
  modules: {},
});

export default store;

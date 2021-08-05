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
    sorting: {
      price: 'UNSORTED',
      price_overall: 'ASCENDING',
      duration: 'UNSORTED',
      distance: 'UNSORTED',
      name: 'UNSORTED'
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
    apiURL: 'https://imposing-water-291212.ew.r.appspot.com',
  },
  mutations: {
    setCurrentCoordinates(state, coords) {
      state.currentCoordinates.latitude = coords.latitude;
      state.currentCoordinates.longitude = coords.longitude;
      state.currentCoordinates.err = coords.error;
    },
    setPlace(state, place) {
      state.place = place;
    },
    setFormData(state, data) {
      state.formData = { ...data };
    },
    setAPIData(state, data) {
      state.apiData.ok = data.ok;
      state.apiData.petrolStations = data.petrolStations;
      state.apiCallError = false;
    },
    setAPICallError(state, error) {
      state.apiCallError = error;
    },
    SortStationsByPricePerLiter(state) {
      if (state.sorting.price == 'ASCENDING' || state.sorting.price == 'UNSORTED') {
        state.apiData.petrolStations.sort((a, b) => {
          return a.price - b.price;
        })
        Object.keys(state.sorting).forEach((key) => state.sorting[key] = 'UNSORTED')
        state.sorting.price = 'DESCENDING'
      } else {
        state.apiData.petrolStations.sort((a, b) => {
          return b.price - a.price;
        });
        Object.keys(state.sorting).forEach((key) => state.sorting[key] = 'UNSORTED')
        state.sorting.price = 'ASCENDING'
      }
    },
    SortStationsByOverallPrice(state) {
      if (state.sorting.price_overall == 'ASCENDING' || state.sorting.price_overall == 'UNSORTED') {
        state.apiData.petrolStations.sort((a, b) => {
          return a.price_overall - b.price_overall;
        })
        Object.keys(state.sorting).forEach((key) => state.sorting[key] = 'UNSORTED')
        state.sorting.price_overall = 'DESCENDING'
      } else {
        state.apiData.petrolStations.sort((a, b) => {
          return b.price_overall - a.price_overall;
        });
        Object.keys(state.sorting).forEach((key) => state.sorting[key] = 'UNSORTED')
        state.sorting.price_overall = 'ASCENDING'
      }
    },
    SortStationsByTravelTime(state) {
      if (state.sorting.duration == 'ASCENDING' || state.sorting.duration == 'UNSORTED') {
        state.apiData.petrolStations.sort((a, b) => {
          return a.duration.value - b.duration.value;
        })
        Object.keys(state.sorting).forEach((key) => state.sorting[key] = 'UNSORTED')
        state.sorting.duration = 'DESCENDING'
      } else {
        state.apiData.petrolStations.sort((a, b) => {
          return b.duration.value - a.duration.value;
        });
        Object.keys(state.sorting).forEach((key) => state.sorting[key] = 'UNSORTED')
        state.sorting.duration = 'ASCENDING'
      }
    },
    SortStationsByDistance(state) {
      if (state.sorting.distance == 'ASCENDING' || state.sorting.distance == 'UNSORTED') {
        state.apiData.petrolStations.sort((a, b) => {
          return a.distance.value - b.distance.value;
        })
        Object.keys(state.sorting).forEach((key) => state.sorting[key] = 'UNSORTED')
        state.sorting.distance = 'DESCENDING'
      } else {
        state.apiData.petrolStations.sort((a, b) => {
          return b.distance.value - a.distance.value;
        });
        Object.keys(state.sorting).forEach((key) => state.sorting[key] = 'UNSORTED')
        state.sorting.distance = 'ASCENDING'
      }
    },
    SortStationsAlphabetically(state) {
      // state.apiData.petrolStations.sort((a, b) => a.name.localeCompare(b.name));
      if (state.sorting.name == 'ASCENDING' || state.sorting.name == 'UNSORTED') {
        state.apiData.petrolStations.sort((a, b) => a.name.localeCompare(b.name));
        Object.keys(state.sorting).forEach((key) => state.sorting[key] = 'UNSORTED')
        state.sorting.name = 'DESCENDING'
      } else {
        state.apiData.petrolStations.sort((a, b) => b.name.localeCompare(a.name));
        Object.keys(state.sorting).forEach((key) => state.sorting[key] = 'UNSORTED')
        state.sorting.name = 'ASCENDING'
      }
    },
    setDetailsID(state, data) {
      state.detailsID = data;
    },
    setDetails(state, data) {
      state.details = data.details;
      state.apiCallError = false;
    },
  },
  getters: {
    foundCoordinates(state) {
      return state.currentCoordinates.latitude !== undefined && state.currentCoordinates.longitude !== undefined;
    },
    errorWithGPS: (state) => state.currentCoordinates.err,
    coords: (state) => ({
      lat: state.currentCoordinates.latitude,
      lng: state.currentCoordinates.longitude,
    }),
    apiCallError: (state) => state.apiCallError,
    getStations: (state) => state.apiData.petrolStations,
    getStationsPositions: (state) => {
      if (state.apiData.ok !== true) {
        return null;
      }
      return state.apiData.petrolStations.map((station) => {
        return {
          id: station.id,
          name: station.name,
          price: station.price,
          position: {
            lat: station.lat,
            lng: station.lng,
          },
          distance: station.distance
        };
      });
    },
  },
  actions: {
    findPetrolStations({ commit, state }) {
      // TODO: Add some validation to make sure that
      // all data is available before sending the request

      // TODO: Add some error handling, in case the API returns errors
      let url = new URL('find', state.apiURL);

      const params = {
        lat: state.currentCoordinates.latitude,
        lng: state.currentCoordinates.longitude,
        fueltype: state.formData.petroltype,
        rad: state.formData.radius,
        tankfill: state.formData.tankfill,
        avg_city: state.formData.avgConsumptionCity,
        avg_motorway: state.formData.avgConsumptionMotorway,
      };

      for (const key in params) {
        url.searchParams.append(key, params[key]);
      }

      fetch(url)
        .then((resp) => resp.json())
        .then((data) => commit('setAPIData', data))
        .catch((err) => commit('setAPICallError', err));
    },
    detailsPetrolStation({ commit, state }) {
      let url = new URL('details', state.apiURL);
      url.searchParams.append('id', state.detailsID);

      fetch(url)
        .then((resp) => resp.json())
        .then((data) => commit('setDetails', data))
        .catch((err) => commit('setAPICallError', err));
    },
  },
  modules: {},
});

export default store;

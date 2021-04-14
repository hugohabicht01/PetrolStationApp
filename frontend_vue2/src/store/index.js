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
  },
  mutations: {
    setCurrentCoordinates(state, coords) {
      state.currentCoordinates.latitude = coords.latitude;
      state.currentCoordinates.longitude = coords.longitude;
      state.currentCoordinates.err = coords.error;
    },
  },
  getters: {
    currentLatitude: (state) => state.currentCoordinates.latitude,
    currentLongitude: (state) => state.currentCoordinates.longitude,
    foundCoordinates(state) {
      return state.currentCoordinates.latitude && state.currentCoordinates.longitude;
    },
    errorWithGPS: (state) => state.currentCoordinates.err,
    formattedCoords: (state) => `${state.currentCoordinates.latitude},${state.currentCoordinates.longitude}`,
  },
  actions: {},
  modules: {},
});

export default store;

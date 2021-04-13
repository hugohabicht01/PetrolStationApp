import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

const store = new Vuex.Store({
  state: {
    currentCoordinates: {
      latitude: 123,
      longitude: 456,
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
    formattedCoords: (state) => `${state.currentCoordinates.latitude},${state.currentCoordinates.longitude}`,
  },
  actions: {
  },
  modules: {
  },
});

export default store;

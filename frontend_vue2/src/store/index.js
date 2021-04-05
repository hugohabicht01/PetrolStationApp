import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    currentCoordinates: {
      latitude: 123,
      longitude: 456,
      accuracy: null,
      err: false,
    },
  },
  mutations: {
    setCurrentCoordinatesGPS(state) {
      navigator.geolocation.getCurrentPosition((pos) => {
        state.currentCoordinates.latitude = pos.coords.latitude;
        state.currentCoordinates.longitude = pos.coords.longitude;
        state.currentCoordinates.accuracy = pos.coords.accuracy;
      }, (err) => {
        console.log(`Error getting current coordinates. ERROR: ${err}`);
        state.currentCoordinates.err = true;
      });
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

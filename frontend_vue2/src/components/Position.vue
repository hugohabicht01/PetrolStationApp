<template>
  <div>
    <button @click="setPosGPS">Find my current position!</button>
    <div>or</div>
    <p>Put in your current coordinates manually</p>
    <p>
      Latitude: <input type="text" v-model="currLat" />, Longitude:
      <input type="text" v-model="currLng" />
    </p>
    <button @click="setPosManually(currLat, currLng)">Set position</button>
    <p>Latitude: {{ currentLatitude }}, Longitude: {{ currentLongitude }}</p>
    <iframe
      width="600"
      height="450"
      style="border: 0"
      loading="lazy"
      allowfullscreen
      :src="
        'https://www.google.com/maps/embed/v1/place?key=AIzaSyD6z4WhJMY85Xgc9ZIRTMbCgr1zfSIMhUg&zoom=5&q=' +
        formattedCoords
      "
    >
    </iframe>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';
import store from '../store/index';

export default {
  data: () => ({
    currLat: 0,
    currLng: 0,
  }),
  computed: mapGetters(['currentLatitude', 'currentLongitude', 'formattedCoords']),
  methods: {
    setPosGPS: () => {
      navigator.geolocation.getCurrentPosition(
        (pos) => {
          const coords = {
            latitude: pos.coords.latitude,
            longitude: pos.coords.longitude,
            error: false,
          };
          store.commit('setCurrentCoordinates', coords);
        },
        (err) => {
          console.log(`Error getting current coordinates. ERROR: ${err}`);
          const coords = { latitude: null, longitude: null, error: true };
          store.commit('setCurrentCoordinates', coords);
        },
      );
    },
    setPosManually: (lat, lng) => {
      store.commit('setCurrentCoordinates', { latitude: lat, longitude: lng, error: false });
    },
  },
};
</script>

<style lang="sass" scoped>
</style>

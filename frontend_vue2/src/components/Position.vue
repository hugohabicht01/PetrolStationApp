<template>
  <div>
    <button @click="setCurrentCoordinatesGPS">Find my current position!</button>
    <p>Latitude: {{ currentLatitude }}, Longitude: {{ currentLongitude }}</p>
    <iframe
      width="600"
      height="450"
      style="border: 0"
      loading="lazy"
      allowfullscreen
      :src="'https://www.google.com/maps/embed/v1/place?key=AIzaSyD6z4WhJMY85Xgc9ZIRTMbCgr1zfSIMhUg&q='+formattedCoords"
    >
    </iframe>
  </div>
</template>

<script>
import { mapGetters, mapMutations } from 'vuex';

export default {
  computed: mapGetters(['currentLatitude', 'currentLongitude', 'formattedCoords']),
  methods: mapMutations(['setCurrentCoordinatesGPS']),
};
</script>

<style lang="sass" scoped>
</style>

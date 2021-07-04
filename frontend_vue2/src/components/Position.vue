<template>
  <div>
    <button @click="setPosGPS">{{ $t('position.button') }}</button>
    <div v-if="errorWithGPS">{{ $t('position.GPSError') }}</div>
    <div>{{ $t('position.or') }}</div>
    <div>
      <Gmap-Autocomplete 
      :placeholder="$t('position.searchPlaceholder')" 
      @place_changed="setPlace"
      :options='{componentRestrictions: { country: "de" }}'>
      </Gmap-Autocomplete>
      <button @click="usePlace">Confirm</button>
    </div>
    <!-- TODO: Maybe show address instead of coordinates -->
    <p v-if="foundCoordinates">
      Latitude: {{ currentLatitude }}, Longitude: {{ currentLongitude }}
    </p>
    <GmapMap
      :center="{lat: 51.163361, lng:10.447683}"
      :zoom="mapZoom"
      ref="googlemap"
      style="width: 600px;height: 450px"
    >
    <!-- Middle point of Germany to center the map-->
    <GmapMarker
      :position="coords"
      v-if="foundCoordinates"
      />
    </GmapMap>
    <!-- <iframe
      width="600"
      height="450"
      style="border: 0"
      loading="lazy"
      allowfullscreen
      :src="
        'https://www.google.com/maps/embed/v1/place?key=AIzaSyD6z4WhJMY85Xgc9ZIRTMbCgr1zfSIMhUg&zoom=5&q=' +
        formattedCoords
      "
      v-if="foundCoordinates"
    >
    </iframe> -->
  </div>
</template>

<script>
import { mapGetters } from 'vuex';
import store from '../store/index';

export default {
  data: () => ({
    currLat: 0,
    currLng: 0,
    place: null,
    mapZoom: 5,
  }),
  computed: mapGetters([
    'currentLatitude',
    'currentLongitude',
    'formattedCoords',
    'coords',
    'errorWithGPS',
    'foundCoordinates',
  ]),
  methods: {
    zoomMapTo(lat, lng, zoom) {
      this.$refs.googlemap.panTo({lat, lng});
      this.mapZoom = zoom;
    },
    setPosGPS () {
      navigator.geolocation.getCurrentPosition(
        (pos) => {
          const coords = {
            latitude: pos.coords.latitude,
            longitude: pos.coords.longitude,
            error: false,
          };
          store.commit('setCurrentCoordinates', coords);
          this.zoomMapTo(coords.latitude, coords.longitude, 12);
          
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
    setPlace(place) {
      this.place = place;
    },
    usePlace(place) {
      if (this.place) {
        const lat = this.place.geometry.location.lat();
        const lng = this.place.geometry.location.lng();
        this.setPosManually(lat, lng);
        this.zoomMapTo(lat, lng, 12);
      }
    }
  },
};
</script>

<style lang="sass" scoped></style>

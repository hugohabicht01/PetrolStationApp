<template>
  <div>
    <button @click="setPosGPS">{{ $t('position.button') }}</button>
    <div v-if="errorWithGPS">{{ $t('position.GPSError') }}</div>
    <div>{{ $t('position.or') }}</div>
    <div>
      <Gmap-Autocomplete
        :placeholder="$t('position.searchPlaceholder')"
        @place_changed="setPlace"
        @keyup.enter.native="usePlace"
        :options="{ componentRestrictions: { country: 'de' } }"
        :select-first-on-enter="true"
        id="gmap-autocomplete"
      >
      </Gmap-Autocomplete>
      <button @click="usePlace">{{ $t('position.confirm') }}</button>
    </div>
    <p v-if="foundCoordinates">
      Latitude: {{ currentLatitude }}, Longitude: {{ currentLongitude }}
      Place: {{ place.formatted_address }}
    </p>
    <GmapMap
      :center="{ lat: 51.163361, lng: 10.447683 }"
      :zoom="mapZoom"
      ref="googlemap"
      style="width: 600px; height: 450px"
    >
      <!-- Middle point of Germany to center the map-->
      <GmapMarker :position="coords" v-if="foundCoordinates && !directionsRenderingMode" />
      <!-- TODO: Show marker for each station and focus them in the list when clicked on -->
    </GmapMap>
  </div>
</template>

<script>
import { mapGetters, mapState } from 'vuex';
import store from '../store/index';
import { gmapApi } from 'gmap-vue';

export default {
  data: () => ({
    currLat: 0,
    currLng: 0,
    place: null,
    mapZoom: 5,
    directionsService: {},
    directionsRenderer: {},
    directionsRenderingMode: false 
  }),
  mounted: async function () {
    let self = this;
    const setupDirections = () => {
      self.directionsService = new self.google.maps.DirectionsService();
      self.directionsRenderer = new self.google.maps.DirectionsRenderer();
      self.directionsRenderer.setMap(self.$refs.googlemap.$mapObject);

      // Once setup, it's not needed anymore
      document.removeEventListener('setup-directions', setupDirections)
    }

    document.addEventListener('setup-directions', setupDirections);

    document.addEventListener('render-directions', (e) => {
      const options = {
        origin: {
          query: e.detail.start,
        },
        destination: {
          query: e.detail.end,
        },
        travelMode: self.google.maps.TravelMode.DRIVING,
      };

      self.directionsService
      .route(
        options
      ).then((response) => {
        self.directionsRenderer.setDirections(response);
      });
      self.directionsRenderingMode = true
    });
  },
  computed: {
    ...mapGetters(['coords', 'errorWithGPS', 'foundCoordinates']),
    ...mapState({
      currentLatitude: (state) => state.currentCoordinates.latitude,
      currentLongitude: (state) => state.currentCoordinates.longitude,
    }),
    google: gmapApi,
  },
  methods: {
    zoomMapTo(lat, lng, zoom) {
      this.$refs.googlemap.panTo({ lat, lng });
      this.mapZoom = zoom;
    },
    setPosGPS() {
      navigator.geolocation.getCurrentPosition(
        (pos) => {
          const coords = {
            latitude: pos.coords.latitude,
            longitude: pos.coords.longitude,
            error: false,
          };

          store.commit('setCurrentCoordinates', coords);
          this.zoomMapTo(coords.latitude, coords.longitude, 12);
          this.directionsRenderingMode = false
          this.directionsRenderer.set('directions', null)

          // Set place to later use for directions
          const geocoder = new this.google.maps.Geocoder();
          geocoder
          .geocode({
            location: {
              lat: coords.latitude,
              lng: coords.longitude
            }
          })
          .then((response) => {
            if (response.results[0]) {
              this.place = response.results[0]
              store.commit('setPlace', response.results[0])
            } else {
              console.log("Couldn't reverse geocode coordinates")
            }
          })
          .catch((e) => console.log(`Geocoder failed due to: ${e}`))
        },
        (err) => {
          console.log(`Error getting current coordinates. ERROR: ${err}`);
          const coords = { latitude: null, longitude: null, error: true };
          store.commit('setCurrentCoordinates', coords);
        }
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
        this.directionsRenderingMode = false
        this.directionsRenderer.set('directions', null)
        store.commit('setPlace', this.place)
      }
    },
  },
};
</script>

<style lang="scss" scoped>
#gmap-autocomplete {
  width: 35%;
}
</style>

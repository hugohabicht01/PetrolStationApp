<template>
  <div>
    <button @click="setPosGPS">{{ $t('position.button') }}</button>
    <!-- TODO: Use gmap js lib to find place id, otherwise the directions map wont work!!!!! 
    Turns out, coordinates work too, so this shouldn't be needed -->

    <div v-if="errorWithGPS">{{ $t('position.GPSError') }}</div>
    <div>{{ $t('position.or') }}</div>
    <div>
      <Gmap-Autocomplete
        :placeholder="$t('position.searchPlaceholder')"
        @place_changed="setPlace"
        :options="{ componentRestrictions: { country: 'de' } }"
        id="gmap-autocomplete"
      >
      </Gmap-Autocomplete>
      <button @click="usePlace">Confirm</button>
    </div>
    <!-- TODO: Maybe show address instead of coordinates -->
    <p v-if="foundCoordinates">
      Latitude: {{ currentLatitude }}, Longitude: {{ currentLongitude }}
    </p>
    <GmapMap
      :center="{ lat: 51.163361, lng: 10.447683 }"
      :zoom="mapZoom"
      ref="googlemap"
      style="width: 600px; height: 450px"
    >
      <!-- Middle point of Germany to center the map-->
      <GmapMarker :position="coords" v-if="foundCoordinates" />
    </GmapMap>
    <div>
      Origin:<input type="text" v-model="origin" />
      <br />
      Destination: <input type="text" v-model="destination" />
      <button @click.prevent="calculateDirections(origin, destination)">Search</button>
    </div>
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
    origin: '',
    destination: '',
  }),
  mounted: async function () {
    // TODO: Nothing emits this events as of right now, fix it
    this.$root.$on('setup-directions', function () {
      let self = this;
      this.$gmapApiPromiseLazy().then(() => {
        this.$nextTick(() => {
          self.directionsService = new google.maps.DirectionsService();
          self.directionsRenderer = new google.maps.DirectionsRenderer();
          // console.log(this.$refs.googlemap);
          console.log(self.$refs.googlemap);
          // TODO: This doesn't work...
          self.directionsRenderer.setMap(self.$refs.googlemap.$mapObject);
        });
      });
    });
    // this.$root.$on('render-directions', function (start, end) {
    //   console.log(this.directionsService);
    //   console.log(this.directionsRenderer);
    //   // calculateDirections(start, end)
    //   this.directionsService
    //     .route({
    //       origin: {
    //         query: start,
    //       },
    //       destination: {
    //         query: end,
    //       },
    //       travelMode: google.maps.TravelMode.DRIVING,
    //     })
    //     .then((response) => {
    //       this.directionsRenderer.setDirections(response);
    //     });
    // });
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
    calculateDirections(start, end) {
      this.directionsService = new google.maps.DirectionsService();
      this.directionsRenderer = new google.maps.DirectionsRenderer();
      // console.log(this.$refs.googlemap);
      // console.log(self.$refs.googlemap);
      // console.log(this.$refs.googlemap.$mapObject)
      // console.log(self.$refs.googlemap.$mapObject)
      // I'm pretty sure that this isn't the actual object and that is why the directions stuff doesn't show up
      this.directionsRenderer.setMap(this.$refs.googlemap.$mapObject);

      this.directionsService
        .route({
          origin: {
            query: start,
          },
          destination: {
            query: end,
          },
          travelMode: google.maps.TravelMode.DRIVING,
        })
        .then((response) => {
          this.directionsRenderer.setDirections(response);
        });
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

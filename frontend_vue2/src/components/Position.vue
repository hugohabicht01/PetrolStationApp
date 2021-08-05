<template>
  <div class="container mx-auto rounded-sm flex flex-row flex-wrap justify-center">
    <div class="p-8 flex flex-col items-center">
      <button @click="setPosGPS" class="btn btn-primary self-center">
        {{ $t('position.button') }}
      </button>
      <div v-if="errorWithGPS">{{ $t('position.GPSError') }}</div>
      <div>{{ $t('position.or') }}</div>
      <!-- <div class="border border-gray-900 rounded-md p-1 flex flex-row"> -->
      <div class="bg-gradient-to-tl from-sky-300 to-blue-300 shadow-sm rounded-md p-2 flex flex-row">
        <Gmap-Autocomplete
          :placeholder="$t('position.searchPlaceholder')"
          @place_changed="setPlace"
          @keyup.enter.native="usePlace"
          :options="{ componentRestrictions: { country: 'de' } }"
          :select-first-on-enter="true"
          class="p-1 mr-2 w-9/12 rounded-md"
        >
        </Gmap-Autocomplete>
        <button @click="usePlace" class="btn btn-primary w-3/12 min-w-min">
          {{ $t('position.confirm') }}
        </button>
      </div>
      <p v-if="foundCoordinates">
        {{ place.formatted_address }}
      </p>
    </div>
    <!-- Middle point of Germany to center the map-->
    <GmapMap
      :center="{ lat: 51.163361, lng: 10.447683 }"
      :zoom="mapZoom"
      ref="googlemap"
      class="w-screen h-96"
    >
      <GmapInfoWindow
        :options="infoOptions"
        :position="infoWindowPos"
        :opened="infoWinOpen"
        @closeclick="infoWinOpen = false"
      >
      </GmapInfoWindow>
      <!-- TODO: Replace icon with a proper icon -->
      <GmapMarker
        :key="station.id"
        v-for="station in getStationsPositions"
        :position="station.position"
        :clickable="true"
        @click="toggleInfoWindow(station)"
        icon="https://developers.google.com/maps/documentation/javascript/examples/full/images/beachflag.png"
      ></GmapMarker>

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
    directionsRenderingMode: false,
    infoWindowPos: null,
    infoWinOpen: false,
    currentMidx: null,
    infoOptions: {
      content: '',
      //optional: offset infowindow so it visually sits nicely on top of our marker
      pixelOffset: {
        width: 0,
        height: -35,
      },
    },
  }),
  mounted: async function () {
    const setupDirections = () => {
      this.directionsService = new this.google.maps.DirectionsService();
      this.directionsRenderer = new this.google.maps.DirectionsRenderer();
      this.directionsRenderer.setMap(this.$refs.googlemap.$mapObject);

      // Once setup, it's not needed anymore
      document.removeEventListener('setup-directions', setupDirections);
    };

    document.addEventListener('setup-directions', setupDirections);

    document.addEventListener('render-directions', (e) => {
      const options = {
        origin: {
          // query: e.detail.start,
          placeId: e.detail.start,
        },
        destination: {
          query: e.detail.end,
        },
        travelMode: this.google.maps.TravelMode.DRIVING,
      };

      this.directionsService.route(options).then((response) => {
        this.directionsRenderer.setDirections(response);
      });
      this.directionsRenderingMode = true;
    });
  },
  computed: {
    ...mapGetters(['coords', 'errorWithGPS', 'foundCoordinates', 'getStationsPositions']),
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
          // If no directions have been rendered yet, don't try to erase directions
          if (this.directionsRenderingMode) {
            this.directionsRenderer.set('directions', null);
          }
          this.directionsRenderingMode = false;

          // Set place to later use for directions
          const geocoder = new this.google.maps.Geocoder();
          geocoder
            .geocode({
              location: {
                lat: coords.latitude,
                lng: coords.longitude,
              },
            })
            .then((response) => {
              if (response.results[0]) {
                this.place = response.results[0];
                store.commit('setPlace', response.results[0]);
              } else {
                console.log("Couldn't reverse geocode coordinates");
              }
            })
            .catch((e) => console.log(`Geocoder failed due to: ${e}`));
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

        if (this.directionsRenderingMode) {
          this.directionsRenderer.set('directions', null);
        }
        this.directionsRenderingMode = false;

        store.commit('setPlace', this.place);
      }
    },
    toggleInfoWindow: function (marker) {
      // TODO: Maybe get some images via google maps places API
      // or atleast provide localization
      // TODO: When opening a marker, show details with Details.vue
      // In order to do this, everything needs to be migrated to use vuex instead of component data
      const popupContent = `<h3>${marker.name}</h3>
      <div>
        <b>Price: ${marker.price}</b>
        <b>Distance: ${marker.distance.text}</b>
      </div`;

      this.infoWindowPos = marker.position;
      this.infoOptions.content = popupContent;

      //check if its the same marker that was selected if yes toggle
      if (this.currentMidx == marker.id) {
        this.infoWinOpen = !this.infoWinOpen;
      }

      //if different marker set infowindow to open and reset current marker index
      else {
        this.infoWinOpen = true;
        this.currentMidx = marker.id;
      }
    },
  },
};
</script>

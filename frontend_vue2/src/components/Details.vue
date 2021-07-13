<template>
  <div>
    <div v-if="err.length === 0 && foundDetails">
      <h3>Details</h3>
      <div>ID: {{ details.id }}</div>
      <div>{{ details.brand }} {{ details.name }}</div>
      <div>
        {{ details.street }} {{ details.houseNumber }}, {{ details.postCode }} {{ details.place }}
      </div>
      <div :class="{ open: details.isOpen, closed: !details.isOpen }">
        {{ details.isOpen ? $t('Details.open') : $t('Details.closed') }}
      </div>
      <table>
        <tr v-if="typeof details.diesel === 'number'">
          <td>Diesel</td>
          <td>{{ details.diesel }}</td>
        </tr>
        <tr v-if="typeof details.e5 === 'number'">
          <td>Super E5</td>
          <td>{{ details.e5 }}</td>
        </tr>
        <tr v-if="typeof details.e10 === 'number'">
          <td>Super E10</td>
          <td>{{ details.e10 }}</td>
        </tr>
      </table>
      <div v-if="details.openingTimes.length !== 0">
        <h4>{{ $t('Details.openingTimes') }}</h4>
        <table>
          <tr v-for="detail in details.openingTimes" :key="detail.text">
            <td>{{ detail.text }}</td>
            <td>{{ detail.start }} {{ $t('Details.until') }} {{ detail.end }}</td>
          </tr>
        </table>
      </div>
    </div>
    <div v-if="err.length !== 0">
      {{ err }}
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex';

export default {
  props: { stationID: String },
  data() {
    return {
      details: {},
      err: '',
    };
  },
  mounted() {
    this.getDetails(this.stationID);
  },
  computed: {
    ...mapState(['apiURL', 'place']),
    foundDetails() {
      return Object.keys(this.details).length !== 0;
    },
  },
  watch: {
    stationID(val) {
      this.getDetails(val);
    },
  },
  methods: {
    getDetails(id) {
      let url = new URL('details', this.apiURL);
      url.searchParams.append('id', id);

      // TODO: Add some error validation
      fetch(url)
        .then((resp) => resp.json())
        .then((data) => (this.details = data.details))
        .then(() => this.renderDirections())
        .catch((err) => {
          console.log(err);
          this.err = 'Failed to fetch details';
        });
    },
    renderDirections() {
      // This is only needed once,
      // but the event handler destructs itself after the first time
      // so the event will just go into the void
      const setupDirections = new CustomEvent('setup-directions');

      document.dispatchEvent(setupDirections);

      // Show directions in map
      let self = this;
      const renderDirections = new CustomEvent('render-directions', {
        detail: {
          start: self.place.formatted_address,
          end: `${self.details.place} ${self.details.street} ${self.details.houseNumber}`,
        },
      });

      document.dispatchEvent(renderDirections);
    },
  },
};
</script>

<style>
.open {
  color: rgb(2, 197, 2);
}
.closed {
  color: rgb(255, 43, 43);
}
</style>
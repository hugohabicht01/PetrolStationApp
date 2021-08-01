<template>
  <div
    class="
      border border-sky-300
      rounded-md
      m-2
      p-4
      overflow-x-auto
      bg-gradient-to-br
      from-sky-100
      to-blue-100
      text-left text-blue-500
      md:max-w-max
    "
  >
    <div v-if="err.length === 0 && foundDetails">
      <h3 class="text-xl font-bold">Details</h3>
      <!-- <div>ID: {{ details.id }}</div> -->
      <div>{{ details.brand }} {{ details.name }}</div>
      <div>
        {{ details.street }} {{ details.houseNumber }}, {{ details.postCode }} {{ details.place }}
      </div>
      <!-- TODO: Generate a google maps navigation link -->
      <!-- <a href="">Set as navigation target</a> -->
      <div :class="{ open: details.isOpen, closed: !details.isOpen }" class="py-4">
        {{ $t('Details.now') }} {{ details.isOpen ? $t('Details.open') : $t('Details.closed') }}
      </div>
      <div class="text-lg">{{ $t('Details.prices') }}:</div>
      <div class="border border-sky-300 rounded-md w-max">
        <table>
          <tr v-if="typeof details.diesel === 'number'" class="border-b border-sky-300">
            <td class="p-2 bg-sky-200 border-r border-sky-300">Diesel</td>
            <td class="p-2">{{ details.diesel }}</td>
          </tr>
          <tr v-if="typeof details.e5 === 'number'" class="border-b border-sky-300">
            <td class="p-2 bg-sky-200 border-r border-sky-300">Super E5</td>
            <td class="p-2">{{ details.e5 }}</td>
          </tr>
          <tr v-if="typeof details.e10 === 'number'">
            <td class="p-2 bg-sky-200 border-r border-sky-300">Super E10</td>
            <td class="p-2">{{ details.e10 }}</td>
          </tr>
        </table>
      </div>
      <div v-if="details.openingTimes.length !== 0">
        <h4 class="text-lg">{{ $t('Details.openingTimes') }}:</h4>
        <div class="border border-sky-300 rounded-md w-max">
          <table>
            <col class="bg-sky-200" />
            <tr v-for="detail in details.openingTimes" :key="detail.text" class="even:border-b border-sky-300">
              <td class="p-2 border-sky-300 border-r ">{{ detail.text }}</td>
              <td class="p-2">{{ detail.start }} {{ $t('Details.until') }} {{ detail.end }}</td>
            </tr>
          </table>
        </div>
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
        .then(() => this.err = '')
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

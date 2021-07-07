<template>
  <div>
    <h3>Details</h3>
    <div>ID: {{ details.id }}</div>
    <div>{{ details.brand }} {{ details.name }}</div>
    <div>
      {{ details.street }} {{ details.houseNumber }}, {{ details.postCode }} {{ details.place }}
    </div>
    <!-- TODO: Colour it green/red -->
    <div>{{ details.isOpen ? 'Open' : 'Closed' }}</div>
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
    <!-- TODO: Add opening times -->
    <div v-if="details.openingTimes.length !== 0">
      <h4>{{ $t('Details.openingTimes') }}</h4>
      <table>
        <tr v-for="detail in details.openingTimes" :key="detail.text">
          <td>{{ detail.text }}</td>
          <td>{{ detail.start }} {{ $t('Details.until') }} {{ detail.end }}</td>
        </tr>
      </table>
    </div>

    <div>
      <h4>{{ $t('Details.directions') }}</h4>
      <iframe
        width="600"
        height="450"
        style="border: 0"
        loading="lazy"
        allowfullscreen
        :src="generateDirectionsLink(currentPosition, details, apikey)"
      ></iframe>
    </div>
  </div>
</template>

<script>
export default {
  props: { details: Object, currentPosition: Object, apikey: String },
  methods: {
    generateDirectionsLink(curr, station, apikey) {
      /* Generates the GMaps Embed API link
      Args:
        curr: coordinates of current position
        station: coordinates of the station
        apikey: google maps api key
      Returns:
        src URL for embedded map
      */ 
      console.log(`curr: ${curr}`)
      console.log(`station: ${station}`)
      const current = `${curr.lat},${curr.lng}`
      const dest = `${station.lat},${station.lng}`

      console.log(dest)
      let url = new URL('https://www.google.com/maps/embed/v1/directions');
      const params = {
        origin: current,
        destination: dest,
        key: apikey,
      };
      for (const key in params) {
        url.searchParams.append(key, params[key]);
      }
      console.log(url.href)
      return url.href;
    },
  },
};
</script>

<style>
</style>
<template>
  <div>
    <div v-if="err.length === 0">
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
export default {
  props: { details: Object, err: String },
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
<template>
  <button @click="getLocation">Get my current location</button>
  <div
    v-if="
      state.coords.latitude !== undefined &&
      state.coords.longitude !== undefined
    "
  >
    <p>
      Latitude: {{ state.coords.latitude }}, Longitude:
      {{ state.coords.longitude }}
    </p>
    Not the right address?
    <input
      type="text"
      v-model="state.address"
      placeholder="Search for address..."
    />
  </div>
</template>

<script setup>
import { reactive } from "vue";

const state = reactive({ coords: {}, address: "" });
console.log(state.coords.latitude);
const getLocation = () =>
  navigator.geolocation.getCurrentPosition((pos) => {
    state.coords = pos.coords;
  });
</script>

<style lang="scss" scoped>
</style>
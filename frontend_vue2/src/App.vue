<template>
  <div id="app">
    <Position />
    <Petrolstations />
  </div>
</template>

<script>
import Position from './components/Position.vue';
import Petrolstations from './components/Petrolstations.vue';

export default {
  name: 'App',
  components: {
    Position,
    Petrolstations,
  },
};
</script>

<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>

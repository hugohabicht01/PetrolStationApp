<template>
  <div id="app">
    <img alt="Vue logo" src="./assets/logo.png">
    <Position/>
  </div>
</template>

<script>
import Position from './components/Position.vue';

export default {
  name: 'App',
  components: {
    Position,
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

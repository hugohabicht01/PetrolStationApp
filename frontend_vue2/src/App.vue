<template>
  <div id="app">
    <Position style="display: none" />
    <SearchForm />
  </div>
</template>

<script>
import Position from './components/Position.vue';
import SearchForm from './components/SearchForm.vue';

export default {
  name: 'App',
  components: {
    Position,
    SearchForm,
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

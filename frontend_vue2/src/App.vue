<template>
  <div id="app">
    <h1>{{ $t('title')}}</h1>
    <Position />
    <SearchForm />
    <PetrolstationList />
  </div>
</template>

<script>
import PetrolstationList from './components/PetrolstationList.vue';
import Position from './components/Position.vue';
import SearchForm from './components/SearchForm.vue';

export default {
  name: 'App',
  components: {
    Position,
    SearchForm,
    PetrolstationList,
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

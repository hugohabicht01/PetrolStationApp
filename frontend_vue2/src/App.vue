<template>
  <div id="app" class="bg-gradient-to-l from-sky-100 to-blue-100 text-gray-900 min-h-screen">
    <Header />
    <Position />
    <SearchForm />
    <PetrolstationList />
  </div>
</template>

<script>
import PetrolstationList from './components/PetrolstationList.vue';
import Position from './components/Position.vue';
import SearchForm from './components/SearchForm.vue';
import Header from './components/Header.vue';

export default {
  name: 'App',
  components: {
    Position,
    SearchForm,
    PetrolstationList,
    Header
  },
};
</script>

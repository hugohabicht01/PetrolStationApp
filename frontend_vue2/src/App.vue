<template>
  <div id="app">
    <h1 class="text-lg">{{ $t('title') }}</h1>
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
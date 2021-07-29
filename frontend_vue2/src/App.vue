<template>
  <div id="app" class="bg-gradient-to-l from-sky-100 to-blue-100 text-gray-900">
    <h1 class="text-xl bg-gradient-to-r from-sky-200 to-blue-200 px-4 py-5">{{ $t('title') }}</h1>
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
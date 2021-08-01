<template>
  <div class="btn btn-primary flex">
    <translate-icon />
    <!-- Current locale: {{ $i18n.locale }}
      Available locales: {{ $i18n.availableLocales }} -->
    <select v-model="$i18n.locale" class="bg-transparent">
      <option v-for="(lang, i) in $i18n.availableLocales" :key="`Lang${i}`" :value="lang" class="bg-sky-500">
        {{ lang }}
      </option>
    </select>
  </div>
</template>

<script>
import TranslateIcon from 'vue-material-design-icons/Translate.vue';
import 'vue-material-design-icons/styles.css';

export default {
  components: {
    TranslateIcon,
  },
};
</script>

<style></style>

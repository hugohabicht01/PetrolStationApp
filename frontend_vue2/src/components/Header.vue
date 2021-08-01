<template>
  <div class="bg-gradient-to-r from-sky-200 to-blue-200 px-4 py-5 flex flex-row justify-between items-center">
    <h1 class="text-xl">{{ $t('title') }}</h1>
    <LocaleSwitcher />
  </div>
</template>

<script>
import LocaleSwitcher from '@/components/LocaleSwitcher.vue';

export default {
    components: {
        LocaleSwitcher,
    }
};
</script>
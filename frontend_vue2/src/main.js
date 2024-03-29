import Vue from 'vue';
import * as VueGoogleMaps from 'gmap-vue';
import App from './App.vue';
import store from './store';
import i18n from './i18n'
import './assets/tailwind.css'

Vue.config.productionTip = false;
Vue.use(VueGoogleMaps, {
  load: {
    key: 'AIzaSyD6z4WhJMY85Xgc9ZIRTMbCgr1zfSIMhUg',
    libraries: 'places', // This is required if you use the Autocomplete plugin
    // OR: libraries: 'places,drawing'
    // OR: libraries: 'places,drawing,visualization'
    // (as you require)
  },

  /// / If you intend to programmatically custom event listener code
  /// / (e.g. `this.$refs.gmap.$on('zoom_changed', someFunc)`)
  /// / instead of going through Vue templates (e.g. `<GmapMap @zoom_changed="someFunc">`)
  /// / you might need to turn this on.
  autobindAllEvents: true,

  /// / If you want to manually install components, e.g.
  /// / import {GmapMarker} from 'gmap-vue/src/components/marker'
  /// / Vue.component('GmapMarker', GmapMarker)
  /// / then set installComponents to 'false'.
  /// / If you want to automatically install all the components this property must be set to 'true':
  installComponents: true,
});

new Vue({
  store,
  i18n,
  render: (h) => h(App)
}).$mount('#app');

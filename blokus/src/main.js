import { createApp, Vue } from 'vue';
import App from './App.vue';

// Vuetify
import 'vuetify/styles';
import '@mdi/font/css/materialdesignicons.css';
import { createVuetify } from 'vuetify';
import * as components from 'vuetify/components';
import * as directives from 'vuetify/directives';

import router from './router';
import store from './store';

const vuetify = createVuetify({
    components,
    directives,
});

const app = createApp(App);
app.use(store);
app.use(vuetify);
app.use(router);
app.mount("#app");
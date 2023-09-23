import { createApp } from 'vue'
import { ApiClient, DefaultApi } from './api/src';
import App from './App.vue'


const app = createApp(App)
const apiLocation = "localhost:8888";

const api = new ApiClient(`http://${apiLocation}`)

const apiFactory = () => new DefaultApi(api);

app.config.globalProperties.$squareSize = 21;
app.config.globalProperties.$apiLocation = apiLocation;
app.config.globalProperties.$api = apiFactory;

app.mount('#app')

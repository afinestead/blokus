import { createApp } from 'vue'
import { ApiClient, DefaultApi } from './api/src';
import App from './App.vue'


const app = createApp(App)

const api = new ApiClient("http://localhost:8000")

const apiFactory = () => new DefaultApi(api);

app.config.globalProperties.$squareSize = 21;
app.config.globalProperties.$api = apiFactory;

app.mount('#app')

import { createApp } from 'vue'
import App from './App.vue'


const app = createApp(App)

app.config.globalProperties.$squareSize = 21;

app.mount('#app')

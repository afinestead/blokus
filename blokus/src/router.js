import { createRouter, createWebHashHistory } from 'vue-router';
import App from './App.vue';
import LobbyManager from './components/LobbyManager.vue';
import Blokus from './components/Blokus.vue';

import { useCookies } from "vue3-cookies";
const { cookies } = useCookies();

// function requireGameToken(to, from, next) {
//     console.log(cookies.get("game_id"));
    
//     // next("/lobby");
// };

const routes = [
    { path: '/', component: App },
    { path: '/lobby', component: LobbyManager },
    { path: '/play', component: Blokus },
];

const router = createRouter({
    history: createWebHashHistory(),
    routes: routes,
});

// router.beforeEach(requireGameToken);

export default router;
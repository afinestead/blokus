import { createRouter, createWebHashHistory } from 'vue-router';
import App from './App.vue';
import GameJoiner from './components/GameJoiner.vue';
import Blokus from './components/Blokus.vue';

import store from "./store"

const routes = [
    { path: '/', component: App },
    { path: '/join', component: GameJoiner },
    {
        path: '/play',
        component: Blokus,
        beforeEnter: () => {
            console.log("entering");
            return store.dispatch("getGameState")
                .then(r => {
                    if (r.status === "done") {
                        throw new Error("Game complete");
                    }
                    return true; // Else stay here
                })
                .catch(() => {
                    store.commit("setToken", null); // revoke token
                    return "/join"
                });
        },
    },
];

const router = createRouter({
    history: createWebHashHistory(),
    routes: routes,
});

// router.beforeEach(requireGameToken);

export default router;
import { createStore } from 'vuex';
import { ApiClient, DefaultApi } from './api/src/index'

const apiLocation = "localhost:8888";

const store = createStore({
    state: {
        apiLocation: apiLocation,
        api: new DefaultApi(new ApiClient(`http://${apiLocation}`)),
        token: localStorage.getItem("access_token"),
    },
    actions: {
        getCurrentPlayer({state}) {
            return state.api.getCurrentPlayerPlayerGet({tokenHeader: state.token});
        },
        joinGame({state, commit}, gameId) {
            return state.api.joinGameGameGameIdJoinPost(gameId)
                .then(r => commit("setToken", r.access_token));
        },
        getGameWebSocket({state}) {
            return new WebSocket(`ws://${state.apiLocation}/ws?token_query=${state.token}`);
        },
        placePiece({state}, placement) {
            return state.api.placePiecePlacePut(placement, {tokenHeader: state.token});
        }
    },
    mutations: {
        setToken (state, token) {
            localStorage.setItem("access_token", token);
            state.token = token;
        },
    }
})

export default store;
import { createStore } from 'vuex';
import { ApiClient, DefaultApi } from './api/src/index'

function getAPIlocation() {
    return `${window.location.hostname}:8888`;
}

const store = createStore({
    state: {
        apiLocation: getAPIlocation(),
        api: new DefaultApi(new ApiClient(`http://${getAPIlocation()}`)),
        token: localStorage.getItem("access_token"),
    },
    actions: {
        getCurrentPlayer({state}) {
            return state.api.getCurrentPlayerPlayerGet({tokenHeader: state.token});
        },
        getGameState({state}) {
            return state.api.gameStateStateGet({tokenHeader: state.token})
        },
        joinGame({state, commit}, {gameId, name, color}) {
            console.log(name, color);
            return state.api.joinGameGameGameIdJoinPost(
                gameId,
                { 
                    playerName: name,
                    color: color
                }
            )
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
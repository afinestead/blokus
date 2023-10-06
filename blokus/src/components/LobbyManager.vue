<template>
  <div class="bkgnd">
    <v-card class="lobby-card" max-width="344">
      <v-card-title class="text-center">Join an active game</v-card-title>
      <v-card-text>
        <v-responsive class="mx-auto" max-width="344">
          <v-text-field
            v-model="gameId"
            label="Game ID"
            placeholder="GAME"
            append-inner-icon="mdi-login"
            @click:append-inner="tryJoin"
            @input="gameId = gameId.toUpperCase(); errorMessage = ''"
            :error="errorMessage.length !== 0"
            :error-messages="errorMessage"
            :loading="joining"
          />
        </v-responsive>
      </v-card-text>
    </v-card>
  </div>
</template>

<script setup>
import { computed, onBeforeMount, ref } from "vue";
import { ApiClient, DefaultApi } from '../api/src/index.js'
import { useRouter } from 'vue-router';
import { useStore } from 'vuex';



const router = useRouter();
const store = useStore();

const apiLocation = "localhost:8888";
const api = new DefaultApi(new ApiClient(`http://${apiLocation}`));

const gameId = ref("");
const joining = ref(false);
const errorMessage = ref("");

onBeforeMount(() => {
  const token = store.state.token;
  if (token) {
    store.dispatch("getCurrentPlayer")
      .then(() => router.push({ path: "/play" }))
      .catch(e => {}); // Do nothing on failure- probably a stale token
  }
});

function tryJoin() {
  joining.value = true;
  store.dispatch("joinGame", gameId.value)
    .then(() => router.push({ path: "/play" }))
    .catch(e => {
      if (e.status === 409) {
        errorMessage.value = "This game is full";
      } else {
        errorMessage.value = "Unable to join game";
      }
    })
    .finally(() => joining.value = false)
}

</script>

<style scoped>
.bkgnd {
  height: 100%;
}

.lobby-card {
  margin: auto;
}
</style>
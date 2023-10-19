<template>
  <div class="bkgnd">
    Lobby :)
  </div>
</template>

<script setup>
import { onBeforeMount, onMounted, ref } from "vue";
import { useRouter } from 'vue-router';
import { useStore } from 'vuex';

const router = useRouter();
const store = useStore();

onBeforeMount(() => {
  store.dispatch("getGameState")
    .then(console.log)
    .catch(() => {});
});


</script>

<style scoped>
.bkgnd {
  height: 100%;
}

.lobby-card {
  margin: auto;
}
</style>
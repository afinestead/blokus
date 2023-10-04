<template>
  <router-view></router-view>
</template>

<script setup>
import { onBeforeMount } from "vue";
import { useCookies } from "vue3-cookies";
import { useRouter } from 'vue-router';

const { cookies } = useCookies();
const router = useRouter();

onBeforeMount(() => {
  console.log(router);

  if (!cookies.get("game_id")) {
    console.log("pusing to lobby");
    router.push({ path: "/lobby" });
  } else {
    console.log("pusing to game");
    router.push({ path: "/play" });
  }
});

</script>

<style>
#app {
  width: 100%;
  height: 100vh;
}
</style>

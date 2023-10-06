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
  if (!cookies.get("game_id")) {
    router.push({ path: "/lobby" });
  } else {
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

<template>
  <router-view></router-view>
</template>

<script setup>
import { onBeforeMount } from "vue";
import { useRouter } from 'vue-router';
import { useStore } from 'vuex';

const router = useRouter();

onBeforeMount(() => {
  router.push({ path: "/join" });
});

</script>

<style>
#app {
  width: 100%;
  height: 100vh;
}
</style>

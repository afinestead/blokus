<template>
  <div class="bkgnd">
    <router-view></router-view>
  </div>
</template>

<script setup>
import { onBeforeMount } from "vue";
import { useRouter } from 'vue-router';

const router = useRouter();

onBeforeMount(() => {
  router.push({ path: "/join" });
});

</script>

<style>

#app {
  width: 100%;
  height: 100vh;
  padding: 2em;
}

.bkgnd {
  height: 100%;
  display: flex;
}

#app:before {
  content: "";
  position: fixed;
  width: 300%;
  height: 300%;
  top: -100%;
  left: -100%;
  z-index: -1;
  background: url("./assets/blokus.svg") repeat;
  background-size: 40%;
  transform: rotate(-30deg);
}
</style>

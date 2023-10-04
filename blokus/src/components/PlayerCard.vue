<template>
  <div class="player-card">
      <span class="player-name text-h6" :style="{color: color}"> {{ name }} </span>
  </div>
</template>

<script setup>

defineProps({
  name: String,
  color: String,
});

</script>

<style scoped>
.player-card {
  padding: 0 2em;
}

.player-name {

}
</style>
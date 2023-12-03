<template>
  <div class="board-square" :style="{backgroundColor: sqColor}"/>
</template>

<script setup>

import { computed, defineProps } from 'vue';

const props = defineProps({
  owner: Number,
  colors: Object,
});

const sqColor = computed(() => (props.colors != null && props.owner != null) ? props.colors[props.owner] : '#ffffff');

</script>

<style scoped>
.board-square {
  border: 1px solid black;
  margin: 1px;
  box-sizing: border-box;
  flex: 1;
  aspect-ratio: 1 / 1;
}
</style>
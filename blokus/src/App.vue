<template>
  <!-- <HelloWorld msg="Welcome to Your Vue.js App"/> -->
  <div
    v-for="row in 20"
    :key="row"
    class="board-row"
  >
    <div
      v-for="col in 20"
      :key="col"
      class="board-square"
      :id="`r${row}-c${col}`"
    />
  </div>
</template>

<script>
// import HelloWorld from './components/HelloWorld.vue'

export default {
  name: 'App',
  components: {
    // HelloWorld
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

#board {
  border-style: double;
}

.board-row {
  display: flex;
}

.board-square {
  border: 1px solid;
  height: 20px;
  width: 20px;
}

/* .board-line {
  height: 20px;
  width: 400px;
  border-top: 2px solid;
} */
</style>

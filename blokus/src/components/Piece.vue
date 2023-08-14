<template>
    <div class="piece">
        <div
            v-for="(block, idx) in blocks"
            :key="idx"
            class="block"
            :style="{
                backgroundColor: color,
                left: `${block[0]*$squareSize}px`,
                top: `${block[1]*$squareSize}px`
            }"
            @click="bubbleClick"
        >
        </div>
    </div>
</template>

<script>
export default {
  name: 'Piece',
  props: {
    blocks: {
        type: Array,
        default: () => [],
    },
    color: {
        type: String,
        default: ""
    },
  },
  data() {
    return {
    }
  },
  mounted: function() {
  },
  methods: {
    bubbleClick(event) {
        this.$emit("click", event)
    }
  }
}
</script>

<style>
.piece {
    position: relative;
}

.block {
    position: absolute;
    border: 1px solid black;
    height: 20px;
    width: 20px;
    box-sizing: border-box;
}
</style>
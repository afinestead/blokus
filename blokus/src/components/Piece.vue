<template>
  <div
    class="piece"
    :style="{width: `${pieceLen[0]*$squareSize}px`, height: `${pieceLen[1]*$squareSize}px`}"
  >
    <div
      v-for="(block, idx) in blocksInternal"
      :key="idx"
      class="block"
      :style="{
        backgroundColor: color,
        left: `${block[0]*$squareSize}px`,
        top: `${block[1]*$squareSize}px`
      }"
      @click.stop="handlePieceClick"
      @mousedown.right="flipPiece"
      @contextmenu.prevent
    />
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
      blocksInternal: [],
      clicks: 0,
      clickTimer: null,
      dblClickDelay: 200,
      pieceLen: 0,
    }
  },
  mounted: function() {
    this.blocksInternal = this.blocks;
    
    let maxX = -Infinity;
    let maxY = -Infinity;
    for (const [x, y] of this.blocks) {
      maxX = Math.max(maxX, x);
      maxY = Math.max(maxY, y);
    }
    
    this.pieceLen = [maxX + 1, maxY + 1];
  },
  watch: {
    blocks(newBlocks) {
      this.blocksInternal = newBlocks
    }
  },
  methods: {
    handlePieceClick(evt) {
      this.clicks++;
      if (this.clicks === 1) {
        this.clickTimer = setTimeout(() => {
          this.$emit("click", evt)
          this.clicks = 0;
        }, this.dblClickDelay);
      } else {
        // Double click
        this.rotatePiece(90);
        clearTimeout(this.clickTimer);
        this.clicks = 0;
      }
    },
    translatePiece(blocks) {
      let minX = Infinity;
      let minY = Infinity;
      for (const [x, y] of blocks) {
        minX = Math.min(minX, x);
        minY = Math.min(minY, y);
      }
      return blocks.map(([x,y]) => [x-minX,y-minY]);
    },
    flipPiece() {
      const p = this.blocksInternal.map(([x,y]) => [-x,y]);
      this.blocksInternal = this.translatePiece(p);
    },
    rotatePiece(deg) {
      const rad = deg * Math.PI / 180;
      const cos = Math.cos(rad);
      const sin = Math.sin(rad);
      let p = this.blocksInternal.map(([x,y]) => [Math.round(x*cos - y*sin), Math.round(x*sin + y*cos)]);
      this.blocksInternal = this.translatePiece(p);
    },
  },
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
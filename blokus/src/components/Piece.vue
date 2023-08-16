<template>
  <div class="piece" :style="pieceStyle">
    <div
      v-for="(block, idx) in blocksInternal"
      :key="idx"
      class="block"
      :style="[
        blockStyle,
        {
          backgroundColor: color,
          left: `${block[0]*squareSize}px`,
          top: `${block[1]*squareSize}px`
        }
      ]"
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
    squareSize: {
      type: Number,
    },
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
      ss: 20,
      pieceStyle: {},
      blockStyle: {},
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

    this.pieceStyle = {
      height: `${this.pieceLen[1]*this.squareSize}px`,
      width: `${this.pieceLen[0]*this.squareSize}px`,
    }
    this.blockStyle = {
      height: `${this.squareSize-1}px`,
      width: `${this.squareSize-1}px`,
    }
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
        this.$emit("change")
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
      this.$emit("change")
    },
    rotatePiece(deg) {
      const rad = deg * Math.PI / 180;
      const cos = Math.cos(rad);
      const sin = Math.sin(rad);
      let p = this.blocksInternal.map(([x,y]) => [Math.round(x*cos - y*sin), Math.round(x*sin + y*cos)]);
      this.blocksInternal = this.translatePiece(p);
      this.$emit("change")
    },
  },
  computed: {
    cssProps() {
      return {
        "--square-size": `${this.squareSize}px`,
        "--piece-width": `${this.pieceLen[0]*this.squareSize}px`,
        "--piece-height": `${this.pieceLen[1]*this.squareSize}px`,
      }
    }
  }
}
</script>

<style scoped>
.piece {
    position: relative;
}

.block {
    position: absolute;
    border: 1px solid black;
    margin: 1px;
    box-sizing: border-box;
}
</style>
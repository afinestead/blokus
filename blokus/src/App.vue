<template>
  <div
    class="board"
    :style="{
      width: `${(boardSize*$squareSize)}px`,
      height: `${(boardSize*$squareSize)}px`
    }"
  >
    <div
      v-for="sq in boardSize**2"
      :key="sq"
      class="board-square"
      :style="{
        left: `${((sq-1)%boardSize)*$squareSize}px`,
        top: `${Math.floor((sq-1)/boardSize)*$squareSize}px`
      }"
    />
  </div>
  
  <div class="my-pieces" :style="{height: `${boardSize*$squareSize}px`}">
    <piece
      class="unplaced-piece"
      v-for="(p,idx) in myPieces"
      :key="idx"
      :color="color"
      :blocks="p"
      :style="{width: `${pieceLen(p)[0]*$squareSize}px`, height: `${pieceLen(p)[1]*$squareSize}px`}"
      @mousedown.right="flipPiece(p, idx)"
      @contextmenu.prevent
      @click.stop="handlePieceClick($event, p, idx)"
    />
  </div>

  <piece
    class="selected-piece"
    :color="color"
    :blocks="selectedPiece === null ? [] : selectedPiece.block"
    :style="{
      display: selectedPiece === null ? 'none' : 'block',
      top: `${cursorY - offsetY}px`,
      left: `${cursorX - offsetX}px`,
    }"
    @mousedown.right="flipPiece(selectedPiece.block, selectedPiece.index)"
    @contextmenu.prevent
    @click.stop="handlePieceClick($event, selectedPiece.block, selectedPiece.index)"
  />

</template>

<script>
// import HelloWorld from './components/HelloWorld.vue'
import Piece from './components/Piece.vue'

export default {
  name: 'App',
  components: {
    Piece,
  },
  data() {
    return {
      myPieces: [],
      color: "green",
      boardSize: 0,
      clicks: 0,
      clickTimer: null,
      dblClickDelay: 200,
      maxPieceLen: 0,
      selectedPiece: null,
      cursorX: null,
      offsetX: null,
      cursorY: null,
      offsetY: null,
    }
  },
  mounted: function () {
    // TODO: Fetch from API
    this.myPieces = [[[0, 1], [1, 0], [1, 1], [0, 0]], [[0, 1], [2, 1], [1, 1], [2, 0], [0, 2]], [[4, 0], [0, 0], [2, 0], [3, 0], [1, 0]], [[0, 1], [1, 2], [2, 1], [1, 1], [1, 0]], [[0, 1], [1, 0], [1, 1]], [[0, 1], [2, 1], [1, 1], [2, 0], [3, 0]], [[0, 1], [2, 1], [3, 1], [1, 1], [3, 0]], [[0, 1], [1, 2], [2, 1], [1, 1], [2, 0]], [[1, 0], [2, 0], [3, 0], [0, 0]], [[1, 0], [2, 0], [0, 0]], [[0, 1], [2, 1], [1, 1], [2, 0], [1, 0]], [[0, 1], [1, 1], [2, 0], [0, 2], [1, 0]], [[0, 1], [2, 1], [0, 0], [1, 1], [2, 0]], [[0, 1], [1, 1], [2, 0], [2, 1]], [[1, 2], [2, 1], [2, 0], [0, 2], [2, 2]], [[0, 1], [1, 0], [1, 1], [2, 1]], [[0, 0]], [[1, 0], [0, 0]], [[0, 1], [2, 1], [1, 1], [2, 0], [2, 2]], [[0, 1], [1, 0], [0, 2], [1, 1]], [[0, 1], [2, 1], [3, 1], [1, 1], [2, 0]]];
    this.maxPieceLen = Math.max(...this.myPieces.map(p => p.length));
    this.boardSize = 20;

    document.onmousemove = (event) => {
      this.cursorX = event.pageX;
      this.cursorY = event.pageY;
    };

    document.onkeydown = (event) => {
      console.log(event);
      if (event.key === "Escape") {
        if (this.selectedPiece) {
          this.dropPiece();
        }
      }
    };
  },
  methods: {
    deg2rad(deg) {
      return deg * Math.PI / 180;
    },
    translatePiece(piece) {
      let minX = Infinity;
      let minY = Infinity;
      for (const [x, y] of piece) {
        minX = Math.min(minX, x);
        minY = Math.min(minY, y);
      }
      return piece.map(([x,y]) => [x-minX,y-minY]);
    },
    rotatePiece(piece, idx, deg) {
      const rad = this.deg2rad(deg);
      const cos = Math.cos(rad);
      const sin = Math.sin(rad);
      let p = piece.map(([x,y]) => [Math.round(x*cos - y*sin), Math.round(x*sin + y*cos)]);
      this.myPieces[idx] = this.translatePiece(p);
    },
    flipPiece(piece, idx) {
      let p = piece.map(([x,y]) => [-x,y]);
      this.myPieces[idx] = this.translatePiece(p);
    },
    pieceLen(piece) {
      let maxX = -Infinity;
      let maxY = -Infinity;
      for (const [x, y] of piece) {
        maxX = Math.max(maxX, x);
        maxY = Math.max(maxY, y);
      }
      return [maxX + 1, maxY + 1];
    },
    pickupPiece(evt, piece, idx) {
      // this.myPieces.splice(idx, 1);
      const block = evt.target.parentElement;
      this.offsetX = evt.clientX - block.getBoundingClientRect().left;
      this.offsetY = evt.clientY - block.getBoundingClientRect().top;
      // console.log(offsetX, offsetY);
      this.selectedPiece = {
        block: piece,
        index: idx,
        elem: block,
      };
      block.classList.add("hidden");
    },
    dropPiece() {
      console.log("dropping");
      if (this.selectedPiece !== null) {
        this.selectedPiece.elem.classList.remove("hidden")
        this.selectedPiece = null;
      }
    },
    placePiece() {
      console.log("placing");
    },
    handlePieceClick(evt, piece, idx) {
      this.clicks++;
      if (this.clicks === 1) {
        this.clickTimer = setTimeout(() => {
          if (this.selectedPiece === null) {
            this.pickupPiece(evt, piece, idx);
          } else {
            this.placePiece();
          }
          this.clicks = 0;
        }, this.dblClickDelay);
      } else {
        // Double click
        this.rotatePiece(piece, idx, 90);
        clearTimeout(this.clickTimer);
        this.clicks = 0;
      }
    }
  }
}
</script>

<style>
#app {
  width: 100%;
}

.board {
  display: block;
  position: relative;
  float: left;
  border: 1px double black;
}

.board-square {
  position: absolute;
  box-sizing: border-box;
  border: 1px solid black;
  height: 20px;
  width: 20px;
}

.board-square:hover {
  border-color: yellow;
}

.my-pieces {
  width: 50%;
  margin-left: 2em;
  position: relative;
  float: left;
  box-sizing: border-box;
  border: 2px dotted green;
}

.unplaced-piece {
  margin: 1em;
  display: inline-block;
  width: 100%;
}

.selected-piece {
  position: absolute;
  z-index: 1000;
}

.hidden {
  visibility: hidden;
  opacity: 0;
}

/* .board-line {
  height: 20px;
  width: 400px;
  border-top: 2px solid;
} */
</style>

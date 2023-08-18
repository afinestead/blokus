<template>
  <!-- TODO:
  If a piece is rotated/flipped while hovering, the highlighting doesn't update
  -->
  <div
    ref="boardRef"
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
      :color="playerProfile.color"
      :blocks="p"
      :square-size="10"
      @click.stop="handlePieceClick($event, p, idx)"
      @contextmenu.prevent
    />
  </div>

  <piece
    class="selected-piece"
    ref="selectedPieceRef"
    :color="playerProfile.color"
    :blocks="selectedPiece === null ? [] : selectedPiece.block"
    :square-size="$squareSize"
    :style="{
      display: selectedPiece === null ? 'none' : 'block',
      top: `${cursorY + offsetY - 8 - ($squareSize / 2)}px`,
      left: `${cursorX + offsetX - 8 - ($squareSize / 2)}px`,
    }"
    @click.stop="handlePieceClick($event, selectedPiece.block, selectedPiece.index)"
    @contextmenu.prevent
    @change="$nextTick(() => snapPieceToCursor())"
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
      playerProfile: {},
      boardSize: 0,
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
    this.playerProfile = {
      id: 0,
      color: "#ff00ff",
      name: "Player 1"
    };

    document.onmousemove = (event) => {
      this.cursorX = event.pageX;
      this.cursorY = event.pageY;

      if (this.selectedPiece) {
        // find square where cursor is hovering
        const boardSqs = this.$refs.boardRef.children;
        const overlap = this.computePieceOverlap();
        this.clearHighlight();
        if (overlap) {
          overlap.forEach(overlapIdx => {
            boardSqs[overlapIdx].classList.add("highlighted");
          });
        }
      }
    };

    document.onkeydown = (event) => {
      if (event.key === "Escape") {
        if (this.selectedPiece) {
          this.dropPiece(true);
        }
      }
    };
  },
  methods: {
    snapPieceToCursor() {
      // debugger; // eslint-disable-line
      // Find left most block
      let x = Infinity;
      let y = Infinity;
      const blocks = this.$refs.selectedPieceRef.$el.children;
      for (const block of blocks) {
        const rect = block.getBoundingClientRect();
        if (rect.left < x) {
          x = rect.left;
        }
      }

      for (const block of blocks) {
        const rect = block.getBoundingClientRect();
        if (rect.left === x && rect.top <= y) {
          y = rect.top;
        }
      }
      const rect = this.$refs.selectedPieceRef.$el.getBoundingClientRect();
      this.offsetX = rect.left - x;
      this.offsetY = rect.top - y;
    },
    pickupPiece(evt, piece, idx) {
      // this.myPieces.splice(idx, 1);
      const block = evt.target.parentElement;
      if (!block.classList.contains("piece")) {
        return;
      }



      this.selectedPiece = {
        block: piece,
        index: idx,
        elem: block,
      };
      block.classList.add("hidden");
      
      this.$nextTick(() => this.snapPieceToCursor());
    },
    dropPiece(discard) {
      if (this.selectedPiece !== null) {
        if (discard) {
          this.selectedPiece.elem.classList.remove("hidden")
        }
        this.selectedPiece = null;
      }
    },
    placePiece() {
      if (this.isMyTurn()) {
        const overlap = this.computePieceOverlap();
        if (this.isPlacementValid(overlap)) {
          const boardSqs = this.$refs.boardRef.children;
          overlap.forEach(overlapIdx => {
            const sq = boardSqs[overlapIdx];
            sq.style.backgroundColor = this.playerProfile.color;
            sq.classList.add("occupied");
          });
          this.issueBoardUpdate();
          this.dropPiece(false);
        }
        
      }
    },
    handlePieceClick(evt, piece, idx) {
      if (this.selectedPiece === null) {
        this.pickupPiece(evt, piece, idx);
      } else {
          this.placePiece();
      }
    },
    clearHighlight() {
      for (const bsq of this.$refs.boardRef.children) {
        bsq.classList.remove("highlighted");
      }
    },
    computePieceOverlap() {
      const board = this.$refs.boardRef;
      const boardRect = board.getBoundingClientRect();
      const boardSqs = board.children;

      const pieces = this.$refs.selectedPieceRef.$el.children;
      let pieceCenters = [];
      for (const psq of pieces) {
        const pRect = psq.getBoundingClientRect();
        pieceCenters.push([pRect.left + (this.$squareSize / 2), pRect.top + (this.$squareSize / 2)]);
      }
      let intersection = []
      pieceCenters.forEach(psq => {
        const sqOffsetX = Math.floor((psq[0] - boardRect.left) / this.$squareSize);
        const sqOffsetY = Math.floor((psq[1] - boardRect.top) / this.$squareSize);
        if (
          sqOffsetX >= 0 && sqOffsetX < this.boardSize &&
          sqOffsetY >= 0 && sqOffsetY < this.boardSize
        ) {
          const asIdx = sqOffsetX + (sqOffsetY * this.boardSize);
          if (!boardSqs[asIdx].classList.contains("occupied")) {
            intersection.push(asIdx);
          }
        }
      });
      
      if (intersection.length === pieceCenters.length) {
        return intersection;
      }
      return [];
      // console.log(piece.children);
    },
    isMyTurn() {
      // TODO
      return true;
    },
    isPlacementValid(placement) {
      // TODO
      return placement !== null;
    },
    issueBoardUpdate() {
      // TODO
      return;
    },
  },
  watch: {
    selectedPiece(newPiece) {
      if (newPiece === null) {
        this.clearHighlight()
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
}

.board-square {
  position: absolute;
  box-sizing: border-box;
  border: 1px solid black;
  margin: 1px;
  height: 20px;
  width: 20px;
}

.highlighted {
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
}

.selected-piece {
  position: absolute;
  z-index: 1000;
}

.hidden {
  visibility: hidden;
  opacity: 0;
}
</style>

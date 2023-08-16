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
      :color="color"
      :blocks="p"
      @click.stop="handlePieceClick($event, p, idx)"
      @contextmenu.prevent
    />
  </div>

  <piece
    class="selected-piece"
    ref="selectedPieceRef"
    :color="color"
    :blocks="selectedPiece === null ? [] : selectedPiece.block"
    :style="{
      display: selectedPiece === null ? 'none' : 'block',
      top: `${cursorY - offsetY}px`,
      left: `${cursorX - offsetX}px`,
    }"
    @click.stop="handlePieceClick($event, selectedPiece.block, selectedPiece.index)"
    @contextmenu.prevent
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

    // const squares = this.$refs.board.children;
    // console.log(squares);
    console.log(this.$refs.boardRef.getBoundingClientRect());

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
      
        
        // check all square have >50% overlap
        //  find bsq center
        //  overlapped if bsq in piece
        // for (const square of squares) {
        //   console.log(square);
        // }
        // for(const piece of this.selectedPiece.elem.children) {

        // }
      }
    };

    document.onkeydown = (event) => {
      if (event.key === "Escape") {
        if (this.selectedPiece) {
          this.dropPiece();
        }
      }
    };
  },
  methods: {
    pickupPiece(evt, piece, idx) {
      // this.myPieces.splice(idx, 1);
      const block = evt.target.parentElement;
      if (!block.classList.contains("piece")) {
        return;
      }

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
      if (this.selectedPiece !== null) {
        this.selectedPiece.elem.classList.remove("hidden")
        this.selectedPiece = null;
      }
    },
    placePiece() {
      const overlap = this.computePieceOverlap();
      const boardSqs = this.$refs.boardRef.children;
      overlap.forEach(overlapIdx => {
        const sq = boardSqs[overlapIdx];
        sq.style.backgroundColor = "green";
        sq.classList.add("occupied");
      });
      
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
  },
  watch: {
    selectedPiece(newPiece) {
      console.log(newPiece);
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
  border: 1px double black;
}

.board-square {
  position: absolute;
  box-sizing: border-box;
  border: 1px solid black;
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

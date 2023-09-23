<template>
  <!-- TODO:
  If a piece is rotated/flipped while hovering, the highlighting doesn't update
  -->
  <div
    v-if="board !== null"
    ref="boardRef"
    class="board"
    :style="{
      width: `${(boardSize*$squareSize)}px`,
      height: `${(boardSize*$squareSize)}px`
    }"
  >
    <div
      v-for="sq, idx in board"
      :key="idx"
      class="board-square"
      :class="[
        sq !== null ? 'occupied' : '',
        sq !== null ? `player-${sq}` : ''
      ]"
      :style="{
        left: `${(idx%boardSize)*$squareSize}px`,
        top: `${Math.floor(idx/boardSize)*$squareSize}px`
      }"
    />

  </div>
  
  <div class="my-pieces" :style="{height: `${boardSize*$squareSize}px`}">
    <piece
      v-if="myPieces.length !== 0"
      class="unplaced-piece"
      v-for="(p,idx) in myPieces"
      :key="idx"
      :color="intToRGB(playerProfile.color)"
      :blocks="p"
      :square-size="10"
      @click.stop="handlePieceClick($event, p, idx)"
      @contextmenu.prevent
    />
  </div>

  <piece
    class="selected-piece"
    ref="selectedPieceRef"
    :color="intToRGB(playerProfile.color)"
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
import Piece from './components/Piece.vue'
import { ApiClient } from './api/src/index.js'

export default {
  name: 'App',
  components: {
    Piece,
  },
  data() {
    return {
      board: null,
      myPieces: [],
      playerProfile: {},
      gameProfile: {},
      boardSize: 0,
      maxPieceLen: 0,
      selectedPiece: null,
      cursorX: null,
      offsetX: null,
      cursorY: null,
      offsetY: null,
      ws: null,
    }
  },
  mounted: function () {
    // TODO: Fetch these from API
    const api = this.$api();
    api.getPiecesPiecesGet(4).then(r => {
      this.myPieces = r.map(p => p.shape.map(b => [b.x, b.y]));
      this.maxPieceLen = Math.max(...this.myPieces.map(p => p.length));
      
    });
    this.boardSize = 20;
    this.playerProfile = {
      player_id: 1,
      color: 0xff00ff,
      name: "Player 1",
    };
    this.gameProfile = {
      id: 0,
      players: [
        {
          player_id: 1,
          color: 0xff00ff,
          name: "Player 1",
        }
      ]
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

    const ws = new WebSocket(`ws://${this.$apiLocation}/ws`)
    ws.onmessage = (e) => {
      const msg = JSON.parse(e.data);
      if ("board" in msg) {
        this.boardSize = msg.board.length;
        this.board = msg.board.flat();
        console.log("UPDATE");
        console.log(this.board);
      }
    }
    this.ws = ws;
  },
  methods: {
    intToRGB(colorInt) {
      return colorInt != null ?
        `#${colorInt.toString(16)}` :
        "#ffffff";
    },
    idxToXY(idx) {
      return {
        x: idx % this.boardSize,
        y: Math.floor(idx / this.boardSize),
      }
    },
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
        const placement = this.computePieceOverlap();
        const boardSqs = this.$refs.boardRef.children;
        placement.forEach(placementIdx => {
          const sq = boardSqs[placementIdx];
          sq.style.backgroundColor = this.intToRGB(this.playerProfile.color);
          sq.classList.add("occupied");
          sq.classList.add(`player-${this.playerProfile.id}`);
        });
        this.issueBoardUpdate(placement);
        this.dropPiece(false);
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

      const OccupiedByMe = (idx) => boardSqs[idx].classList.contains(`player-${this.playerProfile.id}`);

      const GetNeighborIdx = (sqIdx, dir) => {
        if (sqIdx === null) {
          return null;
        }
        switch(dir) {
          case "left": return sqIdx % this.boardSize > 0 ? sqIdx - 1 : null;
          case "right": return sqIdx % this.boardSize < (this.boardSize - 1) ? sqIdx + 1 : null;
          case "up": return sqIdx - this.boardSize > 0 ? sqIdx - this.boardSize : null;
          case "down": return sqIdx + this.boardSize < this.boardSize**2 ? sqIdx + this.boardSize : null;
          default: return null;
        }
      }

      const HasSideNeighbor = (sqIdx) => {
        const leftIdx = GetNeighborIdx(sqIdx, "left");
        const rightIdx = GetNeighborIdx(sqIdx, "right");
        const upIdx = GetNeighborIdx(sqIdx, "up");
        const downIdx = GetNeighborIdx(sqIdx, "down");
        return (
          (leftIdx !== null && OccupiedByMe(leftIdx))
          || (rightIdx !== null && OccupiedByMe(rightIdx))
          || (upIdx !== null && OccupiedByMe(upIdx))
          || (downIdx !== null && OccupiedByMe(downIdx))
        );
      }

      const HasCornerNeighbor = (sqIdx) => {
        const upLeftIdx = GetNeighborIdx(GetNeighborIdx(sqIdx, "left"), "up");
        const upRightIdx = GetNeighborIdx(GetNeighborIdx(sqIdx, "right"), "up");
        const downLeftIdx = GetNeighborIdx(GetNeighborIdx(sqIdx, "left"), "down");
        const downRightIdx = GetNeighborIdx(GetNeighborIdx(sqIdx, "right"), "down");
        return (
          (upLeftIdx !== null && OccupiedByMe(upLeftIdx))
          || (upRightIdx !== null && OccupiedByMe(upRightIdx))
          || (downLeftIdx !== null && OccupiedByMe(downLeftIdx))
          || (downRightIdx !== null && OccupiedByMe(downRightIdx))
        );
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
          intersection.push(asIdx);
        }
      });

      let validCorner = false;
      for (const sq of intersection) {
        if (boardSqs[sq].classList.contains("occupied") || HasSideNeighbor(sq)) {
          return [];
        }
        validCorner = validCorner || HasCornerNeighbor(sq) || sq === 0;
      }
      if (validCorner && intersection.length === pieceCenters.length) {
        return intersection;
      }
      return [];
    },
    isMyTurn() {
      // TODO
      return true;
    },
    async isPlacementValid(placement) {
      // pick an origin and calculate (x,y) based on that
      console.log(placement);
      if (placement.length > 0) {
        const asXY = (sq) => [sq % this.boardSize, Math.round(sq / this.boardSize)];
        const origin = asXY(placement[0], this.boardSize);
        const piece = placement.reduce((acc, sq) => {
          const coord = asXY(sq, this.boardSize);
          acc.push([origin[0] - coord[0], origin[1] - coord[1]]);
          return acc;
        }, []);
        console.log(origin, piece);
      }
      return true;
    },
    translateBoard() {
      // TODO
    },
    issueBoardUpdate(piece) {
      console.log(piece);
      const origin = this.idxToXY(piece[0]);
      const shape = piece.map(tile => ({
        x: this.idxToXY(tile).x - origin.x,
        y: this.idxToXY(tile).y - origin.y
      }));
      console.log(origin);
      console.log(shape)

      const api = this.$api()
      api.placePiecePlacePut(
        this.playerProfile.player_id,
        {
          "piece": {
            "shape": shape
          },
          "origin": origin
        }
      );
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
}

.hidden {
  visibility: hidden;
  opacity: 0;
}
</style>

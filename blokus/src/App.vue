<template>
  <!-- TODO:
  If a piece is rotated/flipped while hovering, the highlighting doesn't update
  -->
  <div
    v-if="board !== null"
    ref="boardRef"
    class="board"
    :style="{
      width: `${(boardSize*squareSize)}px`,
      height: `${(boardSize*squareSize)}px`
    }"
  >
    <div
      v-for="pid, idx in board"
      :key="idx"
      class="board-square"
      :class="[
        pid !== null ? 'occupied' : '',
        pid !== null ? `player-${pid}` : ''
      ]"
      :style="{
        left: `${(idx%boardSize)*squareSize}px`,
        top: `${Math.floor(idx/boardSize)*squareSize}px`
      }"
    />

  </div>
  
  <div class="my-pieces" :style="{height: `${boardSize*squareSize}px`}">
    <piece
      v-if="myPieces.length !== 0"
      class="unplaced-piece"
      v-for="(p,idx) in myPieces"
      :key="idx"
      :color="playerColor"
      :blocks="p"
      :square-size="10"
      @click.stop="handlePieceClick($event, p, idx)"
      @contextmenu.prevent
    />
  </div>

  <piece
    class="selected-piece"
    ref="selectedPieceRef"
    :color="playerColor"
    :blocks="selectedPiece === null ? [] : selectedPiece.block"
    :square-size="squareSize"
    :style="{
      display: selectedPiece === null ? 'none' : 'block',
      top: `${cursorY + offsetY - 8 - (squareSize / 2)}px`,
      left: `${cursorX + offsetX - 8 - (squareSize / 2)}px`,
    }"
    @click.stop="handlePieceClick($event, selectedPiece.block, selectedPiece.index)"
    @contextmenu.prevent
    @change="nextTick(() => snapPieceToCursor())"
  />

</template>

<script setup>
import { nextTick, onMounted, ref, reacted, computed, watch } from 'vue'
import Piece from './components/Piece.vue'
import { ApiClient, DefaultApi } from './api/src/index.js'

const apiLocation = "localhost:8888";
const api = new DefaultApi(new ApiClient(`http://${apiLocation}`));
const squareSize = 21;


const board = ref([]);
const boardSize = ref(0);
const boardRef = ref(null)
const myPieces = ref([]);
const gameProfile = ref({});
const playerID = ref(null);
const playerColor = computed(() => {
  const colorInt = gameProfile.value?.players?.find(p => p.player_id === playerID.value)?.color;
  return colorInt != null ? `#${colorInt.toString(16)}` : "#ffffff";
});
const playerName = computed(() => gameProfile.value?.players?.find(p => p.player_id === playerID.value)?.name);
const maxPieceLen = computed(() => Math.max(...myPieces.map(p => p.length)));
const selectedPiece = ref(null);
const selectedPieceRef = ref(null);
const cursorX = ref(null);
const offsetX = ref(null);
const cursorY = ref(null);
const offsetY = ref(null);
const ws = ref(null);

onMounted(() => {
  // TODO: Fetch these from API
  api.getPiecesPiecesGet(4).then(r => {
    myPieces.value = r.map(p => p.shape.map(b => [b.x, b.y]));    
  });
  playerID.value = 1; // TODO: Fetch

  gameProfile.value = {
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
    cursorX.value = event.pageX;
    cursorY.value = event.pageY;

    if (selectedPiece.value) {
      // find square where cursor is hovering
      const boardSqs = boardRef.value.children;
      const overlap = computePieceOverlap();
      clearHighlight();
      if (overlap) {
        overlap.forEach(overlapIdx => {
          boardSqs[overlapIdx].classList.add("highlighted");
        });
      }
    }
  };

  document.onkeydown = (event) => {
    if (event.key === "Escape") {
      if (selectedPiece.value) {
        dropPiece(true);
      }
    }
  };

  const new_ws = new WebSocket(`ws://${apiLocation}/ws`)
  new_ws.onmessage = (e) => {
    const msg = JSON.parse(e.data);
    console.log(msg);
    if ("board" in msg) {
      boardSize.value = msg.board.length;
      board.value = msg.board.flat();
      console.log("UPDATE");
      console.log(board);
    }
  }
  ws.value = new_ws;
});

  
function intToRGB(colorInt) {
  return colorInt != null ?
    `#${colorInt.toString(16)}` :
    "#ffffff";
};

function idxToXY(idx) {
  return {
    x: idx % boardSize.value,
    y: Math.floor(idx / boardSize.value),
  }
};

function snapPieceToCursor() {
  // debugger; // eslint-disable-line
  // Find left most block
  let x = Infinity;
  let y = Infinity;
  const blocks = selectedPieceRef.value.$el.children;
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
  const rect = selectedPieceRef.value.$el.getBoundingClientRect();
  offsetX.value = rect.left - x;
  offsetY.value = rect.top - y;
};

async function pickupPiece(evt, piece, idx) {
  // this.myPieces.splice(idx, 1);
  const block = evt.target.parentElement;
  if (!block.classList.contains("piece")) {
    return;
  }

  selectedPiece.value = {
    block: piece,
    index: idx,
    elem: block,
  };
  block.classList.add("hidden");
  
  await nextTick();
  snapPieceToCursor();
};

function dropPiece(discard) {
  if (selectedPiece.value !== null) {
    if (discard) {
      selectedPiece.value.elem.classList.remove("hidden")
    }
    selectedPiece.value = null;
  }
};


function placePiece() {
  if (isMyTurn()) {
    const placement = computePieceOverlap();
    const boardSqs = boardRef.value.children;
    console.log(placement);
    placement.forEach(placementIdx => {
      const sq = boardSqs[placementIdx];
      sq.style.backgroundColor = playerColor.value;
      sq.classList.add("occupied");
      sq.classList.add(`player-${playerID.value}`);
    });
    issueBoardUpdate(placement);
    dropPiece(false);
  }
};

function handlePieceClick(evt, piece, idx) {
  if (selectedPiece.value === null) {
    pickupPiece(evt, piece, idx);
  } else {
      placePiece();
  }
};

function clearHighlight() {
  for (const bsq of boardRef.value.children) {
    bsq.classList.remove("highlighted");
  }
};

function computePieceOverlap() {
  const boardRect = boardRef.value.getBoundingClientRect();
  const boardSqs = boardRef.value.children;

  const pieces = selectedPieceRef.value.$el.children;
  let pieceCenters = [];
  for (const psq of pieces) {
    const pRect = psq.getBoundingClientRect();
    pieceCenters.push([pRect.left + (squareSize / 2), pRect.top + (squareSize / 2)]);
  }

  const OccupiedByMe = (idx) => boardSqs[idx].classList.contains(`player-${playerID.value}`);

  const GetNeighborIdx = (sqIdx, dir) => {
    if (sqIdx === null) {
      return null;
    }
    switch(dir) {
      case "left": return sqIdx % boardSize.value > 0 ? sqIdx - 1 : null;
      case "right": return sqIdx % boardSize.value < (boardSize.value - 1) ? sqIdx + 1 : null;
      case "up": return sqIdx - boardSize.value > 0 ? sqIdx - boardSize.value : null;
      case "down": return sqIdx + boardSize.value < boardSize.value**2 ? sqIdx + boardSize.value : null;
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
    const sqOffsetX = Math.floor((psq[0] - boardRect.left) / squareSize);
    const sqOffsetY = Math.floor((psq[1] - boardRect.top) / squareSize);
    if (
      sqOffsetX >= 0 && sqOffsetX < boardSize.value &&
      sqOffsetY >= 0 && sqOffsetY < boardSize.value
    ) {
      const asIdx = sqOffsetX + (sqOffsetY * boardSize.value);
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
};

function isMyTurn() {
  // TODO
  return true;
};

async function isPlacementValid(placement) {
  // pick an origin and calculate (x,y) based on that
  console.log(placement);
  if (placement.length > 0) {
    const asXY = (sq) => [sq % boardSize.value, Math.round(sq / boardSize.value)];
    const origin = asXY(placement[0], boardSize.value);
    const piece = placement.reduce((acc, sq) => {
      const coord = asXY(sq, boardSize.value);
      acc.push([origin[0] - coord[0], origin[1] - coord[1]]);
      return acc;
    }, []);
    console.log(origin, piece);
  }
  return true;
};

function translateBoard() {
  // TODO
};

function issueBoardUpdate(piece) {
  console.log(piece);
  const origin = idxToXY(piece[0]);
  const shape = piece.map(tile => ({
    x: idxToXY(tile).x - origin.x,
    y: idxToXY(tile).y - origin.y
  }));
  console.log(origin);
  console.log(shape)

  api.placePiecePlacePut(
    playerID.value,
    {
      "piece": {
        "shape": shape
      },
      "origin": origin
    }
  );
  return;
};

watch(boardSize, (newSize) => {console.log(newSize)});

watch(selectedPiece, (newPiece) => {
  if (newPiece === null) {
    clearHighlight()
  }
});

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

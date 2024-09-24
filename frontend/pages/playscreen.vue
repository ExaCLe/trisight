<template>
  <div class="playscreen">
    <!-- Fehlermeldung anzeigen, wenn ein Fehler beim Datenabruf auftritt -->
    <div class="error-alert" v-if="fetchError">
      Es gab ein Problem beim Abrufen der Spielkonfiguration. Bitte versuchen
      Sie es erneut.
    </div>

    <!-- Nur anzeigen, wenn isTrisightMode true ist -->
    <div class="score-timer" v-if="isTrisightMode && !isGameOver && !fetchError">
      <div class="left-side">
        <!-- Anzeige des Game Timers als numerische Zeitangabe -->
        <div class="game-timer">
          Verbleibende Zeit: {{ gameTimerDisplay }} Sekunden
        </div>
        <div class="score">Punkte: {{ score }}</div>
      </div>
      <!-- Visuelle Darstellung des Timers als Kreis -->
      <div class="timer-wrapper">
        <svg
          :width="timerSvgSize"
          :height="timerSvgSize"
          class="timer-svg"
          :viewBox="`0 0 ${timerSvgSize} ${timerSvgSize}`"
        >
          <!-- Hintergrundkreis -->
          <circle
            class="timer-background"
            :cx="timerSvgCenter"
            :cy="timerSvgCenter"
            :r="timerRadius"
          />
          <!-- Fortschrittskreis -->
          <circle
            class="timer-path"
            :cx="timerSvgCenter"
            :cy="timerSvgCenter"
            :r="timerRadius"
            :style="{ strokeDashoffset: timerDashOffset }"
          />
        </svg>
      </div>
    </div>

    <!-- Darstellung des Platzhalters oder des aktuellen Spielzustands -->
    <div class="triangle-container" v-if="!isGameOver">
      <!-- Platzhalter anzeigen, wenn das Spiel noch nicht gestartet ist -->
      <div
        v-if="!isGameStarted"
        class="circle-background placeholder"
        :style="{
          width: '200px', /* Platzhaltergröße */
          height: '200px'
        }"
      >
        <div class="triangle placeholder-triangle"></div>
      </div>

      <!-- Aktueller Spielzustand (Triangle und Circle) anzeigen, wenn das Spiel gestartet ist -->
      <div
        v-else
        class="circle-background"
        :style="{
          backgroundColor: currentItem.circle_color,
          width: limitedCircleSize + 'px',
          height: limitedCircleSize + 'px',
        }"
      >
        <div
          class="triangle"
          :style="{
            width: limitedTriangleSize + 'px',
            height: limitedTriangleSize + 'px',
            backgroundColor: currentItem.triangle_color,
            transform: getRotationStyle(currentItem.orientation).rotation,
            margin: getRotationStyle(currentItem.orientation).margin,
          }"
        ></div>
      </div>
    </div>

    <!-- Anweisungen für Benutzer -->
    <div class="instructions" v-show="!isGameStarted && !isGameOver && !fetchError">
      <span>Drücke eine Taste um zu starten!</span>
    </div>

    <!-- Spielende-Anzeige -->
    <div class="game-over" v-if="isGameOver && isTrisightMode">
      <div class="final-score">Dein Score: {{ score }}</div>
      <!-- Neue Buttons für Home und Neue Runde -->
      <div class="button-group">
        <NuxtLink to="/" class="button">Home</NuxtLink>
        <button @click="startNewRound" class="button">Neue Runde</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from "vue";
import { useRoute } from "vue-router";

// Router verwenden, um den Query-Parameter zu erhalten
const route = useRoute();
const isTrisightMode = ref(route.query.isTrisightMode === "true");
const difficulty = ref(route.query.difficulty || "easy"); // Default to 'easy'

const score = ref(0);
const currentIndex = ref(0);
const remainingTime = ref(0);
const currentItem = ref({});
const timer = ref(null);
const gameTimer = ref(null); // Neuer Timer für die Spielzeit
const totalTime = ref(0); // Speichert die Gesamtzeit für den Timer
const isGameOver = ref(false); // Neuer Zustand zur Überprüfung des Spielendes
const isGameStarted = ref(false); // Neuer Zustand zur Überprüfung, ob das Spiel gestartet wurde
const remainingGameTime = ref(60); // Verbleibende Zeit für das Spiel in Sekunden
const randomizedItems = ref([]);
const fetchError = ref(false);

// Begrenzte Größen für das Dreieck und den Kreis
const limitedTriangleSize = computed(() =>
  Math.min(300, Math.max(10, currentItem.value.triangle_size || 10))
);
const limitedCircleSize = computed(() =>
  Math.min(500, Math.max(10, currentItem.value.circle_size || 10))
);

// Berechnung des Radius und der Größe des Timer-SVGs
const timerRadius = computed(() => 50); // Feste Größe des Kreises
const timerSvgSize = computed(() => timerRadius.value * 2 + 10); // SVG-Größe basierend auf dem Radius
const timerSvgCenter = computed(() => timerRadius.value + 5); // Mittelpunkt des Kreises

// Berechnung für den visuellen Timer-Balken
const timerDashOffset = computed(() => {
  const maxDashOffset = 2 * Math.PI * timerRadius.value; // Umfang des Kreises
  return (remainingTime.value / totalTime.value) * maxDashOffset; // Rückwärtslaufender Balken
});

// Anzeige des Game Timers als numerische Zeitangabe
const gameTimerDisplay = computed(() => remainingGameTime.value);

// Funktion zum Mischen des Arrays
const shuffleArray = (array) => {
  for (let i = array.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [array[i], array[j]] = [array[j], array[i]];
  }
  return array;
};

// Timer-Logik für das Trisight Mode Spiel
const startGameTimer = () => {
  clearInterval(gameTimer.value);
  gameTimer.value = setInterval(() => {
    if (remainingGameTime.value > 0) {
      remainingGameTime.value -= 1;
    } else {
      clearInterval(gameTimer.value);
      endGame(); // Beendet das Spiel, wenn die Zeit abgelaufen ist
    }
  }, 1000); // Der Timer reduziert sich jede Sekunde
};

// Funktion zum Abrufen der Daten basierend auf dem Schwierigkeitsgrad
const fetchData = async () => {
  try {
    let endpoint;
    console.log(process, process.env)
    if (isTrisightMode.value) {
      switch (difficulty.value) {
        case "medium":
          endpoint = `${process.env.BACKENDURL}/api/test_configs/3`;
          break;
        case "hard":
          endpoint = `${process.env.BACKENDURL}/api/test_configs/4`;
          break;
        default:
          endpoint = `${process.env.BACKENDURL}/api/test_configs/1`; //auch leicht
      }
    } else {
      endpoint = `${process.env.BACKENDURL}/api/test_configs/2`;
    }
    const response = await $fetch(endpoint);
    fetchError.value = false; // Kein Fehler
    return response;
  } catch (error) {
    console.error("Fehler beim Abrufen der Konfigurationen:", error);
    fetchError.value = true; // Setze Fehlerzustand
    return null;
  }
};

const data = await fetchData();

const initializeGame = () => {
  if (data && data.item_configs.length > 0) {
    randomizedItems.value = isTrisightMode.value
      ? shuffleArray([...data.item_configs]) // Zufällig gemischte Kopie der item_configs für Trisight Mode
      : [...data.item_configs]; // Kopie der item_configs für den Standardmodus
    currentItem.value = randomizedItems.value[0]; // Setze das erste Item als Start
    totalTime.value = currentItem.value.time_visible_ms;
    remainingTime.value = totalTime.value;
  }
};

const startGame = () => {
  isGameStarted.value = true;
  isPlaceholderVisible.value = false; // Platzhalter ausblenden, wenn das Spiel beginnt
  if (isTrisightMode.value) {
    startTimer();
    startGameTimer(); // Starte den universellen Game Timer
  }
};

const startTimer = () => {
  clearInterval(timer.value);
  timer.value = setInterval(() => {
    if (remainingTime.value > 0) {
      remainingTime.value -= 10; // Aktualisierungsrate auf 10 ms gesetzt
    } else {
      clearInterval(timer.value);
      checkAnswer();
    }
  }, 10); // Timer-Intervall auf 10 ms gesetzt
};

const handleKeyPress = (event) => {
  if (
    ["ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight", " "].includes(event.key)
  ) {
    event.preventDefault();
  }
  if (!isGameStarted.value) {
    startGame();
    return;
  }

  if (isGameOver.value) return; // Wenn das Spiel vorbei ist, keine Eingaben verarbeiten

  switch (event.key) {
    case "ArrowUp":
      checkAnswer("N");
      break;
    case "ArrowDown":
      checkAnswer("S");
      break;
    case "ArrowLeft":
      checkAnswer("W");
      break;
    case "ArrowRight":
      checkAnswer("E");
      break;
  }
};

const checkAnswer = (direction) => {
  if (direction === currentItem.value.orientation) {
    score.value += 1;
  }
  loadNextItem();
};

const loadNextItem = () => {
  if (currentIndex.value < randomizedItems.value.length - 1) {
    currentIndex.value++;
    currentItem.value = randomizedItems.value[currentIndex.value];
    totalTime.value = currentItem.value.time_visible_ms;
    remainingTime.value = totalTime.value;
    if (isTrisightMode.value) {
      startTimer(); // Timer nur im Trisight Mode fortsetzen
    }
  } else {
    endGame(); // Beende das Spiel, wenn alle Items durchlaufen sind
  }
};

const endGame = () => {
  isGameOver.value = true; // Setze den Spielzustand auf "vorbei"
  clearInterval(timer.value); // Stoppe den Timer
  clearInterval(gameTimer.value); // Stoppe den Game Timer
  removeKeyListener(); // Entferne die Event-Listener für die Pfeiltasten
};

const removeKeyListener = () => {
  if (typeof window !== "undefined") {
    window.removeEventListener("keydown", handleKeyPress);
  }
};

const startNewRound = () => {
  score.value = 0;
  currentIndex.value = 0;
  remainingTime.value = 0;
  remainingGameTime.value = 60;
  isGameOver.value = false;
  isGameStarted.value = false;
  isPlaceholderVisible.value = true; // Platzhalter wieder anzeigen
  initializeGame();

  if (typeof window !== "undefined") {
    window.addEventListener("keydown", handleKeyPress); // Event-Listener wieder hinzufügen
  }
};

const getRotationStyle = (orientation) => {
  let rotation = "";
  let margin = "";

  switch (orientation) {
    case "N":
      rotation = "rotate(0deg)"; // Norden
      margin = "0 0 10% 0"; // margin-bottom
      break;
    case "E":
      rotation = "rotate(90deg)"; // Osten
      margin = "0 0 0 10%";
      break;
    case "S":
      rotation = "rotate(180deg)"; // Süden
      margin = "10% 0 0 0"; // margin-top
      break;
    case "W":
      rotation = "rotate(270deg)"; // Westen
      margin = "0 10% 0 0";
      break;
    default:
      rotation = "rotate(0deg)"; // Standardmäßig keine Drehung
      margin = "0 0 10% 0"; // Standardmäßig margin-bottom
  }

  return { rotation, margin };
};

onMounted(() => {
  if (typeof window !== "undefined") {
    window.addEventListener("keydown", handleKeyPress);
  }
  initializeGame();
});

onUnmounted(() => {
  removeKeyListener(); // Entferne den Event-Listener, wenn die Komponente zerstört wird
});
</script>

<style scoped>
.playscreen {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 90vh;
  background-color: #fff8ec;
}

.score-timer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 80%;
  margin-bottom: 20px;
  position: relative;
}

.left-side {
  display: flex;
  flex-direction: column;
  align-items: flex-start; /* Linksbündige Ausrichtung */
}

.game-timer {
  font-size: 22px;
  color: #363636;
  margin-bottom: 10px;
}

.timer-wrapper {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
}

.timer-svg {
  width: auto;
  height: auto;
  position: absolute;
}

.timer-background {
  fill: none;
  stroke: #185262d2;
  stroke-width: 5;
}

.timer-path {
  fill: none;
  stroke: #fff8ec;
  stroke-width: 10;
  stroke-dasharray: 314; /* Beispiel für einen Umfang bei Radius 50 */
  transform: rotate(-90deg);
  transform-origin: 50% 50%;
}

.triangle-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 60%;
  width: 60%;
  position: relative;
}

.circle-background {
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 50%;
  transition: background-color 0s ease-in-out;
  position: relative;
}

.triangle {
  clip-path: polygon(50% 0%, 0% 100%, 100% 100%);
  transition: transform 0s ease, width 0s ease, height 0s ease;
  position: absolute;
}

/* Stile für den Platzhalter */
.placeholder {
  background-color: lightgrey;
  border: 2px dashed #185262;
}

.placeholder-triangle {
  width: 50px;
  height: 50px;
  background-color: grey;
  clip-path: polygon(50% 0%, 0% 100%, 100% 100%);
}

.instructions {
  font-size: 26px;
  color: #353535;
  position: absolute;
  bottom: 6%;
}

.timer {
  font-size: 20px;
  color: #181818;
}

.game-over {
  display: flex;
  flex-direction: column; /* Buttons unter dem Score */
  justify-content: center;
  align-items: center;
  height: 100vh;
  color: #185262;
  font-size: 40px;
  font-weight: bold;
  background-color: #fff8ec; /* Hintergrundfarbe bei Spielende */
  text-align: center;
}

.final-score {
  margin-bottom: 20px; /* Abstand zwischen Score und Buttons */
  animation: fadeIn 1s ease-in-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.button-group {
  display: flex;
  gap: 20px;
}

.button {
  background-color: #185262;
  color: #fff8ec;
  padding: 10px 20px;
  border: none;
  border-radius: 40px;
  cursor: pointer;
  font-size: 18px;
  transition: background-color 0.3s, color 0.3s;
}

.button:hover {
  background-color: #0f3e4b;
  color: #fff;
}

/* Stil für den Error Alert */
.error-alert {
  font-size: 24px;
  font-weight: bold;
  color: rgb(189, 52, 52);
}
</style>

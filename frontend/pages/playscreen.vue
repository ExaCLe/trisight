<template>
  <div class="playscreen">
    <div class="score-timer">
      <div class="score">Punkte: {{ score }}</div>
      <!-- Visuelle Timer-Darstellung -->
      <div class="timer-wrapper">
        <svg class="timer-svg" :viewBox="`0 0 120 120`">
          <circle
            class="timer-path"
            cx="60"
            cy="60"
            r="55"
            :style="{ strokeDashoffset: timerDashOffset }"
          />
        </svg>
      </div>
    </div>

    <!-- Darstellung des aktuellen Spielzustands (Triangle und Circle) -->
    <div class="triangle-container">
      <div
        class="circle-background"
        :style="{ backgroundColor: currentItem.circle_color, width: currentItem.circle_size + 'px', height: currentItem.circle_size + 'px' }"
      >
        <div
          class="triangle"
          :style="{ 
            width: currentItem.triangle_size + 'px', 
            height: currentItem.triangle_size + 'px', 
            backgroundColor: currentItem.triangle_color,
            transform: getRotationStyle(currentItem.orientation).rotation,
            margin: getRotationStyle(currentItem.orientation).margin
          }"
        ></div>
      </div>
    </div>

    <!-- Anweisungen für Benutzer -->
    <div class="instructions">
      Verwenden Sie die Pfeiltasten, um die Richtung des Dreiecks zu erraten!
    </div>
  </div>
</template>

<script setup>
defineProps({
  isTrisightMode: Boolean
});

import { ref, computed, onMounted, onUnmounted } from 'vue';

const score = ref(0);
const currentIndex = ref(0);
const remainingTime = ref(0);
const currentItem = ref({});
const timer = ref(null);
const totalTime = ref(0); // Speichert die Gesamtzeit für den Timer

const fetchData = async () => {
  try {
    const response = await $fetch('http://localhost:8000/api/test_configs/1');
    return response;
  } catch (error) {
    console.error('Fehler beim Abrufen der Konfigurationen:', error);
    return null;
  }
};

const data = await fetchData();
console.log(data);

const initializeGame = () => {
  if (data && data.item_configs.length > 0) {
    currentItem.value = data.item_configs[0]; // Setze das erste Item als Start
    totalTime.value = currentItem.value.time_visible_ms;
    remainingTime.value = totalTime.value;
    startTimer();
  }
};

const startTimer = () => {
  clearInterval(timer.value);
  timer.value = setInterval(() => {
    if (remainingTime.value > 0) {
      remainingTime.value -= 100;
    } else {
      clearInterval(timer.value);
      checkAnswer();
    }
  }, 100);
};

const handleKeyPress = (event) => {
  switch (event.key) {
    case 'ArrowUp':
      checkAnswer('N');
      break;
    case 'ArrowDown':
      checkAnswer('S');
      break;
    case 'ArrowLeft':
      checkAnswer('W');
      break;
    case 'ArrowRight':
      checkAnswer('E');
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
  if (currentIndex.value < data.item_configs.length - 1) {
    currentIndex.value++;
    currentItem.value = data.item_configs[currentIndex.value];
    totalTime.value = currentItem.value.time_visible_ms;
    remainingTime.value = totalTime.value;
    startTimer();
  } else {
    console.log('Spiel beendet. Punktestand: ' + score.value);
  }
};

const getRotationStyle = (orientation) => {
  let rotation = '';
  let margin = '';

  switch (orientation) {
    case 'N':
      rotation = 'rotate(0deg)'; // Norden
      margin = '0 0 5% 0'; // margin-bottom
      break;
    case 'E':
      rotation = 'rotate(90deg)'; // Osten
      margin = '0 0 0 5%'; 
      break;
    case 'S':
      rotation = 'rotate(180deg)'; // Süden
      margin = '5% 0 0 0'; // margin-top
      break;
    case 'W':
      rotation = 'rotate(270deg)'; // Westen
      margin = '0 5% 0 0'; 
      break;
    default:
      rotation = 'rotate(0deg)'; // Standardmäßig keine Drehung
      margin = '0 0 5% 0'; // Standardmäßig margin-bottom
  }

  return { rotation, margin };
};

// Berechnung für den visuellen Timer-Balken
const timerDashOffset = computed(() => {
  const maxDashOffset = 2 * Math.PI * 55; // Umfang des Kreises, angepasst an den größeren Radius
  return (1 - remainingTime.value / totalTime.value) * maxDashOffset; // Rückwärtslaufender Balken
});

onMounted(() => {
  if (typeof window !== 'undefined') {
    window.addEventListener('keydown', handleKeyPress);
  }
  initializeGame();
});

onUnmounted(() => {
  if (typeof window !== 'undefined') {
    window.removeEventListener('keydown', handleKeyPress);
  }
});
</script>

<style scoped>
.playscreen {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background-color: #f4f4f4;
}

.score-timer {
  display: flex;
  justify-content: space-between;
  width: 80%;
  margin-bottom: 20px;
  position: relative;
}

.timer-wrapper {
  position: relative;
  width: 120px;
  height: 120px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.timer-svg {
  width: 120px;
  height: 120px;
  position: absolute;
  transform: translate(-700%, 250%);
}

.timer-path {
  fill: none;
  stroke: #5194c0; /* Farbe des Timer-Balkens */
  stroke-width: 2;
  stroke-dasharray: 345.6; /* Gesamtumfang des Kreises für 100% bei Radius 55 */
  transform: rotate(-90deg); /* Startpunkt oben */
  transform-origin: 50% 50%;
}

.triangle-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 60%;
  width: 60%;
  position: relative; /* Sicherstellen, dass Timer auf Container bezogen ist */
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

.instructions {
  margin-top: 20px;
  font-size: 18px;
  color: #333;
}
</style>

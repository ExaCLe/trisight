<template>
  <div class="playscreen">
    <div v-if="isTrisightMode" class="score-timer">
      <div class="score">Punkte: {{ score }}</div>
      <div class="timer">Verbleibende Zeit: {{ remainingTime }}ms</div>
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
            backgroundColor: currentItem.triangle_color 
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
// Props aus der Elternkomponente übernehmen (z.B. für Spielmodus)
defineProps({
  isTrisightMode: Boolean
});

import { ref, onMounted, onUnmounted } from 'vue';
import { useAsyncData } from '#app';

const score = ref(0);
const currentIndex = ref(0);
const remainingTime = ref(0);
const currentItem = ref({});
const timer = ref(null);

// es gibt hier Probleme mit dem Pfad, das gibt nen 404
//const { data, error } = await useAsyncData('itemConfigs', () => $fetch('/api/item_configs'));
const { data, error } = await useAsyncData('itemConfigs', () => $fetch('/api/test_configs'));
//const { data, error } = await useAsyncData('itemConfigs', () => $fetch('/backend/item_config'));

const initializeGame = () => {
  if (data.value && data.value.length > 0) {
    currentItem.value = data.value[0]; // Setze das erste Item als Start
    remainingTime.value = currentItem.value.time_visible_ms;
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
    case "ArrowUp":
      checkAnswer("north");
      break;
    case "ArrowDown":
      checkAnswer("south");
      break;
    case "ArrowLeft":
      checkAnswer("west");
      break;
    case "ArrowRight":
      checkAnswer("east");
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
  if (currentIndex.value < data.value.length - 1) {
    currentIndex.value++;
    currentItem.value = data.value[currentIndex.value];
    remainingTime.value = currentItem.value.time_visible_ms;
    startTimer();
  } else {
    console.log('Spiel beendet. Punktestand: ' + score.value);
  }
};


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

if (error.value) {
  console.error('Fehler beim Abrufen der Konfigurationen:', error.value);
}
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
}

.triangle-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 60%;
  width: 60%;
}

.circle-background {
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 50%;
  transition: background-color 2s ease-in-out;
}

.triangle {
  clip-path: polygon(50% 0%, 0% 100%, 100% 100%);
  transition: transform 0.5s ease, width 0.5s ease, height 0.5s ease;
}

.instructions {
  margin-top: 20px;
  font-size: 18px;
  color: #333;
}
</style>

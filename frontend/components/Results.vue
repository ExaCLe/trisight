<template>
  <div class="results-container">
    <!-- Overview Section -->
    <div class="overview">
      <div class="overview-text">
        <h2>{{ correctAnswers }} von {{ totalQuestions }} richtig</h2>
        <p>Punkte: {{ score }}</p>
      </div>
      <div class="overview-chart">
        <Pie :data="pieData" :options="pieOptions" />
      </div>
    </div>
  
    <!-- Detailed Statistics Section -->
    <div class="detailed-stats">
      <h3>Detaillierte Ergebnisse</h3>
      <div class="stats-grid">
        <UCard v-for="(result, index) in detailedResults" :key="index" class="result-card">
          <div class="card-content">
            <div class="item-visual">
              <div
                class="circle-background"
                :style="{
                  backgroundColor: result.correctOrientation.circle_color,
                  width: getCircleSize(result.correctOrientation.circle_size) + 'px',
                  height: getCircleSize(result.correctOrientation.circle_size) + 'px',
                }"
              >
                <div
                  class="triangle"
                  :style="{
                    width: getTriangleSize(result.correctOrientation.triangle_size, result.correctOrientation.circle_size) + 'px',
                    height: getTriangleSize(result.correctOrientation.triangle_size, result.correctOrientation.circle_size) + 'px',
                    backgroundColor: result.correctOrientation.triangle_color,
                    transform: getRotationStyle(result.correctOrientation.orientation).rotation,
                  }"
                ></div>
              </div>
            </div>
            <div class="result-details">
              <p><strong>Korrekte Orientierung:</strong> {{ orientationFullName(result.correctOrientation.orientation) }}</p>
              <p><strong>Deine Eingabe:</strong> {{ orientationFullName(result.userInput.orientation) }}</p>
              <p v-if="result.isCorrect" class="correct">Richtig</p>
              <p v-else class="incorrect">Falsch</p>
            </div>
          </div>
        </UCard>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, computed } from 'vue';
import { Pie } from 'vue-chartjs';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';

ChartJS.register(ArcElement, Tooltip, Legend);

const props = defineProps({
  correctAnswers: Number,
  totalQuestions: Number,
  score: Number,
  detailedResults: Array
});

const pieData = computed(() => ({
  labels: ['Richtig', 'Falsch'],
  datasets: [
    {
      data: [props.correctAnswers, props.totalQuestions - props.correctAnswers],
      backgroundColor: ['#4caf50', '#f44336'],
      hoverBackgroundColor: ['#66bb6a', '#ef5350']
    }
  ]
}));

const pieOptions = {
  responsive: true,
  plugins: {
    legend: {
      position: 'bottom'
    },
    tooltip: {
      enabled: true
    }
  }
};

// Helper functions to match configurator styles
const getRotationStyle = (orientation) => {
  const rotations = {
    N: "rotate(0deg)",
    E: "rotate(90deg)",
    S: "rotate(180deg)",
    W: "rotate(-90deg)",
  };
  return { rotation: rotations[orientation] || "rotate(0deg)" };
};

const getCircleSize = (size) => Math.min(size * 0.8, 80);

const getTriangleSize = (size, circleSize) => {
  // Skalierung der Dreiecksgröße basierend auf der Kreisgröße
  const baseSize = size * 0.5; // Basis-Skalierung
  return baseSize;
};

// Function to convert orientation code to full name
const orientationFullName = (orientation) => {
  const map = {
    N: 'Norden',
    E: 'Osten',
    S: 'Süden',
    W: 'Westen'
  };
  return map[orientation] || orientation;
};
</script>

<style scoped>
.results-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  width: 100%;
  box-sizing: border-box;
}

.overview {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  max-width: 800px;
  margin-bottom: 40px;
  flex-wrap: wrap; /* Ermöglicht Umbruch auf kleineren Bildschirmen */
}

.overview-text {
  flex: 1;
  min-width: 200px; /* Mindestbreite, um Platz für Text zu gewährleisten */
  text-align: left;
}

.overview-text h2 {
  font-size: 24px;
  color: #185262;
  margin-bottom: 10px;
}

.overview-text p {
  font-size: 18px;
  color: #185262;
}

.overview-chart {
  flex: 1;
  min-width: 200px; /* Mindestbreite für das Diagramm */
  display: flex;
  justify-content: center;
  align-items: center;
}

.overview-chart canvas {
  max-width: 200px;
  max-height: 200px;
}

.detailed-stats {
  width: 100%;
  max-width: 1000px;
  padding: 20px; /* Hinzufügen von Padding */
  box-sizing: border-box;
  overflow: visible; /* Sicherstellen, dass der Inhalt nicht abgeschnitten wird */
}

.detailed-stats h3 {
  font-size: 22px;
  color: #185262;
  margin-bottom: 20px;
  text-align: center;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr); /* Drei Spalten pro Zeile */
  gap: 20px;
}

.result-card {
  padding: 20px;
  background-color: #f5f5f5;
  border-radius: 15px;
  box-shadow: 8px 8px 16px rgba(0, 0, 0, 0.15),
              -8px -8px 16px rgba(255, 255, 255, 0.7);
  display: flex;
  flex-direction: column;
  /* Sicherstellen, dass die Schatten nicht abgeschnitten werden */
  overflow: visible;
}

.card-content {
  display: flex;
  align-items: center;
}

.item-visual {
  margin-right: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.circle-background {
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 50%;
  transition: background-color 0.3s ease-in-out;
  position: relative;
}

.triangle {
  clip-path: polygon(50% 0%, 0% 100%, 100% 100%);
  transition: transform 0.3s ease, width 0.3s ease, height 0.3s ease;
  position: absolute;
}

.result-details {
  display: flex;
  flex-direction: column;
}

.result-details p {
  margin: 5px 0;
  font-size: 16px;
}

.correct {
  color: green;
  font-weight: bold;
}

.incorrect {
  color: red;
  font-weight: bold;
}

/* Responsive Anpassungen */
@media (max-width: 1200px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr); /* Zwei Spalten bei mittleren Bildschirmen */
  }
}

@media (max-width: 800px) {
  .stats-grid {
    grid-template-columns: 1fr; /* Eine Spalte bei kleinen Bildschirmen */
  }
}

@media (max-width: 600px) {
  .overview {
    flex-direction: column;
    align-items: center;
  }

  .overview-text, .overview-chart {
    max-width: 100%;
    text-align: center;
  }

  .item-visual {
    margin-right: 0;
    margin-bottom: 10px;
  }

  .result-card {
    align-items: center;
    text-align: center;
  }
}
</style>

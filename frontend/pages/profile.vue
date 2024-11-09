<template>
  <UContainer class="profile-container">
    <!-- User Info Tile -->
    <div class="user-info-tile">
      <img src="../images/avatar.jpg" alt="User Image" class="user-image" />
      <h2 class="user-name">{{ userName }}</h2>
      <p class="user-email">{{ userEmail }}</p>
    </div>

    <!-- Sehtest Liste Tile -->
    <div class="sehtest-list-tile">
      <h2 class="list-title">Deine gespeicherten Sehtests</h2>

      <!-- Ladeanimation anzeigen, wenn geladen wird -->
      <div v-if="isLoadingTests" class="loader-container">
        <div class="loader"></div>
      </div>

      <!-- Sehtest Liste anzeigen, wenn das Laden abgeschlossen ist -->
      <ul v-else class="sehtest-list">
        <li
          v-for="test in userTests"
          :key="test.id"
          @click="openTestOptions(test.id)"
          class="sehtest-item"
        >
          <span class="test-id">ID: {{ test.id }}</span>
          <span class="test-name">{{ test.name }}</span>
        </li>
      </ul>
    </div>

    <!-- Statistics Section -->
    <div class="statistics-section">
      <div class="general-stats">
        <h2>Allgemeine Statistiken</h2>
        <ul>
          <li>Beantwortete Item Konfigurationen: {{ stats.totalItemConfigs }}</li>
          <li>Richtige Antworten: {{ stats.correctAnswers }}</li>
          <li>Falsche Antworten: {{ stats.wrongAnswers }}</li>
          <li>Durchgeführte Test Konfigurationen: {{ stats.totalTestConfigs }}</li>
          <li>Versuche im Easy Modus: {{ stats.easyTries }}</li>
          <li>Versuche im Medium Modus: {{ stats.mediumTries }}</li>
          <li>Versuche im Hard Modus: {{ stats.hardTries }}</li>
          <li>Test Konfigurationen mit freiem Modus: {{ stats.testConfigsFree }}</li>
        </ul>
      </div>
      <div class="line-chart">
        <h2>Scores nach Schwierigkeitsgrad</h2>
        <Line :data="lineChartData" :options="lineChartOptions" />
      </div>
    </div>

    <!-- Test Config Results as Expandable Cards -->
    <div class="test-config-results">
      <h2>Test Konfigurationsergebnisse</h2>

      <!-- Ladeanimation anzeigen, wenn geladen wird -->
      <div v-if="isLoadingTestConfigs" class="loader-container">
        <div class="loader"></div>
      </div>

      <!-- Test Config Results Liste anzeigen, wenn das Laden abgeschlossen ist -->
      <div v-else class="test-config-list">
        <div
          v-for="testConfig in testConfigResults"
          :key="testConfig.id"
          class="test-config-card"
        >
          <div class="card-header" @click="toggleCard(testConfig.id)">
            <span class="card-title">Test ID: {{ testConfig.name }}</span>
            <span class="toggle-icon">{{ isCardOpen(testConfig.id) ? '-' : '+' }}</span>
          </div>
          <div v-if="isCardOpen(testConfig.id)" class="card-body">
            <p><strong>Name:</strong> {{ testConfig.name }}</p>
            <p><strong>Schwierigkeitsgrad:</strong> {{ getDifficulty(testConfig.test_config_id) }}</p>
            <p><strong>Korrekte Antworten:</strong> {{ testConfig.correct_answers }}</p>
            <p><strong>Falsche Antworten:</strong> {{ testConfig.wrong_answers }}</p>
            <p><strong>Zeitpunkt:</strong> {{ formatDate(testConfig.time) }}</p>
            <h4>Detaillierte Ergebnisse:</h4>
            <ul>
              <li v-for="detail in testConfig.detailedResults" :key="detail.id">
                Item ID: {{ detail.item_config_id }} - {{ detail.correct ? 'Richtig' : 'Falsch' }} - Reaktionszeit: {{ detail.reaction_time_ms }} ms - Antwort: {{ detail.response }}
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal für Sehtest Optionen -->
    <UModal v-model="isOptionsModalOpen">
      <div class="modal-content">
        <h2>Sehtest Optionen</h2>
        <p>Was möchten Sie mit diesem Sehtest tun?</p>
        <div class="modal-footer">
          <UButton @click="editTest(selectedTestId)" class="btn">Bearbeiten</UButton>
          <UButton :to="{ path: '/playscreen', query: { testConfigId: selectedTestId } }" class="btn">Durchführen</UButton>
          <UButton @click="isOptionsModalOpen = false" class="btn">Abbrechen</UButton>
        </div>
      </div>
    </UModal>

    <!-- Logout Button unter dem Grid -->
    <UButton @click="logout" class="logout-button" size="xl">Logout</UButton>
  </UContainer>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRuntimeConfig, navigateTo } from "nuxt/app";
import { Line } from 'vue-chartjs';
import { Chart as ChartJS, LineElement, CategoryScale, LinearScale, PointElement, Legend, Tooltip } from 'chart.js';

ChartJS.register(LineElement, CategoryScale, LinearScale, PointElement, Legend, Tooltip);

const toast = useToast();
const config = useRuntimeConfig();

const userName = ref("Benutzername");
const userEmail = ref("benutzer@example.com");
const userTests = ref([]);
const isOptionsModalOpen = ref(false);
const selectedTestId = ref(null);
const userId = ref(null);
const isLoadingTests = ref(true);
const isLoadingTestConfigs = ref(true);

// Statistics Reactive Variables
const stats = ref({
  totalItemConfigs: 0,
  correctAnswers: 0,
  wrongAnswers: 0,
  totalTestConfigs: 0,
  easyTries: 0,
  mediumTries: 0,
  hardTries: 0,
  testConfigsFree: 0,
});

// Line Chart Data and Options
const lineChartData = ref({
  labels: [], // To be filled with timestamps
  datasets: [
    {
      label: 'Easy',
      data: [],
      borderColor: '#4caf50',
      backgroundColor: 'rgba(76, 175, 80, 0.2)',
    },
    {
      label: 'Medium',
      data: [],
      borderColor: '#ff9800',
      backgroundColor: 'rgba(255, 152, 0, 0.2)',
    },
    {
      label: 'Hard',
      data: [],
      borderColor: '#f44336',
      backgroundColor: 'rgba(244, 67, 54, 0.2)',
    },
  ],
});

const lineChartOptions = {
  responsive: true,
  plugins: {
    legend: {
      position: 'top',
    },
    tooltip: {
      mode: 'index',
      intersect: false,
    },
  },
  scales: {
    x: {
      title: {
        display: true,
        text: 'Zeitpunkt',
      },
    },
    y: {
      title: {
        display: true,
        text: 'Score',
      },
      beginAtZero: true,
    },
  },
};

// Test Config Results Reactive Variables
const testConfigResults = ref([]);
const openCards = ref([]); // To track which cards are open

// Difficulty Mapping
const difficultyMapping = {
  1: 'Easy',
  3: 'Medium',
  4: 'Hard',
};

// Fetch User ID and Information
async function fetchUserId() {
  try {
    const response = await $fetch(`${config.public.backendUrl}/api/users/me`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
    });
    userId.value = response.id;
    userName.value = response.username;
    userEmail.value = response.email;

    // Fetch Tests, Statistics, and Test Config Results
    fetchUserTests();
    fetchStatistics();
    fetchTestConfigResults();
  } catch (error) {
    toast.add({
      title: "Fehler beim Abrufen der Benutzerinformationen.",
      id: "fetch-user-id-failed",
      color: "red",
    });
    isLoadingTests.value = false;
    isLoadingTestConfigs.value = false;
  }
}

// Fetch User Tests
async function fetchUserTests() {
  try {
    const token = localStorage.getItem("token");
    const response = await $fetch(`${config.public.backendUrl}/api/test_configs`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    userTests.value = response.filter((test) => test.user_id === userId.value);
  } catch (error) {
    toast.add({
      title: "Fehler beim Abrufen der Sehtests. Bitte versuchen Sie es erneut.",
      id: "fetch-tests-failed",
      color: "red",
    });
  } finally {
    isLoadingTests.value = false;
  }
}

// Fetch Statistics
async function fetchStatistics() {
  try {
    const token = localStorage.getItem("token");

    // Fetch all item config results for the user
    const itemConfigResults = await $fetch(`${config.public.backendUrl}/api/item_config_results/user`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    // Compute total, correct, wrong
    stats.value.totalItemConfigs = itemConfigResults.length;
    stats.value.correctAnswers = itemConfigResults.filter(r => r.correct).length;
    stats.value.wrongAnswers = stats.value.totalItemConfigs - stats.value.correctAnswers;

    // Fetch all test config results for the user
    const testConfigResultsData = await $fetch(`${config.public.backendUrl}/api/test_config_results/user`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    stats.value.totalTestConfigs = testConfigResultsData.length;

    // Count tries per difficulty
    testConfigResultsData.forEach(tcr => {
      const difficulty = difficultyMapping[tcr.test_config_id] || 'Easy';
      if (difficulty === 'Easy') stats.value.easyTries += 1;
      else if (difficulty === 'Medium') stats.value.mediumTries += 1;
      else if (difficulty === 'Hard') stats.value.hardTries += 1;
    });

    // Prepare data for line chart: all scores sorted by time for each difficulty
    const scoresByDifficulty = {
      Easy: [],
      Medium: [],
      Hard: [],
    };

    // Sort test config results by time ascending
    const sortedTestConfigResults = testConfigResultsData.sort((a, b) => new Date(a.time) - new Date(b.time));

    sortedTestConfigResults.forEach(tcr => {
      const difficulty = difficultyMapping[tcr.test_config_id] || 'Easy';
      scoresByDifficulty[difficulty].push({
        time: new Date(tcr.time),
        score: tcr.correct_answers, // Adjust if score is calculated differently
      });
    });

    // Generate labels (dates) sorted
    const allTimes = new Set();
    Object.values(scoresByDifficulty).forEach(scores => {
      scores.forEach(score => allTimes.add(score.time));
    });
    const sortedTimes = Array.from(allTimes).sort((a, b) => a - b);
    const formattedLabels = sortedTimes.map(time => time.toLocaleDateString('de-DE', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' }));

    // Prepare datasets with scores aligned to labels
    const easyData = [];
    const mediumData = [];
    const hardData = [];

    sortedTimes.forEach(time => {
      const easyScore = scoresByDifficulty.Easy.find(score => score.time.getTime() === time.getTime())?.score || null;
      const mediumScore = scoresByDifficulty.Medium.find(score => score.time.getTime() === time.getTime())?.score || null;
      const hardScore = scoresByDifficulty.Hard.find(score => score.time.getTime() === time.getTime())?.score || null;

      easyData.push(easyScore);
      mediumData.push(mediumScore);
      hardData.push(hardScore);
    });

    // Update line chart data
    lineChartData.value = {
      labels: formattedLabels,
      datasets: [
        {
          label: 'Easy',
          data: easyData,
          borderColor: '#4caf50',
          backgroundColor: 'rgba(76, 175, 80, 0.2)',
          spanGaps: true,
        },
        {
          label: 'Medium',
          data: mediumData,
          borderColor: '#ff9800',
          backgroundColor: 'rgba(255, 152, 0, 0.2)',
          spanGaps: true,
        },
        {
          label: 'Hard',
          data: hardData,
          borderColor: '#f44336',
          backgroundColor: 'rgba(244, 67, 54, 0.2)',
          spanGaps: true,
        },
      ],
    };
  } catch (error) {
    toast.add({
      title: "Fehler beim Abrufen der Statistiken.",
      id: "fetch-stats-failed",
      color: "red",
    });
  }
}

// Fetch Test Config Results for Cards
async function fetchTestConfigResults() {
  try {
    const token = localStorage.getItem("token");

    // Fetch all test config results for the user
    const testConfigResultsData = await $fetch(`${config.public.backendUrl}/api/test_config_results/user`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    // Fetch test configs to get names (assuming /api/test_configs/ returns all test configs)
    const testConfigs = await $fetch(`${config.public.backendUrl}/api/test_configs/`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    // Map test_config_id to test config details
    const testConfigMap = {};
    testConfigs.forEach(tc => {
      if (tc.user_id === userId.value) {
        testConfigMap[tc.id] = tc;
      }
    });

    // Prepare testConfigResults with necessary details
    testConfigResults.value = testConfigResultsData.map(tcr => ({
      id: tcr.id,
      test_config_id: tcr.test_config_id,
      name: testConfigMap[tcr.test_config_id]?.name || `Test Config ${tcr.test_config_id}`,
      correct_answers: tcr.correct_answers,
      wrong_answers: tcr.wrong_answers,
      total_questions: tcr.correct_answers + tcr.wrong_answers,
      score: calculateScore(tcr),
      time: tcr.time,
      detailedResults: tcr.item_config_results,
    }));
  } catch (error) {
    toast.add({
      title: "Fehler beim Abrufen der Testkonfigurationsergebnisse.",
      id: "fetch-test-config-results-failed",
      color: "red",
    });
  } finally {
    isLoadingTestConfigs.value = false;
  }
}

// Function to calculate score (customize as per your scoring logic)
function calculateScore(testConfigResult) {
  // Example: Score could be the number of correct answers
  return testConfigResult.correct_answers;
}

// Function to get difficulty based on test_config_id
function getDifficulty(test_config_id) {
  return difficultyMapping[test_config_id] || 'Easy';
}

// Function to format date
function formatDate(dateString) {
  const options = { year: 'numeric', month: 'short', day: 'numeric', 
                    hour: '2-digit', minute: '2-digit' };
  return new Date(dateString).toLocaleDateString('de-DE', options);
}

// Toggle Card Open/Close
function toggleCard(id) {
  const index = openCards.value.indexOf(id);
  if (index > -1) {
    openCards.value.splice(index, 1);
  } else {
    openCards.value.push(id);
  }
}

function isCardOpen(id) {
  return openCards.value.includes(id);
}

// Handle Test Options Modal
function openTestOptions(id) {
  selectedTestId.value = id;
  isOptionsModalOpen.value = true;
}

async function editTest(id) {
  isOptionsModalOpen.value = false;
  await navigateTo({
    path: "/configurator",
    query: { id },
  });
}

async function logout() {
  try {
    await $fetch(`${config.public.backendUrl}/api/users/logout`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
    });
    localStorage.removeItem("token");
    await navigateTo("/login");
  } catch (error) {
    toast.add({
      title: "Logout fehlgeschlagen. Bitte versuchen Sie es erneut.",
      id: "logout-failed",
      color: "red",
    });
  }
}

onMounted(() => {
  fetchUserId();
});
</script>

<style scoped>
.profile-container {
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: 20px;
  padding: 20px;
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
}

.user-info-tile {
  background-color: #f9f9f9;
  border-radius: 15px;
  padding: 20px;
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.15); /* Deutlicherer Schatten */
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.user-image {
  width: 200px; 
  height: 200px;
  border-radius: 50%;
  margin-bottom: 15px;
}

.user-name {
  font-size: 1.6em;
  font-weight: bold;
  color: #185262;
}

.user-email {
  font-size: 1em;
  color: #888;
  margin-top: 5px;
}

.sehtest-list-tile {
  background-color: #f9f9f9;
  border-radius: 15px;
  padding: 20px;
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.15); /* Deutlicherer Schatten */
  display: flex;
  flex-direction: column;
  position: relative;
}

.loader-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
}

.loader {
  border: 4px solid rgba(0, 0, 0, 0.1);
  border-radius: 50%;
  border-top: 4px solid #185262;
  width: 50px;
  height: 50px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.list-title {
  font-size: 1.5em;
  font-weight: bold;
  color: #185262;
  margin-bottom: 15px;
  text-align: center;
}

.sehtest-list {
  list-style: none;
  padding: 0;
  margin: 0;
  max-height: 400px;
  overflow-y: auto;
}

.sehtest-item {
  padding: 10px;
  border-bottom: 1px solid #ddd;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: background-color 0.2s ease;
}

.sehtest-item:hover {
  background-color: #eaeaea;
}

.sehtest-item:last-child {
  border-bottom: none;
}

.test-id {
  font-weight: bold;
  color: #185262;
}

.test-name {
  color: #888;
  font-weight: 400;
}

.sehtest-list::-webkit-scrollbar {
  width: 8px;
}

.sehtest-list::-webkit-scrollbar-track {
  background: #f1f1f1;
}

.sehtest-list::-webkit-scrollbar-thumb {
  background-color: #888;
  border-radius: 10px;
}

.logout-button {
  grid-column: 1 / -1;
  justify-self: center;
  margin-top: 20px;
  background-color: #185262;
  color: #fff;
}

.logout-button:hover {
  background-color: #133b4b;
}

.modal-content {
  text-align: center;
  padding: 20px;
}

.modal-footer {
  display: flex;
  justify-content: space-around;
  gap: 20px;
  margin-top: 20px;
}

.btn {
  background-color: #185262;
  color: #fff;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.btn:hover {
  background-color: #133b4b;
}

/* Statistics Section */
.statistics-section {
  grid-column: 1 / -1;
  background-color: #f9f9f9;
  border-radius: 15px;
  padding: 20px;
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.15);
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
}

.general-stats {
  flex: 1;
  min-width: 250px;
}

.general-stats h2 {
  font-size: 1.5em;
  color: #185262;
  margin-bottom: 10px;
}

.general-stats ul {
  list-style: none;
  padding: 0;
}

.general-stats li {
  margin-bottom: 5px;
  font-size: 1em;
  color: #333;
}

.line-chart {
  flex: 1;
  min-width: 300px;
}

.line-chart h2 {
  font-size: 1.5em;
  color: #185262;
  margin-bottom: 10px;
}

/* Test Config Results Section */
.test-config-results {
  grid-column: 1 / -1;
  background-color: #f9f9f9;
  border-radius: 15px;
  padding: 20px;
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.15);
  margin-top: 20px;
}

.test-config-results h2 {
  font-size: 1.5em;
  color: #185262;
  margin-bottom: 10px;
  text-align: center;
}

.test-config-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.test-config-card {
  border: 1px solid #ddd;
  border-radius: 10px;
  overflow: hidden;
  transition: box-shadow 0.3s;
}

.test-config-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.card-header {
  background-color: #eaeaea;
  padding: 10px 15px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
}

.card-title {
  font-weight: bold;
  color: #185262;
}

.toggle-icon {
  font-size: 1.5em;
  color: #185262;
}

.card-body {
  padding: 10px 15px;
  background-color: #fff;
}

.card-body p {
  margin: 5px 0;
}

.card-body ul {
  list-style: none;
  padding: 0;
}

.card-body li {
  margin-bottom: 5px;
  font-size: 0.9em;
  color: #555;
}

/* Responsive Anpassungen */
@media (max-width: 1200px) {
  .profile-container {
    grid-template-columns: 1fr;
  }

  .statistics-section {
    flex-direction: column;
  }
}

@media (max-width: 800px) {
  .statistics-section {
    flex-direction: column;
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

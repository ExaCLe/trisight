<template>
  <div class="configurator">
    <h1>Konfigurieren Sie Ihren Sehtest</h1>

    <!-- Fehlermeldung anzeigen, wenn ein Fehler beim Laden der Daten auftritt -->
    <div class="error-alert" v-if="fetchError">
      Es gab ein Problem beim Abrufen der Testkonfigurationen. Bitte versuchen
      Sie es erneut.
    </div>

    <!-- Grid der verfügbaren Testkombinationen -->
    <div class="tile-grid">
      <div
        v-for="(item, index) in testItems"
        :key="item.id"
        class="test-tile"
        :class="{ selected: selectedItems.includes(item.id) }"
        @click="toggleSelection(item.id)"
      >
        <!-- Nummerierung basierend auf der Auswahlreihenfolge anzeigen -->
        <h3 v-if="selectedItems.includes(item.id)">
          {{ getSelectionOrder(item.id) }}
        </h3>
        <div class="tile-content">
          <!-- Visualisierung der Dreieck- und Kreiskombination -->
          <div
            class="circle-background"
            :style="{ backgroundColor: item.circle_color, width: getCircleSize(item.circle_size) + 'px', height: getCircleSize(item.circle_size) + 'px' }"
          >
            <div
              class="triangle"
              :style="{
                width: getTriangleSize(item.triangle_size) + 'px',
                height: getTriangleSize(item.triangle_size) + 'px',
                backgroundColor: item.triangle_color,
                transform: getRotationStyle(item.orientation).rotation
              }"
            ></div>
          </div>
        </div>
      </div>
    </div>

    <!-- Buttons zum Speichern oder Abrufen des Sehtests -->
    <div class="button-group">
      <UButton @click="saveTest" color="amber" variant="solid">Sehtest speichern</UButton>
      <UInput v-model="testId" placeholder="Sehtest ID eingeben" />
      <UButton @click="loadTest" color="sky" variant="solid">Sehtest laden</UButton>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";

// API-Endpunkte
const testItemsEndpoint = "http://localhost:8000/api/test_configs/1"; // Korrigiert, um den richtigen Endpunkt zu verwenden
const saveTestEndpoint = "http://localhost:8000/api/save_test";
const loadTestEndpoint = "http://localhost:8000/api/load_test";

const testItems = ref([]);
const selectedItems = ref([]);
const selectedOrder = ref([]); // Speichert die Reihenfolge der ausgewählten Kacheln
const fetchError = ref(false);
const testId = ref("");

// Daten abrufen
const fetchTestItems = async () => {
  try {
    const response = await $fetch(testItemsEndpoint);
    if (response && response.item_configs) {
      testItems.value = response.item_configs; // Direkt auf die item_configs zugreifen
    } else {
      testItems.value = [];
    }
    fetchError.value = false;
  } catch (error) {
    console.error("Fehler beim Abrufen der Testkonfigurationen:", error);
    fetchError.value = true;
  }
};

// Auswahl einer Kachel umschalten
const toggleSelection = (id) => {
  const index = selectedItems.value.indexOf(id);
  if (index > -1) {
    selectedItems.value.splice(index, 1); // Deselektieren
    selectedOrder.value.splice(selectedOrder.value.indexOf(id), 1); // Reihenfolge aktualisieren
  } else {
    selectedItems.value.push(id); // Selektieren
    selectedOrder.value.push(id); // Zur Reihenfolge hinzufügen
  }
};

// Gibt die Reihenfolge der Auswahl für ein Element zurück
const getSelectionOrder = (id) => {
  return selectedOrder.value.indexOf(id) + 1; // 1-basierte Reihenfolge
};

// Sehtest speichern
const saveTest = async () => {
  try {
    const response = await $fetch(saveTestEndpoint, {
      method: "POST",
      body: { items: selectedItems.value },
    });
    alert(`Sehtest erfolgreich gespeichert! ID: ${response.testId}`);
  } catch (error) {
    console.error("Fehler beim Speichern des Sehtests:", error);
    alert("Es gab ein Problem beim Speichern des Sehtests. Bitte versuchen Sie es erneut.");
  }
};

// Sehtest laden
const loadTest = async () => {
  try {
    const response = await $fetch(loadTestEndpoint, {
      method: "POST",
      body: { testId: testId.value },
    });
    selectedItems.value = response.items;
    selectedOrder.value = [...response.items]; // Reihenfolge basierend auf den geladenen Items
    alert("Sehtest erfolgreich geladen!");
  } catch (error) {
    console.error("Fehler beim Laden des Sehtests:", error);
    alert("Es gab ein Problem beim Laden des Sehtests. Bitte versuchen Sie es erneut.");
  }
};

// Daten abrufen, wenn die Komponente gemountet wird
onMounted(() => {
  fetchTestItems();
});

// Funktion zur Dreiecksrotation
const getRotationStyle = (orientation) => {
  let rotation = "";
  switch (orientation) {
    case "N":
      rotation = "rotate(0deg)";
      break;
    case "E":
      rotation = "rotate(90deg)";
      break;
    case "S":
      rotation = "rotate(180deg)";
      break;
    case "W":
      rotation = "rotate(270deg)";
      break;
    default:
      rotation = "rotate(0deg)";
  }
  return { rotation };
};

// Funktion zur Berechnung der Größe der Kreise
const getCircleSize = (size) => {
  const maxSize = 80; // Maximalgröße für den Kreis in Pixeln
  const scale = 0.8; // Skalierungsfaktor für die Anpassung an die Kachelgröße
  return Math.min(size * scale, maxSize);
};

// Funktion zur Berechnung der Größe des Dreiecks
const getTriangleSize = (size) => {
  const maxSize = 40; // Maximalgröße für das Dreieck in Pixeln
  const scale = 0.5; // Skalierungsfaktor für die Anpassung an die Kachelgröße
  return Math.min(size * scale, maxSize);
};
</script>

<style scoped>
.configurator {
  padding: 20px;
  text-align: center;
}

.error-alert {
  color: red;
  margin-bottom: 20px;
}

.tile-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 20px;
  margin-bottom: 20px;
}

.test-tile {
  border: 2px solid #ccc;
  padding: 10px;
  width: 150px; /* Feste Kachelbreite */
  height: 150px; /* Feste Kachelhöhe */
  cursor: pointer;
  transition: all 0.2s;
}

.test-tile.selected {
  border-color: #185262;
  background-color: #e0f7fa;
}

.tile-content {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  position: relative; /* Um die absolute Positionierung des Dreiecks zu ermöglichen */
}

.button-group {
  margin-top: 20px;
  display: flex;
  justify-content: center;
  gap: 20px;
}

.circle-background {
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative; /* Relative Positionierung für Kind-Elemente */
}

.triangle {
  clip-path: polygon(50% 0%, 0% 100%, 100% 100%);
  position: absolute;
}
</style>

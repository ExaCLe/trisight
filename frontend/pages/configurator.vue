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
      <!-- Geladene Items anzeigen -->
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
            :style="{
              backgroundColor: item.circle_color,
              width: getCircleSize(item.circle_size) + 'px',
              height: getCircleSize(item.circle_size) + 'px',
            }"
          >
            <div
              class="triangle"
              :style="{
                width: getTriangleSize(item.triangle_size) + 'px',
                height: getTriangleSize(item.triangle_size) + 'px',
                backgroundColor: item.triangle_color,
                transform: getRotationStyle(item.orientation).rotation,
              }"
            ></div>
          </div>
        </div>
      </div>

      <!-- Platzhalter-Kachel mit einem Pluszeichen hinzufügen -->
      <div class="test-tile add-item-tile" @click="isOpen = true">
        <div class="tile-content">
          <span class="plus-sign">+</span>
        </div>
      </div>
    </div>

    <!-- Buttons zum Speichern oder Abrufen des Sehtests -->
    <div class="button-group">
      <UButton @click="saveTest" color="amber" variant="solid"
        >Sehtest speichern</UButton
      >
      <UInput v-model="testId" placeholder="Sehtest ID eingeben" />
      <UButton @click="loadTest" color="sky" variant="solid"
        >Sehtest laden</UButton
      >
    </div>
  </div>

  <UModal v-model="isOpen">
    <div class="modal-content">
      <h2 class="modal-title">Neue Item-Konfiguration erstellen</h2>
      <div class="modal-body">
        <!-- Vorschau des Dreiecks auf dem Kreis -->
        <div class="preview-container">
          <div
            class="circle"
            :style="{
              backgroundColor: circleColor,
              width: circleSize + 'px',
              height: circleSize + 'px',
            }"
            @click="selectColor('circle')"
          >
            <div class="triangle-circle">
              <div
                class="triangle"
                :style="{
                  width: triangleSize + 'px',
                  height: triangleSize + 'px',
                  backgroundColor: triangleColor,
                  transform: getRotationStyle(modalOrientation).rotation,
                }"
                @click="selectColor('triangle')"
              ></div>
            </div>
          </div>
        </div>

        <!-- Steuerungsbereich -->
        <div class="controls">
          <div class="size-controls">
            <span>Größe:</span>
            <button class="size-btn" @click="adjustTriangleSize(5)">+</button>
            <button class="size-btn" @click="adjustTriangleSize(-5)">-</button>
          </div>

          <div class="color-controls">
            <div>
              Kreisfarbe:
              <input class="color-input" type="color" v-model="circleColor" />
            </div>
            <div>
              Dreieckfarbe:
              <input class="color-input" type="color" v-model="triangleColor" />
            </div>
          </div>

          <div class="direction-controls">
    
            <button class="direction-btn" @click="setModalOrientation('N')">
              Norden
            </button>
            <button class="direction-btn" @click="setModalOrientation('E')">
              Osten
            </button>
            <button class="direction-btn" @click="setModalOrientation('S')">
              Süden
            </button>
            <button class="direction-btn" @click="setModalOrientation('W')">
              Westen
            </button>
          </div>
        </div>
      </div>

      <!-- Speichern und Schließen Buttons -->
      <div class="modal-footer">
        <button class="btn" @click="saveItemConfig">Speichern</button>
        <button class="btn" @click="isOpen = false">Abbrechen</button>
      </div>
    </div>
  </UModal>
</template>

<script setup>
import { ref, onMounted } from "vue";

const testItemsEndpoint = "http://localhost:8000/api/test_configs/1";
const saveTestEndpoint = "http://localhost:8000/api/save_test";
const loadTestEndpoint = "http://localhost:8000/api/load_test";

const testItems = ref([]);
const selectedItems = ref([]);
const fetchError = ref(false);
const testId = ref("");
const isOpen = ref(false);

const circleColor = ref("#ffcc00");
const triangleColor = ref("#3333ff");
const circleSize = ref(150);
const triangleSize = ref(50);
const modalOrientation = ref("N");

const fetchTestItems = async () => {
  try {
    const response = await $fetch(testItemsEndpoint);
    testItems.value = response?.item_configs || [];
    fetchError.value = false;
  } catch (error) {
    console.error("Fehler beim Abrufen der Testkonfigurationen:", error);
    fetchError.value = true;
  }
};

const openModal = () => {
  isOpen.value = true;
};

const toggleSelection = (id) => {
  if (selectedItems.value.includes(id)) {
    selectedItems.value = selectedItems.value.filter((itemId) => itemId !== id);
  } else {
    selectedItems.value.push(id);
  }
};

const getSelectionOrder = (id) => selectedItems.value.indexOf(id) + 1;

const saveTest = async () => {
  try {
    const response = await $fetch(saveTestEndpoint, {
      method: "POST",
      body: { items: selectedItems.value },
    });
    alert(`Sehtest erfolgreich gespeichert! ID: ${response.testId}`);
  } catch (error) {
    console.error("Fehler beim Speichern des Sehtests:", error);
    alert(
      "Es gab ein Problem beim Speichern des Sehtests. Bitte versuchen Sie es erneut."
    );
  }
};

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
    alert(
      "Es gab ein Problem beim Laden des Sehtests. Bitte versuchen Sie es erneut."
    );
  }
};

const setModalOrientation = (newOrientation) => {
  modalOrientation.value = newOrientation;
};

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

const getTriangleSize = (size) => Math.min(size * 0.5, 40);

const saveItemConfig = () => {
  const newItem = {
    id: Date.now(),
    circle_color: circleColor.value,
    triangle_color: triangleColor.value,
    circle_size: circleSize.value,
    triangle_size: triangleSize.value,
    orientation: modalOrientation.value,
  };
  testItems.value.push(newItem);
  isOpen.value = false;
};

const adjustTriangleSize = (change) => {
  const newSize = triangleSize.value + change;
  if (newSize > 10 && newSize < circleSize.value) triangleSize.value = newSize;
};

onMounted(fetchTestItems);
</script>

<style scoped>
.configurator {
  text-align: center;
  padding: 20px;
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
  width: 150px;
  height: 150px;
  padding: 10px;
  cursor: pointer;
  transition: all 0.2s;
  border-radius: 15px;
}

.test-tile.selected {
  border: 1px dashed #000;
  background-color: #e0f7fa;
}

.add-item-tile {
  border: 2px dashed #ccc;
  border-radius: 15px;
}

.plus-sign {
  font-size: 48px;
  color: #185262;
}

.tile-content,
.circle-background,
.triangle-circle {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
}

.button-group {
  margin-top: 20px;
  display: flex;
  justify-content: center;
  gap: 20px;
}

.circle,
.circle-background {
  border-radius: 50%;
  cursor: pointer;
  position: relative;
}

.triangle {
  clip-path: polygon(50% 0%, 0% 100%, 100% 100%);
  transition: transform 0.3s ease, width 0.3s ease, height 0.3s ease;
}

.modal-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
  text-align: center;
  padding: 40px;
}

.modal-title {
  font-size: 24px;
  font-weight: 900;
  color: #185262;
}

.modal-body,
.controls {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

.modal-footer {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  gap: 20px;
}

.size-controls,
.color-controls,
.direction-controls {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
}

.btn,
.size-btn,
.direction-btn {
  background-color: #185262;
  color: #fff;
  border: none;
  padding: 5px 10px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.btn:hover,
.size-btn:hover,
.direction-btn:hover {
  background-color: #133b4b;
}

.color-input {
  border: 1px dotted black;
  border-radius: 50%;
  cursor: pointer;
  width: 30px;
  height: 30px;
  padding: 0;
  appearance: none;
}

</style>

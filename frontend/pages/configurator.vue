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
          <div class="button-container">
            <button class="action-btn edit-btn" @click.stop="editItem(index)">
              <UIcon name="heroicons:pencil-square-16-solid"></UIcon>
            </button>
            <button
              class="action-btn duplicate-btn"
              @click.stop="duplicateItem(index)"
            >
              <UIcon name="heroicons:document-duplicate"></UIcon>
            </button>
            <button
              class="action-btn delete-btn"
              @click.stop="deleteItem(index)"
            >
              <UIcon name="heroicons:trash-16-solid"></UIcon>
            </button>
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
      <UButton
        class="btn"
        style="padding: 8px 20px; font-size: 16px"
        @click="saveTest"
        variant="solid"
      >
        Sehtest speichern ({{ selectedItems.length }})
      </UButton>

      <UButton
        class="btn"
        style="padding: 8px 20px; font-size: 16px"
        @click="isLoadModalOpen = true"
        variant="solid"
      >
        Sehtest laden
        <UIcon name="heroicons:cloud-arrow-down-16-solid" class="w-5 h-5" />
      </UButton>
    </div>
  </div>

  <UModal v-model="isOpen">
    <div class="modal-content">
      <h2 class="modal-title">Sehtest Objekt konfigurieren</h2>
      <div class="modal-body">
        <!-- Vorschau des Dreiecks auf dem Kreis -->
        <div class="preview-container">
          <div class="preview-box">
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
        </div>

        <!-- Steuerungsbereich -->
        <div class="controls">
          <div class="size-controls">
            <span>Dreieck:</span>
            <input
              class="size-input"
              type="number"
              v-model="triangleSize"
              min="10"
              max="120"
            />
            <div>
              <button class="size-btn" @click="adjustTriangleSize(5)">
                <UIcon name="heroicons:plus-20-solid" />
              </button>
              <button class="size-btn" @click="adjustTriangleSize(-5)">
                <UIcon name="heroicons:minus-20-solid" />
              </button>
            </div>

            <span>Kreis:</span>
            <input
              class="size-input"
              type="number"
              v-model="circleSize"
              min="50"
              max="200"
            />
            <div>
              <button class="size-btn" @click="adjustCircleSize(5)">
                <UIcon name="heroicons:plus-20-solid" />
              </button>
              <button class="size-btn" @click="adjustCircleSize(-5)">
                <UIcon name="heroicons:minus-20-solid" />
              </button>
            </div>
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
              Oben
            </button>
            <button class="direction-btn" @click="setModalOrientation('E')">
              Rechts
            </button>
            <button class="direction-btn" @click="setModalOrientation('S')">
              Unten
            </button>
            <button class="direction-btn" @click="setModalOrientation('W')">
              Links
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
  <UModal v-model="isLoadModalOpen">
    <div class="modal-content">
      <h2 class="modal-title">Sehtest ID eingeben</h2>
      <div class="modal-body">
        <UInput v-model="inputTestId" placeholder="Sehtest ID eingeben" />
      </div>
      <div class="modal-footer">
        <button class="btn" @click="loadTest">Laden</button>
        <button class="btn" @click="isLoadModalOpen = false">Abbrechen</button>
      </div>
    </div>
  </UModal>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { watch } from "vue";

const testItemsEndpoint = "http://localhost:8000/api/test_configs/1";
const saveTestEndpoint = "http://localhost:8000/api/test_configs";
const loadTestEndpoint = "http://localhost:8000/api/test_configs/";

const testItems = ref([]);
const selectedItems = ref([]);
const fetchError = ref(false);
const testId = ref("");
const isOpen = ref(false);
const isLoadModalOpen = ref(false);
const inputTestId = ref("");

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

watch(triangleSize, (newValue) => {
  if (newValue > 120) triangleSize.value = 120;
  if (newValue < 10) triangleSize.value = 10;
});

watch(circleSize, (newValue) => {
  if (newValue > 200) circleSize.value = 200;
  if (newValue < 50) circleSize.value = 50;
});

const adjustCircleSize = (change) => {
  const newSize = circleSize.value + change;
  if (newSize >= 50 && newSize <= 200) circleSize.value = newSize;
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
    // Authentifizierungs-Token (falls vorhanden) abrufen
    const token = localStorage.getItem("authToken"); // Angenommen, das Token wird im `localStorage` gespeichert

    // Sende die Anfrage mit dem Authentifizierungs-Header
    const response = await $fetch("http://localhost:8000/api/test_configs/", {
      method: "POST",
      body: { items: selectedItems.value },
      headers: {
        Authorization: `Bearer ${token}`, // Token im Header mitsenden
      },
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
      body: { testId: inputTestId.value }, // Verwende die ID aus dem Modal
    });
    selectedItems.value = response.items;
    selectedOrder.value = [...response.items]; // Reihenfolge basierend auf den geladenen Items
    alert("Sehtest erfolgreich geladen!");
    isLoadModalOpen.value = false; // Schließe das Modal nach dem Laden
  } catch (error) {
    console.error("Fehler beim Laden des Sehtests:", error);
    alert(
      "Es gab ein Problem beim Laden des Sehtests. Bitte versuchen Sie es erneut."
    );
  }
};

const editItem = (index) => {
  const item = testItems.value[index];
  // Setze die Eigenschaften des zu bearbeitenden Items in die Modal-Werte
  circleColor.value = item.circle_color;
  triangleColor.value = item.triangle_color;
  circleSize.value = item.circle_size;
  triangleSize.value = item.triangle_size;
  modalOrientation.value = item.orientation;

  isOpen.value = true;
  editingIndex.value = index;
};

const duplicateItem = (index) => {
  const item = testItems.value[index];
  const newItem = { ...item, id: Date.now() };
  testItems.value.push(newItem);
};

const deleteItem = (index) => {
  const itemId = testItems.value[index].id;
  testItems.value.splice(index, 1);
  selectedItems.value = selectedItems.value.filter((id) => id !== itemId);
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
h1 {
  font-size: x-large;
  margin: 20px;
}

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
  flex-direction: column;
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

.color-controls,
.direction-controls {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
}

.size-controls {
  display: flex;
  align-items: center;
  gap: 10px;
}

.btn,
.direction-btn {
  background-color: #185262;
  color: #fff;
  border: none;
  padding: 5px 10px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.size-btn {
  font-size: large;
  border-radius: 30px;
  display: flex;
}

.size-btn:hover {
  background-color: #d6d6d6;
}

.btn:hover,
.direction-btn:hover {
  background-color: #133b4b;
}

.color-input {
  border: none;
  cursor: pointer;
  width: 40px;
}

.size-input {
  width: 50px;
  text-align: center;
  border: 1px solid #ccc;
  border-radius: 5px;
  padding: 5px;
  margin: 0 5px; /* Weniger Abstand links und rechts */
}

.button-container {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin-top: 10px;
}

.action-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 16px;
  transition: transform 0.3s;
}

.action-btn:hover {
  transform: scale(1.2);
}

.edit-btn {
  color: #4caf50;
}

.duplicate-btn {
  color: #007bff; /* Blau für Duplizieren */
}

.delete-btn {
  color: #f44336; /* Rot für Löschen */
}

.preview-container {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 20px;
  width: 300px; /* Breite der gesamten Vorschau */
  height: 300px; /* Höhe der gesamten Vorschau */
  border: 1px solid #ccc; /* Optional: Rand um die Vorschau */
  border-radius: 10px; /* Optional: abgerundete Ecken */
  overflow: hidden; /* Verhindert, dass Elemente aus der Box herausragen */
}

.preview-box {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100%;
  position: relative; /* Positionierung innerhalb des Containers */
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

.modal-body {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.modal-footer {
  display: flex;
  justify-content: center;
  gap: 20px;
}

.btn {
  background-color: #185262;
  color: #fff;
  padding: 5px 10px;
  border-radius: 5px;
  cursor: pointer;
}

.btn:hover {
  background-color: #133b4b;
}
</style>

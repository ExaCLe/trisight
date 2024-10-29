<template>
  <div class="configurator">
    <h1>Konfigurieren Sie Ihren Sehtest</h1>

    <div v-if="loadedTestId" class="loaded-test-name">
      <h2>
        Konfiguration:
        <input v-model="loadedTestName" class="test-name-input" />
        <span class="test-id">ID: {{ loadedTestId }}</span>
      </h2>
    </div>
    <div v-else class="loaded-test-name">
      <h2>Konfiguration: {{ loadedTestName }}</h2>
    </div>

    <p class="select-info">
      Hier finden Sie einige Beispiele, wie Ihre Kacheln aussehen können. Bitte
      wählen Sie die Kacheln aus, die Sie in Ihrer Konfiguration speichern
      möchten, oder erstellen Sie sich Ihre eigenen Kacheln.
    </p>

    <!-- Dynamischer Success Alert -->
    <transition name="fade-alert">
      <UAlert
        v-if="showAlert && alertType === 'success'"
        :icon="alertIcon"
        :color="alertColor"
        variant="solid"
        :title="alertMessage"
        class="mb-4"
      />
    </transition>

    <!-- Dynamischer Error Alert -->
    <transition name="fade-alert">
      <UAlert
        v-if="showAlert && alertType === 'error'"
        :icon="alertIcon"
        :color="alertColor"
        variant="solid"
        :title="alertMessage"
        class="mb-4"
      />
    </transition>

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
                width:
                  getTriangleSize(item.triangle_size, item.circle_size, true) +
                  'px',
                height:
                  getTriangleSize(item.triangle_size, item.circle_size, true) +
                  'px',
                backgroundColor: item.triangle_color,
                transform: getRotationStyle(item.orientation).rotation,
              }"
            ></div>
          </div>
          <div class="button-container">
            <button
              class="action-btn edit-btn"
              @click.stop="openItemModal(index)"
            >
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
      <div class="test-tile add-item-tile" @click="openItemModal()">
        <div class="tile-content">
          <span class="plus-sign">+</span>
        </div>
      </div>
    </div>

    <!-- Buttons zum Speichern oder Abrufen des Sehtests -->
    <!-- Buttons zum Speichern oder Abrufen des Sehtests -->
    <div class="button-group">
      <UButton
        v-if="loadedTestId"
        class="green"
        style="padding: 8px 20px; font-size: 16px"
        :to="{ path: '/playscreen', query: { testConfigId: loadedTestId } }"
        variant="solid"
      >
        Sehtest durchführen
        <UIcon name="i-heroicons-play-circle-solid" class="w-5 h-5" />
      </UButton>

      <UButton
        class="btn"
        style="padding: 8px 20px; font-size: 16px"
        @click="handleSaveTestConfig"
        variant="solid"
      >
        {{ loadedTestId ? "Sehtest aktualisieren" : "Sehtest speichern" }} ({{
          selectedItems.length
        }})
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
      <UButton
        v-if="loadedTestId"
        class="btn delete-btn-scnd"
        style="padding: 8px 20px; font-size: 16px"
        @click="confirmDeleteTest"
        variant="solid"
      >
        Sehtest löschen
        <UIcon name="i-heroicons-trash-16-solid" class="w-5 h-5" />
      </UButton>
    </div>
  </div>

  <UModal v-model="isItemModalOpen">
    <div class="modal-content">
      <h2 class="modal-title">
        {{
          isEditing ? "Item Konfiguration bearbeiten" : "Neues Item erstellen"
        }}
      </h2>
      <div class="modal-body">
        <!-- Vorschau des Dreiecks auf dem Kreis -->
        <div class="preview-container">
          <div
            class="preview-box"
            :style="{ transform: circleSize > 300 ? 'scale(0.6)' : 'scale(1)' }"
          >
            <div
              class="circle"
              :style="{
                backgroundColor: circleColor,
                width: circleSize + 'px',
                height: circleSize + 'px',
              }"
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
              max="220"
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
              max="660"
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
      <div class="modal-footer">
        <button class="btn" @click="saveOrUpdateItemConfig">
          {{ isEditing ? "Aktualisieren" : "Speichern" }}
        </button>
        <button class="btn" @click="isItemModalOpen = false">Abbrechen</button>
      </div>
    </div>
  </UModal>
  <!-- Modal zum Laden eines Sehtests -->
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

  <!-- Modal zum Speichern einer neuen Sehtest-Konfiguration -->
  <UModal v-model="isNameModalOpen">
    <div class="modal-content">
      <h2 class="modal-title">Konfigurationsnamen eingeben</h2>
      <div class="modal-body">
        <UInput
          v-model="configName"
          placeholder="Namen der Konfiguration eingeben"
        />
      </div>
      <div class="modal-footer">
        <button class="btn" @click="saveNewTestConfig">Speichern</button>
        <button class="btn" @click="isNameModalOpen = false">Abbrechen</button>
      </div>
    </div>
  </UModal>

  <!-- Modal zur Bestätigung des Löschvorgangs -->
  <UModal v-model="isDeleteConfirmModalOpen">
    <div class="modal-content">
      <h2 class="modal-title">Sehtest löschen?</h2>
      <p>
        Möchten Sie diesen Sehtest wirklich löschen? Diese Aktion kann nicht
        rückgängig gemacht werden.
      </p>
      <div class="modal-footer">
        <button class="btn delete-btn" @click="deleteTestConfig">
          Löschen
        </button>
        <button class="btn" @click="isDeleteConfirmModalOpen = false">
          Abbrechen
        </button>
      </div>
    </div>
  </UModal>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { watch } from "vue";
import { useRoute } from "vue-router";

definePageMeta({
  middleware: "auth",
});

const route = useRoute();
const saveTestEndpoint = "http://localhost:8000/api/test_configs";
const loadTestEndpoint = "http://localhost:8000/api/test_configs/";

const testItems = ref([]);
const selectedItems = ref([]);
const fetchError = ref(false);
const inputTestId = ref("");
const configName = ref("");
const loadedTestName = ref("");

//ALERT
const showAlert = ref(false);
const alertType = ref("");
const alertMessage = ref("");
const alertIcon = ref("");
const alertColor = ref("");

const triggerAlert = (type, message) => {
  alertType.value = type;
  alertMessage.value = message;
  alertIcon.value =
    type === "success"
      ? "i-heroicons-check-circle"
      : "i-heroicons-exclamation-triangle";
  alertColor.value = type === "success" ? "green" : "red";
  showAlert.value = true;

  // Automatisches Ausblenden nach 3 Sekunden
  setTimeout(() => (showAlert.value = false), 3000);
};

// modale
const isLoadModalOpen = ref(false);
const isNameModalOpen = ref(false);
const isDeleteConfirmModalOpen = ref(false);
const isItemModalOpen = ref(false);
const isEditing = ref(false);
const editingIndex = ref(null);

// item confing
const circleColor = ref("#ffcc00");
const triangleColor = ref("#3333ff");
const circleSize = ref(150);
const triangleSize = ref(50);
const modalOrientation = ref("N");
const previewScaleFactor = 0.6;

const confirmDeleteTest = () => {
  isDeleteConfirmModalOpen.value = true;
};

const generateRandomConfigs = () => {
  const colors = ["#ffcc00", "#3333ff", "#ff5733", "#33ff57", "#3357ff"];
  const orientations = ["N", "E", "S", "W"];

  const randomConfig = () => {
    const triangleSize = Math.floor(Math.random() * 111) + 10; // Dreieck zwischen 10 und 120

    // Setze den Kreis auf mindestens das 1,5-fache des Dreiecks
    const minCircleSize = Math.ceil(triangleSize * 1.5);

    return {
      id: Date.now() + Math.floor(Math.random() * 1000),
      triangle_size: triangleSize,
      triangle_color: colors[Math.floor(Math.random() * colors.length)],
      circle_size: Math.max(
        Math.floor(Math.random() * 151) + 50,
        minCircleSize
      ), // Kreisgröße mindestens `minCircleSize`
      circle_color: colors[Math.floor(Math.random() * colors.length)],
      orientation:
        orientations[Math.floor(Math.random() * orientations.length)],
      time_visible_ms: 5000,
      createdByUser: true,
      isUnsaved: true, // Markiert das Item als ungespeichert
    };
  };

  testItems.value = Array.from({ length: 15 }, randomConfig);
};

const saveUnsavedItems = async () => {
  const token = localStorage.getItem("token");

  for (let i = 0; i < selectedItems.value.length; i++) {
    const itemId = selectedItems.value[i];
    const item = testItems.value.find((config) => config.id === itemId);

    // Prüfen, ob das Item ungespeichert ist
    if (item && item.isUnsaved) {
      try {
        const response = await $fetch(
          "http://localhost:8000/api/item_configs",
          {
            method: "POST",
            body: {
              triangle_size: item.triangle_size,
              triangle_color: item.triangle_color,
              circle_size: item.circle_size,
              circle_color: item.circle_color,
              orientation: item.orientation,
              time_visible_ms: 5000,
            },
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );
        // Aktualisiere die ID und markiere das Item als gespeichert
        item.id = response.id;
        item.isUnsaved = false;
        selectedItems.value[i] = response.id;
      } catch (error) {
        triggerAlert("error", "Fehler beim Speichern des Items.");
      }
    }
  }
};

const deleteTestConfig = async () => {
  isDeleteConfirmModalOpen.value = false; // Modal schließen
  try {
    const token = localStorage.getItem("token");
    await $fetch(`${loadTestEndpoint}${loadedTestId.value}`, {
      method: "DELETE",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    // Zustand zurücksetzen und Erfolgsmeldung anzeigen
    loadedTestId.value = null;
    loadedTestName.value = "";
    testItems.value = [];
    selectedItems.value = [];

    // Lösch-Feedback-Alert anzeigen
    triggerAlert("success", "Sehtest erfolgreich gelöscht!");
  } catch (error) {
    if (error.response?.status === 401) {
      triggerAlert(
        "error",
        "Sie sind nicht berechtigt, diesen Sehtest zu löschen."
      );
    } else {
      triggerAlert("error", "Fehler beim Löschen des Sehtests.");
    }
  }
};

const handleSaveTestConfig = async () => {
  if (selectedItems.value.length === 0) {
    triggerAlert(
      "error",
      "Bitte wählen Sie mindestens eine Kachel aus, bevor Sie speichern."
    );
    return;
  }

  await saveUnsavedItems();
  if (!loadedTestId.value) {
    isNameModalOpen.value = true; // Öffnet das Speichern-Modal
  } else {
    updateTestConfig();
  }
};

const saveNewTestConfig = async () => {
  await saveUnsavedItems();
  try {
    const token = localStorage.getItem("token");
    const response = await $fetch(saveTestEndpoint, {
      method: "POST",
      body: {
        name: configName.value,
        item_config_ids: selectedItems.value,
      },
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    loadedTestId.value = response.id;
    loadedTestName.value = configName.value;
    isNameModalOpen.value = false;
    triggerAlert("success", "Sehtest erfolgreich gespeichert!");
  } catch (error) {
    triggerAlert("error", "Fehler beim Speichern der Konfiguration.");
  }
};

watch(triangleSize, (newValue) => {
  if (newValue > 220) triangleSize.value = 220;
  if (newValue < 10) triangleSize.value = 10;
});

watch(circleSize, (newValue) => {
  if (newValue > 660) circleSize.value = 660;
  if (newValue < 50) circleSize.value = 50;
});

const adjustCircleSize = (change) => {
  const newSize = circleSize.value + change;
  circleSize.value = newSize;
};

const toggleSelection = (id) => {
  if (selectedItems.value.includes(id)) {
    selectedItems.value = selectedItems.value.filter((itemId) => itemId !== id);
  } else {
    selectedItems.value.push(id);
  }
};

const loadTest = async () => {
  try {
    const token = localStorage.getItem("token");
    const response = await $fetch(`${loadTestEndpoint}${inputTestId.value}`, {
      method: "GET",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    if (response && response.item_configs) {
      testItems.value = response.item_configs;
      selectedItems.value = response.item_configs.map((item) => item.id);
      loadedTestId.value = response.id;
      loadedTestName.value = response.name;
      isLoadModalOpen.value = false;

      triggerAlert("success", "Sehtest erfolgreich geladen!");
    } else {
      triggerAlert("error", "Fehler. Ungültige Antwortstruktur.");
    }
  } catch (error) {
    if (error.response?.status === 404) {
      triggerAlert("error", "Fehler: Dieser Sehtest existiert nicht");
    } else {
      triggerAlert("error", "Fehler beim Laden der Konfiguration.");
    }
  }
};

const resetModalFields = () => {
  circleColor.value = "#ffcc00";
  triangleColor.value = "#3333ff";
  circleSize.value = 150;
  triangleSize.value = 50;
  modalOrientation.value = "N";
};

const openItemModal = (index = null) => {
  if (index !== null) {
    // Bearbeiten-Modus
    const item = testItems.value[index];
    circleColor.value = item.circle_color;
    triangleColor.value = item.triangle_color;
    circleSize.value = item.circle_size;
    triangleSize.value = item.triangle_size;
    modalOrientation.value = item.orientation;
    isEditing.value = true;
    editingIndex.value = index;
  } else {
    // Neu-Modus
    resetModalFields(); // setzt die Felder zurück
    isEditing.value = false;
  }
  isItemModalOpen.value = true;
};

const loadTestById = async (testId) => {
  try {
    const token = localStorage.getItem("token");
    const response = await $fetch(`${loadTestEndpoint}${testId}`, {
      method: "GET",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    if (response && response.item_configs) {
      testItems.value = response.item_configs;
      selectedItems.value = response.item_configs.map((item) => item.id);
      loadedTestId.value = response.id;
      loadedTestName.value = response.name;
      isLoadModalOpen.value = false;

      triggerAlert("success", "Sehtest erfolgreich geladen!");
    } else {
      triggerAlert("error", "Fehler. Ungültige Antwortstruktur.");
    }
  } catch (error) {
    triggerAlert("error", "Fehler beim Laden des Sehtests.");
  }
};

const duplicateItem = (index) => {
  const item = testItems.value[index];
  const newItem = {
    ...item,
    id: crypto.randomUUID(), // Neue temporäre ID setzen, um die Einzigartigkeit sicherzustellen
    isUnsaved: true, // Markiere das Item als ungespeichert
    createdByUser: true, // Markiere es als durch den Nutzer erstellt
  };

  testItems.value.push(newItem); // Neues Item zu `testItems` hinzufügen
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

const getTriangleSize = (size, circleSize, isPreview = false) => {
  let scaledSize = size * 0.5; // Grundlegende Skalierung für Dreieck
  if (isPreview && circleSize > 300) {
    // Kleinere Skalierung des Dreiecks, wenn der Kreis größer als 300 ist
    scaledSize *= previewScaleFactor;
  }
  return scaledSize;
};

const saveOrUpdateItemConfig = async () => {
  const updatedItem = {
    triangle_size: triangleSize.value,
    triangle_color: triangleColor.value,
    circle_size: circleSize.value,
    circle_color: circleColor.value,
    orientation: modalOrientation.value,
    time_visible_ms: 5000,
  };

  const token = localStorage.getItem("token");

  if (isEditing.value && editingIndex.value !== null) {
    // Bearbeiten eines bestehenden Items
    const item = testItems.value[editingIndex.value];
    const oldItemId = item.id;

    try {
      let response;
      if (!item.id || item.createdByUser) {
        // POST-Request für ein neues Item
        response = await $fetch("http://localhost:8000/api/item_configs", {
          method: "POST",
          body: updatedItem,
          headers: { Authorization: `Bearer ${token}` },
        });

        // Aktualisieren der neuen ID und `selectedItems`
        item.id = response.id;
        item.isUnsaved = false;
        const index = selectedItems.value.indexOf(oldItemId);
        if (index !== -1) {
          selectedItems.value.splice(index, 1, response.id);
        }
      } else {
        // PUT-Request für ein bereits gespeichertes Item
        await $fetch(`http://localhost:8000/api/item_configs/${item.id}`, {
          method: "PUT",
          body: updatedItem,
          headers: { Authorization: `Bearer ${token}` },
        });
      }

      // Aktualisiere das bearbeitete Item in `testItems`
      testItems.value[editingIndex.value] = { ...updatedItem, id: item.id };
      editingIndex.value = null;
      isItemModalOpen.value = false;
    } catch (error) {
      if (error.response?.status === 401) {
        triggerAlert(
          "error",
          "Sie sind nicht berechtigt, dieses Item zu aktualisieren."
        );
      } else {
        triggerAlert("error", "Fehler beim Aktualisieren der Konfiguration.");
      }
    }
  } else {
    // Neues Item erstellen und in `testItems` und `selectedItems` hinzufügen
    try {
      const response = await $fetch("http://localhost:8000/api/item_configs", {
        method: "POST",
        body: updatedItem,
        headers: { Authorization: `Bearer ${token}` },
      });
      testItems.value.push({ ...updatedItem, id: response.id });
      selectedItems.value.push(response.id);
      isItemModalOpen.value = false;
    } catch (error) {
      triggerAlert("error", "Fehler beim Speichern der Konfiguration.");
    }
  }
};

const loadedTestId = ref(null); // Referenz für die aktuell geladene Test-ID

// Neue Methode für die direkte Aktualisierung der Konfiguration
const updateTestConfig = async () => {
  try {
    const token = localStorage.getItem("token");
    const updateUrl = `${saveTestEndpoint}/${loadedTestId.value}`;

    await $fetch(updateUrl, {
      method: "PUT",
      body: {
        name: loadedTestName.value, // Der bearbeitbare Name im Input-Feld
        item_config_ids: selectedItems.value,
      },
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    // Zeige den Erfolg-Alert an
    triggerAlert("success", "Sehtest erfolgreich aktualisiert!");
  } catch (error) {
    if (error.response?.status === 401) {
      triggerAlert(
        "error",
        "Sie sind nicht berechtigt, diesen Sehtest zu aktualisieren."
      );
    } else {
      triggerAlert("error", "Fehler beim Aktualisieren der Konfiguration.");
    }
  }
};

const adjustTriangleSize = (change) => {
  const newSize = triangleSize.value + change;
  if (newSize > 10 && newSize < circleSize.value) triangleSize.value = newSize;
};

onMounted(() => {
  const { id } = route.query;
  if (id) {
    loadTestById(id); // Lädt den Test automatisch, wenn ein `id`-Query vorhanden ist
  } else {
    generateRandomConfigs(); // Fallback, falls keine ID übergeben wurde
  }
});
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
  border: none;
  width: 150px;
  height: 150px;
  padding: 10px;
  cursor: pointer;
  transition: all 0.2s;
  border-radius: 15px;
  background-color: #f5f5f5;
  box-shadow: 8px 8px 16px rgba(0, 0, 0, 0.15),
    -8px -8px 16px rgba(255, 255, 255, 0.7);
}

.test-tile.selected {
  background-color: #f7f7f7;
  box-shadow: 0 12px 24px -10px rgba(0, 0, 0, 0.3),
    0 8px 16px -8px rgba(0, 0, 0, 0.15);
  transform: translateY(-3px) scale(1.03);
  transition: transform 0.25s ease, box-shadow 0.3s ease-in-out,
    background-color 0.3s ease;
  border: none;
  outline: none;
  position: relative;
}

.test-tile.selected:hover {
  background-color: #eaeaea;
}

.test-tile.selected::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  border-radius: 15px;
  border: 1px solid #ffffff8a; /* Leichter Grauton für die Border */
  box-shadow: 0 0 15px #ffa413; /* Dezenterer Schimmer-Effekt */
  z-index: -1;
  transition: box-shadow 0.3s ease-in-out, border-color 0.3s ease;
}

.test-tile:focus {
  outline: none;
}

.test-tile:hover {
  box-shadow: 0 15px 25px -10px rgba(0, 0, 0, 0.35),
    0 12px 20px -8px rgba(0, 0, 0, 0.25); /* Verfeinerter Hover-Schatten */
  transform: translateY(-6px) scale(1.04); /* Stärkerer Effekt beim Hover */
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
  margin-top: 40px;
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
  width: 700px; /* Breite der gesamten Vorschau */
  height: 400px; /* Höhe der gesamten Vorschau */
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

.loaded-test-name {
  margin-bottom: 20px;
  font-size: 1.2em;
  color: #185262;
}

.test-name-input {
  font-size: 1em;
  padding: 5px;
  border: 1px solid #ccc;
  border-radius: 5px;
  width: 200px;
  margin-left: 10px;
}

.select-info {
  margin-bottom: 30px;
  font-size: 14px;
  color: #666;
}

.green {
  background-color: #4caf50;
}

.green:hover {
  background-color: #26a82a;
  transition: 200ms ease-in-out;
}

.toast-warning {
  position: absolute;
  color: red;
  top: 20%;
}

.test-id {
  font-size: 1em;
  color: #185262;
  margin-left: 10px;
}

.fade-alert-enter-active,
.fade-alert-leave-active {
  transition: opacity 0.5s ease, transform 0.5s ease;
}
.fade-alert-enter-from,
.fade-alert-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
.fade-alert-enter-to,
.fade-alert-leave-from {
  opacity: 1;
  transform: translateY(0);
}

.delete-btn-scnd {
  background-color: #f44336; /* Rot für Löschen */
  color: #fff;
}

.delete-btn-scnd:hover {
  background-color: #d32f2f; /* Dunkleres Rot bei Hover */
}

.configurator {
  text-align: center;
  padding: 20px;
  background-color: #f5f5f5;
  color: #333;
}

.dark-configurator {
  background-color: #333;
  color: #eee;
}
</style>

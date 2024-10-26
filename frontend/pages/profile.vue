<template>
  <UContainer class="container">
    <UButton @click="logout" class="logout-button bg-blue-dianne-900" size="xl">Logout</UButton>


    <h2>Deine gespeicherten Sehtests:</h2>

    <!-- Sehtest Übersicht -->
    <div class="tile-grid">
      <div 
        v-for="test in userTests" 
        :key="test.id" 
        class="test-tile"
        @click="openTestOptions(test.id)"
      >
        <div class="tile-content">
          <span>ID: {{ test.id }}</span>
          <span class="name">{{ test.name }}</span> <!-- Zeigt den Namen des Sehtests an -->
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
          <UButton @click="runTest(selectedTestId)" class="btn">Durchführen</UButton>
          <UButton @click="isOptionsModalOpen = false" class="btn">Abbrechen</UButton>
        </div>
      </div>
    </UModal>
  </UContainer>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRuntimeConfig, navigateTo } from 'nuxt/app';

const toast = useToast();
const config = useRuntimeConfig();

const userTests = ref([]);
const isOptionsModalOpen = ref(false);
const selectedTestId = ref(null);
const userId = ref(null);

async function fetchUserId() {
  try {
    const response = await $fetch(`${config.public.backendUrl}/api/users/me`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    });
    userId.value = response.id; // Benutzer-ID speichern
    fetchUserTests(); // Tests für diesen Benutzer abrufen
  } catch (error) {
    toast.add({
      title: 'Fehler beim Abrufen der Benutzer-ID.',
      id: 'fetch-user-id-failed',
      color: "red",
    });
  }
}

async function fetchUserTests() {
  try {
    const response = await $fetch(`${config.public.backendUrl}/api/test_configs`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    });

    // Nur Tests abrufen, bei denen die user_id mit der Benutzer-ID übereinstimmt
    userTests.value = response.filter(test => test.user_id === userId.value);
  } catch (error) {
    toast.add({
      title: 'Fehler beim Abrufen der Sehtests. Bitte versuchen Sie es erneut.',
      id: 'fetch-tests-failed',
      color: "red",
    });
  }
}

function openTestOptions(id) {
  selectedTestId.value = id;
  isOptionsModalOpen.value = true;
}

async function editTest(id) {
  isOptionsModalOpen.value = false;
  await navigateTo({
    path: "/configurator",
    query: { id }, // Weiterleitung ohne den vorherigen Weg über inputTestId
  });
}



async function runTest(id) {
  isOptionsModalOpen.value = false;
  await navigateTo(`/run-test/${id}`);
}

async function logout() {
  try {
    await $fetch(`${config.public.backendUrl}/api/users/logout`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    });
    localStorage.removeItem('token');
    await navigateTo('/login');
  } catch (error) {
    toast.add({
      title: 'Logout fehlgeschlagen. Bitte versuchen Sie es erneut.',
      id: 'logout-failed',
      color: "red",
    });
  }
}

onMounted(() => {
  fetchUserId(); // Benutzer-ID abrufen und Tests laden
});
</script>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  height: 60vh;
  gap: 20px;
}

.tile-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 20px;
  justify-content: center;
  width: 100%;
}

.test-tile {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 150px;
  height: 150px;
  background-color: #f5f5f5;
  border-radius: 15px;
  cursor: pointer;
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s, box-shadow 0.2s;
}

.test-tile:hover {
  transform: scale(1.05);
  box-shadow: 0 16px 32px rgba(0, 0, 0, 0.15);
}

.tile-content {
  display: flex;
  flex-direction: column;
  font-size: 18px;
  font-weight: bold;
  color: #185262;
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

.name {
  color: rgb(133, 133, 133);
  font-weight: 300;
}
</style>

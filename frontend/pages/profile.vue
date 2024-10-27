<template>
  <UContainer class="profile-container">
    <!-- User Info Kachel -->
    <div class="user-info-tile">
      <img src="../images/avatar.jpg" alt="User Image" class="user-image" />
      <h2 class="user-name">{{ userName }}</h2>
      <p class="user-email">{{ userEmail }}</p>
    </div>

    <!-- Sehtest Liste Kachel -->
    <div class="sehtest-list-tile">
      <h2 class="list-title">Deine gespeicherten Sehtests</h2>

      <!-- Ladeanimation anzeigen, wenn geladen wird -->
      <div v-if="isLoading" class="loader-container">
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

    <!-- Logout Button unter dem Grid -->
    <UButton @click="logout" class="logout-button" size="xl">Logout</UButton>
  </UContainer>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRuntimeConfig, navigateTo } from "nuxt/app";

const toast = useToast();
const config = useRuntimeConfig();

const userName = ref("Benutzername");
const userEmail = ref("benutzer@example.com");
const userTests = ref([]);
const isOptionsModalOpen = ref(false);
const selectedTestId = ref(null);
const userId = ref(null);
const isLoading = ref(true);

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
    fetchUserTests();
  } catch (error) {
    toast.add({
      title: "Fehler beim Abrufen der Benutzer-ID.",
      id: "fetch-user-id-failed",
      color: "red",
    });
    isLoading.value = false;
  }
}

async function fetchUserTests() {
  try {
    const response = await $fetch(`${config.public.backendUrl}/api/test_configs`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`,
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
    isLoading.value = false;
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
    query: { id },
  });
}

async function runTest(id) {
  isOptionsModalOpen.value = false;
  await navigateTo(`/run-test/${id}`);
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

</style>

<template>
  <UContainer class="container">
    <!-- Benutzerinformationen anzeigen -->
    <div class="profile-card">
      <h2>Profilinformationen</h2>

      <div class="profile-field">
        <label for="username">Benutzername:</label>
        <div class="input-group">
          <UInput v-model="username" id="username" class="profile-input" disabled />
          <UButton @click="isUsernameModalOpen = true" color="sky" size="sm">Ändern</UButton>
        </div>
      </div>

      <div class="profile-field">
        <label for="email">E-Mail:</label>
        <UInput v-model="email" id="email" class="profile-input" disabled />
      </div>

      <div class="profile-field">
        <label for="password">Passwort:</label>
        <div class="input-group">
          <UInput :type="showPassword ? 'text' : 'password'" v-model="password" id="password" class="profile-input" placeholder="********" />
          <UIcon name="heroicons:eye-20-solid" @click="togglePasswordVisibility" class="password-toggle" />
          <UButton @click="isPasswordModalOpen = true" color="amber" size="sm">Passwort ändern</UButton>
        </div>
      </div>

      <!-- Logout Button -->
      <UButton @click="logout" class="logout-button bg-blue-dianne-900" size="xl">Logout</UButton>
    </div>

    <!-- UModal für das Ändern des Benutzernamens -->
    <UModal v-model="isUsernameModalOpen">
      <div class="modal-content">
        <h2 class="modal-title">Benutzername ändern</h2>
        <div class="modal-body">
          <UInput v-model="newUsername" class="profile-input" placeholder="Neuen Benutzernamen eingeben" />
        </div>
        <div class="modal-footer">
          <UButton @click="confirmUsernameChange" color="sky">Ändern</UButton>
          <UButton @click="isUsernameModalOpen = false">Abbrechen</UButton>
        </div>
      </div>
    </UModal>

    <!-- UModal für das Ändern des Passworts -->
    <UModal v-model="isPasswordModalOpen">
      <div class="modal-content">
        <h2 class="modal-title">Passwort ändern</h2>
        <div class="modal-body">
          <UInput type="password" v-model="newPassword" class="profile-input" placeholder="Neues Passwort eingeben" />
        </div>
        <div class="modal-footer">
          <UButton @click="confirmPasswordChange" color="amber">Ändern</UButton>
          <UButton @click="isPasswordModalOpen = false">Abbrechen</UButton>
        </div>
      </div>
    </UModal>
  </UContainer>
</template>

<script setup>
const toast = useToast()
const config = useRuntimeConfig();

definePageMeta({
  middleware: ["auth"]
})
import { ref, onMounted } from "vue";

const username = ref("");
const newUsername = ref("");
const email = ref("");
const password = ref("");
const newPassword = ref("");
const showPassword = ref(false);

// Modal-Zustände für das Ändern von Benutzernamen und Passwort
const isUsernameModalOpen = ref(false);
const isPasswordModalOpen = ref(false);


const fetchUserInfo = async () => {
  try {
    const response = await $fetch("http://localhost:8000/api/users/me", {
      method: "GET",
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
    });

    username.value = response.username;
    email.value = response.email;
  } catch (error) {
    console.error("Fehler beim Abrufen der Benutzerinformationen:", error);
    toast.add({
      title: "Fehler beim Laden der Profilinformationen.",
      id: "fetch-error",
      color: "red",
    });
  }
};

// Funktion zum Aktualisieren des Benutzernamens
const confirmUsernameChange = async () => {
  try {
    await $fetch("http://localhost:8000/api/users/me", {
      method: "PATCH",
      body: { username: newUsername.value },
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
    });
    username.value = newUsername.value;
    isUsernameModalOpen.value = false;
    toast.add({
      title: "Benutzername erfolgreich geändert.",
      id: "username-success",
      color: "green",
    });
  } catch (error) {
    console.error("Fehler beim Aktualisieren des Benutzernamens:", error);
    toast.add({
      title: "Benutzername konnte nicht geändert werden.",
      id: "username-error",
      color: "red",
    });
  }
};

// Funktion zum Aktualisieren des Passworts
const confirmPasswordChange = async () => {
  try {
    await $fetch("http://localhost:8000/api/users/change-password", {
      method: "PATCH",
      body: { password: newPassword.value },
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
    });
    isPasswordModalOpen.value = false;
    toast.add({
      title: "Passwort erfolgreich geändert.",
      id: "password-success",
      color: "green",
    });
  } catch (error) {
    console.error("Fehler beim Aktualisieren des Passworts:", error);
    toast.add({
      title: "Passwort konnte nicht geändert werden.",
      id: "password-error",
      color: "red",
    });
  }
};

const togglePasswordVisibility = () => {
  showPassword.value = !showPassword.value;
};

// Logout-Funktion
async function logout() {
  if (!import.meta.env.SSR) {
    try {
      await $fetch("http://localhost:8000/api/users/logout", {
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
}

// Initialisiere die Daten, sobald die Komponente geladen wird
onMounted(fetchUserInfo);
</script>

<style scoped>
.container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 60vh;
}

.profile-card {
  width: 100%;
  max-width: 500px;
  background: #f7f9fc;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.profile-card h2 {
  font-size: 24px;
  margin-bottom: 20px;
  color: #333;
}

.profile-field {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 15px;
}

.profile-field label {
  font-size: 16px;
  font-weight: 500;
  margin-right: 10px;
}

.input-group {
  display: flex;
  align-items: center;
  width: 100%; /* Gleiche Breite für alle Gruppen */
}

.profile-input {
  flex: 1;
  max-width: 300px; /* Einheitliche Eingabefeldgröße */
  margin-right: 10px;
}

.password-toggle {
  cursor: pointer;
  font-size: 20px;
  margin-left: -30px; /* Passende Positionierung für das Icon */
}

.logout-button {
  margin-top: 30px;
}

.modal-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
  text-align: center;
  padding: 30px;
}

.modal-title {
  font-size: 24px;
  color: #185262;
}

.modal-footer {
  display: flex;
  justify-content: center;
  gap: 20px;
}
</style>

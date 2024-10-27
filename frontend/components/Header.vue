<template>
  <header v-if="!loading" :class="{ 'dark-header': darkMode }">
    <a href="/">
      <img
        src="/images/TRISIGHT-LOGO-TRANSPARENT-NEU.png"
        alt="TRISIGHT Logo"
        class="logo"
      />
    </a>

    <div class="header-buttons">
      <!-- Darkmode Schalter -->
      <button @click="toggleDarkMode" class="darkmode-toggle">
        <span v-if="darkMode">🌙</span>
        <span v-else>☀️</span>
      </button>

      <NuxtLink v-if="loggedIn" class="login-button" :to="{ path: './profile' }">Profile</NuxtLink>
      <NuxtLink v-else class="login-button" :to="{ path: '/login' }">Login</NuxtLink>
    </div>
  </header>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const loggedIn = ref(false)
const darkMode = ref(false)
const loading = ref(true)

function toggleDarkMode() {
  darkMode.value = !darkMode.value
  localStorage.setItem('darkMode', darkMode.value) // Darkmode-Status speichern
}

onMounted(() => {
  if (!import.meta.env.SSR) {
    // Lade die Werte aus dem localStorage und setze die Zustände
    darkMode.value = localStorage.getItem('darkMode') === 'true'
    loggedIn.value = localStorage.getItem('token') !== null
    loading.value = false // Ladezustand deaktivieren, wenn alle Werte geladen sind
  }
})
</script>

<style scoped>
/* Header Standard und Darkmode */
header {
  position: sticky;
  top: 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 10vh;
  padding: 0 20px;
  z-index: 999;
  background-color: #185262;
  transition: background-color 0.3s ease;
}

.dark-header {
  background-color: #1a1a1a;
}

.logo {
  height: 60px;
}

/* Flex-Container für die Buttons */
.header-buttons {
  display: flex;
  align-items: center;
}

/* Darkmode-Toggle-Button */
.darkmode-toggle {
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
  margin-right: 15px;
  color: white;
}

/* Login Button Standard und Darkmode */
.login-button {
  background-color: #fff8ec;
  width: 140px;
  color: #185262;
  border: none;
  padding: 10px 20px;
  margin-right: 30px;
  border-radius: 20px;
  cursor: pointer;
  font-size: 16px;
  font-weight: bold;
  transition: background-color 0.3s, color 0.3s;
  text-align: center;
}

.dark-header .login-button {
  background-color: #444;
  color: #eee;
}

.login-button:hover {
  background-color: #0f3e4b;
  color: #fff8ec;
}

.dark-header .login-button:hover {
  background-color: #555;
  color: #ddd;
}
</style>

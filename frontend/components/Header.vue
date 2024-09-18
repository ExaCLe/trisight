<template>
  <header>
    <a href="/">
      <img
        src="/images/TRISIGHT-LOGO-TRANSPARENT-NEU.png"
        alt="TRISIGHT Logo"
        class="logo"
      />
    </a>
    <button v-if="loggedIn" class="logout-button" @click="logout">Logout</button>
    <NuxtLink v-else class="login-button" :to="{path: '/login'}">Login</NuxtLink>
  </header>
</template>

<script setup>
import { ref, onMounted } from 'vue'

// Create a reactive loggedIn ref
const loggedIn = ref(false)

// Check if it's not SSR and update the loggedIn status
onMounted(() => {
  if (!import.meta.env.SSR) {
    loggedIn.value = localStorage.getItem('token') !== null
  }
})

function logout() {
  if (!import.meta.env.SSR) {
    localStorage.removeItem('token')
    location.reload()
  }
}
</script>

<style scoped>
header {
  position: sticky;
  top: 0;
  background-color: #185262;
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 10vh;
  padding: 0 20px;
  z-index: 999;
}

.logo {
  height: 60px;
}

.login-button {
  background-color: white;
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

.login-button:hover {
  background-color: #0f3e4b;
  color: white;
}

.logout-button {
  color: white;
  /* under line the text */
  text-decoration: underline;
  margin-right: 20px;
  padding: 10px 20px;
}

</style>

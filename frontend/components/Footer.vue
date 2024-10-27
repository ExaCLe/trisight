<template>
  <footer v-if="!loading" :class="['footer', { 'dark-footer': darkMode }]">
    <div class="divider"></div>
    <div class="footer-block">
      <h3>Programmierer</h3>
      <p>Leon Biermann</p>
      <p>Email: leon@biermann.de</p>
      <p>Aaron Hampe</p>
      <p>Email: hampeaaron@gmail.com</p>
    </div>
    <div class="footer-block">
      <h3>Services</h3>
      <ul>
        <li>Online Lernen</li>
        <li>Kundensupport</li>
        <li>FAQ</li>
      </ul>
    </div>
    <div class="footer-block">
      <h3>Unternehmen</h3>
      <p>Über uns</p>
      <p>Stellenangebote</p>
      <p>Presse</p>
    </div>
  </footer>
</template>

<script setup>
import { ref, onMounted } from 'vue'

// Darkmode und Ladezustand
const darkMode = ref(false)
const loading = ref(true)

onMounted(() => {
  if (!import.meta.env.SSR) {
    // Darkmode aus dem localStorage abrufen
    darkMode.value = localStorage.getItem('darkMode') === 'true'
    loading.value = false
  }
})
</script>

<style scoped>
.footer {
  background-color: #0d2329;
  color: #fff8ec;
  padding: 20px 0;
  height: 50vh;
  display: flex;
  justify-content: space-around;
  align-items: flex-start;
  flex-wrap: wrap;
  position: relative;
}

.dark-footer {
  background-color: #111;
  color: #d3d3d3;
}

.divider {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 2px;
  background-color: #888888; 
}

.footer-block {
  flex: 1;
  min-width: 200px;
  margin-top: 20px; 
  margin-left: 200px;
  padding: 20px;
}

.footer-block h3 {
  margin-bottom: 10px;
}

.footer-block p, .footer-block ul {
  margin: 0;
  padding: 0;
  list-style: none;
}

.footer-block ul li {
  margin-bottom: 5px;
}
</style>

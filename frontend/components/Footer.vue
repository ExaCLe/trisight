<template>
  <footer v-if="!loading" :class="['footer', { 'dark-footer': themeStore.isDarkMode }]">
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
import { ref, onMounted } from 'vue';
import { useThemeStore } from '@/stores/theme';

// Darkmode und Ladezustand
const themeStore = useThemeStore();
const loading = ref(true);

onMounted(() => {
  if (!import.meta.env.SSR) {
    themeStore.initializeDarkMode(); // Darkmode aus dem Store initialisieren
    loading.value = false;
  }
});
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

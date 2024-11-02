import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useThemeStore = defineStore('theme', () => {
  const isDarkMode = ref(false);

  function toggleDarkMode() {
    isDarkMode.value = !isDarkMode.value;
    localStorage.setItem('darkMode', JSON.stringify(isDarkMode.value));
  }

  function initializeDarkMode() {
    const savedMode = JSON.parse(localStorage.getItem('darkMode') || 'false');
    isDarkMode.value = savedMode;
  }

  return { isDarkMode, toggleDarkMode, initializeDarkMode };
});

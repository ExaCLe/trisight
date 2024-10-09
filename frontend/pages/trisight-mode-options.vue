<template>
    <div class="trisight-options">
      <h1>Trisight Mode: Schwierigkeit auswählen</h1>
      <p>Wählen Sie eine Schwierigkeitsstufe, um den Trisight Mode zu starten:</p>
      
      <div class="option-buttons">
        <NuxtLink 
          :to="{ path: '/playscreen', query: { isTrisightMode: true, difficulty: 'easy' } }" 
          class="difficulty-button"
        >
          Leicht
        </NuxtLink>
        <NuxtLink 
          :to="{ path: '/playscreen', query: { isTrisightMode: true, difficulty: 'medium' } }" 
          class="difficulty-button"
        >
          Mittel
        </NuxtLink>
        <NuxtLink 
          :to="{ path: '/playscreen', query: { isTrisightMode: true, difficulty: 'hard' } }" 
          class="difficulty-button"
        >
          Schwer
        </NuxtLink>
      </div>
  
      <!-- Zurück Button -->
      <NuxtLink to="/" class="back-button">Zurück zur Startseite</NuxtLink>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {};
    },
  };
  </script>
  
  <style scoped>
  .trisight-options {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    min-height: 90vh;
    background-color: #ffffff;
    padding: 40px;
  }
  
  h1 {
    color: #185262;
    font-size: 36px;
    margin-bottom: 20px;
  }
  
  p {
    color: #333;
    font-size: 18px;
    max-width: 600px;
    margin-bottom: 40px;
  }
  
  .option-buttons {
    display: flex;
    flex-direction: column;
    gap: 20px;
    margin-bottom: 40px;
  }
  
  .difficulty-button {
    background-color: #185262;
    color: #ffffff;
    padding: 15px 30px;
    border-radius: 10px;
    font-size: 18px;
    text-decoration: none;
    transition: background-color 0.3s;
  }
  
  .difficulty-button:hover {
    background-color: #0f3e4b;
  }
  
  .back-button {
    margin-top: 20px;
    color: #185262;
    font-size: 16px;
    text-decoration: underline;
  }
  </style>
  
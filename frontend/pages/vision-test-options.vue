<template>
    <div class="vision-test-options">
      <!-- Titelbereich -->
      <h1>Wählen Sie Ihren Vision Test Modus</h1>
      <p>Sie können den Standard Sehtest nutzen oder Ihren eigenen Sehtest konfigurieren.</p>
  
      <!-- Auswahlkarten -->
      <div class="option-cards">
        <!-- Standardmodus Karte -->
        <div class="option-card">
          <h2>Standardmodus</h2>
          <p>Ein Standard Sehtest mit konstant ansteigender Schwierigkeit.</p>
          <NuxtLink :to="{ path: '/playscreen', query: { isTrisightMode: false } }" class="button">
              Standard Modus starten
            </NuxtLink>
        </div>
  
        <!-- Konfigurator Karte -->
        <div class="option-card">
          <h2>Konfigurator</h2>
          <p>Erstellen Sie Ihren eigenen Sehtest mit individuell anpassbaren Einstellungen.</p>
          <NuxtLink to="/configurator" class="button">Zum Konfigurator</NuxtLink>
        </div>
      </div>
  
      <!-- Zurück Button -->
      <NuxtLink to="/" class="back-button">Zurück</NuxtLink>
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
.vision-test-options {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 40px;
  background-color: #f5f5f5;
  min-height: 90vh;
  text-align: center;
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

.option-cards {
  display: flex;
  gap: 20px;
  justify-content: center;
  margin-bottom: 40px;
}

.option-card {
  background-color: #f4f4f4;
  border-radius: 20px;
  padding: 20px;
  width: 300px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  text-align: center;
  transition: transform 0.3s;
}

.option-card:hover {
  transform: translateY(-5px);
}

.option-card h2 {
  color: #185262;
  font-size: 24px;
  margin-bottom: 10px;
}

.option-card p {
  font-size: 16px;
  margin-bottom: 20px;
}

.button {
  background-color: #185262;
  color: #fff;
  padding: 10px 20px;
  border: none;
  border-radius: 20px;
  cursor: pointer;
  font-size: 16px;
  text-decoration: none;
  transition: background-color 0.3s;
}

.button:hover {
  background-color: #0f3e4b;
}

.back-button {
  margin-top: 20px;
  color: #185262;
  font-size: 16px;
  text-decoration: underline;
  cursor: pointer;
}
</style>


  
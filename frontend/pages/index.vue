<template>
  <div class="homepage">
    <!-- Obere Sektion mit blauem Hintergrund -->
    <div class="intro-section">
      <div class="content-container">
        <div class="animation-area">
          <img
            class="triangle-image"
            src="../images/trisight-spinning-triangle.png"
            alt="Spinning Triangle"
          />
        </div>
        <div class="info-container">
          <h1>Wie schnell ist dein Auge...?</h1>
          <div class="button-group">
            <button class="test-button">Vision Test</button>
            <button class="test-button">Trisight Mode</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Untere Sektion mit weißem Hintergrund -->
    <div class="info-section">
      <h2>Über den Sehtest</h2>
      <p>
        Der Sehtest ist ein spannendes Spiel, das Ihre Augen auf die Probe stellt. Finden Sie heraus, wie schnell Sie die Richtung eines Dreiecks erkennen können, während sich die Schwierigkeit erhöht.
      </p>
      <h2>Wie funktioniert es?</h2>
      <p>
        Beantworten Sie so schnell wie möglich, in welche Richtung das Dreieck zeigt. Die Größe und der Kontrast des Dreiecks ändern sich, um die Herausforderung zu erhöhen.
      </p>
      <h2>Vorteile des Spiels</h2>
      <ul>
        <li>Verbessert die visuelle Wahrnehmung</li>
        <li>Stärkt die Konzentrationsfähigkeit</li>
        <li>Eine unterhaltsame Art, das Sehvermögen zu testen</li>
      </ul>
    </div>
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
.homepage {
  width: 100%;
  overflow: hidden; /* Verhindert unerwünschtes Scrollen */
}

/* Obere Sektion */
.intro-section {
  background-color: #185262;
  color: white;
  min-height: 90vh;
  display: flex;
  justify-content: center;
  align-items: center;
}

.content-container {
  display: flex;
  justify-content: center;
  gap: 60px;
  width: 100%;
  max-width: 1400px;
  margin-top: -50px;
}

.animation-area {
  flex: 1;
  height: 40vh;
  padding: 20px;
  border-radius: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
}

.triangle-image {
  height: 400px;
  animation: rotateAndPulse 9s infinite linear;
}

/* Kombinierte Keyframes für Drehung und Pulsiereffekt */
@keyframes rotateAndPulse {
  0% {
    transform: rotate(0deg) scale(0.6);
  }
  50% {
    transform: rotate(180deg) scale(1.1);
  }
  100% {
    transform: rotate(360deg) scale(0.6);
  }
}

.info-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: flex-start; 
  margin-top: 80px;
  padding: 20px;
  position: relative;
}

h1 {
  margin-bottom: 10px;
  margin-left: 0; /* Entferne linke Marge */
  font-size: 40px;
  text-align: left;
  margin-left: 10px; /* Gleiche Margin wie die Buttons für Ausrichtung */
}

.button-group {
  display: flex;
  gap: 10px;
  margin-left: 10px; /* Gleiche Margin wie das H1-Element */
}

.test-button {
  background-color: white;
  color: #185262;
  border: none;
  padding: 10px 20px;
  border-radius: 20px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s, color 0.3s;
  width: 150px; /* Einheitliche Breite für beide Buttons */
  text-align: center;
}

.test-button:hover {
  background-color: #0f3e4b;
  color: white;
}

/* Untere Sektion */
.info-section {
  background-color: #ffffff;
  color: rgb(56, 56, 56);
  height: 100vh;
  padding: 40px;
  text-align: center;
}

.info-section h2 {
  margin-top: 20px;
}

.info-section p,
.info-section ul {
  max-width: 800px;
  margin: 0 auto;
  line-height: 1.6;
}

.info-section ul {
  padding: 0;
  list-style: none;
}

.info-section ul li {
  margin-bottom: 5px;
}
</style>

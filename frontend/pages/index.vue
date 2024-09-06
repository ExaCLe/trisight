<template>
  <div class="homepage">
    <!-- Obere Sektion mit blauem Hintergrund -->
    <div class="intro-section">
      <div class="content-container">
        <div class="animation-area">
          <video autoplay muted loop class="animation-video">
            <source src="../animations/spinning-triangle.mp4" type="video/mp4" />
            Your browser does not support the video tag.
          </video>
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

    <!-- Dreieckiger Übergang -->
    <div class="triangle-transition">
      <!-- Mehrere Dreiecke mit verschiedenen Größen und Animationen -->
      <div class="triangle triangle-small"></div>
      <div class="triangle triangle-medium"></div>
      <div class="triangle triangle-large"></div>
      <div class="triangle triangle-small-2"></div>
      <div class="triangle triangle-medium-2"></div>
      <div class="triangle triangle-large-2"></div>
      <div class="triangle triangle-small-3"></div>
      <div class="triangle triangle-medium-3"></div>
      <div class="triangle triangle-large-3"></div>
      
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

<style scoped>
.homepage {
  width: 100%;
  overflow: hidden; /* Verhindert unerwünschtes Scrollen */
}

/* Obere Sektion */
.intro-section {
  background-color: #185262;
  color: white;
  min-height: 80vh;
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

.animation-video {
  width: 90%;
  height: 100%;
  object-fit: cover;
  border-radius: 10px;
}

.info-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: flex-start; /* Linksbündig ausrichten */
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

/* Übergang mit Dreiecken */
.triangle-transition {
  position: relative;
  width: 100%;
  height: 100px; /* Höhe des Übergangs */
  background-color: #185262;
  overflow: hidden; /* Verhindert, dass Animationen aus dem Container ragen */
}

.triangle {
  position: absolute;
  bottom: 0;
  width: 80px;
  height: 80px;
  background-color: rgb(255, 255, 255);
  clip-path: polygon(50% 0%, 0% 100%, 100% 100%);
  animation: moveSideways 10s infinite ease-in-out;
}

.triangle-small {
  width: 50px;
  height: 50px;
  left: 8%;
  animation-duration: 6s;
  animation-delay: -2s;
  background-color: rgba(180, 93, 93, 0.199);
}

.triangle-small-2 {
  width: 100px;
  height: 50px;
  left: 60%;
}

.triangle-small-3 {
  width: 220px;
  height: 70px;
  left: 80%;
  animation-duration: 6s;
  animation-delay: -2s;
}

.triangle-medium {
  width: 100px;
  height: 100px;
  left: 40%;
  animation-duration: 8s;
  animation-delay: -4s;
  background-color: rgba(180, 93, 93, 0.199);
}

.triangle-medium-2 {
  width: 160px;
  height: 100px;
  left: 0%;
  animation-duration: 8s;
  animation-delay: 1s;
}

.triangle-medium-3 {
  width: 160px;
  height: 100px;
  left: 15%;
  animation-duration: 8s;
  animation-delay: 10s;
}


.triangle-large {
  width: 150px;
  height: 100px;
  left: 80%;
  animation-duration: 12s;
  animation-delay: -6s;
  background-color: rgba(180, 93, 93, 0.199);
}

.triangle-large-2 {
  width: 250px;
  height: 80px;
  left: 30%;
  animation-duration: 12s;
  animation-delay: -7s;
}

.triangle-large-3 {
  width: 150px;
  height: 80px;
  left: 90%;
  animation-duration: 12s;
  animation-delay: -7s;
}

@keyframes moveSideways {
  0%, 100% {
    transform: translateX(0);
  }
  50% {
    transform: translateX(50px);
  }
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

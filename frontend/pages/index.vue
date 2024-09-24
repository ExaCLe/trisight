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
            <NuxtLink
              :to="{ path: '/playscreen', query: { isTrisightMode: true } }"
              class="button-quick"
            >
              Quick Start
            </NuxtLink>
            <NuxtLink
              :to="{
                path: '/vision-test-options',
                query: { isTrisightMode: false },
              }"
              class="test-button"
            >
              Vision Test
            </NuxtLink>
            <NuxtLink
              :to="{ path: '/trisight-mode-options', query: { isTrisightMode: true } }"
              class="test-button"
            >
              Trisight Mode
            </NuxtLink>
          </div>
        </div>
      </div>
    </div>

    <!-- Untere Sektion mit weißem Hintergrund -->
    <div class="info-section">
      <div class="text-container">
        <h2>Wie funktioniert es?</h2>
        <p>
          Beim Sehtest und im Spiel "Trisight Mode" wird Ihre visuelle
          Wahrnehmung auf die Probe gestellt. Ein Dreieck erscheint in der Mitte
          des Bildschirms und zeigt in eine von vier Richtungen:
          <b>Norden, Osten, Süden oder Westen</b>. Ihre Aufgabe ist es, so
          schnell wie möglich die Richtung zu bestimmen und die entsprechende
          <b>Pfeiltaste</b> zu drücken. Die Schwierigkeit erhöht sich, indem die
          <b>Größe</b> des Dreiecks variiert und der <b>Kontrast</b> zum
          Hintergrund verändert wird. Im "Trisight Mode" müssen Sie gegen die
          Zeit antreten: Ein Timer läuft, und Ihre Punktezahl wird gezählt,
          basierend auf der Schnelligkeit und Richtigkeit Ihrer Antworten. Beim
          klassischen Sehtest gibt es keinen Timer, sodass Sie sich in Ruhe auf
          die Aufgabe konzentrieren können. Testen Sie Ihre Fähigkeiten und
          finden Sie heraus, wie schnell Ihre Augen wirklich sind!
        </p>
      </div>
      <div class="image-container">
        <img src="../images/arrow-keys.png" />
      </div>
    </div>
    <div class="info-section">
      <div class="text-container">
        <h2>Ansteigende Schwierigkeit</h2>
        <p>
          Im Spiel "Trisight Mode" steigt die Schwierigkeit nach und nach an, um
          Ihre visuelle Wahrnehmung und Reaktionszeit immer weiter zu fordern.
          Zu Beginn erscheint ein großes, deutlich sichtbares Dreieck auf einem
          kontrastreichen Hintergrund. Die Richtung – Norden, Osten, Süden oder
          Westen – lässt sich leicht erkennen, und Sie können schnell die
          richtige Pfeiltaste drücken.
          <b
            >Mit fortschreitendem Spiel wird das Dreieck jedoch kleiner und der
            Kontrast zum Hintergrund nimmt ab</b
          >. Es wird zunehmend schwieriger, die Richtung des Dreiecks sofort zu
          bestimmen, da es sich optisch weniger abhebt und mehr Konzentration
          erfordert. Zusätzlich läuft im "Trisight Mode" ein Timer, und Ihre
          Punktezahl hängt von der Schnelligkeit und Richtigkeit Ihrer Antworten
          ab. Jede Sekunde zählt, während die Herausforderung wächst – je
          schneller Sie die Richtung erkennen und die richtige Taste drücken,
          desto höher ist Ihre Punktzahl. Das Spiel fordert Ihre Augen und Ihre
          Reaktionsfähigkeit auf höchstem Niveau!
        </p>
      </div>
      <div class="image-container">
        <div class="circle-background">
          <img
            class="triangle-image-2"
            src="../images/blue-neon-triangle.png"
            alt="Blue Neon Triangle"
          />
        </div>
      </div>
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
  overflow: hidden;
}

/* Obere Sektion */
.intro-section {
  background-color: #185262;
  background-image: url(../images/trisight-background-home-desktop.png);
  background-repeat: no-repeat;
  background-size: cover;
  background-position: center;
  color: #fff8ec;
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

.triangle-image-2 {
  animation: pulseSize 9s infinite linear;
  margin-bottom: 60px;
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

@keyframes colorChange {
  0% {
    background-color: rgba(255, 166, 0, 0.815);
  }
  50% {
    background-color: #185262;
  }
  100% {
    background-color: rgb(255, 185, 56);
  }
}

@keyframes pulseSize {
  0%,
  100% {
    transform: scale(0.3);
  }
  50% {
    transform: scale(1);
  }
}

.circle-background {
  width: 340px;
  height: 340px;
  border-radius: 50%;
  background: orange; /* Ausgangsfarbe */
  display: flex;
  justify-content: center;
  align-items: center;
  animation: colorChange 6s infinite ease-in-out;
  position: relative;
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
  background-color: #fff8ec;
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
  color: #fff8ec;
}

.button-quick {
  background-color: #ffffff00;
  color: #fff8ec;
  border: solid 1px;
  padding: 10px 20px;
  border-radius: 20px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s, color 0.3s;
  width: 150px; /* Einheitliche Breite für beide Buttons */
  text-align: center;
}

.info-section {
  background-color: #fff8ec;
  color: rgb(56, 56, 56);
  height: auto; /* Automatische Höhe, damit es sich an den Inhalt anpasst */
  padding: 40px;
  text-align: left;
  display: flex;
  flex-wrap: wrap; /* Flexibles Layout für kleinere Bildschirme */
  justify-content: center;
  align-items: center;
  gap: 40px;
}

.text-container {
  flex: 1;
  max-width: 600px;
  line-height: 1.6;
  margin-left: 200px;
}

.image-container {
  flex: 0.5;
  display: flex;
  justify-content: center;
  align-items: center;
}

.image-container img {
  max-width: 100%;
  height: 370px;
  margin-top: 20px;
  object-fit: cover;
}

.info-section h2 {
  margin-top: 20px;
  font-size: 38px;
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

/* Responsive Styles */
@media (max-width: 1200px) {
  .content-container {
    flex-direction: column;
    align-items: center;
    gap: 40px;
    margin-top: 0;
  }

  .text-container {
    margin-left: 0;
    text-align: center;
  }

  .info-container {
    align-items: center;
    text-align: center;
  }
}

@media (max-width: 768px) {
  .triangle-image {
    height: 300px;
  }

  .info-section {
    flex-direction: column;
    padding: 20px;
  }

  .text-container {
    margin-left: 0;
    text-align: center;
    max-width: 90%;
  }

  .info-section h2 {
    font-size: 32px;
  }
}

@media (max-width: 480px) {
  .triangle-image {
    height: 200px;
  }

  .circle-background {
    width: 300px;
    height: 300px;
  }

  .info-section {
    padding: 10px;
  }

  .text-container {
    max-width: 100%;
  }

  .test-button {
    width: 120px;
    padding: 8px 16px;
    font-size: 14px;
  }

  h1 {
    font-size: 32px;
  }
}
</style>

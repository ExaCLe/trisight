<template>
  <div class="home">
    <div class="content">
      <div class="animation-area">
        
      </div>
      <div class="info-area">
        <h1>Wie schnell ist dein Auge...?</h1>
        <div class="buttons">
          <button class="info-button">Vision Test</button>
          <button class="info-button">Trisight Mode</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.home {
  background-color: #185262;
  color: white;
  height: 100vh; 
  display: flex;
  justify-content: center;
  align-items: center; 
}

.content {
  display: flex;
  justify-content: center;
  width: 80%;
  max-width: 1400px;
  margin-top: -250px; 
}

.animation-area {
  flex: 1;
  background-color: #f0f0f0; 
  color: black; 
  padding: 20px;
  border-radius: 20px;
}

.info-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
}

h1 {
  margin-bottom: 10px;
  margin-left: 30%;
  font-size: 40px;
  text-align: center;
}

.buttons {
  display: flex;
  gap: 10px;
}

.info-button {
  background-color: white;
  color: #185262;
  border: none;
  padding: 10px 20px;
  border-radius: 20px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s, color 0.3s;
}

.info-button:hover {
  background-color: #0f3e4b;
  color: white;
}
</style>

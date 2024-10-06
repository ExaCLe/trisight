<template>
    <div class="modal-overlay" @click.self="closeModal">
      <div class="modal-content">
        <div class="preview-container">
          <div
            class="circle"
            :style="{ backgroundColor: circleColor, width: circleSize + 'px', height: circleSize + 'px' }"
            @click="openColorPicker('circle')"
          >
            <div
              class="triangle"
              :style="{
                width: triangleSize + 'px',
                height: triangleSize + 'px',
                backgroundColor: triangleColor,
              }"
              @click="openColorPicker('triangle')"
            ></div>
          </div>
        </div>
  
        <div class="controls-container">
          <div class="size-controls">
            <button @click="changeTriangleSize(5)">+</button>
            <button @click="changeTriangleSize(-5)">-</button>
          </div>
          <div class="color-picker">
            <span>Kreisfarbe: </span>
            <div class="color-box" :style="{ backgroundColor: circleColor }" @click="openColorPicker('circle')"></div>
            <span>Dreieckfarbe: </span>
            <div class="color-box" :style="{ backgroundColor: triangleColor }" @click="openColorPicker('triangle')"></div>
          </div>
        </div>
  
        <!-- Color Picker Modal -->
        <div v-if="isColorPickerOpen" class="color-picker-modal">
          <input type="color" v-model="currentColor" @change="updateColor()" />
          <button @click="closeColorPicker">Fertig</button>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  
  const triangleSize = ref(50);
  const circleSize = ref(200);
  const circleColor = ref('#ffcc00');
  const triangleColor = ref('#3333ff');
  const isColorPickerOpen = ref(false);
  const colorTarget = ref(null);
  const currentColor = ref('');
  
  // Externe Methoden
  const openColorPicker = (target) => {
    colorTarget.value = target;
    currentColor.value = target === 'circle' ? circleColor.value : triangleColor.value;
    isColorPickerOpen.value = true;
  };
  
  const updateColor = () => {
    if (colorTarget.value === 'circle') circleColor.value = currentColor.value;
    if (colorTarget.value === 'triangle') triangleColor.value = currentColor.value;
  };
  
  const closeColorPicker = () => {
    isColorPickerOpen.value = false;
  };
  
  const changeTriangleSize = (delta) => {
    const newSize = triangleSize.value + delta;
    if (newSize >= 10 && newSize <= circleSize.value) {
      triangleSize.value = newSize;
    }
  };
  
  // Methode, um das Modal zu schließen
  const closeModal = () => {
    // Emitiere ein Event zum Schließen des Modals
    emit('close');
  };
  </script>
  
  <style scoped>
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
  }
  
  .modal-content {
    width: 600px;
    height: 400px;
    background: #fff;
    padding: 20px;
    border-radius: 8px;
    display: flex;
  }
  
  .preview-container {
    flex: 1;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  
  .circle {
    display: flex;
    justify-content: center;
    align-items: center;
    border-radius: 50%;
    cursor: pointer;
  }
  
  .triangle {
    clip-path: polygon(50% 0%, 0% 100%, 100% 100%);
    cursor: pointer;
  }
  
  .controls-container {
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }
  
  .size-controls {
    display: flex;
    flex-direction: column;
    margin-bottom: 20px;
  }
  
  .size-controls button {
    margin: 5px;
  }
  
  .color-box {
    width: 30px;
    height: 30px;
    border: 1px solid #333;
    margin: 5px 0;
    cursor: pointer;
  }
  
  .color-picker-modal {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    padding: 20px;
    background-color: #ffffff;
  }
  </style>
  
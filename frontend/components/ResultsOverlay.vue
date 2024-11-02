<template>
  <div class="overlay" v-if="isVisible">
    <div class="overlay-content">
      <Results
        :correct-answers="correctAnswers"
        :total-questions="totalQuestions"
        :score="score"
        :detailed-results="detailedResults"
      />
      <div class="button-group">
        <NuxtLink to="/" class="button">Home</NuxtLink>
        <button @click="$emit('new-round')" class="button">Neue Runde</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue';
import Results from '~/components/Results.vue';

const props = defineProps({
  isVisible: {
    type: Boolean,
    default: false
  },
  correctAnswers: Number,
  totalQuestions: Number,
  score: Number,
  detailedResults: Array
});

const emit = defineEmits(['new-round']);
</script>

<style scoped>
.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.overlay-content {
  background: white;
  padding: 20px;
  border-radius: 10px;
  max-width: 90%;
  max-height: 90%;
  overflow-y: auto;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.button-group {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 20px;
}

.button {
  background-color: #185262;
  color: #fff8ec;
  padding: 10px 20px;
  border: none;
  border-radius: 40px;
  cursor: pointer;
  font-size: 18px;
  transition: background-color 0.3s, color 0.3s;
}

.button:hover {
  background-color: #0f3e4b;
  color: #fff;
}
</style>

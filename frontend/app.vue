<script setup lang="ts">
import Playscreen from './pages/playscreen.vue';
</script>


<template>
  <div id="app">
    <NuxtLayout>
      <Header />
      <!--<NuxtPage />-->
        <Playscreen></Playscreen>
      <Footer />
    </NuxtLayout>
  </div>
</template>

<style>
* {
  font-family: "Gill Sans", "Gill Sans MT", Calibri, "Trebuchet MS", sans-serif;
}
</style>

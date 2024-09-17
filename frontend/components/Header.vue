<template>
  <header>
    <a href="/">
      <img
        src="/images/TRISIGHT-LOGO-TRANSPARENT-NEU.png"
        alt="TRISIGHT Logo"
        class="logo"
      />
    </a>
    <NuxtLink class="login-button" :to="{path: '/register'}">Login</NuxtLink>
  </header>
</template>

<style scoped>
header {
  position: sticky;
  top: 0;
  background-color: #185262;
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 10vh;
  padding: 0 20px;
  z-index: 999;
}

.logo {
  height: 60px;
}

.login-button {
  background-color: white;
  width: 140px;
  color: #185262;
  border: none;
  padding: 10px 20px;
  margin-right: 30px;
  border-radius: 20px;
  cursor: pointer;
  font-size: 16px;
  font-weight: bold;
  transition: background-color 0.3s, color 0.3s;
  text-align: center;
}

.login-button:hover {
  background-color: #0f3e4b;
  color: white;
}
</style>

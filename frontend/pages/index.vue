<template>
    <div class="home">
      <header>
        <img src="/images/TRISIGHT-LOGO-TRANSPARENT-NEU.png" alt="TRISIGHT Logo" class="logo"/>
        <button class="login-button">Login</button>
      </header>
    </div>
  </template>
  
  <style scoped>
  .home {
    background-color: #185262; 
    color: white; 
    min-height: 100vh; 
  }
  
  header {
    display: flex;  
    justify-content: space-between; 
    align-items: center; 
    height: 100px;
    padding: 0 20px; 
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
  }
  
  .login-button:hover {
    background-color: #0f3e4b; 
    color: white;
  }
  </style>
  
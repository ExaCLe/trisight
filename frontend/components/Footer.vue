<template>
    <footer class="footer">
      <div class="divider"></div>
      <div class="footer-block">
        <h3>Programmierer</h3>
        <p>Leon Biermann</p>
        <p>Email: leon@biermann.de</p>
        <p>Aaron Hampe</p>
        <p>Email: hampeaaron@gmail.com</p>
      </div>
      <div class="footer-block">
        <h3>Services</h3>
        <ul>
          <li>Online Lernen</li>
          <li>Kundensupport</li>
          <li>FAQ</li>
        </ul>
      </div>
      <div class="footer-block">
        <h3>Unternehmen</h3>
        <p>Über uns</p>
        <p>Stellenangebote</p>
        <p>Presse</p>
      </div>
    </footer>
  </template>

<style scoped>
  .footer {
    background-color: #0d2329;
    color: white;
    padding: 20px 0;
    height: 50vh;
    display: flex;
    justify-content: space-around;
    align-items: flex-start;
    flex-wrap: wrap;
    position: relative;
  }
  
  .divider {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 2px;
    background-color: #888888; 
  }
  
  .footer-block {
    flex: 1;
    min-width: 200px;
    margin-top: 20px; 
    margin-left: 200px;
    padding: 20px;
  }
  
  .footer-block h3 {
    margin-bottom: 10px;
  }
  
  .footer-block p, .footer-block ul {
    margin: 0;
    padding: 0;
    list-style: none;
  }
  
  .footer-block ul li {
    margin-bottom: 5px;
  }
</style>

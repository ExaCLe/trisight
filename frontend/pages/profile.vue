<template>
  <UContainer class="container">
    <UButton @click="logout" class="logout-button bg-blue-dianne-900" size="xl">Logout</UButton>
  </UContainer>
</template>

<script setup>
const toast = useToast()
const config = useRuntimeConfig();

async function logout() {
  if (!import.meta.env.SSR) {
    try {
      // Remove the token on the server 
      await $fetch(`${config.public.backendUrl}/api/users/me`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      })
      // Remove the token on the server 
      await $fetch(`${config.public.backendUrl}/api/users/logout`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      })
      localStorage.removeItem('token')
      
      // Redirect to the login page
      await navigateTo('/login')
    } catch (error) {
      toast.add({
        title: 'Logout fehlgeschlagen. Bitte versuchen Sie es erneut.',
        id: 'logout-failed',
        color: "red",
      })
    }
  }
}
</script>
<style scoped>  
  .container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 60vh;
  }
</style>
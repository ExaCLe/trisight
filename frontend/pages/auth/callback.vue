<!-- pages/auth/callback.vue -->
<template>
  <div>
    Redirecting...
  </div>
</template>

<script setup>
import { useRouter, useRoute } from 'vue-router';

const router = useRouter();
const route = useRoute();

if (import.meta.client) {
  // Extract the token from the query parameters
  const accessToken = route.query.access_token;

  if (accessToken) {
    // Store the token in local storage or cookies for future API requests
    localStorage.setItem('token', accessToken);

    // Redirect the user to the dashboard or homepage
    router.push('/');
  } else {
    // Handle the case where no access token is provided (e.g., show an error)
    console.error('No access token found');
  }
}
</script>

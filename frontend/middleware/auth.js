export default defineNuxtRouteMiddleware((to, from) => {
  if (import.meta.client) {
    const token = localStorage.getItem('token');
    if (!token) {
      return navigateTo('/login'); // Redirect to the login page if no token is found
    }
  }
});
// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2024-04-03',
  devtools: { enabled: true },
  pages: true,
  modules: ["@nuxt/ui"], 
  runtimeConfig: {
    public: {
      backendUrl: process.env.BACKEND_URL || "http://localhost:8000",
    }
  }
})
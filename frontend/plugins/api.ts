export default defineNuxtPlugin((nuxtApp) => {
    const api = $fetch.create({
        baseURL: 'http://127.0.0.1:8000',  // Your FastAPI backend URL
        onRequest({ options }) {
            // You can add headers or other options here
            options.headers = options.headers || {}
        },
    })

    // Provide the custom $fetch instance globally
    return {
        provide: {
            api
        }
    }
})
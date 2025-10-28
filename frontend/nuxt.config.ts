// https://nuxt.com/docs/api/configuration/nuxt-config
import tailwindcss from "@tailwindcss/vite";
export default defineNuxtConfig({

  srcDir: 'app',
  runtimeConfig: {
    public: {
      apiBase: 'http://localhost:8000/api/v1' // <<— BACKEND
    }
  },

  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
   css: ['~/assets/css/input.css'], // you'll have to create this file
  vite: {
    plugins: [
      tailwindcss(),
    ],
  },


})

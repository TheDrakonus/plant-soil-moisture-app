// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  devtools: { enabled: true },
  modules: [
    '@nuxtjs/tailwindcss',
  ],
  nitro: {
    routeRules : {
      "/api": {
        cors: true,
      },
    }
  }
})
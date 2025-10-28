export default defineNuxtPlugin((nuxtApp) => {
  const config = useRuntimeConfig()
  const token = useCookie('accessToken')

  const api = $fetch.create({
    baseURL: config.public.apiBase, // es: http://localhost:8000/api/v1
    onRequest({ options }) {
      options.headers = options.headers || {}
      if (token.value) {
        options.headers.Authorization = `Bearer ${token.value}`
      }
    },
    onResponseError({ response }) {
      if (response.status === 401) {
        const t = useCookie('accessToken')
        t.value = null
        if (process.client) navigateTo('/login')
      }
    }
  })

  return {
    provide: {
      api
    }
  }
})

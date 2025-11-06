// plugins/ofetch-auth.client.js
export default defineNuxtPlugin((nuxtApp) => {
  // Hook globale degli errori delle fetch ($fetch è ofetch)
  nuxtApp.$fetch = $fetch.create({
    onResponseError({ response }) {
      if (response.status === 401) {
        const tokenState = useState('token', () => null)
        tokenState.value = null
        try { localStorage.removeItem('token') } catch {}
        // torna alla login mantenendo dove eri (facoltativo)
        const route = useRoute()
        navigateTo(`/login?next=${encodeURIComponent(route.fullPath)}`)
      }
    }
  })
})

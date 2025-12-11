// composables/useApi.js
// Wrapper centralizzato per $fetch con baseURL, timeout, Bearer e gestione 401

export const useApi = () => {
  const config = useRuntimeConfig()
  const token  = useState('token', () => null)
  const route  = process.client ? useRoute() : null

  // Fallbacks
  const apiBase   = config.public?.apiBase || config.public?.NUXT_PUBLIC_API_BASE || 'http://localhost:8000'
  const apiTimeout = Number(config.public?.apiTimeout ?? 15000)

  const isAbsolute = (u) => /^https?:\/\//i.test(u)

  const apiFetch = (url, opts = {}) => {
    const headers = { ...(opts.headers || {}) }

    // Authorization se non già impostato
    if (token.value && !headers.Authorization) {
      headers.Authorization = `Bearer ${token.value}`
    }

    // Se l'URL è relativo, usa baseURL; se è assoluto, non lo toccare
    const fetchOpts = {
      ...opts,
      headers,
      timeout: opts.timeout ?? apiTimeout,
      ...(isAbsolute(url) ? {} : { baseURL: apiBase }),
      // Gestione errori centralizzata (es. 401)
      onResponseError(ctx) {
        opts.onResponseError?.(ctx) // permette override per singola chiamata

        const status = ctx.response?.status
        if (status === 401) {
          // Token scaduto o non valido → logout soft
          try { localStorage.removeItem('token') } catch {}
          token.value = null

          if (process.client) {
            const current = route?.path || '/'
            // Evita loop se sei già in pagine pubbliche
            const publicRoutes = new Set(['/', '/login', '/register'])
            if (!publicRoutes.has(current)) navigateTo('/login')
          }
        }
      }
    }

    return $fetch(url, fetchOpts)
  }

  // Piccole scorciatoie
  const apiGet  = (url, opts = {}) => apiFetch(url, { ...opts, method: 'GET' })
  const apiPost = (url, body, opts = {}) => apiFetch(url, { ...opts, method: 'POST', body })
  const apiPatch = (url, body, opts = {}) => apiFetch(url, { ...opts, method: 'PATCH', body })
  const apiDelete = (url, opts = {}) => apiFetch(url, { ...opts, method: 'DELETE' })

  return { apiFetch, apiGet, apiPost, apiPatch, apiDelete, apiBase }
}

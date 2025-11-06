// composables/useAuth.js
function decodeJwt (token) {
  try {
    const base64 = token.split('.')[1] || ''
    const json = atob(base64.replace(/-/g, '+').replace(/_/g, '/'))
    return JSON.parse(decodeURIComponent(escape(json)))
  } catch {
    return null
  }
}

function isExpiredToken (token) {
  const p = decodeJwt(token)
  if (!p || typeof p.exp !== 'number') return false
  const now = Math.floor(Date.now() / 1000)
  return p.exp <= now
}

export const useAuth = () => {
  const { apiFetch } = useApi()
  const token = useState('token', () => null)

  // Reidrata da localStorage (client-side)
  if (process.client && token.value == null) {
    try {
      const saved = localStorage.getItem('token')
      token.value = saved || null
    } catch {}
  }

  // Se presente ma scaduto → logout immediato (solo client)
  if (process.client && token.value && isExpiredToken(token.value)) {
    token.value = null
    try { localStorage.removeItem('token') } catch {}
  }

  const login = async (email, password) => {
    const res = await apiFetch('/auth/login', {
      method: 'POST',
      body: { email, password }
    })
    token.value = res.access_token
    // persisti
    try { localStorage.setItem('token', res.access_token) } catch {}
    return res
  }

  const logout = () => {
    token.value = null
    try { localStorage.removeItem('token') } catch {}
    navigateTo('/login')
  }

  const isAuthenticated = computed(() => !!token.value && !isExpiredToken(token.value))
  const payload = computed(() => (token.value ? decodeJwt(token.value) : null))
  const isExpired = computed(() => (token.value ? isExpiredToken(token.value) : false))

  return { login, logout, token, isAuthenticated, payload, isExpired }
}

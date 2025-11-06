// middleware/auth.global.js
function getJwtExp(token) {
  try {
    const payload = JSON.parse(atob(token.split('.')[1] || ''))
    return typeof payload.exp === 'number' ? payload.exp : null
  } catch {
    return null
  }
}
function isExpired(token) {
  const exp = getJwtExp(token)
  if (!exp) return false
  const nowSec = Math.floor(Date.now() / 1000)
  return exp <= nowSec
}

export default defineNuxtRouteMiddleware(async (to) => {
  // non girare sul server
  if (process.server) return

  // === Token state & rehydration ===
  const tokenState = useState('token', () => null)
  let token = tokenState.value

  if (!token) {
    try {
      const saved = localStorage.getItem('token')
      if (saved) tokenState.value = saved
      token = tokenState.value
    } catch {}
  }

  // scadenza token → logout soft
  if (token && isExpired(token)) {
    tokenState.value = null
    try { localStorage.removeItem('token') } catch {}
    token = null

    // pulizia anche dello stato utente cache (se presente)
    const meState = useState('me', () => null)
    const lastTok = useState('me_last_token', () => null)
    meState.value = null
    lastTok.value = null
  }

  // === Rotte pubbliche ===
  const publicRoutes = new Set(['/', '/login', '/register'])
  const isMetaPublic = to.matched.some(r => r.meta?.public === true)
  const isPublic = publicRoutes.has(to.path) || isMetaPublic

  // blocco se non autenticato
  if (!token && !isPublic) {
    return navigateTo('/login')
  }

  // redirect se già autenticato
  if (token && (to.path === '/login' || to.path === '/register')) {
    return navigateTo('/overview')
  }

  // === Aggiorna/inizializza l'utente "me" quando autenticato ===
  // così l'header mostra subito nome/email senza dover ricaricare
  if (token) {
    const { me, fetchMe } = useMe()
    const lastTok = useState('me_last_token', () => null)

    // se il token è cambiato o me non è presente → forza refresh
    if (!me.value || lastTok.value !== token) {
      try {
        await fetchMe(true) // forza per evitare cache del login precedente
      } catch {
        // non bloccare la navigazione su errori transienti
      }
    }
  }
})

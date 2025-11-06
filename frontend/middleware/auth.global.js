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
  if (!exp) return false // se non c’è exp, considera valido (o metti true per forzare)
  const nowSec = Math.floor(Date.now() / 1000)
  return exp <= nowSec
}

export default defineNuxtRouteMiddleware((to) => {
  if (process.server) return

  const tokenState = useState('token', () => null)
  let token = tokenState.value

  // Se token presente ma scaduto → logout immediato
  if (token && isExpired(token)) {
    tokenState.value = null
    // se usi anche localStorage, puliscilo
    try { localStorage.removeItem('token') } catch {}
    token = null
  }

  // Rotte pubbliche
  const publicRoutes = new Set(['/', '/login', '/register'])
  const isMetaPublic = to.matched.some(r => r.meta?.public === true)
  const isPublic = publicRoutes.has(to.path) || isMetaPublic

  // Non autenticato → blocca tutto tranne rotte pubbliche
  if (!token && !isPublic) {
    return navigateTo('/login')
  }

  // Già autenticato → evita /login e /register
  if (token && (to.path === '/login' || to.path === '/register')) {
    return navigateTo('/overview')
  }
})

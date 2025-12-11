export const useMe = () => {
  const { apiGet } = useApi()
  const { token, payload } = useAuth()

  const me = useState('me', () => null)
  const pendingMe = useState('me_pending', () => false)
  const meError = useState('me_error', () => null)
  const lastToken = useState('me_last_token', () => null) // 👈 traccia token usato per caricare me

  const fetchMe = async (force = false) => {
    if (!token.value) {
      me.value = null
      lastToken.value = null
      return null
    }
    // evita richieste inutili se token identico e me già presente
    if (!force && lastToken.value === token.value && me.value) {
      return me.value
    }

    pendingMe.value = true
    meError.value = null
    try {
      const data = await apiGet('/auth/me')
      me.value = data || null
      lastToken.value = token.value
      return me.value
    } catch (e) {
      // fallback minimo dal JWT se disponibile
      const p = payload.value
      me.value = p ? { id: p.sub, email: p.email || '', name: p.name || '' } : null
      lastToken.value = token.value
      meError.value = e?.data?.detail || e?.message || 'Errore nel recupero profilo'
      return me.value
    } finally {
      pendingMe.value = false
    }
  }

  const clearMe = () => {
    me.value = null
    lastToken.value = null
    meError.value = null
  }

  // 🔁 Reagisci ai cambi token (login/logout / cambio utente)
  watch(token, async (newTok, oldTok) => {
    if (!newTok) {
      clearMe()
      return
    }
    if (newTok !== oldTok) {
      await fetchMe(true) // forza refresh quando cambia il token
    }
  }, { immediate: false })

  return { me, pendingMe, meError, fetchMe, clearMe }
}

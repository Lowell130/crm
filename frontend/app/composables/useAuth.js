export function useAuth() {
  const token = useCookie('accessToken', { sameSite: 'lax', secure: process.env.NODE_ENV === 'production' })
  const isAuthenticated = computed(() => Boolean(token.value))

  const login = async ({ email, password }) => {
    const config = useRuntimeConfig()
    const res = await $fetch('/auth/login', {
      baseURL: config.public.apiBase,
      method: 'POST',
      body: { email, password }
    })
    token.value = res.access_token // ritorna { access_token, token_type }
  }

  const logout = () => {
    token.value = null
    navigateTo('/login')
  }

  return { isAuthenticated, login, logout, token }
}

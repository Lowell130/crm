export default defineNuxtRouteMiddleware((to) => {
  if (to.path.startsWith('/app')) {
    const token = useCookie('accessToken')
    if (!token.value) return navigateTo('/login')
  }
})

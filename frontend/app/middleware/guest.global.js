export default defineNuxtRouteMiddleware((to) => {
  if (to.path === '/login') {
    const token = useCookie('accessToken')
    if (token.value) return navigateTo('/app/overview')
  }
})

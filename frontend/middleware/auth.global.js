// middleware/auth.global.js
// Protegge tutte le pagine eccetto /login
export default defineNuxtRouteMiddleware((to) => {
if (process.server) return
const token = useState('token').value
const publicRoutes = new Set(['/login'])
if (!token && !publicRoutes.has(to.path)) {
return navigateTo('/login')
}
})
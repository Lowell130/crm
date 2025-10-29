// composables/useAuth.js

export const useAuth = () => {
const { apiFetch } = useApi()
const token = useState('token')


const login = async (email, password) => {
const res = await apiFetch('/auth/login', {
method: 'POST',
body: { email, password }
})
token.value = res.access_token
return res
}


const logout = () => {
token.value = null
navigateTo('/login')
}


return { login, logout, token }
}
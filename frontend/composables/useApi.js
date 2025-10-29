// composables/useApi.js

// Wrapper centralizzato per $fetch con baseURL, timeout e Bearer
export const useApi = () => {
const config = useRuntimeConfig()
const token = useState('token')


const apiFetch = (url, opts = {}) => {
const headers = Object.assign({}, opts.headers || {})
if (token.value) headers['Authorization'] = `Bearer ${token.value}`


return $fetch(url, {
baseURL: config.public.apiBase,
timeout: config.public.apiTimeout,
headers,
...opts
})
}


return { apiFetch }
}
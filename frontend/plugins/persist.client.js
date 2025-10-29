// plugins/persist.client.js

// Sincronizza il token su localStorage senza Pinia
export default defineNuxtPlugin(() => {
const token = useState('token', () => null)
if (process.client) {
const saved = localStorage.getItem('crm_token')
if (saved && !token.value) token.value = saved
watch(token, (v) => {
if (v) localStorage.setItem('crm_token', v)
else localStorage.removeItem('crm_token')
})
}
})
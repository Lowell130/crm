<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900">
    <form @submit.prevent="onSubmit" class="w-full max-w-sm bg-white dark:bg-gray-800 rounded-xl shadow p-6 space-y-4">
      <h1 class="text-xl font-semibold text-gray-900 dark:text-gray-100">Accedi</h1>

      <div>
        <label class="block text-sm mb-1 text-gray-700 dark:text-gray-300">Email</label>
        <input v-model="email" type="email" required class="w-full rounded-lg border-gray-300 dark:border-gray-700 dark:bg-gray-900" placeholder="admin@mycrm.local" />
      </div>

      <div>
        <label class="block text-sm mb-1 text-gray-700 dark:text-gray-300">Password</label>
        <input v-model="password" type="password" required class="w-full rounded-lg border-gray-300 dark:border-gray-700 dark:bg-gray-900" placeholder="••••••••" />
      </div>

      <p v-if="error" class="text-sm text-red-600">{{ error }}</p>

      <button :disabled="pending" class="w-full inline-flex items-center justify-center rounded-lg bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 disabled:opacity-60">
        <span v-if="!pending">Entra</span>
        <span v-else>Accesso…</span>
      </button>
    </form>
  </div>
</template>

<script setup>
definePageMeta({ layout: 'public' })
const email = ref('')
const password = ref('')
const error = ref('')
const pending = ref(false)
const { login } = useAuth()

const onSubmit = async () => {
  error.value = ''
  pending.value = true
  try {
    await login({ email: email.value, password: password.value })
    navigateTo('/app/overview')
  } catch (e) {
    error.value = e?.data?.detail || 'Credenziali non valide'
  } finally {
    pending.value = false
  }
}
</script>

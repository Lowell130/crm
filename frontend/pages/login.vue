<template>
  <section class="min-h-[calc(100vh-64px-72px)] flex items-center bg-gray-50">
    <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 w-full">
      <div class="grid lg:grid-cols-2 gap-10 items-center">

        <!-- Side text (desktop only) -->
        <div class="hidden lg:block">
          <h2 class="text-3xl font-bold text-gray-900">Bentornato!</h2>
          <p class="mt-3 text-gray-600">
            Accedi per gestire clienti, fatture e i tuoi KPI in un’unica dashboard.
          </p>
        </div>

        <!-- Login form -->
        <div class="w-full max-w-md ml-auto">
          <div class="bg-white border border-gray-200 rounded-2xl shadow p-6">
            <h1 class="text-2xl font-semibold mb-6 text-gray-900">Accedi al CRM</h1>

            <form @submit.prevent="onSubmit" class="space-y-4">
              <!-- Email -->
              <div>
                <label for="email" class="block mb-2 text-sm font-medium text-gray-900">Email</label>
                <input
                  id="email"
                  v-model="email"
                  type="email"
                  required
                  class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5"
                  placeholder="you@example.com"
                />
              </div>

              <!-- Password -->
              <div>
                <label for="password" class="block mb-2 text-sm font-medium text-gray-900">Password</label>
                <input
                  id="password"
                  v-model="password"
                  type="password"
                  required
                  class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5"
                  placeholder="••••••••"
                />
              </div>

              <!-- Submit button -->
              <button
                type="submit"
                :disabled="isLoading"
                :class="{'opacity-50 cursor-not-allowed': isLoading}"
                class="w-full text-white bg-primary-600 hover:bg-primary-700 focus:ring-4 focus:outline-none focus:ring-primary-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center"
              >
                {{ isLoading ? 'Accesso in corso...' : 'Entra' }}
              </button>

              <!-- Alert -->
              <div v-if="error" class="text-sm text-red-600">
                {{ error }}
              </div>
            </form>

            <!-- Link a registrazione -->
            <p class="mt-4 text-sm text-gray-600">
              Non hai un account?
              <NuxtLink to="/register" class="text-primary-600 hover:underline">Registrati</NuxtLink>
            </p>
          </div>
        </div>

      </div>
    </div>
  </section>
</template>

<script setup>
definePageMeta({ layout: 'marketing', public: true })

const email = ref('')
const password = ref('')
const error = ref('')
const isLoading = ref(false)
const { login } = useAuth()

const onSubmit = async () => {
  if (isLoading.value) return

  error.value = ''
  isLoading.value = true
  try {
    await login(email.value, password.value)
    navigateTo('/overview')
  } catch (e) {
    error.value = e?.data?.detail || 'Credenziali non valide'
  } finally {
    isLoading.value = false
  }
}
</script>

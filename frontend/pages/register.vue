<template>
  <section class="min-h-[calc(100vh-64px-72px)] flex items-center bg-gray-50">
    <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 w-full">
      <div class="grid lg:grid-cols-2 gap-10 items-center">
        
        <!-- Text block (solo su desktop) -->
        <div class="hidden lg:block">
          <h2 class="text-3xl font-bold text-gray-900">Crea il tuo account</h2>
          <p class="mt-3 text-gray-600">
            Inizia gratis. Nessuna carta richiesta.
          </p>
        </div>

        <!-- Registration form -->
        <div class="w-full max-w-md ml-auto">
          <div class="bg-white border border-gray-200 rounded-2xl shadow p-6">
            <h1 class="text-2xl font-semibold mb-6 text-gray-900">Registrazione</h1>

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

              <!-- Submit Button -->
              <button
                type="submit"
                class="w-full text-white bg-primary-600 hover:bg-primary-700 focus:ring-4 focus:outline-none focus:ring-primary-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center"
              >
                Crea account
              </button>

              <!-- Alert messaggi -->
              <div v-if="error" class="text-sm text-red-600">
                {{ error }}
              </div>

              <div v-if="success" class="text-sm text-green-700">
                Registrazione avvenuta. Ora puoi 
                <NuxtLink to="/login" class="underline hover:text-primary-600">accedere</NuxtLink>.
              </div>
            </form>

            <!-- Link login -->
            <p class="mt-4 text-sm text-gray-600">
              Hai già un account? 
              <NuxtLink to="/login" class="text-primary-600 hover:underline">Accedi</NuxtLink>
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
const success = ref(false)

const runtime = useRuntimeConfig()
const API_BASE = runtime.public?.apiBase || runtime.public?.NUXT_PUBLIC_API_BASE || 'http://localhost:8000'

const onSubmit = async () => {
  error.value = ''
  success.value = false
  try {
    await $fetch(`${API_BASE}/auth/register`, {
      method: 'POST',
      body: { email: email.value, password: password.value }
    })
    success.value = true
  } catch (e) {
    error.value = e?.data?.detail || 'Registrazione non riuscita'
  }
}
</script>

<template>
  <div>
    <!-- Topbar pubblica -->
    <header class="border-b bg-white/70 dark:bg-gray-900/70 backdrop-blur">
      <div class="mx-auto max-w-7xl px-4 py-3 flex items-center justify-between">
        <NuxtLink to="/" class="font-semibold text-lg">MyCRM</NuxtLink>

        <nav class="flex items-center gap-3">
          <NuxtLink to="/login" class="px-3 py-1.5 rounded-lg bg-blue-600 text-white hover:bg-blue-700">
            Accedi
          </NuxtLink>
          <button @click="toggleTheme" class="px-3 py-1.5 rounded-lg bg-gray-100 dark:bg-gray-800">
            {{ theme.value === 'dark' ? '☀️' : '🌙' }}
          </button>
        </nav>
      </div>
    </header>

    <!-- Contenuto pagina pubblica -->
    <main class="mx-auto max-w-7xl px-4 py-8">
      <slot />
    </main>

    <!-- Footer semplice -->
    <footer class="border-t mt-12">
      <div class="mx-auto max-w-7xl px-4 py-6 text-sm text-gray-500">
        © {{ new Date().getFullYear() }} MyCRM — Tutti i diritti riservati
      </div>
    </footer>
  </div>
</template>

<script setup>
const theme = useCookie('theme', { sameSite: 'lax' })
const toggleTheme = () => {
  theme.value = theme.value === 'dark' ? '' : 'dark'
  if (process.client) {
    document.documentElement.classList.toggle('dark', theme.value === 'dark')
  }
}
</script>

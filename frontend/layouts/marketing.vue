<template>
  <div class="min-h-screen flex flex-col bg-white">
    <!-- Navbar -->
    <header class="sticky top-0 z-20 border-b bg-white/80 backdrop-blur">
      <nav class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        <!-- Logo -->
        <NuxtLink to="/" class="flex items-center gap-2">
          <span class="inline-flex h-8 w-8 items-center justify-center rounded-full bg-primary-600 text-white font-bold">
            C
          </span>
          <span class="text-lg font-semibold text-gray-900">CRM</span>
        </NuxtLink>

        <!-- Desktop nav -->
        <div class="hidden sm:flex items-center gap-3">
          <NuxtLink
            to="/login"
            class="text-sm px-4 py-2 rounded-lg border border-gray-300 text-gray-700 hover:bg-gray-50 hover:text-gray-900 transition"
          >
            Accedi
          </NuxtLink>
          <NuxtLink
            to="/register"
            class="text-sm px-4 py-2 rounded-lg bg-primary-600 text-white hover:bg-primary-700 transition"
          >
            Inizia gratis
          </NuxtLink>
        </div>

        <!-- Mobile nav button (solo login) -->
        <div class="sm:hidden">
          <NuxtLink
            to="/login"
            class="text-sm px-3 py-2 rounded-lg border border-gray-300 text-gray-700 hover:bg-gray-100 transition"
          >
            Accedi
          </NuxtLink>
        </div>
      </nav>
    </header>

    <!-- Contenuto dinamico -->
    <main class="flex-1">
      <slot />
    </main>

    <!-- Footer -->
    <footer class="border-t bg-white">
      <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-8 text-center text-sm text-gray-500">
        © {{ new Date().getFullYear() }} CRM — Tutti i diritti riservati.
      </div>
    </footer>
  </div>
</template>

<script setup>
// Layout "marketing" senza header/sidebar applicativo
</script>

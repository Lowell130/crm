<template>
  <div class="min-h-screen flex">
    <!-- Sidebar -->
    <aside
      class="w-64 shrink-0 hidden md:flex md:flex-col border-r bg-white dark:bg-gray-900"
      aria-label="Sidebar"
    >
      <div class="h-14 px-4 flex items-center border-b">
        <NuxtLink to="/app/overview" class="font-semibold text-lg">MyCRM</NuxtLink>
      </div>

      <nav class="p-3 space-y-1">
        <NuxtLink to="/app/overview" class="nav-item" :class="isActive('/app/overview')">🏠 Dashboard</NuxtLink>
        <NuxtLink to="/app/customers" class="nav-item" :class="isActive('/app/customers')">👥 Clienti</NuxtLink>
        <NuxtLink to="/app/communications" class="nav-item" :class="isActive('/app/communications')">✉️ Comunicazioni</NuxtLink>
        <NuxtLink to="/app/exports" class="nav-item" :class="isActive('/app/exports')">⬇️ Export</NuxtLink>
        <NuxtLink to="/app/settings" class="nav-item" :class="isActive('/app/settings')">⚙️ Impostazioni</NuxtLink>
      </nav>

      <div class="mt-auto p-3 border-t">
      <button @click="toggleTheme" class="w-full px-3 py-2 rounded-lg bg-gray-100 dark:bg-gray-800 text-left">
  Tema: <strong>{{ (theme && theme.value === 'dark') ? 'Dark' : 'Light' }}</strong>
</button>
      </div>
    </aside>

    <!-- Contenuto -->
    <div class="flex-1 flex flex-col min-w-0">
      <!-- Topbar -->
      <header class="h-14 border-b bg-white/60 dark:bg-gray-900/60 backdrop-blur">
        <div class="h-full px-4 flex items-center justify-between">
          <div class="flex items-center gap-2">
            <!-- burger per mobile -->
            <button class="md:hidden px-2 py-1 rounded-lg bg-gray-100 dark:bg-gray-800" @click="drawerOpen = !drawerOpen">☰</button>
            <span class="text-sm text-gray-500">Area riservata</span>
          </div>
          <div class="flex items-center gap-2">
            <NuxtLink to="/" class="px-3 py-1.5 rounded-lg bg-gray-100 dark:bg-gray-800">Landing</NuxtLink>
            <button @click="logout" class="px-3 py-1.5 rounded-lg bg-red-600 text-white hover:bg-red-700">
              Esci
            </button>
          </div>
        </div>
      </header>

      <!-- Drawer mobile -->
      <transition name="fade">
        <div v-if="drawerOpen" class="md:hidden fixed inset-0 z-40">
          <div class="absolute inset-0 bg-black/40" @click="drawerOpen=false"></div>
          <aside class="absolute left-0 top-0 bottom-0 w-64 bg-white dark:bg-gray-900 border-r p-3 space-y-1">
            <div class="h-14 px-2 flex items-center border-b">
              <NuxtLink to="/app/overview" class="font-semibold text-lg" @click="drawerOpen=false">MyCRM</NuxtLink>
            </div>
            <NuxtLink @click="drawerOpen=false" to="/app/overview" class="nav-item" :class="isActive('/app/overview')">🏠 Dashboard</NuxtLink>
            <NuxtLink @click="drawerOpen=false" to="/app/customers" class="nav-item" :class="isActive('/app/customers')">👥 Clienti</NuxtLink>
            <NuxtLink @click="drawerOpen=false" to="/app/communications" class="nav-item" :class="isActive('/app/communications')">✉️ Comunicazioni</NuxtLink>
            <NuxtLink @click="drawerOpen=false" to="/app/exports" class="nav-item" :class="isActive('/app/exports')">⬇️ Export</NuxtLink>
            <NuxtLink @click="drawerOpen=false" to="/app/settings" class="nav-item" :class="isActive('/app/settings')">⚙️ Impostazioni</NuxtLink>

            <div class="mt-4 border-t pt-3">
              <button @click="toggleTheme" class="w-full px-3 py-2 rounded-lg bg-gray-100 dark:bg-gray-800 text-left">
                Tema: <strong>{{ theme.value === 'dark' ? 'Dark' : 'Light' }}</strong>
              </button>
            </div>
          </aside>
        </div>
      </transition>

      <!-- Main slot -->
      <main class="p-4">
        <slot />
      </main>
    </div>
  </div>
</template>

<script setup>
const route = useRoute()
// ✅ default vuoto per SSR: il ref esiste sempre
const theme = useCookie('theme', { sameSite: 'lax', default: () => '' })
const drawerOpen = ref(false)

function isActive(prefix) {
  return route.path.startsWith(prefix) ? 'bg-gray-100 dark:bg-gray-800' : ''
}
function toggleTheme() {
  theme.value = theme.value === 'dark' ? '' : 'dark'
  if (process.client) {
    document.documentElement.classList.toggle('dark', theme.value === 'dark')
  }
}

const { logout } = useAuth()
</script>


<style scoped>
.nav-item {
  display: block;
  padding: 0.5rem 0.75rem;
  border-radius: 0.5rem;
}
.fade-enter-active, .fade-leave-active { transition: opacity .15s }
.fade-enter-from, .fade-leave-to { opacity: 0 }
</style>

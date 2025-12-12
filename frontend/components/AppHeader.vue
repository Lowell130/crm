<template>
  <nav class="bg-white border-b border-gray-200 px-4 py-2.5 dark:bg-gray-800 dark:border-gray-700 fixed left-0 right-0 top-0 z-50">
    <div class="flex flex-wrap justify-between items-center">
      <div class="flex justify-start items-center">
        <!-- Hamburger button (mobile only) -->
        <button
          @click="toggleSidebar"
          type="button"
          class="inline-flex items-center p-2 text-sm text-gray-500 rounded-lg md:hidden hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-200 dark:text-gray-400 dark:hover:bg-gray-700 dark:focus:ring-gray-600"
          aria-controls="drawer-navigation"
          aria-expanded="false"
        >
          <span class="sr-only">Apri menu</span>
          <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M3 5a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM3 10a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM3 15a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z" clip-rule="evenodd"></path>
          </svg>
        </button>

        <a href="#" class="flex items-center justify-between mr-4">
          <img src="https://flowbite.s3.amazonaws.com/logo.svg" class="mr-3 h-8" alt="Logo"/>
          <span class="self-center text-2xl font-semibold whitespace-nowrap dark:text-white">CRM</span>
        </a>
      </div>

      <div class="flex items-center lg:order-2 gap-3">
        <!-- Testo con nome/email -->
        <div v-if="me" class="text-sm text-gray-700 dark:text-gray-200">
          {{ me.name || me.email || 'Utente' }}
        </div>

        <!-- Avatar + (opzionale) menu -->
        <div class="relative" v-if="me">
          <button
            type="button"
            class="flex text-sm bg-gray-800 rounded-full focus:ring-4 focus:ring-gray-300 dark:focus:ring-gray-600"
            aria-label="User menu"
            @click="open = !open"
          >
            <img class="w-8 h-8 rounded-full" src="https://flowbite.s3.amazonaws.com/blocks/marketing-ui/avatars/michael-gough.png" alt="user"/>
          </button>
          <div
            v-if="open"
            class="absolute right-0 mt-2 w-44 bg-white border border-gray-200 rounded-lg shadow-lg dark:bg-gray-800 dark:border-gray-700"
          >
            <div class="px-4 py-2 text-xs text-gray-500 dark:text-gray-400">
              {{ me.email }}
            </div>
            <button
              @click="doLogout"
              class="w-full text-left px-4 py-2 text-sm text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700"
            >
              Esci
            </button>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
const { me, fetchMe, clearMe } = useMe()
const { logout } = useAuth()
const open = ref(false)

// Sidebar state (shared via event bus or composable)
const sidebarOpen = useState('sidebarOpen', () => false)

function toggleSidebar() {
  sidebarOpen.value = !sidebarOpen.value
}

onMounted(async () => { await fetchMe() })

const doLogout = () => {
  clearMe()
  logout()  // questo rimuove il token e fa navigateTo('/login')
}
</script>

<template>
  <!-- Backdrop (mobile only) -->
  <div
    v-if="sidebarOpen"
    @click="sidebarOpen = false"
    class="fixed inset-0 z-30 bg-black/50 md:hidden"
  ></div>

  <!-- sidebar fissa a sinistra sotto l’header -->
  <aside
    :class="[
      'fixed top-0 left-0 z-40 w-64 h-screen pt-14 transition-transform bg-white border-r border-gray-200 md:translate-x-0 dark:bg-gray-800 dark:border-gray-700',
      sidebarOpen ? 'translate-x-0' : '-translate-x-full'
    ]"
    aria-label="Sidenav"
    id="drawer-navigation"
  >








    <div class="overflow-y-auto py-5 px-3 h-full bg-white dark:bg-gray-800">
      <ul class="space-y-2">
        <li>
          <NuxtLink
            to="/overview"
            @click="closeSidebar"
            class="flex items-center p-2 text-base font-medium text-gray-900 rounded-lg dark:text-white hover:bg-gray-100 dark:hover:bg-gray-700 group"
          >
            <svg aria-hidden="true" class="w-6 h-6 text-gray-500 transition duration-75 dark:text-gray-400 group-hover:text-gray-900 dark:group-hover:text-white" fill="currentColor" viewBox="0 0 20 20">
              <path d="M2 10a8 8 0 018-8v8h8a8 8 0 11-16 0z"></path>
              <path d="M12 2.252A8.014 8.014 0 0117.748 8H12V2.252z"></path>
            </svg>
            <span class="ml-3">Overview</span>
          </NuxtLink>
        </li>

  <li>
          <NuxtLink
            to="/dashboard"
            @click="closeSidebar"
            class="flex items-center p-2 text-base font-medium text-gray-900 rounded-lg dark:text-white hover:bg-gray-100 dark:hover:bg-gray-700 group"
          >
            <svg class="w-6 h-6 text-gray-500 dark:text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" viewBox="0 0 24 24">
  <path fill-rule="evenodd" d="M8 4a4 4 0 1 0 0 8 4 4 0 0 0 0-8Zm-2 9a4 4 0 0 0-4 4v1a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2v-1a4 4 0 0 0-4-4H6Zm7.25-2.095c.478-.86.75-1.85.75-2.905a5.973 5.973 0 0 0-.75-2.906 4 4 0 1 1 0 5.811ZM15.466 20c.34-.588.535-1.271.535-2v-1a5.978 5.978 0 0 0-1.528-4H18a4 4 0 0 1 4 4v1a2 2 0 0 1-2 2h-4.535Z" clip-rule="evenodd"/>
</svg>

            <span class="ml-3">Clienti</span>
          </NuxtLink>
        </li>
      <!-- dentro <ul class="space-y-2"> -->
<li>
  <NuxtLink
    to="/invoices"
    @click="closeSidebar"
    class="flex items-center p-2 text-base font-medium text-gray-900 rounded-lg dark:text-white hover:bg-gray-100 dark:hover:bg-gray-700 group"
  >
    <!-- icona semplice (receipt) -->
    <svg aria-hidden="true" class="w-6 h-6 text-gray-500 transition duration-75 group-hover:text-gray-900 dark:group-hover:text-white" fill="currentColor" viewBox="0 0 20 20">
      <path d="M6 2a2 2 0 00-2 2v12l3-1 3 1 3-1 3 1V4a2 2 0 00-2-2H6zM7 6h6v2H7V6zm0 4h6v2H7v-2z"/>
    </svg>
    <span class="ml-3">Fatture</span>
  </NuxtLink>
</li>

<li>
  <button
    @click="logout"
    class="w-full flex items-center p-2 text-base font-medium text-gray-900 rounded-lg dark:text-white hover:bg-red-50 dark:hover:bg-red-900/30 group"
  >
    <svg
      aria-hidden="true"
      class="w-6 h-6 text-red-600 transition duration-75 group-hover:text-red-700 dark:group-hover:text-red-400"
      fill="none"
      stroke="currentColor"
      stroke-width="2"
      viewBox="0 0 24 24"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a2 2 0 01-2 2H6a2 2 0 01-2-2V7a2 2 0 012-2h5a2 2 0 012 2v1"
      />
    </svg>
    <span class="ml-3 text-red-700 dark:text-red-400 group-hover:text-red-600 dark:group-hover:text-red-300">
      Logout
    </span>
  </button>
</li>


      </ul>
    </div>



    
  </aside>
</template>

<script setup>
import { useAuth } from '@/composables/useAuth'

const { logout } = useAuth()

// Shared state with AppHeader
const sidebarOpen = useState('sidebarOpen', () => false)

function closeSidebar() {
  // Close sidebar when clicking a link (mobile)
  if (window.innerWidth < 768) {
    sidebarOpen.value = false
  }
}
</script>
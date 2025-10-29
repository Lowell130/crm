<template>
  <!-- topbar fissa -->
  <nav
    class="bg-white border-b border-gray-200 px-4 py-2.5 dark:bg-gray-800 dark:border-gray-700 fixed left-0 right-0 top-0 z-50"
  >
    <div class="flex flex-wrap justify-between items-center">
      <div class="flex justify-start items-center">
        <!-- toggle sidebar (solo estetico qui) -->
        <button
          class="p-2 mr-2 text-gray-600 rounded-lg cursor-pointer md:hidden hover:text-gray-900 hover:bg-gray-100 focus:bg-gray-100 dark:focus:bg-gray-700 focus:ring-2 focus:ring-gray-100 dark:focus:ring-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white"
          aria-label="Toggle sidebar"
        >
          <svg aria-hidden="true" class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd"
              d="M3 5a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM3 10a1 1 0 011-1h6a1 1 0 110 2H4a1 1 0 01-1-1zM3 15a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z"
              clip-rule="evenodd"/>
          </svg>
          <span class="sr-only">Toggle sidebar</span>
        </button>

        <a href="#" class="flex items-center justify-between mr-4">
          <img src="https://flowbite.s3.amazonaws.com/logo.svg" class="mr-3 h-8" alt="Logo"/>
          <span class="self-center text-2xl font-semibold whitespace-nowrap dark:text-white">CRM</span>
        </a>

        <!-- search (desktop) -->
        <!-- <form action="#" method="GET" class="hidden md:block md:pl-2">
          <label for="topbar-search" class="sr-only">Search</label>
          <div class="relative md:w-96">
            <div class="flex absolute inset-y-0 left-0 items-center pl-3 pointer-events-none">
              <svg class="w-5 h-5 text-gray-500 dark:text-gray-400" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" clip-rule="evenodd"
                  d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z"/>
              </svg>
            </div>
            <input
              type="text" id="topbar-search" placeholder="Search"
              class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full pl-10 p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white"
            />
          </div>
        </form> -->
      </div>

      <div class="flex items-center lg:order-2">
        <!-- qualche icona a destra -->
        <button
          type="button"
          class="p-2 text-gray-500 rounded-lg hover:text-gray-900 hover:bg-gray-100 dark:text-gray-400 dark:hover:text-white dark:hover:bg-gray-700 focus:ring-4 focus:ring-gray-300 dark:focus:ring-gray-600"
          aria-label="Apps"
        >
          <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
            <path
              d="M5 3a2 2 0 00-2 2v2a2 2 0 002 2h2a2 2 0 002-2V5a2 2 0 00-2-2H5zM5 11a2 2 0 00-2 2v2a2 2 0 002 2h2a2 2 0 002-2v-2a2 2 0 00-2-2H5zM11 5a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V5zM11 13a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z"/>
          </svg>
        </button>

        <button
          type="button"
          class="flex mx-3 text-sm bg-gray-800 rounded-full focus:ring-4 focus:ring-gray-300 dark:focus:ring-gray-600"
          aria-label="User menu"
        >
          <img class="w-8 h-8 rounded-full" src="https://flowbite.s3.amazonaws.com/blocks/marketing-ui/avatars/michael-gough.png" alt="user"/>
        </button>
      </div>
    </div>
  </nav>
</template>

<script setup>
// nessuna logica JS necessaria per mostrarlo
</script>

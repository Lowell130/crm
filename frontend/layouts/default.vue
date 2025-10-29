<template>
  <div class="antialiased bg-gray-50 dark:bg-gray-900">
    <!-- Header fisso -->
    <AppHeader />

    <!-- Sidebar fissa a sinistra -->
    <AppSidebar />

    <!-- Contenuto pagina -->
    <main class="p-4 md:ml-64 h-auto pt-20">
      <slot />
    </main>
  </div>
</template>

<script setup>
import AppHeader from '~/components/AppHeader.vue'
import AppSidebar from '~/components/AppSidebar.vue'
</script>

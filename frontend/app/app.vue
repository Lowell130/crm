<template>
  <div :class="themeClass" class="min-h-screen bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-gray-100">
    <!-- Announcer per accessibilità -->
    <NuxtRouteAnnouncer />

    <!-- Wrapper layout dinamico -->
    <NuxtLayout>
      <NuxtPage />
    </NuxtLayout>
  </div>
</template>

<script setup>
// Dark mode handling (toggle gestito via cookie o system preference)
const theme = useCookie('theme', { sameSite: 'lax' })
const themeClass = computed(() => (theme.value === 'dark' ? 'dark' : ''))

// Imposta dark mode di default se il sistema la preferisce
onMounted(() => {
  if (!theme.value && window.matchMedia('(prefers-color-scheme: dark)').matches) {
    theme.value = 'dark'
  }
})
</script>

<style>
/* Garantisce che Tailwind dark mode funzioni in modalità 'class' */
html.dark {
  color-scheme: dark;
}
</style>

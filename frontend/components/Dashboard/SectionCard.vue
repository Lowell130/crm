<template>
  <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700">
    <div class="px-4 py-3 border-b border-gray-100 dark:border-gray-700">
      <h2 class="text-sm font-semibold text-gray-700 dark:text-gray-200">{{ title }}</h2>
    </div>
    <div class="p-4">
      <slot />
    </div>
  </div>
</template>

<script setup>
const props = defineProps({ title: { type: String, default: '' } })
</script>

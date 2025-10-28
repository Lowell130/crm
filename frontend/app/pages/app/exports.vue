<template>
  <div>
    <h1 class="text-xl font-semibold">Export</h1>
    <div class="mt-4 flex gap-2">
      <button @click="downloadCsv" class="px-4 py-2 rounded bg-gray-100 dark:bg-gray-800">Scarica CSV</button>
      <button @click="downloadXlsx" class="px-4 py-2 rounded bg-gray-100 dark:bg-gray-800">Scarica XLSX</button>
    </div>
  </div>
</template>

<script setup>
definePageMeta({ layout: 'dashboard' })
const { downloadCsv, downloadXlsx } = useExports()
</script>

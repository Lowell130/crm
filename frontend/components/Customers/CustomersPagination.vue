<template>
  <nav class="flex flex-col md:flex-row justify-between items-start md:items-center space-y-3 md:space-y-0 p-4" aria-label="Table navigation">
    <span class="text-sm text-gray-500">
      Mostrando <span class="font-semibold text-gray-900">{{ fromItem }} – {{ toItem }}</span> di
      <span class="font-semibold text-gray-900">{{ totalDisplay }}</span>
    </span>
    <ul class="inline-flex items-stretch -space-x-px">
      <li>
        <button :disabled="page===1" @click="$emit('prev')" class="flex items-center justify-center h-full py-1.5 px-3 ml-0 text-gray-500 bg-white rounded-l-lg border border-gray-300 hover:bg-gray-100 hover:text-gray-700 disabled:opacity-50">
          <span class="sr-only">Precedente</span>
          <svg class="w-5 h-5" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clip-rule="evenodd"/></svg>
        </button>
      </li>
      <li>
        <span class="flex items-center justify-center text-sm py-2 px-3 leading-tight text-primary-600 bg-primary-50 border border-primary-300">{{ page }}</span>
      </li>
      <li>
        <button :disabled="!hasNext" @click="$emit('next')" class="flex items-center justify-center h-full py-1.5 px-3 text-gray-500 bg-white rounded-r-lg border border-gray-300 hover:bg-gray-100 hover:text-gray-700 disabled:opacity-50">
          <span class="sr-only">Successivo</span>
          <svg class="w-5 h-5" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd"/></svg>
        </button>
      </li>
    </ul>
  </nav>
</template>

<script setup>
defineProps({
  page: { type: Number, required: true },
  hasNext: { type: Boolean, required: true },
  fromItem: { type: Number, required: true },
  toItem: { type: Number, required: true },
  totalDisplay: { type: [String, Number], required: true }
})
defineEmits(['prev','next'])
</script>

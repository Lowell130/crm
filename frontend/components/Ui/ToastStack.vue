<template>
  <div class="fixed top-4 right-4 z-[60] space-y-3">
    <div
      v-for="t in toasts"
      :key="t.id"
      class="flex items-center w-full max-w-xs p-4 text-gray-500 bg-white rounded-lg shadow-sm border border-red-100"
      role="alert"
    >
      <!-- Icona -->
      <div class="inline-flex items-center justify-center shrink-0 w-8 h-8 text-red-500 bg-red-100 rounded-lg">
        <svg class="w-5 h-5" viewBox="0 0 20 20" fill="currentColor">
          <path d="M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5Zm3.707 11.793a1 1 0 1 1-1.414 1.414L10 11.414l-2.293 2.293a1 1 0 0 1-1.414-1.414L8.586 10 6.293 7.707a1 1 0 0 1 1.414-1.414L10 8.586l2.293-2.293a1 1 0 0 1 1.414 1.414L11.414 10l2.293 2.293Z"/>
        </svg>
        <span class="sr-only">Error icon</span>
      </div>

      <!-- Testo -->
      <div class="ms-3 text-sm font-normal flex-1">
        <!-- <div v-if="t.title" class="text-sm font-medium text-gray-900">{{ t.title }}</div> -->
        <div class="text-sm">{{ t.message }}</div>

        <div v-if="t.onRetry" class="flex gap-2 mt-2">
          <button
            class="px-2.5 py-1 text-xs rounded border text-gray-700 hover:bg-gray-100"
            @click="() => { t.onRetry?.(); dismissToast(t.id) }"
          >
            Riprova
          </button>
        </div>
      </div>

      <!-- Chiudi -->
      <button
        type="button"
        class="ms-auto -mx-1.5 -my-1.5 bg-white text-gray-400 hover:text-gray-900 rounded-lg focus:ring-2 focus:ring-gray-300 p-1.5 hover:bg-gray-100 inline-flex items-center justify-center h-8 w-8"
        @click="dismissToast(t.id)"
        aria-label="Chiudi"
      >
        <svg class="w-3 h-3" viewBox="0 0 14 14" fill="none">
          <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6"/>
        </svg>
      </button>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  toasts: { type: Array, default: () => [] },
  dismissToast: { type: Function, required: true }
})
// Render-only: non mutiamo props, nessun ulteriore script necessario
</script>

<!-- components/Customers/CustomersSearch.vue -->

<template>
  <form class="flex items-center" @submit.prevent="$emit('search')">
    <label for="customers-search" class="sr-only">Cerca</label>
    <div class="relative w-full">
      <div class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
       <svg aria-hidden="true" class="w-5 h-5 text-gray-500" fill="currentColor" viewBox="0 0 20 20"> <path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd" /> </svg>
      </div>

      <input
        :value="modelValue"
        @input="$emit('update:modelValue', $event.target.value)"
        id="customers-search"
        type="text"
        class="bg-gray-50 border border-gray-300 text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full pl-10 pr-8 p-2"
        placeholder="Cerca per nome, ragione sociale, CF/P.IVA, email…"
        @keyup.esc="$emit('clear')"
      />

      <button
        v-if="modelValue"
        type="button"
        class="absolute inset-y-0 right-0 flex items-center pr-2 text-gray-400 hover:text-gray-600"
        @click="$emit('clear')"
        aria-label="Pulisci ricerca"
        title="Pulisci"
      >
        <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none">
          <path stroke="currentColor" stroke-linecap="round" stroke-width="2" d="M6 18 18 6M18 18 6 6"/>
        </svg>
      </button>
    </div>
  </form>
</template>

<script setup>
defineProps({ modelValue: { type: String, default: '' } })
defineEmits(['update:modelValue','search','clear'])
</script>

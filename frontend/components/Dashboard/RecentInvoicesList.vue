<template>
  <div class="space-y-2">
    <div class="text-sm text-gray-500">Nessuna fattura recente (placeholder)</div>
    <!-- Quando avrai i dati:
    <ul class="divide-y">
      <li v-for="inv in invoices" :key="inv.id" class="py-2 flex items-center justify-between">
        <NuxtLink :to="`/invoices/details/${inv.id}`" class="text-blue-600 hover:underline">
          {{ inv.number }}
        </NuxtLink>
        <div class="text-sm text-gray-700">{{ inv.total.toFixed(2) }} €</div>
      </li>
    </ul>
    -->
  </div>
</template>

<script setup>
// const props = defineProps({ invoices: { type: Array, default: () => [] } })
</script>

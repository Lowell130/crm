<template>
  <div class="overflow-x-auto">
    <table class="w-full text-sm text-left text-gray-500">
      <thead class="text-xs text-gray-700 uppercase bg-gray-50">
        <tr>
          <th class="px-4 py-3">Cliente</th>
          <th class="px-4 py-3">Tipo</th>
          <th class="px-4 py-3">CF / P.IVA</th>
          <th class="px-4 py-3">Email</th>
          <th class="px-4 py-3"><span class="sr-only">Azioni</span></th>
        </tr>
      </thead>

      <tbody>
        <!-- SKELETON -->
        <template v-if="pending">
          <tr v-for="i in 8" :key="'sk-'+i" class="border-b dark:border-gray-700">
            <td class="px-4 py-3">
              <div class="animate-pulse">
                <div class="h-4 bg-gray-200 rounded w-40 mb-2"></div>
                <div class="h-3 bg-gray-200 rounded w-24"></div>
              </div>
            </td>
            <td class="px-4 py-3"><div class="animate-pulse h-5 bg-gray-200 rounded w-16"></div></td>
            <td class="px-4 py-3"><div class="animate-pulse h-4 bg-gray-200 rounded w-32"></div></td>
            <td class="px-4 py-3"><div class="animate-pulse h-4 bg-gray-200 rounded w-48"></div></td>
            <td class="px-4 py-3"><div class="animate-pulse h-5 bg-gray-200 rounded w-8 ml-auto"></div></td>
          </tr>
        </template>

        <!-- EMPTY -->
        <tr v-else-if="!items.length" class="border-b dark:border-gray-700">
          <td class="px-4 py-8 text-center text-gray-500" colspan="5">
            <slot name="empty">
              <div class="flex flex-col items-center gap-2">
                <svg class="w-8 h-8" viewBox="0 0 24 24" fill="none">
                  <path d="M10 4h10M4 8h16M4 12h10M4 16h16M4 20h10" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
                </svg>
                <div class="text-sm">Nessun cliente trovato</div>
                <div class="text-xs text-gray-400">Prova a cambiare i filtri o la ricerca</div>
              </div>
            </slot>
          </td>
        </tr>

        <!-- ROWS -->
        <tr v-else v-for="c in items" :key="c._id" class="border-b dark:border-gray-700">
          <th class="px-4 py-3 font-medium text-gray-900 whitespace-nowrap">
            <div class="flex flex-col">
              <span v-if="c.kind==='B2B'">{{ c.company_name || '—' }}</span>
              <span v-else>{{ [c.first_name, c.last_name].filter(Boolean).join(' ') || '—' }}</span>
              <span class="text-xs text-gray-500">ID: <span class="font-mono">{{ c._id }}</span></span>
            </div>
          </th>

          <td class="px-4 py-3">
            <span class="px-2 py-0.5 rounded-full text-xs"
                  :class="c.kind==='B2B' ? 'bg-blue-100 text-blue-700' : 'bg-emerald-100 text-emerald-700'">
              {{ c.kind }}
            </span>
          </td>

          <td class="px-4 py-3">
            <span v-if="c.kind==='B2B'">{{ c.vat_number || '—' }}</span>
            <span v-else>{{ c.codice_fiscale || '—' }}</span>
          </td>

          <td class="px-4 py-3">{{ c.email || '—' }}</td>

          <td class="px-4 py-3 flex items-center justify-end gap-1">
            <slot name="actions" :customer="c" />
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
defineProps({
  items: { type: Array, default: () => [] },
  pending: { type: Boolean, default: false }
})
</script>


<style scoped>
.border-b {
    border-bottom-width: 1px;
    border-color: #e5e7eb;
}

</style>
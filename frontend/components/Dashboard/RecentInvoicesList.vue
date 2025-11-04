<!-- components/Dashboard/RecentInvoicesList.vue -->
<template>
  <div class="space-y-3">
    <!-- Stato: loading / error -->
    <div v-if="loading" class="text-sm text-gray-500">Caricamento…</div>
    <div v-else-if="error" class="text-sm text-red-600">{{ error }}</div>

    <!-- Lista -->
    <ul v-else>
      <li
        v-for="inv in invoices"
        :key="inv.id"
        class="py-2 flex items-center justify-between border-b"
      >
        <div class="flex items-center gap-2 min-w-0">
          <NuxtLink
            :to="`/invoices/details/${inv.id}`"
            class="text-blue-600 hover:underline truncate"
            :title="inv.number"
          >
            {{ inv.number || '—' }}
          </NuxtLink>

          <span
            class="text-xs px-2 py-0.5 rounded shrink-0"
            :class="inv.status === 'issued'
              ? 'bg-green-100 text-green-700'
              : inv.status === 'draft'
                ? 'bg-yellow-100 text-yellow-700'
                : 'bg-red-100 text-red-700'"
          >
            {{ inv.status }}
          </span>
        </div>

        <div class="text-sm text-gray-700 whitespace-nowrap">
          {{ fmt(inv.total) }} €
        </div>
      </li>

      <li v-if="!invoices.length" class="py-2 text-sm text-gray-500">
        Nessuna fattura recente
      </li>
    </ul>

    <!-- Footer con pulsanti -->
    <div
      class="pt-3 flex flex-col sm:flex-row sm:justify-between sm:items-center gap-2 mt-2"
    >
      <NuxtLink
        v-if="showButton"
        to="/invoices"
        class="inline-flex justify-center items-center text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:ring-4 focus:ring-blue-300 rounded-full px-4 py-2 w-full sm:w-auto text-center"
      >
        Vedi tutte
      </NuxtLink>

      <NuxtLink
        to="/invoices/create"
        class="inline-flex justify-center items-center text-sm font-medium text-white bg-emerald-600 hover:bg-emerald-700 focus:ring-4 focus:ring-emerald-300 rounded-full px-4 py-2 w-full sm:w-auto text-center"
      >
        + Nuova fattura
      </NuxtLink>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  limit: { type: Number, default: 5 },
  showButton: { type: Boolean, default: true }
})

const invoices = ref([])
const loading  = ref(true)
const error    = ref('')

const token   = useState('token', () => null)
const runtime = useRuntimeConfig()
const API_BASE = runtime.public?.apiBase || runtime.public?.NUXT_PUBLIC_API_BASE || 'http://localhost:8000'
const headers = computed(() => (token.value ? { Authorization: `Bearer ${token.value}` } : {}))

function fmt(v) {
  const n = Number(v ?? 0)
  return n.toFixed(2)
}

async function loadRecent() {
  loading.value = true
  error.value = ''
  try {
    const list = await $fetch(`${API_BASE}/invoices`, {
      headers: headers.value,
      query: { limit: props.limit, skip: 0 }
    })
    invoices.value = Array.isArray(list) ? list : []
  } catch (e) {
    error.value = e?.data?.detail || e?.message || 'Errore caricamento'
  } finally {
    loading.value = false
  }
}

onMounted(loadRecent)
</script>

<style scoped>
.border-b {
  border-bottom-width: 1px;
  border-color: #e5e7eb;
}
</style>

<!-- Dashboard/UpcomingDue -->
<template>
  <div class="space-y-2">
    <div v-if="loading" class="text-sm text-gray-500">Caricamento…</div>
    <ul v-else class="">
      <li v-for="inv in dueSoon" :key="inv.id" class="py-2 flex items-center justify-between border-b">
        <NuxtLink :to="`/invoices/details/${inv.id}`" class="text-blue-600 hover:underline">
          {{ inv.number }} <span class="text-xs text-gray-500">({{ inv.due_date || '—' }})</span>
        </NuxtLink>
        <div class="text-sm" :class="inv.paid ? 'text-emerald-700' : 'text-amber-700'">
          {{ inv.total.toFixed(2) }} € {{ inv.paid ? '• pagata' : '• da incassare' }}
        </div>
      </li>
      <li v-if="!dueSoon.length" class="py-2 text-sm text-gray-500">Nessuna scadenza nei prossimi 10 giorni</li>
    </ul>
  </div>
</template>

<script setup>
const loading = ref(true)
const all = ref([])
const dueSoon = computed(() => {
  const today = new Date()
  const in10 = new Date(today); in10.setDate(today.getDate() + 10)
  return all.value
    .filter(inv => inv.status === 'issued' && !inv.paid && inv.due_date)
    .filter(inv => {
      const d = new Date(inv.due_date)
      return d >= today && d <= in10
    })
    .sort((a,b) => a.due_date.localeCompare(b.due_date))
    .slice(0, 8)
})

const token = useState('token', () => null)
const runtime = useRuntimeConfig()
const API_BASE = runtime.public?.apiBase || runtime.public?.NUXT_PUBLIC_API_BASE || 'http://localhost:8000'
const headers = computed(() => (token.value ? { Authorization: `Bearer ${token.value}` } : {}))

async function loadIssuedBatch () {
  loading.value = true
  try {
    // prendo un batch ragionevole (100) e filtro client-side
    const list = await $fetch(`${API_BASE}/invoices`, {
      headers: headers.value,
      query: { status: 'issued', limit: 100, skip: 0 }
    })
    all.value = list
  } finally {
    loading.value = false
  }
}
onMounted(loadIssuedBatch)
</script>

<style scoped>
.border-b {
    border-bottom-width: 1px;
    border-color: #e5e7eb;
}

</style>
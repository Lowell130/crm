<template>
  <section class="p-4 space-y-4">
    <div class="flex items-center justify-between">
      <h1 class="text-xl font-semibold">Fatture</h1>
      <NuxtLink to="/invoices/new" class="px-3 py-2 rounded bg-blue-600 text-white hover:bg-blue-700">
        Nuova fattura
      </NuxtLink>
    </div>

    <div class="flex items-center gap-2">
      <input v-model="q" @keyup.enter="refetch" type="search" placeholder="Cerca per numero…"
             class="border rounded px-3 py-2 w-64" />
      <button @click="refetch" class="px-3 py-2 rounded border">Cerca</button>
    </div>

    <div class="overflow-x-auto">
      <table class="w-full text-sm text-left">
        <thead class="text-xs uppercase bg-gray-50">
          <tr>
            <th class="px-4 py-3">Numero</th>
            <th class="px-4 py-3">Data</th>
            <th class="px-4 py-3">Cliente</th>
            <th class="px-4 py-3 text-right">Totale</th>
            <th class="px-4 py-3">Stato</th>
          </tr>
        </thead>
     <tbody>
  <tr v-for="inv in items" :key="inv.id" class="border-b">
    <td class="px-4 py-3 font-medium">
      <NuxtLink :to="`/invoices/${inv.id}`" class="text-blue-600 hover:underline">
        {{ inv.number }}
      </NuxtLink>
    </td>
    <td class="px-4 py-3">{{ inv.issue_date }}</td>
    <td class="px-4 py-3">
      <NuxtLink :to="`/invoices/${inv.id}`" class="text-blue-600 hover:underline">
        <span v-if="inv.customer_snapshot?.kind === 'B2B'">{{ inv.customer_snapshot?.company_name }}</span>
        <span v-else>{{ inv.customer_snapshot?.first_name }} {{ inv.customer_snapshot?.last_name }}</span>
      </NuxtLink>
    </td>
    <td class="px-4 py-3 text-right">{{ inv.total.toFixed(2) }} €</td>
    <td class="px-4 py-3">
      <span class="inline-flex items-center px-2 py-1 rounded text-xs"
            :class="inv.status === 'issued' ? 'bg-green-100 text-green-700'
                   : inv.status === 'draft' ? 'bg-yellow-100 text-yellow-700'
                   : 'bg-red-100 text-red-700'">
        {{ inv.status }}
      </span>
    </td>
  </tr>

  <tr v-if="!pending && items.length === 0">
    <td colspan="5" class="px-4 py-8 text-center text-gray-500">Nessuna fattura</td>
  </tr>
</tbody>

      </table>
    </div>

    <div class="flex items-center justify-end gap-2">
      <button class="px-3 py-2 border rounded" :disabled="skip===0 || pending" @click="prev">Prec</button>
      <span class="text-sm text-gray-600">Mostra {{ items.length }} / {{ total }}</span>
      <button class="px-3 py-2 border rounded" :disabled="skip+limit>=total || pending" @click="next">Succ</button>
    </div>
  </section>
</template>

<script setup>
definePageMeta({ layout: 'default' })

const token = useState('token', () => null)
const runtime = useRuntimeConfig()
const API_BASE = runtime.public?.NUXT_PUBLIC_API_BASE || 'http://localhost:8000'

const q = ref('')
const limit = ref(20)
const skip = ref(0)
const total = ref(0)

const headers = computed(() => ({
  Authorization: token.value ? `Bearer ${token.value}` : ''
}))

const { data, pending, refresh } = await useAsyncData('invoices-list', async () => {
  const res = await $fetch(`${API_BASE}/invoices`, {
    headers: headers.value,
    query: { q: q.value || undefined, skip: skip.value, limit: limit.value },
    onResponse({ response }) {
      const t = response.headers.get('x-total-count')
      total.value = t ? Number(t) : 0
    }
  })
  return res
}, { watch: [skip, limit] })

const items = computed(() => data.value ?? [])

function refetch(){ refresh() }
function next(){ skip.value += limit.value }
function prev(){ skip.value = Math.max(0, skip.value - limit.value) }
</script>

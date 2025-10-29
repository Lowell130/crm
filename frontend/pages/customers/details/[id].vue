<template>
 <section class="p-4 space-y-4">
  <!-- Breadcrumb -->
<AppBreadcrumb
  :items="[
    { label: 'Home', to: '/dashboard', icon: 'home' },
    { label: 'Clienti', to: '/customers' },
    { label: displayName || 'Dettaglio', current: true }
  ]"
/>
    <div class="mb-4 flex items-center justify-between">
      <div>
        <h1 class="text-xl font-semibold text-gray-900">Dettaglio cliente</h1>
        <p class="text-sm text-gray-500">ID: <span class="font-mono">{{ route.params.id }}</span></p>
      </div>
      <div class="flex gap-2">
        <button @click="goBack" class="text-gray-900 bg-white border border-gray-300 focus:outline-none hover:bg-gray-100 focus:ring-4 focus:ring-gray-100 font-medium rounded-full text-sm px-5 py-2.5 me-2 mb-2 dark:bg-gray-800 dark:text-white dark:border-gray-600 dark:hover:bg-gray-700 dark:hover:border-gray-600 dark:focus:ring-gray-700">Indietro</button>
      </div>
    </div>

    <!-- Stato: loading -->
    <div v-if="pending" class="bg-white rounded-lg shadow p-6">
      <div class="animate-pulse space-y-3">
        <div class="h-4 w-1/3 bg-gray-200 rounded"></div>
        <div class="h-4 w-1/2 bg-gray-200 rounded"></div>
        <div class="h-4 w-2/3 bg-gray-200 rounded"></div>
        <div class="h-4 w-1/4 bg-gray-200 rounded"></div>
      </div>
    </div>

    <!-- Stato: errore -->
    <div v-else-if="error" class="bg-white rounded-lg shadow p-6">
      <p class="text-red-600 mb-3">{{ errorMessage }}</p>
      <button @click="fetchCustomer" class="px-3 py-2 text-sm rounded-lg border hover:bg-gray-50">Riprova</button>
    </div>

    <!-- Stato: ok -->
    <div v-else-if="customer" class="bg-white rounded-lg shadow p-6 space-y-6">
      <div class="flex items-center justify-between">
        <div class="flex items-center gap-3">
          <span
            class="px-2 py-0.5 rounded-full text-xs"
            :class="customer.kind==='B2B' ? 'bg-blue-100 text-blue-700' : 'bg-emerald-100 text-emerald-700'"
          >{{ customer.kind }}</span>

          <h2 class="text-lg font-medium text-gray-900">
            <template v-if="customer.kind==='B2B'">
              {{ customer.company_name || '—' }}
            </template>
            <template v-else>
              {{ [customer.first_name, customer.last_name].filter(Boolean).join(' ') || '—' }}
            </template>
          </h2>
        </div>
      </div>

      <!-- Dati principali -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div class="space-y-3">
          <h3 class="text-sm font-semibold text-gray-700 uppercase">Anagrafica / Azienda</h3>

          <div v-if="customer.kind==='B2B'" class="space-y-1">
            <div class="text-sm"><span class="text-gray-500">Ragione sociale:</span> <span class="text-gray-900">{{ customer.company_name || '—' }}</span></div>
            <div class="text-sm"><span class="text-gray-500">P.IVA:</span> <span class="text-gray-900">{{ customer.vat_number || '—' }}</span></div>
          </div>

          <div v-else class="space-y-1">
            <div class="text-sm"><span class="text-gray-500">Nome:</span> <span class="text-gray-900">{{ customer.first_name || '—' }}</span></div>
            <div class="text-sm"><span class="text-gray-500">Cognome:</span> <span class="text-gray-900">{{ customer.last_name || '—' }}</span></div>
            <div class="text-sm"><span class="text-gray-500">Codice Fiscale:</span> <span class="text-gray-900">{{ customer.codice_fiscale || '—' }}</span></div>
          </div>
        </div>

        <div class="space-y-3">
          <h3 class="text-sm font-semibold text-gray-700 uppercase">Contatti</h3>
          <div class="text-sm"><span class="text-gray-500">Email:</span> <span class="text-gray-900">{{ customer.email || '—' }}</span></div>
          <div class="text-sm"><span class="text-gray-500">Telefono:</span> <span class="text-gray-900">{{ customer.phone || '—' }}</span></div>
          <div class="text-sm"><span class="text-gray-500">Indirizzo:</span> <span class="text-gray-900">{{ customer.address || '—' }}</span></div>
        </div>
      </div>

      <div class="space-y-2">
        <h3 class="text-sm font-semibold text-gray-700 uppercase">Note</h3>
        <p class="text-sm text-gray-900 whitespace-pre-line">{{ customer.notes || '—' }}</p>
      </div>
    </div>

    <!-- Fallback (quasi mai) -->
    <div v-else class="bg-white rounded-lg shadow p-6">
      <p class="text-gray-600">Nessun dato disponibile.</p>
    </div>
  </section>
</template>

<script setup>
definePageMeta({ layout: 'default' })

const route = useRoute()
const router = useRouter()
const { apiFetch } = useApi()

const customer = ref(null)
const pending = ref(true)    // <-- parte in loading
const error = ref(null)

const errorMessage = computed(() => {
  if (!error.value) return ''
  return error.value?.data?.detail || error.value?.message || 'Errore durante il caricamento'
})

const fetchCustomer = async () => {
  pending.value = true
  error.value = null
  customer.value = null
  try {
    const id = route.params.id
    customer.value = await apiFetch(`/customers/${id}`)
  } catch (e) {
    error.value = e
  } finally {
    pending.value = false
  }
}

const goBack = () => {
  if (window.history.length > 1) router.back()
  else router.push('/dashboard')  // o '/customers' se hai la lista
}

onMounted(fetchCustomer)
watch(() => route.params.id, fetchCustomer)
// Breadcrump name
const displayName = computed(() => {
  if (!customer.value) return ''
  if (customer.value.kind === 'B2B') return customer.value.company_name || customer.value._id
  const full = [customer.value.first_name, customer.value.last_name].filter(Boolean).join(' ')
  return full || customer.value._id
})

</script>

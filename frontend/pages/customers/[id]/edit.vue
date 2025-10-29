<template>
  <section class="p-4 space-y-4">
    <!-- Breadcrumb -->
 <AppBreadcrumb
  :items="[
    { label: 'Home', to: '/dashboard', icon: 'home' },
    { label: 'Clienti', to: '/customers' },
    { label: displayName || 'Dettaglio', to: `/customers/details/${route.params.id}` },
    { label: 'Modifica', current: true }
  ]"
/>

    <!-- Header -->
    <div class="mb-2 flex items-center justify-between">
      <div>
        <h1 class="text-xl font-semibold text-gray-900">Modifica cliente</h1>
        <p class="text-sm text-gray-500">
          ID: <span class="font-mono">{{ route.params.id }}</span>
        </p>
      </div>
      <div class="flex gap-2">
        <button
          @click="goBack"
          class="text-gray-900 bg-white border border-gray-300 focus:outline-none hover:bg-gray-100 focus:ring-4 focus:ring-gray-100 font-medium rounded-full text-sm px-5 py-2.5"
        >
          Indietro
        </button>
      </div>
    </div>

    <!-- loading -->
    <div v-if="pending" class="bg-white rounded-lg shadow p-6">
      <div class="animate-pulse space-y-3">
        <div class="h-4 w-1/3 bg-gray-200 rounded"></div>
        <div class="h-4 w-1/2 bg-gray-200 rounded"></div>
        <div class="h-4 w-2/3 bg-gray-200 rounded"></div>
      </div>
    </div>

    <!-- errore -->
    <div v-else-if="error" class="bg-white rounded-lg shadow p-6">
      <p class="text-red-600 mb-3">{{ errorMessage }}</p>
      <button @click="fetchCustomer" class="px-3 py-2 text-sm rounded-lg border hover:bg-gray-50">
        Riprova
      </button>
    </div>

    <!-- form -->
    <div v-else class="bg-white rounded-lg shadow p-6">
      <CustomerForm
        mode="edit"
        :id="route.params.id"
        :initialData="customer"
        @saved="onSaved"
        @cancel="goBack"
      />
    </div>
  </section>
</template>

<script setup>
definePageMeta({ layout: 'default' })

const route = useRoute()
const router = useRouter()
const { apiFetch } = useApi()

const customer = ref(null)
const pending = ref(false)
const error = ref(null)

const errorMessage = computed(() =>
  error.value?.data?.detail || error.value?.message || 'Errore durante il caricamento'
)

// Nome/label dinamica per breadcrumb (ragione sociale o nome+cognome; fallback su _id)
const displayName = computed(() => {
  if (!customer.value) return ''
  if (customer.value.kind === 'B2B') return customer.value.company_name || customer.value._id
  const full = [customer.value.first_name, customer.value.last_name].filter(Boolean).join(' ')
  return full || customer.value._id
})

async function fetchCustomer () {
  pending.value = true
  error.value = null
  try {
    customer.value = await apiFetch(`/customers/${route.params.id}`)
  } catch (e) {
    error.value = e
  } finally {
    pending.value = false
  }
}

function goBack () {
  if (history.length > 1) router.back()
  else router.push(`/customers/details/${route.params.id}`)
}

function onSaved () {
  // dopo il salvataggio vai alla pagina dettaglio
  router.push(`/customers/details/${route.params.id}`)
}

onMounted(fetchCustomer)
watch(() => route.params.id, fetchCustomer)
</script>

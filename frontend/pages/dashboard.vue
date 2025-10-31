<template>
  <section class="bg-gray-50 p-3 sm:p-5 antialiased">
    <div class="mx-auto max-w-screen-xl px-4 lg:px-12">
      <div class="bg-white relative shadow-md sm:rounded-lg overflow-hidden">

        
        <!-- Toolbar -->
        <div class="flex flex-col md:flex-row items-center justify-between space-y-3 md:space-y-0 md:space-x-4 p-4">
          <div class="w-full md:w-1/2">
            <CustomersSearch
              :model-value="qInput"
              @update:modelValue="v => qInput = v"
              @search="applySearch"
              @clear="clearSearch"
            />
          </div>

          <div class="w-full md:w-auto flex flex-col md:flex-row space-y-2 md:space-y-0 items-stretch md:items-center justify-end md:space-x-3 flex-shrink-0">

            <button type="button" @click="showCreate = true" class="flex items-center justify-center text-white bg-primary-700 hover:bg-primary-800 focus:ring-4 focus:ring-primary-300 font-medium rounded-full text-sm px-4 py-2">
              <svg class="h-3.5 w-3.5 mr-2" viewBox="0 0 20 20" fill="currentColor"><path clip-rule="evenodd" fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z"/></svg>
              Aggiungi cliente
            </button>

            <CustomersFilters
              :model-value="kind"
              @update:modelValue="v => kind = v"
              @apply="applyFilters"
              @reset="resetFilters"
            />
          </div>
        </div>

        <!-- Tabella -->
      <CustomersTable :items="customers" :pending="pending">
  <!-- Empty custom (opzionale) -->
  <template #empty>
    <div class="flex flex-col items-center gap-2">
      <div class="text-sm">Nessun cliente trovato</div>
      <div class="text-xs text-gray-400">Prova a cambiare i filtri o la ricerca</div>
      <div class="flex gap-2 mt-2">
        <button @click="resetFilters(); applyFilters()" class="px-3 py-1.5 text-xs rounded-lg border">Reset filtri</button>
        <button @click="showCreate = true" class="px-3 py-1.5 text-xs rounded-lg text-white bg-primary-700 hover:bg-primary-800">Aggiungi cliente</button>
      </div>
    </div>
  </template>

  <!-- Actions per riga -->
  <template #actions="{ customer: c }">
    <!-- Dettaglio -->
    <NuxtLink
      :to="`/customers/details/${c._id}`"
      class="inline-flex items-center p-1.5 rounded-full text-gray-500 hover:text-gray-800 hover:bg-gray-100"
      title="Dettaglio"
    >
      <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none">
        <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M13.213 9.787a3.391 3.391 0 0 0-4.795 0l-3.425 3.426a3.39 3.39 0 0 0 4.795 4.794l.321-.304m-.321-4.49a3.39 3.39 0 0 0 4.795 0l3.424-3.426a3.39 3.39 0 0 0-4.794-4.795l-1.028.961"/>
      </svg>
    </NuxtLink>

    <!-- Modifica -->
    <button
      class="inline-flex items-center p-1.5 rounded-full text-gray-500 hover:text-gray-800 hover:bg-gray-100"
      title="Modifica"
      @click="onEdit(c)"
    >
      <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none">
        <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="m14.304 4.844 2.852 2.852M7 7H4a1 1 0 0 0-1 1v10a1 1 0 0 0 1 1h11a1 1 0 0 0 1-1v-4.5m2.409-9.91a2.017 2.017 0 0 1 0 2.853l-6.844 6.844L8 14l.713-3.565 6.844-6.844a2.015 2.015 0 0 1 2.852 0Z"/>
      </svg>
    </button>

    <!-- Elimina -->
    <button
      class="inline-flex items-center p-1.5 rounded-full text-gray-500 hover:text-red-700 hover:bg-red-50 disabled:opacity-50"
      :disabled="deletingId===c._id"
      title="Elimina"
      @click="onDelete(c)"
    >
      <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none">
        <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M6 18 17.94 6M18 18 6.06 6"/>
      </svg>
    </button>
  </template>
</CustomersTable>

        <!-- Paginazione -->
        <CustomersPagination
          :page="page"
          :hasNext="hasNext"
          :fromItem="fromItem"
          :toItem="toItem"
          :totalDisplay="totalDisplay"
          @prev="prevPage"
          @next="nextPage"
        />
      </div>
    </div>

    <!-- Modale creazione -->
    <CustomerCreateModal :open="showCreate" @close="showCreate=false" @created="onCreated" />

    <!-- Toasts -->
    <ToastStack :toasts="toasts" :dismissToast="dismissToast" />
  </section>
</template>

<script setup>
import CustomersSearch from '@/components/Customers/CustomersSearch.vue'
import CustomersFilters from '@/components/Customers/CustomersFilters.vue'
import CustomersTable from '@/components/Customers/CustomersTable.vue'
import CustomersPagination from '@/components/Customers/CustomersPagination.vue'
import CustomerCreateModal from '@/components/Customers/CustomerCreateModal.vue'
import ToastStack from '@/components/Ui/ToastStack.vue'

const { apiFetch } = useApi()
const router = useRouter()

// stato modale + eliminazione
const showCreate = ref(false)
const deletingId = ref(null)

// toasts
const { toasts, pushToast, dismissToast } = useToasts()

// customers (logica in composable)
const {
  q, qInput, kind, page, limit,
  customers, pending, error, total, hasNext,
  fromItem, toItem, totalDisplay, errorMessage,
  fetchCustomers, applySearch, clearSearch,
  prevPage, nextPage, applyFilters, resetFilters
} = useCustomers(apiFetch)

// azioni riga
function onEdit(c) {
  router.push(`/customers/${c._id}/edit`)
}
async function onDelete(c) {
  if (deletingId.value || !c?._id) return
  const ok = window.confirm(`Confermi l'eliminazione del cliente ${c.company_name || (c.first_name + ' ' + c.last_name) || c._id}?`)
  if (!ok) return
  try {
    deletingId.value = c._id
    await apiFetch(`/customers/${c._id}`, { method: 'DELETE' })

    if (customers.value.length === 1 && page.value > 1) page.value -= 1
    await fetchCustomers()

    pushToast({ title: 'Cliente eliminato', message: 'Eliminato correttamente.' })
  } catch (e) {
    const msg = e?.data?.detail || e?.message || 'Errore durante l’eliminazione'
    pushToast({ title: 'Eliminazione fallita', message: msg, onRetry: () => onDelete(c) })
  } finally {
    deletingId.value = null
  }
}

// callback modale
const onCreated = async () => {
  page.value = 1
  await fetchCustomers()
  showCreate.value = false
}
</script>



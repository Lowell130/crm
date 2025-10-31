<template>
  <section class="bg-white rounded-lg shadow p-6 mt-6">
    <div class="flex items-center justify-between mb-4">
      <h3 class="text-base font-semibold text-gray-900">Fatture del cliente</h3>

      <NuxtLink
        :to="`/invoices/new?customer_id=${customerId}`"
       type="button" class="inline-flex items-center text-white bg-primary-700 hover:bg-primary-800 focus:ring-4 focus:ring-primary-300 font-medium rounded-full text-sm px-3 py-2"
      >
        <svg class="h-3.5 w-3.5 mr-2" fill="currentColor" viewBox="0 0 20 20" aria-hidden="true">
          <path clip-rule="evenodd" fill-rule="evenodd"
                d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" />
        </svg>
        Nuova fattura
      </NuxtLink>
    </div>

    <!-- Toolbar -->
    <div class="flex flex-col md:flex-row items-center justify-between gap-3 mb-3">
      <div class="w-full md:w-1/2">
        <CustomersSearch
          :model-value="qInput"
          @update:modelValue="v => qInput = v"
          @search="applySearch"
          @clear="clearSearch"
        />
      </div>

      <div class="w-full md:w-auto">
        <select
          v-model="status"
          @change="applyStatus"
          class="w-full md:w-48 py-2 px-3 text-sm bg-white border border-gray-200 rounded-lg hover:bg-gray-50"
        >
          <option value="">Tutti gli stati</option>
          <option value="issued">Emesse</option>
          <option value="draft">Bozze</option>
          <option value="cancelled">Annullate</option>
        </select>
      </div>
    </div>

    <!-- Stato: loading -->
    <div v-if="pending" class="py-8 text-sm text-gray-500">Caricamento…</div>

    <!-- Stato: errore -->
    <div v-else-if="error" class="py-8 text-sm text-red-600">
      {{ errorMessage }}
      <button @click="refresh" class="ml-2 px-3 py-1 border rounded text-gray-700 hover:bg-gray-50">Riprova</button>
    </div>

    <!-- Tabella -->
    <div v-else>
      <div class="overflow-x-auto">
        <table class="w-full text-sm text-left text-gray-600">
          <thead class="text-xs uppercase bg-gray-50">
            <tr>
              <th class="px-4 py-3">Numero</th>
              <th class="px-4 py-3">Data</th>
              <th class="px-4 py-3 text-right">Totale</th>
              <th class="px-4 py-3">Stato</th>
              <th class="px-4 py-3"><span class="sr-only">Azioni</span></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="inv in items" :key="inv.id" class="border-b">
              <td class="px-4 py-3">
                <NuxtLink :to="`/invoices/details/${inv.id}`" class="text-blue-600 hover:underline">
                  {{ inv.number }}
                </NuxtLink>
              </td>
              <td class="px-4 py-3">{{ inv.issue_date }}</td>
              <td class="px-4 py-3 text-right">{{ inv.total.toFixed(2) }} €</td>
              <td class="px-4 py-3">
                <span class="inline-flex items-center px-2 py-1 rounded text-xs shadow-sm"
                      :class="inv.status === 'issued' ? 'bg-green-100 text-green-700'
                             : inv.status === 'draft' ? 'bg-yellow-100 text-yellow-700'
                             : 'bg-red-100 text-red-700'">
                  {{ inv.status }}
                </span>
              </td>
              <td class="px-4 py-3 text-right">
                <NuxtLink :to="`/invoices/details/${inv.id}`" type="button" class="text-white bg-purple-700 hover:bg-purple-800 focus:outline-none focus:ring-4 focus:ring-purple-300 font-medium rounded-full text-xs px-5 py-2.5 text-center mb-2 dark:bg-purple-600 dark:hover:bg-purple-700 dark:focus:ring-purple-900">Apri</NuxtLink>
              </td>
            </tr>

         

            <tr v-if="!pending && items.length === 0">
              <td colspan="5" class="px-4 py-8 text-center text-gray-500">Nessuna fattura</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Paginazione -->
      <CustomersPagination
        :page="page"
        :hasNext="hasNext"
        :fromItem="fromItem"
        :toItem="toItem"
        :totalDisplay="total"
        @prev="prevPage"
        @next="nextPage"
      />
    </div>
  </section>
</template>

<script setup>
import CustomersSearch from '@/components/Customers/CustomersSearch.vue'
import CustomersPagination from '@/components/Customers/CustomersPagination.vue'

const props = defineProps({
  customerId: { type: String, required: true }
})

const { apiFetch } = useApi()

// ricerca e filtri
const qInput = ref('')
const q = ref('')
const status = ref('')

// paginazione
const limit = ref(10)
const skip = ref(0)
const total = ref(0)

const { data, pending, error, refresh } = await useAsyncData(
  () => `customer-invoices-${props.customerId}-${q.value}-${status.value}-${skip.value}-${limit.value}`,
  async () => {
    const res = await apiFetch('/invoices', {
      query: {
        customer_id: props.customerId,
        q: q.value || undefined,
        status: status.value || undefined,
        skip: skip.value,
        limit: limit.value
      },
      onResponse({ response }) {
        const t = response.headers.get('x-total-count')
        total.value = t ? Number(t) : 0
      }
    })
    return res
  }
)

const items = computed(() => data.value ?? [])
const page = computed(() => Math.floor(skip.value / limit.value) + 1)
const hasNext = computed(() => skip.value + items.value.length < total.value)
const fromItem = computed(() => (total.value === 0 ? 0 : skip.value + 1))
const toItem   = computed(() => Math.min(skip.value + items.value.length, total.value))

function prevPage(){ if (skip.value > 0){ skip.value = Math.max(0, skip.value - limit.value); refresh() } }
function nextPage(){ if (hasNext.value){ skip.value += limit.value; refresh() } }

function applySearch(){
  q.value = (qInput.value || '').trim()
  skip.value = 0
  refresh()
}
function clearSearch(){
  qInput.value = ''
  q.value = ''
  skip.value = 0
  refresh()
}
function applyStatus(){
  skip.value = 0
  refresh()
}

const errorMessage = computed(() =>
  error.value?.data?.detail || error.value?.message || 'Errore durante il caricamento'
)
const route = useRoute()
onMounted(() => {
  const cid = route.query.customer_id
  if (cid) {
    form.customer_id = cid
    // opzionale: mostrare un badge “cliente preselezionato”
    // oppure fetchare /customers/:id per mostrare nome subito
  }
})

</script>

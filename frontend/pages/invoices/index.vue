<template>
  <section class="bg-gray-50 dark:bg-gray-900 p-3 sm:p-5">
    <div class="mx-auto max-w-screen-xl px-4 lg:px-12">
      <!-- Start coding here -->
      <div class="bg-white dark:bg-gray-800 relative shadow-md sm:rounded-lg overflow-hidden">




        <!-- Toolbar: search + actions -->
        <div class="flex flex-col md:flex-row items-center justify-between space-y-3 md:space-y-0 md:space-x-4 p-4">
          <!-- Search -->
        <!-- Search -->
<!-- Search -->
<div class="w-full md:w-1/2">
  <CustomersSearch
    :model-value="qInput"
    @update:modelValue="v => qInput = v"
    @search="applySearch"
    @clear="clearSearch"
  />
</div>


          <!-- Actions -->
          <div class="w-full md:w-auto flex flex-col md:flex-row space-y-2 md:space-y-0 items-stretch md:items-center justify-end md:space-x-3 flex-shrink-0">
          
          
          
            <NuxtLink to="/invoices/new" type="button" class="flex items-center justify-center rounded-full text-white bg-primary-700 hover:bg-primary-800 focus:ring-4 focus:ring-primary-300 font-medium text-sm px-4 py-2 dark:bg-primary-600 dark:hover:bg-primary-700 focus:outline-none dark:focus:ring-primary-800"
            >
            <svg class="h-3.5 w-3.5 mr-2" viewBox="0 0 20 20" fill="currentColor"><path clip-rule="evenodd" fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z"/></svg>
              Crea fattura
            </NuxtLink>

            <!-- (Facoltativo) Filtro stato -->
            <div class="flex items-center space-x-3 w-full md:w-auto">
              <div class="w-full md:w-48">
                <select
                  v-model="status"
                  @change="onFilterStatus"
                  class="w-full py-2 px-3 text-sm bg-white border border-gray-200 rounded-lg hover:bg-gray-50 dark:bg-gray-800 dark:border-gray-600 dark:text-gray-200"
                >
                  <option value="">Tutti gli stati</option>
                  <option value="issued">Emesse</option>
                  <option value="draft">Bozze</option>
                  <option value="cancelled">Annullate</option>
                </select>
              </div>
            </div>
          </div>
        </div>




        <!-- Table -->
        <div class="overflow-x-auto">
          <table class="w-full text-sm text-left text-gray-500 dark:text-gray-400">
            <thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
              <tr>
                <th scope="col" class="px-4 py-3">Numero</th>
                <th scope="col" class="px-4 py-3">Data</th>
                <th scope="col" class="px-4 py-3">Cliente</th>
                <th scope="col" class="px-4 py-3 text-right">Totale</th>
                <th scope="col" class="px-4 py-3">Pagato</th>
                <th scope="col" class="px-4 py-3">Stato</th>
                <th scope="col" class="px-4 py-3"><span class="sr-only">Azioni</span></th>
              </tr>
            </thead>

            <tbody>
              <tr v-for="inv in items" :key="inv.id" class="border-b dark:border-gray-700">
                <th scope="row" class="px-4 py-3 font-medium text-gray-900 whitespace-nowrap dark:text-white">
                  <NuxtLink :to="`/invoices/details/${inv.id}`" class="text-blue-600 hover:underline">
                    {{ inv.number }}
                  </NuxtLink>
                </th>
                <td class="px-4 py-3">{{ inv.issue_date }}</td>
                <td class="px-4 py-3">
                  <!-- <NuxtLink :to="`/invoices/${inv.id}`" class="text-blue-600 hover:underline">
                    <span v-if="inv.customer_snapshot?.kind === 'B2B'">{{ inv.customer_snapshot?.company_name }}</span>
                    <span v-else>{{ inv.customer_snapshot?.first_name }} {{ inv.customer_snapshot?.last_name }}</span>
                  </NuxtLink> -->
                  <NuxtLink :to="`/customers/details/${inv.customer_id}`" class="text-blue-600 hover:underline">
  <span v-if="inv.customer_snapshot?.kind === 'B2B'">
    {{ inv.customer_snapshot?.company_name }}
  </span>
  <span v-else>
    {{ inv.customer_snapshot?.first_name }} {{ inv.customer_snapshot?.last_name }}
  </span>
</NuxtLink>
                </td>
                <td class="px-4 py-3 text-right">{{ inv.total.toFixed(2) }} €</td>
                <td class="px-4 py-3 text-center">
  <span
    :class="inv.paid ? 'bg-emerald-100 text-emerald-700' : 'bg-gray-100 text-gray-600'"
    class="inline-flex items-center px-2 py-0.5 rounded text-xs"
  >
    {{ inv.paid ? ('Sì' + (inv.paid_at ? ` (${formatDate(inv.paid_at)})` : '')) : 'No' }}
  </span>
</td>
                <td class="px-4 py-3">
                  <span class="inline-flex items-center px-2 py-1 rounded text-xs shadow-sm"
                        :class="inv.status === 'issued' ? 'bg-green-100 text-green-700'
                               : inv.status === 'draft' ? 'bg-yellow-100 text-yellow-700'
                               : 'bg-red-100 text-red-700'">
                    {{ inv.status }}
                  </span>
                </td>
                <td class="px-4 py-3 flex items-center justify-end relative">
                  <button
                    class="inline-flex items-center p-0.5 text-sm font-medium text-center text-gray-500 hover:text-gray-800 rounded-lg focus:outline-none dark:text-gray-400 dark:hover:text-gray-100"
                    type="button"
                    @click="toggleRow(inv.id)"
                  >
                    <svg class="w-5 h-5" aria-hidden="true" fill="currentColor" viewBox="0 0 20 20">
                      <path d="M6 10a2 2 0 11-4 0 2 2 0 014 0zM12 10a2 2 0 11-4 0 2 2 0 014 0zM16 12a2 2 0 100-4 2 2 0 000 4z"/>
                    </svg>
                  </button>

                  <!-- Dropdown Azioni (gestito via Vue, niente data-dropdown-toggle) -->
                  <div
                    v-if="openRowId === inv.id"
                    class="absolute right-0 top-8 z-10 w-44 bg-white rounded divide-y divide-gray-100 shadow dark:bg-gray-700 dark:divide-gray-600"
                  >
                    <ul class="py-1 text-sm text-gray-700 dark:text-gray-200">
                      <li>
                        <NuxtLink :to="`/invoices/details/${inv.id}`" class="block py-2 px-4 hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white">
                          Apri
                        </NuxtLink>
                      </li>
                      <li>
  <NuxtLink
    :to="`/customers/details/${inv.customer_id}`"
    class="block py-2 px-4 hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white"
  >
    Apri cliente
  </NuxtLink>
</li>
<li>
  <button
    class="w-full text-left block py-2 px-4 hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white"
    @click="togglePaid(inv)"
  >
    {{ inv.paid ? 'Segna come non pagata' : 'Segna come pagata' }}
  </button>
</li>


                      <li>
                        <button
                          class="w-full text-left block py-2 px-4 hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white"
                          @click="editNumber(inv)"
                        >
                          Modifica numero
                        </button>
                      </li>
                    </ul>
                    <div class="py-1">
                      <button
                        class="w-full text-left block py-2 px-4 text-sm text-red-700 hover:bg-gray-100 dark:hover:bg-gray-600 dark:text-red-400 dark:hover:text-white"
                        @click="deleteInvoice(inv)"
                      >
                        Elimina
                      </button>
                    </div>
                  </div>
                </td>
              </tr>

              <tr v-if="!pending && items.length === 0">
                <td colspan="6" class="px-4 py-8 text-center text-gray-500">Nessuna fattura</td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Pagination -->
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
  </section>
</template>

<script setup>
import CustomersPagination from '@/components/Customers/CustomersPagination.vue'
import CustomersSearch from '@/components/Customers/CustomersSearch.vue'
definePageMeta({ layout: 'default' })

const token = useState('token', () => null)
const runtime = useRuntimeConfig()
const API_BASE = runtime.public?.NUXT_PUBLIC_API_BASE || 'http://localhost:8000'
const page = computed(() => Math.floor(skip.value / limit.value) + 1)
const hasNext = computed(() => skip.value + items.value.length < total.value)
const fromItem = computed(() => (total.value === 0 ? 0 : skip.value + 1))
const toItem = computed(() => Math.min(skip.value + items.value.length, total.value))
const totalDisplay = computed(() => total.value)

function prevPage() {
  if (skip.value === 0) return
  skip.value = Math.max(0, skip.value - limit.value)
  refresh()
}
function nextPage() {
  if (!hasNext.value) return
  skip.value += limit.value
  refresh()
}

const qInput = ref('')  // ciò che l'utente digita
const q = ref('')       // query effettivamente applicata
const status = ref('')         // filtro stato ('' = tutti)
const limit = ref(20)
const skip = ref(0)
const total = ref(0)

const openRowId = ref(null)

let qTimer = null
watch(qInput, (val) => {
  clearTimeout(qTimer)
  qTimer = setTimeout(() => {
    q.value = (val || '').trim()
    skip.value = 0
    refresh()
  }, 250) // 250ms è un buon compromesso
})


const headers = computed(() => ({
  Authorization: token.value ? `Bearer ${token.value}` : ''
}))

const { data, pending, refresh } = await useAsyncData('invoices-list', async () => {
  const res = await $fetch(`${API_BASE}/invoices`, {
    headers: headers.value,
    query: {
      q: q.value || undefined,           // <— usa la query applicata
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
}, { watch: [skip, limit, status] })


function applySearch() {
  q.value = (qInput.value || '').trim()
  skip.value = 0
  refresh()
}
function clearSearch() {
  qInput.value = ''
  q.value = ''
  skip.value = 0
  refresh()
}



const items = computed(() => data.value ?? [])
const showingStart = computed(() => total.value === 0 ? 0 : skip.value + 1)
const showingEnd = computed(() => Math.min(skip.value + items.value.length, total.value))

function onSearch(){
  skip.value = 0
  refresh()
}
function onFilterStatus(){
  skip.value = 0
  refresh()
}
function next(){ if (skip.value + limit.value < total.value) skip.value += limit.value }
function prev(){ skip.value = Math.max(0, skip.value - limit.value) }

function toggleRow(id){
  openRowId.value = openRowId.value === id ? null : id
}
async function editNumber(inv){
  const current = inv.number || ''
  const val = window.prompt('Nuovo numero fattura:', current)
  if (val == null || val === current) return
  try{
    const updated = await $fetch(`${API_BASE}/invoices/${inv.id}`, {
      method: 'PATCH',
      headers: { ...headers.value, 'Content-Type':'application/json' },
      body: { number: val }
    })
    // aggiorna localmente
    const i = items.value.findIndex(x => x.id === inv.id)
    if (i !== -1) items.value[i] = updated
  }catch(e){
    alert(e?.data?.detail || 'Errore aggiornamento numero')
  }finally{
    openRowId.value = null
  }
}
async function deleteInvoice(inv){
  if (!confirm(`Eliminare la fattura ${inv.number}?`)) return
  try{
    await $fetch(`${API_BASE}/invoices/${inv.id}`, {
      method: 'DELETE',
      headers: headers.value
    })
    // reload pagina corrente
    const newSkip = (skip.value >= limit.value && items.value.length === 1) ? skip.value - limit.value : skip.value
    skip.value = Math.max(0, newSkip)
    refresh()
  }catch(e){
    alert(e?.data?.detail || 'Errore eliminazione')
  }finally{
    openRowId.value = null
  }
}

// search


function formatDate(s){
  if(!s) return ''
  // s è ISO "YYYY-MM-DD" (dal backend), o ISO datetime.
  const d = new Date(s)
  if (Number.isNaN(d.getTime())) return s
  return d.toLocaleDateString('it-IT')
}

async function togglePaid(inv){
  const nowISO = new Date().toISOString().slice(0,10) // YYYY-MM-DD
  const body = inv.paid
    ? { paid: false, paid_at: null }
    : { paid: true,  paid_at: nowISO }

  try{
    const updated = await $fetch(`${API_BASE}/invoices/${inv.id}`, {
      method: 'PATCH',
      headers: { ...headers.value, 'Content-Type':'application/json' },
      body
    })
    // aggiorna local
    const i = items.value.findIndex(x => x.id === inv.id)
    if (i !== -1) items.value[i] = updated
  }catch(e){
    alert(e?.data?.detail || 'Errore aggiornamento pagamento')
  }finally{
    openRowId.value = null
  }
}

</script>

<style scoped>
.border-b {
    border-bottom-width: 1px;
    border-color: #e5e7eb;
}

</style>
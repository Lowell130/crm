<template>
  <section class="bg-gray-50 p-3 sm:p-5 antialiased">
    <div class="mx-auto max-w-screen-xl px-4 lg:px-12">
      <div class="bg-white relative shadow-md sm:rounded-lg overflow-hidden">
        <!-- Toolbar (search + actions) -->
        <div class="flex flex-col md:flex-row items-center justify-between space-y-3 md:space-y-0 md:space-x-4 p-4">
          <div class="w-full md:w-1/2">
            <form class="flex items-center" @submit.prevent="applySearch">
              <label for="simple-search" class="sr-only">Cerca</label>
              <div class="relative w-full">
                <div class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
                  <svg aria-hidden="true" class="w-5 h-5 text-gray-500" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd" />
                  </svg>
                </div>
                <input v-model.trim="qInput" @keyup.enter.prevent="applySearch" id="simple-search" type="text"
                       class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full pl-10 p-2"
                       placeholder="Cerca per nome, ragione sociale, CF/P.IVA, email…" />
              </div>
            </form>
          </div>

          <div class="w-full md:w-auto flex flex-col md:flex-row space-y-2 md:space-y-0 items-stretch md:items-center justify-end md:space-x-3 flex-shrink-0">
            <button type="button" @click="openCreate"
                    class="flex items-center justify-center text-white bg-primary-700 hover:bg-primary-800 focus:ring-4 focus:ring-primary-300 font-medium rounded-lg text-sm px-4 py-2">
              <svg class="h-3.5 w-3.5 mr-2" fill="currentColor" viewBox="0 0 20 20" aria-hidden="true">
                <path clip-rule="evenodd" fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" />
              </svg>
              Aggiungi cliente
            </button>

      <!-- Filtri quick -->
<div class="relative">
 <button
  ref="filterBtn"
  @click="toggleFilter"
  class="w-full md:w-auto flex items-center justify-center py-2 px-4 text-sm font-medium text-gray-900 bg-white rounded-lg border border-gray-200 hover:bg-gray-100 hover:text-primary-700 focus:z-10 focus:ring-4 focus:ring-gray-200"
  type="button">
  <!-- icone + testo -->
  Filtra
  <!-- icone -->
</button>


  <!-- pannello -->
  <div
    v-show="showFilter"
    ref="filterRef"
    @click.stop
    class="absolute right-0 mt-2 z-10 w-56 p-3 bg-white rounded-lg shadow"
  >
    <h6 class="mb-3 text-sm font-medium text-gray-900">Tipo cliente</h6>
    <ul class="space-y-2 text-sm">
      <li class="flex items-center">
        <input id="flt-all" type="radio" value="" v-model="kind"
               class="w-4 h-4 bg-gray-100 border-gray-300 rounded text-primary-600 focus:ring-primary-500">
        <label for="flt-all" class="ml-2 text-sm font-medium text-gray-900">Tutti</label>
      </li>
      <li class="flex items-center">
        <input id="flt-b2b" type="radio" value="B2B" v-model="kind"
               class="w-4 h-4 bg-gray-100 border-gray-300 rounded text-primary-600 focus:ring-primary-500">
        <label for="flt-b2b" class="ml-2 text-sm font-medium text-gray-900">B2B</label>
      </li>
      <li class="flex items-center">
        <input id="flt-b2c" type="radio" value="B2C" v-model="kind"
               class="w-4 h-4 bg-gray-100 border-gray-300 rounded text-primary-600 focus:ring-primary-500">
        <label for="flt-b2c" class="ml-2 text-sm font-medium text-gray-900">B2C</label>
      </li>
    </ul>

    <div class="flex justify-end mt-3 gap-2">
      <button class="px-3 py-1.5 text-sm rounded-lg border" @click="resetFilters">Reset</button>
      <button class="px-3 py-1.5 text-sm rounded-lg text-white bg-primary-700 hover:bg-primary-800"
              @click="applyFilters">Applica</button>
    </div>
  </div>
</div>

          </div>
        </div>

        <!-- Tabella -->
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
              <tr v-if="pending" class="border-b"><td class="px-4 py-3" colspan="5">Caricamento…</td></tr>
              <tr v-else-if="error" class="border-b"><td class="px-4 py-3 text-red-600" colspan="5">{{ errorMessage }}</td></tr>
              <tr v-else-if="!customers.length" class="border-b"><td class="px-4 py-3" colspan="5">Nessun cliente trovato.</td></tr>

              <tr v-for="c in customers" :key="c._id" class="border-b">
                <th scope="row" class="px-4 py-3 font-medium text-gray-900 whitespace-nowrap">
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
                <td class="px-4 py-3 flex items-center justify-end">
                  <button class="inline-flex items-center text-sm font-medium hover:bg-gray-100 p-1.5 text-gray-500 hover:text-gray-800 rounded-lg" type="button">
                    <svg class="w-5 h-5" aria-hidden="true" fill="currentColor" viewBox="0 0 20 20"><path d="M6 10a2 2 0 11-4 0 2 2 0 014 0zM12 10a2 2 0 11-4 0 2 2 0 014 0zM16 12a2 2 0 100-4 2 2 0 000 4z" /></svg>
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Paginazione -->
        <nav class="flex flex-col md:flex-row justify-between items-start md:items-center space-y-3 md:space-y-0 p-4" aria-label="Table navigation">
          <span class="text-sm text-gray-500">
            Mostrando <span class="font-semibold text-gray-900">{{ fromItem }}–{{ toItem }}</span> di
            <span class="font-semibold text-gray-900">{{ totalDisplay }}</span>
          </span>
          <ul class="inline-flex items-stretch -space-x-px">
            <li>
              <button :disabled="page===1" @click="prevPage"
                      class="flex items-center justify-center h-full py-1.5 px-3 ml-0 text-gray-500 bg-white rounded-l-lg border border-gray-300 hover:bg-gray-100 hover:text-gray-700 disabled:opacity-50">
                <span class="sr-only">Precedente</span>
                <svg class="w-5 h-5" aria-hidden="true" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clip-rule="evenodd" /></svg>
              </button>
            </li>
            <li>
              <span class="flex items-center justify-center text-sm py-2 px-3 leading-tight text-primary-600 bg-primary-50 border border-primary-300">{{ page }}</span>
            </li>
            <li>
              <button :disabled="!hasNext" @click="nextPage"
                      class="flex items-center justify-center h-full py-1.5 px-3 leading-tight text-gray-500 bg-white rounded-r-lg border border-gray-300 hover:bg-gray-100 hover:text-gray-700 disabled:opacity-50">
                <span class="sr-only">Successivo</span>
                <svg class="w-5 h-5" aria-hidden="true" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd" /></svg>
              </button>
            </li>
          </ul>
        </nav>
      </div>
    </div>

    <!-- Modale con componente -->
    <div v-show="showCreate"   class="fixed inset-0 z-50 flex items-center justify-center" role="dialog" aria-modal="true">
      <div class="fixed inset-0 bg-black/40" @click="closeCreate"></div>
      <div :class="{ 'hide-scrollbar': showCreate }" class="relative p-4 w-full max-w-2xl max-h-[90vh] overflow-y-auto overscroll-contain bg-white rounded-lg shadow sm:p-5">
        <div class="flex justify-between items-center pb-4 mb-4 border-b">
          <h3 class="text-lg font-semibold text-gray-900">Aggiungi cliente</h3>
          <button type="button" class="text-gray-400 hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm p-1.5" @click="closeCreate">
            <svg aria-hidden="true" class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" /></svg>
            <span class="sr-only">Chiudi</span>
          </button>
        </div>

        <!-- QUI il componente -->
        <CustomerForm :kindDefault="'B2C'" @created="onCreated" @cancel="closeCreate" />
      </div>
    </div>
  </section>
</template>

<style scoped>
.hide-scrollbar {
  scrollbar-width: none;
  -ms-overflow-style: none;
}

.hide-scrollbar::-webkit-scrollbar {
  width: 0;
  height: 0;
  display: none;
}

</style>

<script setup>
import { onClickOutside } from '@vueuse/core'

const { apiFetch } = useApi()

// UI: modale e scroll-lock
const showCreate = ref(false)
const lockScroll = () => document.documentElement.classList.add('overflow-y-hidden')
const unlockScroll = () => document.documentElement.classList.remove('overflow-y-hidden')
watch(showCreate, (open) => open ? lockScroll() : unlockScroll())


onBeforeUnmount(unlockScroll)

const openCreate = () => { showCreate.value = true }
const closeCreate = () => { showCreate.value = false }

// stato query/lista
const q = ref('')
const qInput = ref('')
const kind = ref('')
const page = ref(1)
const limit = ref(10)
const customers = ref([])
const pending = ref(false)
const error = ref(null)
const total = ref(null)
const hasNext = ref(false)

const fetchCustomers = async () => {
  pending.value = true
  error.value = null
  try {
    const query = {
      skip: (page.value - 1) * limit.value,
      limit: limit.value,
      ...(q.value ? { q: q.value } : {}),
      ...(kind.value ? { kind: kind.value } : {})
    }
    let xTotal = null
    const data = await apiFetch('/customers', {
      query,
      onResponse({ response }) { xTotal = response.headers.get('x-total-count') }
    })
    customers.value = data || []
    total.value = xTotal ? Number(xTotal) : null
    hasNext.value = customers.value.length === limit.value &&
      (total.value ? page.value * limit.value < total.value : true)
  } catch (e) {
    error.value = e?.data?.detail || e?.message || 'Errore durante il caricamento'
  } finally {
    pending.value = false
  }
}

const applySearch = () => {
  if (q.value !== qInput.value) {
    q.value = qInput.value
    page.value = 1
    fetchCustomers()
  }
}

const prevPage = () => {
  if (page.value > 1) {
    page.value -= 1
    fetchCustomers()
  }
}
const nextPage = () => {
  if (hasNext.value) {
    page.value += 1
    fetchCustomers()
  }
}

// dropdown filtri
const showFilter = ref(false)
const filterRef = ref(null)
const filterBtn = ref(null)

const toggleFilter = () => { showFilter.value = !showFilter.value }

// chiudi SOLO se click fuori dal pannello e NON sul pulsante "Filtra"
onClickOutside(filterRef, (e) => {
  if (!showFilter.value) return
  const target = e.target
  if (filterBtn.value && target instanceof Element && filterBtn.value.contains(target)) return
  showFilter.value = false
})

// applica i filtri e chiudi
const applyFilters = () => {
  page.value = 1
  fetchCustomers()
  showFilter.value = false
}

// reset filtri (non chiude il pannello: puoi decidere se chiuderlo)
const resetFilters = () => { kind.value = '' }

// derived
const fromItem = computed(() => customers.value.length ? (page.value - 1) * limit.value + 1 : 0)
const toItem = computed(() => (page.value - 1) * limit.value + customers.value.length)
const totalDisplay = computed(() => (total.value ?? `${toItem.value}+`))
const errorMessage = computed(() => String(error.value || ''))

// primo load
onMounted(fetchCustomers)

// callback dal form (modale)
const onCreated = async () => {
  page.value = 1
  await fetchCustomers()
  closeCreate()
}
</script>

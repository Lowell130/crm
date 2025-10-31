<template>
<section class="bg-gray-50 p-3 sm:p-5 antialiased">
    <div class="mx-auto max-w-screen-xl px-4 lg:px-12">
  
   
  
    
      <div class="bg-white rounded-lg shadow p-6 space-y-6">
   <h1 class="text-xl font-semibold">
        {{ mode === 'edit' ? `Modifica fattura ${form.number || ''}` : 'Nuova fattura' }}
      </h1>
    <!-- FORM -->
    <form @submit.prevent class="space-y-6">
      <!-- Cliente -->
      <div>
        <label class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Cliente</label>

        <!-- Selezionato -->
        <div
          v-if="selectedCustomer"
          class="flex items-center justify-between rounded-lg bg-gray-50 dark:bg-gray-700 border border-gray-300 dark:border-gray-600 px-3 py-2"
        >
          <div class="text-sm text-gray-900 dark:text-gray-100">
            <span class="font-medium">
              <template v-if="selectedCustomer.kind==='B2B'">
                {{ selectedCustomer.company_name }}
              </template>
              <template v-else>
                {{ [selectedCustomer.first_name, selectedCustomer.last_name].filter(Boolean).join(' ') }}
              </template>
            </span>
            <span class="text-gray-500 dark:text-gray-300 ml-2">
              <template v-if="selectedCustomer.kind==='B2B'">
                P.IVA: {{ selectedCustomer.vat_number || '—' }}
              </template>
              <template v-else>
                CF: {{ selectedCustomer.codice_fiscale || '—' }}
              </template>
            </span>
          </div>

          <button
            v-if="canChangeCustomer"
            type="button"
            class="text-blue-600 hover:underline text-sm"
            @click="clearSelectedCustomer"
          >
            Cambia
          </button>
        </div>

        <!-- Ricerca -->
        <div v-else class="space-y-2">
          <div class="flex gap-2">
            <input
              v-model="customerQuery"
              @input="debouncedSearch"
              type="search"
              id="customer_search"
              placeholder="Cerca cliente (nome, azienda, CF/P.IVA, email)…"
              class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500
                     focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600
                     dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
            />
            <button
              type="button"
              class="px-4 py-2 text-sm font-medium rounded-lg border bg-white hover:bg-gray-50
                     dark:bg-gray-800 dark:border-gray-600 dark:text-gray-200"
              @click="openList = !openList"
            >
              Lista
            </button>
          </div>

          <div
            v-if="openList && results.length"
            class="mt-1 border border-gray-200 dark:border-gray-600 rounded-lg divide-y bg-white dark:bg-gray-800"
          >
            <button
              v-for="c in results"
              :key="c.id || c._id || c._id_str"
              type="button"
              class="w-full text-left px-3 py-2 hover:bg-gray-50 dark:hover:bg-gray-700 text-sm"
              @click="selectCustomer(c)"
            >
              <div class="font-medium text-gray-900 dark:text-gray-100">
                <span v-if="c.kind==='B2B'">{{ c.company_name }}</span>
                <span v-else>{{ c.first_name }} {{ c.last_name }}</span>
              </div>
              <div class="text-xs text-gray-500 dark:text-gray-300">
                <span v-if="c.kind==='B2B'">P.IVA: {{ c.vat_number || '—' }}</span>
                <span v-else>CF: {{ c.codice_fiscale || '—' }}</span> • {{ c.email || '—' }}
              </div>
            </button>
          </div>
        </div>
      </div>

      <!-- Dati fattura (stile del tuo template) -->
      <div class="grid gap-6 md:grid-cols-2">
        <div>
          <label for="issue_date" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">
            Data emissione
          </label>
          <input
            v-model="form.issue_date"
            type="date"
            id="issue_date"
            class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500
                   focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600
                   dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
          />
        </div>

        <div>
          <label for="due_date" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">
            Scadenza
          </label>
          <input
            v-model="form.due_date"
            type="date"
            id="due_date"
            class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500
                   focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600
                   dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
          />
        </div>

        <div class="md:col-span-2">
          <label for="number" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">
            Numero (opzionale)
          </label>
          <div class="flex gap-2">
            <input
              v-model="form.number"
              id="number"
              placeholder="es. 2025-00001"
              class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500
                     focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600
                     dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
            />
            <button
              type="button"
              class="text-gray-900 bg-white border border-gray-300 focus:outline-none hover:bg-gray-100 focus:ring-4 focus:ring-gray-100 font-medium rounded-full text-sm px-5 py-2.5 dark:bg-gray-800 dark:text-white dark:border-gray-600 dark:hover:bg-gray-700 dark:hover:border-gray-600 dark:focus:ring-gray-700"
              @click="prefillNumber"
            >
              Suggerisci
            </button>
          </div>
        </div>
      </div>

      <!-- Righe -->
      <div>
        <div class="flex items-center justify-between mb-2">
          <h2 class="font-semibold">Righe</h2>
          <button
            type="button"
            class="text-white bg-green-700 hover:bg-green-800 focus:outline-none focus:ring-4 focus:ring-green-300 font-medium rounded-full text-xs px-5 py-2.5 text-center dark:bg-green-600 dark:hover:bg-green-700 dark:focus:ring-green-800"
            @click="addRow"
          >
            Aggiungi riga
          </button>
        </div>

        <div class="overflow-x-auto">
          <table class="w-full text-sm">
            <thead class="text-xs uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-300">
              <tr>
                <th class="px-2 py-2 text-left">Descrizione</th>
                <th class="px-2 py-2 w-32">Q.tà</th>
                <th class="px-2 py-2 w-32">Prezzo</th>
                <th class="px-2 py-2 w-28">% IVA</th>
                <th class="px-2 py-2 w-32 text-right">Totale riga</th>
                <th class="px-2 py-2 w-12"></th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(it, idx) in form.items" :key="idx" class="border-b">
                <td class="px-2 py-2">
                  <input
                    v-model="it.description"
                    placeholder="Voce di fattura"
                    class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500
                           focus:border-blue-500 block w-full p-2 dark:bg-gray-700 dark:border-gray-600
                           dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                  />
                </td>
                <td class="px-2 py-2">
                  <input
                    v-model.number="it.quantity"
                    type="number" step="0.01" min="0"
                    class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500
                           focus:border-blue-500 block w-full p-2 dark:bg-gray-700 dark:border-gray-600
                           dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                  />
                </td>
                <td class="px-2 py-2">
                  <input
                    v-model.number="it.unit_price"
                    type="number" step="0.01" min="0"
                    class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500
                           focus:border-blue-500 block w-full p-2 dark:bg-gray-700 dark:border-gray-600
                           dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                  />
                </td>
                <td class="px-2 py-2">
                  <input
                    v-model.number="it.vat_rate"
                    type="number" step="0.01" min="0"
                    class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500
                           focus:border-blue-500 block w-full p-2 dark:bg-gray-700 dark:border-gray-600
                           dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                  />
                </td>
                <td class="px-2 py-2 text-right align-middle">
                  {{ lineTotal(it).toFixed(2) }} €
                </td>
                <td class="px-2 py-2 text-right align-middle">
                  <button
                    type="button"
                    class="px-2 py-1 text-red-600 hover:underline"
                    @click="removeRow(idx)"
                  >
                    ✕
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Note -->
        <div class="mt-6">
          <label for="notes" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Note</label>
          <textarea
            v-model="form.notes"
            id="notes"
            rows="3"
            placeholder="Aggiungi eventuali note o condizioni di pagamento..."
            class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500
                   focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600
                   dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
          ></textarea>
        </div>

        <!-- Totali -->
        <div class="mt-4 ml-auto w-full sm:w-72 space-y-1 text-sm">
          <div class="flex justify-between">
            <span>Imponibile</span><span>{{ subtotal.toFixed(2) }} €</span>
          </div>
          <div class="flex justify-between">
            <span>IVA</span><span>{{ vat_total.toFixed(2) }} €</span>
          </div>
          <div class="flex justify-between font-semibold text-lg">
            <span>Totale</span><span>{{ total.toFixed(2) }} €</span>
          </div>
        </div>
      </div>

      <!-- Azioni -->
      <div class="flex flex-wrap items-center gap-3">
        <button
          type="button"
          class="text-white bg-purple-700 hover:bg-purple-800 focus:outline-none focus:ring-4 focus:ring-purple-300 font-medium rounded-full text-sm px-5 py-2.5 text-center  dark:bg-purple-600 dark:hover:bg-purple-700 dark:focus:ring-purple-900 disabled:opacity-50"
          :disabled="submitting || !canSubmit"
          @click="save('draft')"
          title="Salva come bozza"
        >
          {{ mode === 'edit' ? 'Salva come bozza' : 'Salva bozza' }}
        </button>

        <button
          type="button"
          class="text-white bg-blue-700 hover:bg-blue-800 focus:outline-none focus:ring-4 focus:ring-blue-300 font-medium rounded-full text-sm px-5 py-2.5 text-center me-2  dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800 disabled:opacity-50"
          :disabled="submitting || !canSubmit"
          @click="save(mode === 'edit' ? (form.status === 'issued' ? 'issued' : 'issued') : 'issued')"
          :title="mode==='edit' ? 'Salva modifiche' : 'Emetti fattura'"
        >
          {{ mode === 'edit' ? 'Salva modifiche' : 'Emetti fattura' }}
        </button>

        <button
          type="button"
          class="text-white bg-red-700 hover:bg-red-800 focus:outline-none focus:ring-4 focus:ring-red-300 font-medium rounded-full text-sm px-5 py-2.5 text-center dark:bg-red-600 dark:hover:bg-red-700 dark:focus:ring-red-900"
          @click="goBack"
          title="Annulla e torna indietro"
        >
          Annulla
        </button>

        <span v-if="errorMsg" class="text-red-600 text-sm">{{ errorMsg }}</span>
        <span v-if="successMsg" class="text-green-700 text-sm">{{ successMsg }}</span>
      </div>
    </form>

    <!-- Debug -->
    <details class="mt-6 border rounded p-3 bg-gray-50 text-xs text-gray-700 dark:bg-gray-800 dark:text-gray-200">
      <summary class="cursor-pointer">Debug</summary>
      <div class="mt-2 space-y-1">
        <div><b>API_BASE:</b> {{ API_BASE }}</div>
        <div><b>Token presente:</b> {{ !!token }}</div>
        <div><b>customer_id:</b> {{ form.customer_id }}</div>
        <div><b>mode:</b> {{ mode }}</div>
        <div><b>items:</b> {{ form.items.length }}</div>
      </div>
    </details>
    
    </div>
  </div>
</section>
</template>




<script setup>
const props = defineProps({
  mode: { type: String, default: 'create' },               // 'create' | 'edit'
  initialInvoice: { type: Object, default: null }          // InvoiceOut quando si edita
})
const emit = defineEmits(['saved'])

definePageMeta({ layout: 'default' })

const route = useRoute()
const router = useRouter()

const token = useState('token', () => null)
const runtime = useRuntimeConfig()
const API_BASE = runtime.public?.apiBase || runtime.public?.NUXT_PUBLIC_API_BASE || 'http://localhost:8000'

const headers = computed(() => {
  const h = token.value ? { Authorization: `Bearer ${token.value}` } : {}
  return h
})

// form base
const today = new Date().toISOString().slice(0,10)
const form = reactive({
  id: null, // usato in edit
  customer_id: null,
  issue_date: today,
  due_date: today,
  number: '',
  notes: '',
  status: 'draft',
  items: [{ description: '', quantity: 1, unit_price: 0, vat_rate: 22 }]
})

const canSubmit = computed(() => {
  if (submitting.value) return false
  if (!form.customer_id) return false
  if (!form.items.length) return false
  const okRows = form.items.every(it =>
    (it.description || '').trim().length > 0 &&
    Number(it.quantity) > 0 &&
    Number(it.unit_price) >= 0 &&
    Number(it.vat_rate) >= 0
  )
  return okRows
})


// ricerca cliente
const customerQuery = ref('')
const results = ref([])
const openList = ref(false)
const selectedCustomer = ref(null)

let timer = null
function debouncedSearch(){
  clearTimeout(timer)
  timer = setTimeout(searchCustomers, 300)
}
async function searchCustomers(){
  if (!customerQuery.value) { results.value = []; return }
  try {
    const list = await $fetch(`${API_BASE}/customers`, {
      headers: headers.value,
      query: { q: customerQuery.value, limit: 10 }
    })
    results.value = list
    openList.value = true
  } catch (e) { console.error(e) }
}
function selectCustomer(c){
  const cid = c.id ?? c._id ?? (c._id && c._id.$oid) ?? c._id_str
  if (!cid) return
  selectedCustomer.value = c
  form.customer_id = cid
  openList.value = false
  customerQuery.value = ''
}
function clearSelectedCustomer(){
  if (!canChangeCustomer.value) return
  selectedCustomer.value = null
  form.customer_id = null
  customerQuery.value = ''
  results.value = []
  openList.value = false
}

// se stai modificando, permetti cambio cliente solo se la fattura è bozza
const canChangeCustomer = computed(() => {
  if (props.mode !== 'edit') return true
  return form.status === 'draft'
})

// numerazione suggerita
async function prefillNumber(){
  try{
    const n = await $fetch(`${API_BASE}/invoices/number/preview/next`, {
      headers: headers.value,
      query: { issue_date: form.issue_date }
    })
    form.number = n
  }catch(e){ console.error(e) }
}

// righe
function addRow(){ form.items.push({ description:'', quantity:1, unit_price:0, vat_rate:22 }) }
function removeRow(i){ form.items.splice(i,1) }

// totali client
const subtotal = computed(() =>
  form.items.reduce((s,it)=> s + (Number(it.quantity||0)*Number(it.unit_price||0)), 0)
)
const vat_total = computed(() =>
  form.items.reduce((s,it)=> s + ((Number(it.quantity||0)*Number(it.unit_price||0))*(Number(it.vat_rate||0)/100)), 0)
)
const total = computed(() => subtotal.value + vat_total.value)
function lineTotal(it){
  const net = Number(it.quantity||0)*Number(it.unit_price||0)
  const vat = net*(Number(it.vat_rate||0)/100)
  return net + vat
}

// submit
const submitting = ref(false)
const errorMsg = ref('')
const successMsg = ref('')

async function save(action = 'issued'){
  errorMsg.value = ''
  successMsg.value = ''
  if (!form.customer_id){ errorMsg.value = 'Seleziona un cliente.'; return }
  if (!form.items.length){ errorMsg.value = 'Aggiungi almeno una riga.'; return }

  submitting.value = true
  try{
    const payload = {
      customer_id: form.customer_id,
      issue_date: form.issue_date,
      due_date: form.due_date || null,
      notes: form.notes || null,
      items: form.items.map(i => ({
        description: i.description,
        quantity: Number(i.quantity||0),
        unit_price: Number(i.unit_price||0),
        vat_rate: Number(i.vat_rate||0)
      })),
      status: action
    }
    if (form.number) payload.number = form.number

    let saved
    if (props.mode === 'edit' && form.id){
      // PATCH
      saved = await $fetch(`${API_BASE}/invoices/${form.id}`, {
        method: 'PATCH',
        headers: { ...headers.value, 'Content-Type':'application/json' },
        body: payload
      })
    } else {
      // POST
      saved = await $fetch(`${API_BASE}/invoices`, {
        method: 'POST',
        headers: { ...headers.value, 'Content-Type':'application/json' },
        body: payload
      })
    }

    successMsg.value = props.mode === 'edit'
      ? 'Fattura aggiornata'
      : (action === 'draft' ? `Bozza ${saved.number || ''} salvata` : `Fattura ${saved.number} emessa`)

    emit('saved', saved)
    setTimeout(()=> navigateTo(`/invoices/details/${saved.id}`), 650)
  }catch(e){
    errorMsg.value = e?.data?.detail || e?.message || 'Errore salvataggio'
  }finally{
    submitting.value = false
  }
}

function goBack(){
  if (window.history.length > 1) router.back()
  else router.push('/invoices')
}

// --- preload ---
// 1) edit: carica dati dalla fattura iniziale
function loadFromInitial(){
  if (!props.initialInvoice) return
  const inv = props.initialInvoice
  form.id = inv.id
  form.customer_id = inv.customer_id
  form.issue_date = inv.issue_date
  form.due_date = inv.due_date || today
  form.number = inv.number || ''
  form.notes = inv.notes || ''
  form.status = inv.status || 'draft'
  form.items = inv.items?.length ? inv.items.map(i => ({
    description: i.description, quantity: i.quantity, unit_price: i.unit_price, vat_rate: i.vat_rate
  })) : [{ description:'', quantity:1, unit_price:0, vat_rate:22 }]

  // mostra il cliente preselezionato usando snapshot (più gradevole a vista)
  if (inv.customer_snapshot){
    selectedCustomer.value = {
      ...inv.customer_snapshot,
      id: inv.customer_id
    }
  }
}

// 2) create: prefill da ?customer_id=...
async function prefillFromQuery() {
  if (props.mode !== 'create') return
  const cid = route.query.customer_id
  if (!cid) return
  try {
    const c = await $fetch(`${API_BASE}/customers/${cid}`, { headers: headers.value })
    const normId = c.id ?? c._id ?? (c._id && c._id.$oid) ?? c._id_str ?? cid
    selectedCustomer.value = c
    form.customer_id = normId
  } catch (e) {
    // ignora
  }
}

onMounted(() => {
  if (props.mode === 'edit') loadFromInitial()
  else prefillFromQuery()
})
watch(() => props.initialInvoice, () => {
  if (props.mode === 'edit') loadFromInitial()
})
watch(() => route.query.customer_id, () => prefillFromQuery())
</script>

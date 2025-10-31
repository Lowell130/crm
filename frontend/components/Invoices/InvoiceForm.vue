<template>
  <section class="p-4 space-y-6 max-w-5xl">
    <div class="flex items-center justify-between">
      <h1 class="text-xl font-semibold">
        {{ mode === 'edit' ? `Modifica fattura ${form.number || ''}` : 'Nuova fattura' }}
      </h1>

      <div class="flex gap-2">
        <button
          type="button"
          class="text-gray-900 bg-white border border-gray-300 hover:bg-gray-100 focus:ring-4 focus:ring-gray-100 font-medium rounded-full text-sm px-4 py-2"
          @click="goBack"
        >
          Annulla
        </button>
        <NuxtLink to="/invoices" class="text-blue-600 hover:underline">Torna all’elenco</NuxtLink>
      </div>
    </div>

    <!-- Cliente -->
    <div>
      <label class="block text-sm font-medium mb-1">Cliente</label>

      <!-- cliente selezionato -->
      <div v-if="selectedCustomer" class="flex items-center justify-between rounded border px-3 py-2 bg-gray-50">
        <div class="text-sm">
          <span class="font-medium">
            <template v-if="selectedCustomer.kind==='B2B'">
              {{ selectedCustomer.company_name }}
            </template>
            <template v-else>
              {{ [selectedCustomer.first_name, selectedCustomer.last_name].filter(Boolean).join(' ') }}
            </template>
          </span>
          <span class="text-gray-500 ml-2">
            <template v-if="selectedCustomer.kind==='B2B'">
              P.IVA: {{ selectedCustomer.vat_number || '—' }}
            </template>
            <template v-else>
              CF: {{ selectedCustomer.codice_fiscale || '—' }}
            </template>
          </span>
        </div>

        <!-- In edit si può decidere se permettere il cambio cliente solo per bozze -->
        <button
          v-if="canChangeCustomer"
          type="button"
          class="text-blue-600 hover:underline text-sm"
          @click="clearSelectedCustomer"
        >
          Cambia
        </button>
      </div>

      <!-- ricerca -->
      <div v-else>
        <div class="flex gap-2">
          <input
            v-model="customerQuery"
            @input="debouncedSearch"
            type="search"
            placeholder="Cerca cliente (nome, azienda, CF/P.IVA, email)…"
            class="border rounded px-3 py-2 flex-1"
          />
          <button @click="openList = !openList" type="button" class="px-3 py-2 border rounded">Lista</button>
        </div>

        <div v-if="openList && results.length" class="mt-2 border rounded divide-y bg-white">
          <button
            v-for="c in results"
            :key="c.id || c._id || c._id_str"
            class="w-full text-left px-3 py-2 hover:bg-gray-50"
            @click="selectCustomer(c)"
          >
            <div class="font-medium">
              <span v-if="c.kind==='B2B'">{{ c.company_name }}</span>
              <span v-else>{{ c.first_name }} {{ c.last_name }}</span>
            </div>
            <div class="text-xs text-gray-500">
              <span v-if="c.kind==='B2B'">P.IVA: {{ c.vat_number || '—' }}</span>
              <span v-else>CF: {{ c.codice_fiscale || '—' }}</span> • {{ c.email || '—' }}
            </div>
          </button>
        </div>
      </div>
    </div>

    <!-- Dati fattura -->
    <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
      <div>
        <label class="block text-sm font-medium mb-1">Data emissione</label>
        <input v-model="form.issue_date" type="date" class="border rounded px-3 py-2 w-full" />
      </div>
      <div>
        <label class="block text-sm font-medium mb-1">Scadenza</label>
        <input v-model="form.due_date" type="date" class="border rounded px-3 py-2 w-full" />
      </div>
      <div>
        <label class="block text-sm font-medium mb-1">Numero (opzionale)</label>
        <div class="flex gap-2">
          <input v-model="form.number" placeholder="es. 2025-00001" class="border rounded px-3 py-2 w-full" />
          <button type="button" class="px-3 py-2 border rounded" @click="prefillNumber">Suggerisci</button>
        </div>
      </div>
    </div>

    <!-- Righe -->
    <div>
      <div class="flex items-center justify-between mb-2">
        <h2 class="font-semibold">Righe</h2>
        <button class="px-3 py-2 rounded border" @click="addRow">Aggiungi riga</button>
      </div>

      <div class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead class="text-xs uppercase bg-gray-50">
            <tr>
              <th class="px-2 py-2">Descrizione</th>
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
                <input v-model="it.description" class="border rounded px-2 py-1 w-full" placeholder="Voce di fattura" />
              </td>
              <td class="px-2 py-2"><input v-model.number="it.quantity" type="number" step="0.01" min="0" class="border rounded px-2 py-1 w-full" /></td>
              <td class="px-2 py-2"><input v-model.number="it.unit_price" type="number" step="0.01" min="0" class="border rounded px-2 py-1 w-full" /></td>
              <td class="px-2 py-2"><input v-model.number="it.vat_rate" type="number" step="0.01" min="0" class="border rounded px-2 py-1 w-full" /></td>
              <td class="px-2 py-2 text-right">{{ lineTotal(it).toFixed(2) }} €</td>
              <td class="px-2 py-2 text-right">
                <button class="px-2 py-1 text-red-600" @click="removeRow(idx)">✕</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Note -->
      <div class="mt-6">
        <label class="block text-sm font-medium mb-1">Note</label>
        <textarea
          v-model="form.notes"
          rows="3"
          placeholder="Aggiungi eventuali note o condizioni di pagamento..."
          class="border rounded px-3 py-2 w-full"
        ></textarea>
      </div>

      <!-- Totali client-side -->
      <div class="mt-4 ml-auto w-full sm:w-72 space-y-1 text-sm">
        <div class="flex justify-between"><span>Imponibile</span><span>{{ subtotal.toFixed(2) }} €</span></div>
        <div class="flex justify-between"><span>IVA</span><span>{{ vat_total.toFixed(2) }} €</span></div>
        <div class="flex justify-between font-semibold text-lg"><span>Totale</span><span>{{ total.toFixed(2) }} €</span></div>
      </div>
    </div>

    <!-- Azioni -->
    <div class="flex flex-wrap items-center gap-3">
      <button
        class="px-4 py-2 rounded border text-gray-700 hover:bg-gray-50 disabled:opacity-50"
        :disabled="submitting || !canSubmit"
        @click="save('draft')"
        type="button"
        title="Salva come bozza"
      >
        {{ mode === 'edit' ? 'Salva come bozza' : 'Salva bozza' }}
      </button>

      <button
        class="px-4 py-2 rounded bg-blue-600 text-white hover:bg-blue-700 disabled:opacity-50"
        :disabled="submitting || !canSubmit"
        @click="save(mode === 'edit' ? (form.status === 'issued' ? 'issued' : 'issued') : 'issued')"
        type="button"
        :title="mode==='edit' ? 'Salva modifiche' : 'Emetti fattura'"
      >
        {{ mode === 'edit' ? 'Salva modifiche' : 'Emetti fattura' }}
      </button>

      <button
        type="button"
        class="px-4 py-2 rounded border text-gray-700 hover:bg-gray-50"
        @click="goBack"
        title="Annulla e torna indietro"
      >
        Annulla
      </button>

      <span v-if="errorMsg" class="text-red-600 text-sm">{{ errorMsg }}</span>
      <span v-if="successMsg" class="text-green-700 text-sm">{{ successMsg }}</span>
    </div>

    <!-- Debug -->
    <details class="mt-6 border rounded p-3 bg-gray-50 text-xs text-gray-700">
      <summary class="cursor-pointer">Debug</summary>
      <div class="mt-2 space-y-1">
        <div><b>API_BASE:</b> {{ API_BASE }}</div>
        <div><b>Token presente:</b> {{ !!token }}</div>
        <div><b>customer_id:</b> {{ form.customer_id }}</div>
        <div><b>mode:</b> {{ mode }}</div>
        <div><b>items:</b> {{ form.items.length }}</div>
      </div>
    </details>
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

const canSubmit = computed(() => !!form.customer_id && form.items.length > 0 && !submitting.value)

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

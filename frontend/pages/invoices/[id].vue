<template>
  <section class="p-4 space-y-6">
    <div class="flex items-center justify-between">
      <div class="flex items-center gap-3">
        <NuxtLink to="/invoices" class="text-blue-600 hover:underline">&larr; Elenco</NuxtLink>
        <h1 class="text-xl font-semibold">Fattura {{ invoice?.number || '—' }}</h1>
        <span v-if="invoice" class="inline-flex items-center px-2 py-1 rounded text-xs"
              :class="invoice.status === 'issued' ? 'bg-green-100 text-green-700'
                    : invoice.status === 'draft' ? 'bg-yellow-100 text-yellow-700'
                    : 'bg-red-100 text-red-700'">
          {{ invoice.status }}
        </span>
      </div>

      <div class="flex flex-wrap gap-2">
        <button class="px-3 py-2 border rounded" @click="printInvoice">Stampa</button>
        <button class="px-3 py-2 border rounded" @click="editNumber">Modifica numero</button>
        <button class="px-3 py-2 border rounded" @click="markPaid">Segna come pagata</button>
        <button class="px-3 py-2 border rounded" @click="duplicate">Duplica</button>
        <button class="px-3 py-2 border rounded text-orange-700" @click="cancelInvoice"
                :disabled="invoice?.status==='cancelled'">Annulla</button>
        <button class="px-3 py-2 border rounded text-red-700" @click="deleteInvoice">Elimina</button>
      </div>
    </div>

    <!-- Avvisi -->
    <p v-if="errorMsg" class="text-red-600 text-sm">{{ errorMsg }}</p>
    <p v-if="successMsg" class="text-green-700 text-sm">{{ successMsg }}</p>

    <!-- Scheda fattura -->
    <div v-if="invoice" id="print-area" class="bg-white rounded-lg shadow p-6 text-sm text-black print:shadow-none print:p-0">
      <div class="flex flex-col md:flex-row md:items-start md:justify-between gap-6">
        <!-- Intestazione -->
        <div class="space-y-1">
          <h2 class="text-2xl font-semibold">Fattura {{ invoice.number }}</h2>
          <div class="text-gray-600">
            <div>Data: <strong>{{ invoice.issue_date }}</strong></div>
            <div v-if="invoice.due_date">Scadenza: <strong>{{ invoice.due_date }}</strong></div>
            <div>ID: <code class="text-xs">{{ invoice.id }}</code></div>
          </div>
        </div>

        <!-- Cliente -->
        <div class="bg-gray-50 border rounded p-3 w-full md:w-96">
          <div class="font-semibold mb-1">Dati cliente</div>
          <div v-if="invoice.customer_snapshot?.kind==='B2B'">
            <div>{{ invoice.customer_snapshot?.company_name }}</div>
            <div v-if="invoice.customer_snapshot?.vat_number">P.IVA: {{ invoice.customer_snapshot?.vat_number }}</div>
          </div>
          <div v-else>
            <div>{{ invoice.customer_snapshot?.first_name }} {{ invoice.customer_snapshot?.last_name }}</div>
            <div v-if="invoice.customer_snapshot?.codice_fiscale">CF: {{ invoice.customer_snapshot?.codice_fiscale }}</div>
          </div>
          <div v-if="invoice.customer_snapshot?.email">{{ invoice.customer_snapshot?.email }}</div>
          <div v-if="invoice.customer_snapshot?.address">
            {{ invoice.customer_snapshot?.address }}<template v-if="invoice.customer_snapshot?.city">, {{ invoice.customer_snapshot?.city }}</template>
            <template v-if="invoice.customer_snapshot?.zip"> ({{ invoice.customer_snapshot?.zip }})</template>
            <template v-if="invoice.customer_snapshot?.country"> - {{ invoice.customer_snapshot?.country }}</template>
          </div>
        </div>
      </div>

      <!-- Righe -->
      <div class="mt-6 overflow-x-auto">
        <table class="w-full">
          <thead class="bg-gray-100 text-xs uppercase">
            <tr>
              <th class="px-3 py-2 text-left">Descrizione</th>
              <th class="px-3 py-2 text-right w-28">Q.tà</th>
              <th class="px-3 py-2 text-right w-32">Prezzo</th>
              <th class="px-3 py-2 text-right w-24">% IVA</th>
              <th class="px-3 py-2 text-right w-36">Totale riga</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(it, i) in invoice.items" :key="i" class="border-b">
              <td class="px-3 py-2">{{ it.description }}</td>
              <td class="px-3 py-2 text-right">{{ n(it.quantity) }}</td>
              <td class="px-3 py-2 text-right">{{ n(it.unit_price) }} €</td>
              <td class="px-3 py-2 text-right">{{ n(it.vat_rate) }}%</td>
              <td class="px-3 py-2 text-right">{{ n(lineTotal(it)) }} €</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Totali -->
      <div class="mt-6 ml-auto w-full md:w-80 space-y-1">
        <div class="flex justify-between"><span>Imponibile</span><span>{{ n(invoice.subtotal) }} €</span></div>
        <div class="flex justify-between"><span>IVA</span><span>{{ n(invoice.vat_total) }} €</span></div>
        <div class="flex justify-between text-lg font-semibold border-t pt-2"><span>Totale</span><span>{{ n(invoice.total) }} €</span></div>
      </div>

      <!-- Note -->
      <div v-if="invoice.notes" class="mt-6">
        <div class="font-medium mb-1">Note</div>
        <p class="whitespace-pre-wrap text-gray-700">{{ invoice.notes }}</p>
      </div>
    </div>

    <div v-else class="text-gray-500">Caricamento…</div>
  </section>
</template>

<script setup>
definePageMeta({ layout: 'default' })

const route = useRoute()
const id = computed(() => route.params.id)

const token = useState('token', () => null)
const runtime = useRuntimeConfig()
const API_BASE = runtime.public?.NUXT_PUBLIC_API_BASE || 'http://localhost:8000'
const headers = computed(() => ({ Authorization: token.value ? `Bearer ${token.value}` : '' }))

const invoice = ref(null)
const errorMsg = ref('')
const successMsg = ref('')

function n(v){ return Number(v || 0).toFixed(2) }
function lineTotal(it){
  const net = Number(it.quantity||0)*Number(it.unit_price||0)
  const vat = net*(Number(it.vat_rate||0)/100)
  return net + vat
}

async function load(){
  errorMsg.value = ''
  try{
    invoice.value = await $fetch(`${API_BASE}/invoices/${id.value}`, { headers: headers.value })
  }catch(e){
    errorMsg.value = e?.data?.detail || 'Errore caricamento'
  }
}
await load()

async function editNumber(){
  const current = invoice.value?.number || ''
  const val = window.prompt('Nuovo numero fattura:', current)
  if (val == null || val === current) return
  try{
    const updated = await $fetch(`${API_BASE}/invoices/${id.value}`, {
      method: 'PATCH',
      headers: { ...headers.value, 'Content-Type':'application/json' },
      body: { number: val }
    })
    invoice.value = updated
    successMsg.value = 'Numero aggiornato'
    setTimeout(()=> successMsg.value='', 1200)
  }catch(e){
    errorMsg.value = e?.data?.detail || 'Errore aggiornamento numero'
  }
}

async function markPaid(){
  // Backend non ha campo "paid_at": annotiamo nelle note mantenendo quelle esistenti
  const today = new Date().toISOString().slice(0,10)
  const prefix = `[PAGATA ${today}] `
  const already = (invoice.value?.notes || '').includes('[PAGATA ')
  const newNotes = already ? invoice.value.notes : (prefix + (invoice.value?.notes || ''))
  try{
    const updated = await $fetch(`${API_BASE}/invoices/${id.value}`, {
      method: 'PATCH',
      headers: { ...headers.value, 'Content-Type':'application/json' },
      body: { notes: newNotes }
    })
    invoice.value = updated
    successMsg.value = 'Segnata come pagata'
    setTimeout(()=> successMsg.value='', 1200)
  }catch(e){
    errorMsg.value = e?.data?.detail || 'Errore aggiornamento'
  }
}

async function cancelInvoice(){
  if (!confirm('Confermi annullamento della fattura?')) return
  try{
    const updated = await $fetch(`${API_BASE}/invoices/${id.value}`, {
      method: 'PATCH',
      headers: { ...headers.value, 'Content-Type':'application/json' },
      body: { status: 'cancelled' }
    })
    invoice.value = updated
    successMsg.value = 'Fattura annullata'
    setTimeout(()=> successMsg.value='', 1200)
  }catch(e){
    errorMsg.value = e?.data?.detail || 'Errore annullamento'
  }
}

async function duplicate(){
  if (!invoice.value) return
  const src = invoice.value
  try{
    const payload = {
      customer_id: src.customer_id,
      issue_date: src.issue_date,
      due_date: src.due_date,
      notes: src.notes,
      items: src.items.map(i => ({
        description: i.description, quantity: i.quantity, unit_price: i.unit_price, vat_rate: i.vat_rate
      })),
      status: src.status
      // numero NON inviato -> autogenerato
    }
    const created = await $fetch(`${API_BASE}/invoices`, {
      method: 'POST',
      headers: { ...headers.value, 'Content-Type':'application/json' },
      body: payload
    })
    successMsg.value = `Duplicata come ${created.number}`
    setTimeout(()=> navigateTo(`/invoices/${created.id}`), 600)
  }catch(e){
    errorMsg.value = e?.data?.detail || 'Errore duplicazione'
  }
}

async function deleteInvoice(){
  if (!confirm('Eliminare definitivamente la fattura?')) return
  try{
    await $fetch(`${API_BASE}/invoices/${id.value}`, {
      method: 'DELETE',
      headers: headers.value
    })
    navigateTo('/invoices')
  }catch(e){
    errorMsg.value = e?.data?.detail || 'Errore eliminazione'
  }
}

function printInvoice(){
  window.print()
}
</script>

<style>
@media print {
  body { background: white !important; }
  #__nuxt > *:not(#__nuxt [id="print-area"]) { display: none !important; }
  #print-area { display: block !important; }
}
</style>

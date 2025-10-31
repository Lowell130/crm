<template>
  <div v-if="pending" class="p-4">Caricamento…</div>
  <div v-else-if="error" class="p-4 text-red-600">{{ errorMessage }}</div>
  <InvoiceForm
    v-else
    mode="edit"
    :initial-invoice="invoice"
    @saved="onSaved"
  />
</template>

<script setup>
import InvoiceForm from '@/components/Invoices/InvoiceForm.vue'

definePageMeta({ layout: 'default' })

const route = useRoute()
const id = computed(() => route.params.id)

const token = useState('token', () => null)
const runtime = useRuntimeConfig()
const API_BASE = runtime.public?.NUXT_PUBLIC_API_BASE || 'http://localhost:8000'
const headers = computed(() => ({ Authorization: token.value ? `Bearer ${token.value}` : '' }))

const invoice = ref(null)
const pending = ref(true)
const error = ref(null)

const errorMessage = computed(() => error.value?.data?.detail || error.value?.message || 'Errore caricamento')

async function load(){
  pending.value = true; error.value = null
  try{
    invoice.value = await $fetch(`${API_BASE}/invoices/${id.value}`, { headers: headers.value })
  }catch(e){ error.value = e }
  finally{ pending.value = false }
}
await load()

function onSaved(){ /* opzionale */ }
</script>

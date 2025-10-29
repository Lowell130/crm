<template>
<div>
    <!-- <hr class="h-px mb-3 bg-gray-200 border-0 dark:bg-gray-700"> -->

  <form @submit.prevent="submit" class="space-y-6">
    <!-- Tipo cliente -->
    <div class="flex gap-6">
      <label for="B2B" class="flex items-center gap-2 cursor-pointer">
        <input id="B2B" type="radio" value="B2B" v-model="form.kind" name="customer-type"
               class="w-4 h-4 text-blue-600 bg-gray-50 border border-gray-300 focus:ring-2 focus:ring-blue-500" />
        <span class="text-sm font-medium text-gray-900">B2B</span>
      </label>
      <label for="B2C" class="flex items-center gap-2 cursor-pointer">
        <input id="B2C" type="radio" value="B2C" v-model="form.kind" name="customer-type"
               class="w-4 h-4 text-blue-600 bg-gray-50 border border-gray-300 focus:ring-2 focus:ring-blue-500" />
        <span class="text-sm font-medium text-gray-900">B2C</span>
      </label>
    </div>

    <!-- Dati aziendali (solo B2B) -->
    <fieldset v-if="isB2B" class="grid gap-6 md:grid-cols-2">
      <legend class="block mb-2 text-sm font-medium text-gray-900">Dati aziendali</legend>
      <div>
        <label for="company_name" class="block mb-2 text-sm font-medium text-gray-900">Ragione sociale</label>
        <input id="company_name" v-model="form.company_name" :required="isB2B" type="text"
               class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
               placeholder="ACME S.p.A." />
        <p v-if="isB2B" class="text-xs text-gray-500 mt-1">Obbligatorio per clienti B2B</p>
      </div>
      <div>
        <label for="vat_number" class="block mb-2 text-sm font-medium text-gray-900">P.IVA</label>
        <input id="vat_number" v-model="form.vat_number" :required="isB2B" type="text"
               class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 uppercase"
               placeholder="IT12345678901" />
        <p v-if="isB2B" class="text-xs text-gray-500 mt-1">Obbligatorio per clienti B2B</p>
      </div>
    </fieldset>

    <!-- Dati anagrafici (sempre visibili, obbligatori solo se B2C) -->
    <fieldset class="grid gap-6 md:grid-cols-3">
      <legend class="block mb-2 text-sm font-medium text-gray-900">Dati anagrafici</legend>
      <div>
        <label for="first_name" class="block mb-2 text-sm font-medium text-gray-900">Nome</label>
        <input id="first_name" v-model="form.first_name" :required="isB2C" type="text"
               class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
               placeholder="Mario" />
        <p v-if="isB2C" class="text-xs text-gray-500 mt-1">Obbligatorio per clienti B2C</p>
      </div>
      <div>
        <label for="last_name" class="block mb-2 text-sm font-medium text-gray-900">Cognome</label>
        <input id="last_name" v-model="form.last_name" :required="isB2C" type="text"
               class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
               placeholder="Rossi" />
        <p v-if="isB2C" class="text-xs text-gray-500 mt-1">Obbligatorio per clienti B2C</p>
      </div>
      <div>
        <label for="codice_fiscale" class="block mb-2 text-sm font-medium text-gray-900">Codice Fiscale</label>
        <input id="codice_fiscale" v-model="form.codice_fiscale" :required="isB2C" type="text"
               class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 uppercase"
               placeholder="RSSMRA80A01H501U" />
        <p v-if="isB2C" class="text-xs text-gray-500 mt-1">Obbligatorio per clienti B2C</p>
      </div>
    </fieldset>

    <!-- Contatti -->
    <div class="grid gap-6 md:grid-cols-3">
      <div>
        <label for="email" class="block mb-2 text-sm font-medium text-gray-900">Email</label>
        <input id="email" v-model="form.email" type="email"
               class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
               placeholder="nome.cognome@example.com" />
      </div>
      <div>
        <label for="phone" class="block mb-2 text-sm font-medium text-gray-900">Telefono</label>
        <input id="phone" v-model="form.phone" type="tel"
               class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
               placeholder="+39 333 1234567" />
      </div>
      <div class="md:col-span-3">
        <label for="address" class="block mb-2 text-sm font-medium text-gray-900">Indirizzo</label>
        <input id="address" v-model="form.address" type="text"
               class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
               placeholder="Via Roma 1, Milano" />
      </div>
    </div>

    <!-- Note -->
    <div>
      <label for="notes" class="block mb-2 text-sm font-medium text-gray-900">Note</label>
      <textarea id="notes" v-model="form.notes" rows="3"
                class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
                placeholder="Note aggiuntive"></textarea>
    </div>

    <!-- Azioni -->
    <div class="flex gap-3 items-center">
      <button type="submit" :disabled="loading"
        class="focus:outline-none text-white bg-green-700 hover:bg-green-800 focus:ring-4 focus:ring-green-300 font-medium rounded-lg text-sm px-5 py-2.5 me-2 mb-2 dark:bg-green-600 dark:hover:bg-green-700 dark:focus:ring-green-800"     >
        {{ loading ? 'Salvataggio...' : 'Crea cliente' }}
      </button>
      <button type="button" @click="$emit('cancel')"
              class="text-gray-900 bg-white border border-gray-300 focus:outline-none hover:bg-gray-100 focus:ring-4 focus:ring-gray-100 font-medium rounded-lg text-sm px-5 py-2.5 me-2 mb-2 dark:bg-gray-800 dark:text-white dark:border-gray-600 dark:hover:bg-gray-700 dark:hover:border-gray-600 dark:focus:ring-gray-700">
        Annulla
      </button>
      <p v-if="formError" class="text-red-600 text-sm">{{ formError }}</p>
      <p v-if="success" class="text-green-700 text-sm">Cliente creato!</p>
    </div>
  </form>
  </div>
</template>

<script setup>
const emit = defineEmits(['created','cancel'])
const props = defineProps({
  kindDefault: { type: String, default: 'B2C' }
})

const { apiFetch } = useApi()
const loading = ref(false)
const formError = ref('')
const success = ref(false)

const form = reactive({
  kind: props.kindDefault,
  first_name: '',
  last_name: '',
  codice_fiscale: '',
  company_name: '',
  vat_number: '',
  email: '',
  phone: '',
  address: '',
  notes: ''
})

const isB2B = computed(() => form.kind === 'B2B')
const isB2C = computed(() => form.kind === 'B2C')

// pulizia campi al cambio tipo
watch(() => form.kind, (k) => {
  if (k === 'B2B') { form.first_name = ''; form.last_name = ''; form.codice_fiscale = '' }
  if (k === 'B2C') { form.company_name = ''; form.vat_number = '' }
})

const submit = async () => {
  loading.value = true; formError.value = ''; success.value = false
  try {
    const payload = { ...form }
    if (payload.codice_fiscale) payload.codice_fiscale = payload.codice_fiscale.trim().toUpperCase()
    if (payload.vat_number) payload.vat_number = payload.vat_number.trim().toUpperCase()

    const created = await apiFetch('/customers', { method: 'POST', body: payload })
    success.value = true

    // reset soft mantenendo tipo selezionato
    if (isB2B.value) { form.company_name = ''; form.vat_number = '' }
    if (isB2C.value) { form.first_name = ''; form.last_name = ''; form.codice_fiscale = '' }
    form.email = ''; form.phone = ''; form.address = ''; form.notes = ''

    emit('created', created)
  } catch (e) {
    formError.value = e?.data?.detail || 'Errore durante la creazione'
  } finally {
    loading.value = false
  }
}
</script>

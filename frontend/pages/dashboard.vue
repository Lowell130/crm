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

    <input
      v-model.trim="qInput"
      id="simple-search"
      type="text"
      class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full pl-10 pr-8 p-2"
      placeholder="Cerca per nome, ragione sociale, CF/P.IVA, email…"
      @keyup.esc="clearSearch"
    />

    <!-- pulsante pulisci -->
    <button
      v-if="qInput"
      type="button"
      class="absolute inset-y-0 right-0 flex items-center pr-2 text-gray-400 hover:text-gray-600"
      @click="clearSearch"
      aria-label="Pulisci ricerca"
      title="Pulisci"
    >
      <!-- icona X -->
     <svg data-v-45d6b13a="" class="w-5 h-5" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path data-v-45d6b13a="" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18 17.94 6M18 18 6.06 6"></path></svg>
    </button>
  </div>
</form>

          </div>

          <div class="w-full md:w-auto flex flex-col md:flex-row space-y-2 md:space-y-0 items-stretch md:items-center justify-end md:space-x-3 flex-shrink-0">
            <button type="button" @click="openCreate"
                    class="flex items-center justify-center text-white bg-primary-700 hover:bg-primary-800 focus:ring-4 focus:ring-primary-300 font-medium rounded-full text-sm px-4 py-2">
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
  class="w-full md:w-auto flex items-center justify-center py-2 px-4 text-sm font-medium text-gray-900 bg-white rounded-full border border-gray-200 hover:bg-gray-100 hover:text-primary-700 focus:z-10 focus:ring-4 focus:ring-gray-200"
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
      <button class="px-3 py-2 text-xs font-medium text-center focus:outline-none text-white bg-red-700 hover:bg-red-800 focus:ring-4 focus:ring-red-300 rounded-full  dark:bg-red-600 dark:hover:bg-red-700 dark:focus:ring-red-900" @click="resetFilters">Reset</button>
      <button class="px-3 py-2 text-xs font-medium text-center text-white bg-green-700 hover:bg-green-800 focus:outline-none focus:ring-4 focus:ring-green-300 rounded-full dark:bg-green-600 dark:hover:bg-green-700 dark:focus:ring-green-800" @click="applyFilters">Applica</button>
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
  <!-- SKELETON: loading -->
  <template v-if="pending">
    <tr v-for="i in 8" :key="'sk-'+i" class="border-b">
      <td class="px-4 py-3">
        <div class="animate-pulse">
          <div class="h-4 bg-gray-200 rounded w-40 mb-2"></div>
          <div class="h-3 bg-gray-200 rounded w-24"></div>
        </div>
      </td>
      <td class="px-4 py-3">
        <div class="animate-pulse h-5 bg-gray-200 rounded w-16"></div>
      </td>
      <td class="px-4 py-3">
        <div class="animate-pulse h-4 bg-gray-200 rounded w-32"></div>
      </td>
      <td class="px-4 py-3">
        <div class="animate-pulse h-4 bg-gray-200 rounded w-48"></div>
      </td>
      <td class="px-4 py-3">
        <div class="animate-pulse h-5 bg-gray-200 rounded w-8 ml-auto"></div>
      </td>
    </tr>
  </template>

  <!-- ERRORE: riga con retry -->
  <tr v-else-if="error" class="border-b">
    <td class="px-4 py-5 text-red-700" colspan="5">
      <div class="flex items-start justify-between gap-4">
        <div class="text-sm">
          <div class="font-medium">Errore durante il caricamento</div>
          <div class="opacity-80">{{ errorMessage }}</div>
        </div>
        <div class="flex gap-2">
          <button
            class="px-3 py-1.5 text-sm rounded-lg border"
            @click="fetchCustomers()"
          >
            Riprova
          </button>
        </div>
      </div>
    </td>
  </tr>

  <!-- NESSUN RISULTATO -->
  <tr v-else-if="!customers.length" class="border-b">
    <td class="px-4 py-8 text-center text-gray-500" colspan="5">
      <div class="flex flex-col items-center gap-2">
        <svg class="w-8 h-8" viewBox="0 0 24 24" fill="none" aria-hidden="true">
          <path d="M10 4h10M4 8h16M4 12h10M4 16h16M4 20h10" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
        </svg>
        <div class="text-sm">Nessun cliente trovato</div>
        <div class="text-xs text-gray-400">Prova a cambiare i filtri o la ricerca</div>
        <div class="flex gap-2 mt-2">
          <button @click="resetFilters(); applyFilters()" class="px-3 py-1.5 text-xs rounded-lg border">Reset filtri</button>
          <button @click="openCreate" class="px-3 py-1.5 text-xs rounded-lg text-white bg-primary-700 hover:bg-primary-800">Aggiungi cliente</button>
        </div>
      </div>
    </td>
  </tr>

  <!-- RIGHE DATI -->
  <tr v-else v-for="c in customers" :key="c._id" class="border-b">
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

<td class="px-4 py-3 flex items-center justify-end gap-1">
  <!-- Dettaglio -->
  <NuxtLink
    :to="`/customers/details/${c._id}`"
    class="inline-flex items-center p-1.5 rounded-lg text-gray-500 hover:text-gray-800 hover:bg-gray-100"
    aria-label="Apri dettaglio cliente"
    title="Dettaglio"
  >
  <svg class="w-5 h-5" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24">
  <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.213 9.787a3.391 3.391 0 0 0-4.795 0l-3.425 3.426a3.39 3.39 0 0 0 4.795 4.794l.321-.304m-.321-4.49a3.39 3.39 0 0 0 4.795 0l3.424-3.426a3.39 3.39 0 0 0-4.794-4.795l-1.028.961"/>
</svg>



  </NuxtLink>

  <!-- Modifica -->
  <button
    type="button"
    class="inline-flex items-center p-1.5 rounded-lg text-gray-500 hover:text-gray-800 hover:bg-gray-100"
    aria-label="Modifica cliente"
    title="Modifica"
    @click="onEdit(c)"
  >
    <!-- icona matita -->
    <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" aria-hidden="true">
      <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
            d="m14.304 4.844 2.852 2.852M7 7H4a1 1 0 0 0-1 1v10a1 1 0 0 0 1 1h11a1 1 0 0 0 1-1v-4.5m2.409-9.91a2.017 2.017 0 0 1 0 2.853l-6.844 6.844L8 14l.713-3.565 6.844-6.844a2.015 2.015 0 0 1 2.852 0Z"/>
    </svg>
  </button>

  <!-- Elimina -->
  <button
    type="button"
    class="inline-flex items-center p-1.5 rounded-lg text-gray-500 hover:text-red-700 hover:bg-red-50 disabled:opacity-50"
    :disabled="deletingId===c._id"
    aria-label="Elimina cliente"
    title="Elimina"
    @click="onDelete(c)"
  >
    <!-- icona X -->
    <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" aria-hidden="true">
      <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
            d="M6 18 17.94 6M18 18 6.06 6"/>
    </svg>
  </button>
</td>



  </tr>
</tbody>


          </table>
        </div>

        <!-- Paginazione -->
        <nav class="flex flex-col md:flex-row justify-between items-start md:items-center space-y-3 md:space-y-0 p-4" aria-label="Table navigation">
          <span class="text-sm text-gray-500">
            Mostrando <span class="font-semibold text-gray-900">{{ fromItem }} – {{ toItem }}</span> di
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
   <!-- Modale con componente -->
<Transition name="fade">
  <div
    v-if="showCreate"
    class="fixed inset-0 z-50 flex items-center justify-center"
    role="dialog"
    aria-modal="true"
  >
    <!-- backdrop -->
    <div class="fixed inset-0 bg-black/40" @click="closeCreate"></div>

    <!-- dialog -->
    <div
      ref="modalRef"
      class="relative p-4 w-full max-w-2xl max-h-[90vh] overflow-y-auto overscroll-contain bg-white rounded-lg shadow sm:p-5 hide-scrollbar outline-none"
      tabindex="-1"
    >
      <div class="flex justify-between items-center pb-4 mb-4">
        <h3 id="modal-title" class="text-lg font-semibold text-gray-900">Aggiungi cliente</h3>
        <button
          type="button"
          class="text-gray-400 hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm p-1.5"
          @click="closeCreate"
        >
          <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
            <path
              fill-rule="evenodd"
              d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
              clip-rule="evenodd"
            />
          </svg>
        </button>
      </div>

      <CustomerForm :kindDefault="'B2C'" @created="onCreated" @cancel="closeCreate" />
    </div>
  </div>
</Transition>

<!-- Toasts -->
<!-- Toasts -->
<div class="fixed top-4 right-4 z-[60] space-y-3">
  <div
    v-for="t in toasts"
    :key="t.id"
    class="flex items-center w-full max-w-xs p-4 text-gray-500 bg-white rounded-lg shadow-sm border border-red-100 dark:text-gray-400 dark:bg-gray-800"
    role="alert"
  >
    <!-- Icona -->
    <div
      class="inline-flex items-center justify-center shrink-0 w-8 h-8 text-red-500 bg-red-100 rounded-lg dark:bg-red-800 dark:text-red-200"
    >
      <svg
        class="w-5 h-5"
        aria-hidden="true"
        xmlns="http://www.w3.org/2000/svg"
        fill="currentColor"
        viewBox="0 0 20 20"
      >
        <path
          d="M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5Zm3.707 11.793a1 1 0 1 1-1.414 1.414L10 11.414l-2.293 2.293a1 1 0 0 1-1.414-1.414L8.586 10 6.293 7.707a1 1 0 0 1 1.414-1.414L10 8.586l2.293-2.293a1 1 0 0 1 1.414 1.414L11.414 10l2.293 2.293Z"
        />
      </svg>
      <span class="sr-only">Error icon</span>
    </div>

    <!-- Contenuto -->
    <div class="ms-3 text-sm font-normal flex-1">
      <!-- <div class="font-medium text-gray-900">{{ t.title }}</div> -->
      <div class="ms-3 text-sm font-normal">{{ t.message }}</div>

      <div v-if="t.onRetry" class="flex gap-2 mt-2">
        <button
          class="px-2.5 py-1 text-xs rounded border text-gray-700 hover:bg-gray-100"
          @click="() => { t.onRetry(); dismissToast(t.id) }"
        >
          Riprova
        </button>
      </div>
    </div>

    <!-- Bottone Chiudi -->
    <button
      type="button"
      class="ms-auto -mx-1.5 -my-1.5 bg-white text-gray-400 hover:text-gray-900 rounded-lg focus:ring-2 focus:ring-gray-300 p-1.5 hover:bg-gray-100 inline-flex items-center justify-center h-8 w-8 dark:text-gray-500 dark:hover:text-white dark:bg-gray-800 dark:hover:bg-gray-700"
      @click="dismissToast(t.id)"
      aria-label="Chiudi"
    >
      <span class="sr-only">Close</span>
      <svg
        class="w-3 h-3"
        aria-hidden="true"
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 14 14"
      >
        <path
          stroke="currentColor"
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6"
        />
      </svg>
    </button>
  </div>
</div>



  </section>
</template>

<style scoped>

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Nasconde la scrollbar ma mantiene lo scroll */
.hide-scrollbar {
  -ms-overflow-style: none; /* IE/Edge */
  scrollbar-width: none;    /* Firefox */
}
.hide-scrollbar::-webkit-scrollbar { display: none; }

/* Evita il "salto" quando blocchi lo scroll del body */
.body-lock {
  overflow: hidden;
}



</style>

<script setup>
import { onClickOutside, useDebounceFn } from '@vueuse/core'


const { apiFetch } = useApi()

const router = useRouter()
const deletingId = ref(null)

function onEdit(c) {
  // Semplice: portiamo l’utente in una pagina di edit (la crei dopo).
  // Opzione A: pagina dedicata /customers/[id]/edit
  router.push(`/customers/${c._id}/edit`)

  // In alternativa (se non vuoi creare una pagina subito):
  // router.push(`/customers/${c._id}?edit=1`)
  // e nella pagina dettaglio, se trovi ?edit=1, mostri un form di edit.
}

async function onDelete(c) {
  if (deletingId.value || !c?._id) return
  const ok = window.confirm(`Confermi l'eliminazione del cliente ${c.company_name || (c.first_name + ' ' + c.last_name) || c._id}?`)
  if (!ok) return

  try {
    deletingId.value = c._id
    await apiFetch(`/customers/${c._id}`, { method: 'DELETE' })

    // aggiorna lista
    // se rimane lista vuota e non sei alla prima pagina, torna indietro di pagina
    if (customers.value.length === 1 && page.value > 1) {
      page.value -= 1
    }
    await fetchCustomers()

    pushToast({
      title: 'Cliente eliminato',
      message: `Il cliente è stato eliminato correttamente.`
    })
  } catch (e) {
    const msg = e?.data?.detail || e?.message || 'Errore durante l’eliminazione'
    pushToast({
      title: 'Eliminazione fallita',
      message: msg,
      onRetry: () => onDelete(c)
    })
  } finally {
    deletingId.value = null
  }
}


// UI: modale e scroll-lock
// stato esistente
const showCreate = ref(false)

// —— SCROLL LOCK senza salto (compensazione scrollbar) ——
let prevFocusEl = null
let bodyOriginalPaddingRight = ''
const getScrollbarWidth = () => {
  const sc = document.createElement('div')
  sc.style.visibility = 'hidden'
  sc.style.overflow = 'scroll'
  sc.style.msOverflowStyle = 'scrollbar'
  sc.style.position = 'absolute'
  sc.style.top = '-9999px'
  sc.style.width = '100px'
  document.body.appendChild(sc)
  const inner = document.createElement('div')
  inner.style.width = '100%'
  sc.appendChild(inner)
  const width = sc.offsetWidth - inner.offsetWidth
  sc.parentNode.removeChild(sc)
  return width
}

const lockScroll = () => {
  const sw = getScrollbarWidth()
  bodyOriginalPaddingRight = document.body.style.paddingRight || ''
  if (sw > 0) document.body.style.paddingRight = `${sw}px`
  document.body.classList.add('body-lock')
}
const unlockScroll = () => {
  document.body.classList.remove('body-lock')
  document.body.style.paddingRight = bodyOriginalPaddingRight
}

// —— Focus trap + ESC + restore focus ——
const modalRef = ref(null)
const closeBtnRef = ref(null)
const focusableSelector = [
  'a[href]',
  'area[href]',
  'input:not([disabled]):not([type="hidden"])',
  'select:not([disabled])',
  'textarea:not([disabled])',
  'button:not([disabled])',
  'iframe',
  '[tabindex]:not([tabindex="-1"])',
  '[contenteditable="true"]'
].join(',')

const focusFirstElement = () => {
  const root = modalRef.value
  if (!root) return
  const els = Array.from(root.querySelectorAll(focusableSelector))
  // preferisci il primo campo del form, altrimenti il bottone chiudi
  const preferred = els.find(el => el.tagName === 'INPUT' || el.tagName === 'SELECT' || el.tagName === 'TEXTAREA')
  if (preferred) preferred.focus()
  else if (closeBtnRef.value) closeBtnRef.value.focus()
  else root.focus()
}

const trapTab = (e) => {
  if (e.key !== 'Tab') return
  const root = modalRef.value
  if (!root) return
  const els = Array.from(root.querySelectorAll(focusableSelector)).filter(el => el.offsetParent !== null || el === document.activeElement)
  if (els.length === 0) return

  const first = els[0]
  const last = els[els.length - 1]
  const active = document.activeElement

  if (e.shiftKey && (active === first || active === root)) {
    e.preventDefault()
    last.focus()
  } else if (!e.shiftKey && active === last) {
    e.preventDefault()
    first.focus()
  }
}

const onModalKeydown = (e) => {
  if (e.key === 'Escape') {
    e.preventDefault()
    closeCreate()
    return
  }
  trapTab(e)
}

const openCreate = () => {
  prevFocusEl = document.activeElement
  showCreate.value = true
}

const closeCreate = () => {
  showCreate.value = false
}

watch(showCreate, (open) => {
  if (open) {
    // lock scroll + focus management
    lockScroll()
    // aspetta il render
    requestAnimationFrame(() => {
      if (modalRef.value) modalRef.value.focus()
      focusFirstElement()
    })
  } else {
    // restore
    unlockScroll()
    if (prevFocusEl && typeof prevFocusEl.focus === 'function') {
      prevFocusEl.focus()
    }
  }
})

onBeforeUnmount(() => {
  unlockScroll()
})

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
    const msg = e?.data?.detail || e?.message || 'Errore durante il caricamento'
    error.value = msg
    // toast con retry
    pushToast({
      title: 'Impossibile caricare i clienti',
      message: msg,
      onRetry: () => fetchCustomers()
    })
  } finally {
    pending.value = false
  }
}

// --- LIVE SEARCH con debounce ---
const debouncedApplySearch = useDebounceFn(() => {
  if (q.value !== qInput.value) {
    q.value = qInput.value
    page.value = 1
  }
  fetchCustomers()
}, 300)

// trigger live ogni volta che digiti
watch(qInput, () => {
  debouncedApplySearch()
})

// fallback: submit manuale (invoca subito, senza debounce)
const applySearch = () => {
  if (q.value !== qInput.value) {
    q.value = qInput.value
    page.value = 1
  }
  fetchCustomers()
}

// utility: pulisci ricerca
const clearSearch = () => {
  if (!qInput.value) return
  qInput.value = ''
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
const totalDisplay = computed(() => {
  if (total.value !== null && total.value !== undefined) return total.value
  // se non sappiamo il totale:
  if (customers.value.length === 0) return '0'
  // abbiamo almeno una pagina piena ma senza totale certo
  return `${toItem.value}+`
})
const errorMessage = computed(() => String(error.value || ''))

// primo load
onMounted(fetchCustomers)

// callback dal form (modale)
const onCreated = async () => {
  page.value = 1
  await fetchCustomers()
  closeCreate()
}


// --- TOAST API minimal ---
const toasts = reactive([])
let toastIdSeq = 1

function pushToast({ title, message, onRetry } = {}) {
  const id = toastIdSeq++
  const t = { id, title: title || 'Errore', message: message || '', onRetry: onRetry || null }
  toasts.push(t)
  // autodismiss in 5s
  setTimeout(() => dismissToast(id), 5000)
  return id
}
function dismissToast(id) {
  const idx = toasts.findIndex(t => t.id === id)
  if (idx !== -1) toasts.splice(idx, 1)
}


</script>

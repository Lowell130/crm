// Gestisce stato + fetch + paginazione + filtri + ricerca live (debounced)
import { useDebounceFn } from '@vueuse/core'

export function useCustomers(apiFetch) {
  // --- stato query/lista ---
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

  // --- derived (ui helpers) ---
  const fromItem = computed(() => customers.value.length ? (page.value - 1) * limit.value + 1 : 0)
  const toItem   = computed(() => (page.value - 1) * limit.value + customers.value.length)
  const totalDisplay = computed(() => {
    if (total.value !== null && total.value !== undefined) return total.value
    if (customers.value.length === 0) return '0'
    return `${toItem.value}+`
  })
  const errorMessage = computed(() => String(error.value || ''))

  // --- fetch lista ---
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
        onResponse({ response }) {
          xTotal = response.headers.get('x-total-count')
        }
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

  // --- ricerca live con debounce ---
  const debouncedApplySearch = useDebounceFn(() => {
    if (q.value !== qInput.value) {
      q.value = qInput.value
      page.value = 1
    }
    fetchCustomers()
  }, 300)

  watch(qInput, debouncedApplySearch)

  // --- azioni toolbar ---
  const applySearch = () => {
    if (q.value !== qInput.value) {
      q.value = qInput.value
      page.value = 1
    }
    fetchCustomers()
  }
  const clearSearch = () => { if (qInput.value) qInput.value = '' }

  const prevPage = () => { if (page.value > 1) { page.value -= 1; fetchCustomers() } }
  const nextPage = () => { if (hasNext.value) { page.value += 1; fetchCustomers() } }

  const applyFilters = () => { page.value = 1; fetchCustomers() }
  const resetFilters = () => { kind.value = '' }

  onMounted(fetchCustomers)

  return {
    // stato
    q, qInput, kind, page, limit,
    customers, pending, error, total, hasNext,
    // derived
    fromItem, toItem, totalDisplay, errorMessage,
    // azioni
    fetchCustomers, applySearch, clearSearch,
    prevPage, nextPage, applyFilters, resetFilters,
  }
}

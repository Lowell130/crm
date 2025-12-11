// composables/useDashboardStats.js
export function useDashboardStats () {
  const token = useState('token', () => null)
  const runtime = useRuntimeConfig()
  const API_BASE = runtime.public?.apiBase || runtime.public?.NUXT_PUBLIC_API_BASE || 'http://localhost:8000'

  const headers = computed(() => (token.value ? { Authorization: `Bearer ${token.value}` } : {}))

  // STATE
  const kpi = ref(null)
  const series = ref([])
  const topCustomers = ref([])
  const clientsDistribution = ref({ b2b: 0, b2c: 0, total: 0 }) // 👈 NEW
  const loading = ref(false)
  const error = ref(null)

  async function loadKpi (params = {}) {
    const { date_from, date_to } = params
    return await $fetch(`${API_BASE}/invoices/stats`, {
      headers: headers.value,
      query: { date_from, date_to }
    })
  }

  async function loadTimeseries (days = 30) {
    return await $fetch(`${API_BASE}/invoices/timeseries`, {
      headers: headers.value,
      query: { days }
    })
  }

  async function loadTopCustomers ({ limit = 5, days = 90 } = {}) {
    return await $fetch(`${API_BASE}/invoices/top-customers`, {
      headers: headers.value,
      query: { limit, days }
    })
  }

  // 👇 NEW: distribuzione clienti
  async function loadClientsDistribution () {
    return await $fetch(`${API_BASE}/customers/stats/distribution`, {
      headers: headers.value
    })
  }

  async function refreshAll ({ kpiRange = {}, tsDays = 30, topCfg = { limit: 5, days: 90 } } = {}) {
    loading.value = true
    error.value = null
    try {
      const [k, ts, top, dist] = await Promise.all([
        loadKpi(kpiRange),
        loadTimeseries(tsDays),
        loadTopCustomers(topCfg),
        loadClientsDistribution(),            // 👈 NEW
      ])
      kpi.value = k
      series.value = ts
      topCustomers.value = top
      clientsDistribution.value = dist || { b2b: 0, b2c: 0, total: 0 } // 👈 NEW
    } catch (e) {
      error.value = e?.data?.detail || e?.message || 'Errore caricamento dashboard'
    } finally {
      loading.value = false
    }
  }

  return {
    kpi, series, topCustomers, clientsDistribution, // 👈 expose
    loading, error,
    refreshAll, loadKpi, loadTimeseries, loadTopCustomers, loadClientsDistribution
  }
}

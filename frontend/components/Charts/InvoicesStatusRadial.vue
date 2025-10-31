<template>
  <ClientOnly>
    <!-- <div class="max-w-sm w-full bg-white rounded-lg shadow-sm dark:bg-gray-800 p-4 md:p-6"> -->
     <div class=" w-full bg-white rounded-lg shadow-sm dark:bg-gray-800 p-4 md:p-6">
      <!-- Header -->
      <div class="flex justify-between mb-3">
        <div class="flex items-center">
          <h5 class="text-xl font-bold leading-none text-gray-900 dark:text-white pe-1">
            Stato Fatture
          </h5>
        </div>
      </div>

      <!-- KPI pill summary -->
      <div class="bg-gray-50 dark:bg-gray-700 p-3 rounded-lg">
        <div class="grid grid-cols-3 gap-3 mb-2">
          <dl class="bg-emerald-50 dark:bg-gray-600 rounded-lg flex flex-col items-center justify-center h-[78px]">
            <dt class="w-8 h-8 rounded-full bg-emerald-100 dark:bg-gray-500 text-emerald-600 dark:text-emerald-300 text-sm font-medium flex items-center justify-center mb-1">
              {{ stats.paid }}
            </dt>
            <dd class="text-emerald-600 dark:text-emerald-300 text-sm font-medium">Pagate</dd>
          </dl>
          <dl class="bg-blue-50 dark:bg-gray-600 rounded-lg flex flex-col items-center justify-center h-[78px]">
            <dt class="w-8 h-8 rounded-full bg-blue-100 dark:bg-gray-500 text-blue-600 dark:text-blue-300 text-sm font-medium flex items-center justify-center mb-1">
              {{ stats.issued }}
            </dt>
            <dd class="text-blue-600 dark:text-blue-300 text-sm font-medium">Emesse</dd>
          </dl>
          <dl class="bg-yellow-50 dark:bg-gray-600 rounded-lg flex flex-col items-center justify-center h-[78px]">
            <dt class="w-8 h-8 rounded-full bg-yellow-100 dark:bg-gray-500 text-yellow-600 dark:text-yellow-300 text-sm font-medium flex items-center justify-center mb-1">
              {{ stats.draft }}
            </dt>
            <dd class="text-yellow-600 dark:text-yellow-300 text-sm font-medium">Bozze</dd>
          </dl>
        </div>
        <div class="grid grid-cols-1">
          <dl class="bg-red-50 dark:bg-gray-600 rounded-lg flex items-center justify-center h-[48px]">
            <div class="flex items-center gap-2">
              <span class="w-6 h-6 rounded-full bg-red-100 dark:bg-gray-500 text-red-600 dark:text-red-300 text-xs font-medium flex items-center justify-center">
                {{ stats.cancelled }}
              </span>
              <span class="text-red-600 dark:text-red-300 text-sm font-medium">Annullate</span>
            </div>
          </dl>
        </div>
      </div>

      <!-- Radial Chart -->
      <div class="py-6">
        <div id="radial-chart" class="w-full"></div>
      </div>
    </div>
  </ClientOnly>
</template>

<script setup>
// === Config & state ===
const token = useState('token', () => null)
const runtime = useRuntimeConfig()
const API_BASE = runtime.public?.apiBase || runtime.public?.NUXT_PUBLIC_API_BASE || 'http://localhost:8000'

const headers = computed(() =>
  token.value ? { Authorization: `Bearer ${token.value}` } : {}
)

const stats = reactive({
  paid: 0,
  issued: 0,
  draft: 0,
  cancelled: 0,
})

let chart = null
let Apex = null

// === Helpers ===
async function fetchCount(params) {
  // Usiamo $fetch e leggiamo X-Total-Count tramite onResponse
  let total = 0
  await $fetch(`${API_BASE}/invoices`, {
    headers: headers.value,
    query: { skip: 0, limit: 1, ...params },
    onResponse({ response }) {
      const t = response.headers.get('x-total-count')
      total = t ? Number(t) : 0
    }
  })
  return total
}

async function loadStats() {
  const [paid, issued, draft, cancelled] = await Promise.all([
    fetchCount({ paid: true }),
    fetchCount({ status: 'issued' }),
    fetchCount({ status: 'draft' }),
    fetchCount({ status: 'cancelled' }),
  ])
  stats.paid = paid
  stats.issued = issued
  stats.draft = draft
  stats.cancelled = cancelled

  renderChart()
}

function getChartOptions() {
  const series = [stats.paid, stats.issued, stats.draft, stats.cancelled]
  return {
    series,
    colors: ['#10B981', '#1C64F2', '#F59E0B', '#EF4444'],
    chart: {
      height: 350,
      width: '100%',
      type: 'radialBar',
      sparkline: { enabled: true },
    },
    plotOptions: {
      radialBar: {
        track: { background: '#E5E7EB' },
        dataLabels: { show: false },
        hollow: { margin: 0, size: '32%' },
      },
    },
    grid: {
      show: false,
      strokeDashArray: 4,
      padding: { left: 2, right: 2, top: -23, bottom: -20 },
    },
    labels: ['Pagate', 'Emesse', 'Bozze', 'Annullate'],
    legend: {
      show: true,
      position: 'bottom',
      fontFamily: 'Inter, sans-serif',
    },
    tooltip: {
      enabled: true,
      y: { formatter: (val) => `${val}` },
      x: { show: true },
    },
    yaxis: { show: false },
  }
}

async function renderChart() {
  // Import dinamico solo lato client
  if (!Apex) {
    const mod = await import('apexcharts')
    Apex = mod.default || mod
  }

  const el = document.querySelector('#radial-chart')
  if (!el) return

  // Se esiste già, aggiorno; altrimenti creo
  if (chart) {
    chart.updateOptions(getChartOptions())
  } else {
    chart = new Apex(el, getChartOptions())
    await chart.render()
  }
}

// === Lifecycle ===
onMounted(() => {
  loadStats()
  // opzionale: refresh ogni tot minuti
  // const interval = setInterval(loadStats, 60_000)
  // onUnmounted(() => clearInterval(interval))
})

onUnmounted(() => {
  if (chart) {
    chart.destroy()
    chart = null
  }
})
</script>

<!-- components/Dashboard/TopClientsBar.vue -->
<template>
  <div class="h-64">
    <div v-if="loading" class="h-full flex items-center justify-center text-sm text-gray-500">
      Caricamento…
    </div>
    <div v-else ref="el" class="h-full"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, watch, nextTick, computed } from 'vue'

const props = defineProps({
  loading: { type: Boolean, default: false },
  // [{ name, amount, invoices, customer_id }]
  items:   { type: Array,   default: () => [] }
})

let chart = null
let Apex  = null
const el = ref(null)

const cats = computed(() => props.items.map(i => i.name || '—'))
const vals = computed(() => props.items.map(i => Number(i.amount || 0)))

function options () {
  return {
    chart: {
      type: 'bar',
      height: '100%',
      toolbar: { show: false },
      // 👉 click sulle barre
      events: {
        dataPointSelection: (_event, _ctx, config) => {
          const idx = config?.dataPointIndex
          if (idx == null) return
          const row = props.items[idx]
          const id  = row?.customer_id
          if (id) navigateTo(`/customers/details/${id}`)
        }
      }
    },
    plotOptions: {
      bar: {
        horizontal: true,
        borderRadius: 4,
        distributed: false
      }
    },
    series: [{ name: 'Fatturato', data: vals.value }],
    xaxis: {
      categories: cats.value,
      labels: { style: { fontSize: '12px' } }
    },
    dataLabels: { enabled: false },
    // 👇 tooltip standard (solo formatter del valore)
    tooltip: { y: { formatter: v => `${Number(v || 0).toFixed(2)} €` } },
    colors: ['#4f46e5'],
    grid: { borderColor: '#e5e7eb', strokeDashArray: 4 },
    noData: { text: 'Nessun dato' },
    legend: { show: false }
  }
}

async function ensureApex () {
  if (typeof window !== 'undefined' && window.ApexCharts) {
    Apex = window.ApexCharts
    return
  }
  if (!Apex && typeof window !== 'undefined') {
    const mod = await import('apexcharts')
    Apex = mod.default || mod
  }
}

async function mountChart () {
  if (!process.client) return
  await ensureApex()
  if (!Apex || !el.value) return
  if (chart) { chart.destroy(); chart = null }
  chart = new Apex(el.value, options())
  await chart.render()
}

async function updateChart () {
  if (!chart) return
  await chart.updateOptions(options(), false, true)
}

onMounted(async () => {
  if (!props.loading) {
    await nextTick()
    await mountChart()
  }
})

watch(() => props.loading, async (now) => {
  if (!now) {
    await nextTick()
    await mountChart()
  }
})

watch(() => props.items, updateChart, { deep: true })

onBeforeUnmount(() => { if (chart) chart.destroy() })
</script>

<style scoped>
/* cursore “mano” sulle barre */
:deep(.apexcharts-series path),
:deep(.apexcharts-bar-area) {
  cursor: pointer;
}
</style>

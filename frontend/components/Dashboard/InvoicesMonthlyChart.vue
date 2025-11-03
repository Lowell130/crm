<!-- components/Dashboard/InvoicesMonthlyChart.vue -->
<template>
  <div class="h-64">
    <div v-if="loading" class="h-full flex items-center justify-center text-sm text-gray-500">
      Caricamento…
    </div>
    <div v-else ref="el" class="h-full"></div>
  </div>
</template>

<script setup>
import { onMounted, onBeforeUnmount, ref, watch, nextTick } from 'vue'

const props = defineProps({
  loading:     { type: Boolean, default: false },
  categories:  { type: Array,   default: () => [] }, // date/etichette asse X
  series:      { type: Array,   default: () => [] }  // [{ name, data: [...] }, ...]
})

let chart = null
let Apex  = null
const el = ref(null)

function options () {
  const cats = (props.categories?.length ? props.categories : [])
  const sers = (props.series?.length ? props.series : [{ name: 'Serie', data: [] }])

  return {
    chart: {
      type: 'area',
      height: '100%',
      toolbar: { show: false },
      dropShadow: { enabled: false },
      animations: { enabled: true }
    },
    series: sers,
    xaxis: {
      categories: cats,
      type: 'category',
      labels: { rotate: -45, trim: true },
      axisBorder: { show: false },
      axisTicks:  { show: false }
    },
    yaxis: {
      labels: {
        formatter: (v) => Number(v || 0).toFixed(0)
      }
    },
    dataLabels: { enabled: false },
    stroke: { curve: 'smooth', width: 3 },
    fill: {
      type: 'gradient',
      gradient: {
        opacityFrom: 0.45,
        opacityTo: 0,
      }
    },
    grid: {
      show: true,
      strokeDashArray: 4,
      padding: { left: 2, right: 2, top: 0 }
    },
    tooltip: { shared: true },
    colors: ['#1A56DB', '#16BDCA', '#F59E0B'],
    noData: { text: 'Nessun dato' },
    legend: { show: true, position: 'bottom' }
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

// se non sta caricando, monta al mount
onMounted(async () => {
  if (!props.loading) {
    await nextTick()
    await mountChart()
  }
})

// quando loading diventa false, monta il grafico
watch(() => props.loading, async (now) => {
  if (!now) {
    await nextTick()
    await mountChart()
  }
})

// aggiorna quando cambiano categories/series
watch(() => [props.categories, props.series], updateChart, { deep: true })

onBeforeUnmount(() => { if (chart) chart.destroy() })
</script>

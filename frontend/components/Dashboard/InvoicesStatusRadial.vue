<!-- components/Dashboard/InvoicesStatusRadial.vue -->
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
  loading: { type: Boolean, default: false },
  labels:  { type: Array,   default: () => [] },
  series:  { type: Array,   default: () => [] }
})

let chart = null
let Apex = null              // <-- istanza modulo, se usiamo import()
const el = ref(null)

function options () {
  return {
    series: props.series?.length ? props.series : [0, 0, 0],
    labels: props.labels?.length ? props.labels : ['Emesse', 'Bozze', 'Annullate'],
    chart: { type: 'radialBar', height: '100%', toolbar: { show: false } },
    plotOptions: {
      radialBar: {
        track: { background: '#E5E7EB' },
        dataLabels: { show: true, name: { show: true }, value: { show: true } },
        hollow: { size: '35%' }
      }
    },
    legend: { show: true, position: 'bottom' },
    colors: ['#22c55e','#f59e0b','#ef4444'],
    noData: { text: 'Nessun dato' }
  }
}

async function ensureApex () {
  if (typeof window !== 'undefined' && window.ApexCharts) {
    Apex = window.ApexCharts
    return
  }
  // fallback: import del modulo NPM (solo client)
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

// Se loading passa da true -> false, crea il grafico in quel momento
watch(() => props.loading, async (now) => {
  if (!now) {
    await nextTick()
    await mountChart()
  }
})

// Aggiorna quando cambiano dati/etichette
watch(() => [props.series, props.labels], updateChart, { deep: true })

onBeforeUnmount(() => { if (chart) chart.destroy() })
</script>

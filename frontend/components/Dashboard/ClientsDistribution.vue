<!-- components/Dashboard/ClientsDistribution.vue -->
<template>
  <div class="h-64">
    <div v-if="loading" class="h-full flex items-center justify-center text-sm text-gray-500">
      Caricamento…
    </div>

    <!-- stato: nessun dato -->
    <div v-else-if="total === 0" class="h-full flex items-center justify-center text-sm text-gray-500">
      Nessun dato (B2B: {{ b2b }}, B2C: {{ b2c }})
    </div>

    <!-- grafico -->
    <div v-else ref="el" class="h-full"></div>

    <!-- opzionale: debug UI, disattivo per default -->
    <div v-if="debug" class="mt-2 text-xs text-gray-500">
      <div>hasApex: {{ !!Apex }}</div>
      <div>chartExists: {{ !!chart }}</div>
      <div>mounted: {{ mounted }}</div>
      <div>loading: {{ loading }}</div>
      <div>counts.b2b: {{ b2b }}</div>
      <div>counts.b2c: {{ b2c }}</div>
      <div>series: [{{ series.join(', ') }}]</div>
      <div>labels: [{{ labels.join(', ') }}]</div>
      <div>total: {{ total }}</div>
      <div>clientOnly: true</div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount, watch, nextTick } from 'vue'

const props = defineProps({
  loading: { type: Boolean, default: false },
  counts:  { type: Object,  default: () => ({ b2b: 0, b2c: 0 }) },
  debug:   { type: Boolean, default: false }, // 👈 default OFF
})

const b2b = computed(() => Number(props.counts?.b2b || 0))
const b2c = computed(() => Number(props.counts?.b2c || 0))
const total = computed(() => b2b.value + b2c.value)
const labels = ['B2B', 'B2C']
const series = computed(() => [b2b.value, b2c.value])

let chart = null
let Apex  = null
const el = ref(null)
const mounted = ref(false)

function chartOptions () {
  return {
    chart: {
      type: 'donut',
      height: '100%',
      toolbar: { show: false }
    },
    labels,
    series: series.value,
    legend: { show: true, position: 'bottom' },
    dataLabels: { enabled: true },
    tooltip: {
      y: {
        formatter: (v) => `${v} (${total.value ? Math.round((v / total.value) * 100) : 0}%)`
      }
    },
    colors: ['#0ea5e9','#22c55e'], // opzionale
    
    stroke: { width: 1 },
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
  if (total.value === 0) return
  await ensureApex()
  if (!Apex || !el.value) return
  if (chart) { chart.destroy(); chart = null }
  chart = new Apex(el.value, chartOptions())
  await chart.render()
}

async function updateChart () {
  if (!chart) return
  await chart.updateOptions(chartOptions(), false, true)
}

onMounted(async () => {
  mounted.value = true
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

watch([b2b, b2c], async () => {
  if (total.value === 0) {
    if (chart) { chart.destroy(); chart = null }
    return
  }
  if (!chart) {
    await nextTick()
    await mountChart()
  } else {
    await updateChart()
  }
})

onBeforeUnmount(() => { if (chart) chart.destroy() })
</script>

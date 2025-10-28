<template>
  <div>
    <PageHeader title="Dashboard" subtitle="Panoramica CRM" />
    <div class="grid md:grid-cols-3 gap-4 mt-4">
      <StatsCard label="Clienti totali" :value="summary?.total ?? '—'" />
      <StatsCard label="B2C" :value="summary?.b2c ?? '—'" />
      <StatsCard label="B2B" :value="summary?.b2b ?? '—'" />
    </div>

    <div class="mt-6">
      <ChartCard title="Clienti attivi per mese" :series="series" />
    </div>
  </div>
</template>

<script setup>
definePageMeta({ layout: 'dashboard' })

const {$api} = useNuxtApp()
// summary
const { data: summary } = await useAsyncData('stats:summary', () => $api('/stats/summary'))
// series
const { data: monthly } = await useAsyncData('stats:active', () => $api('/stats/active-by-month'))
const series = computed(() => (monthly.value?.data || []).map(d => ({ x: d._id, y: d.count })))
</script>

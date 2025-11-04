<template>
  <section class="p-4 space-y-6">
    <!-- Header -->
    <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-3">
      <h1 class="text-2xl font-semibold text-gray-900">Overview</h1>
      <div class="flex flex-wrap gap-2">
        <button class="text-gray-900 bg-white border border-gray-300 focus:outline-none hover:bg-gray-100 focus:ring-4 focus:ring-gray-100 font-medium rounded-full text-sm px-5 py-2.5 me-2 mb-2 dark:bg-gray-800 dark:text-white dark:border-gray-600 dark:hover:bg-gray-700 dark:hover:border-gray-600 dark:focus:ring-gray-700" @click="doRefresh" :disabled="loading">
          {{ loading ? 'Aggiorno…' : 'Aggiorna' }}
        </button>
        <button class="text-white bg-green-700 hover:bg-green-800 focus:outline-none focus:ring-4 focus:ring-green-300 font-medium rounded-full text-sm px-5 py-2.5 text-center me-2 mb-2 dark:bg-green-600 dark:hover:bg-green-700 dark:focus:ring-green-800">Esporta</button>
      </div>
    </div>

    <div v-if="error" class="p-3 bg-red-50 text-red-700 rounded">{{ error }}</div>

    <!-- KPI row -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      <StatsCard title="Fatture totali" :value="k.totalInvoices" icon="file" color="indigo" />
      <StatsCard title="Emesse" :value="k.issued" icon="check" color="emerald" />
      <StatsCard title="Bozze" :value="k.draft" icon="draft" color="amber" />
      <StatsCard title="Da incassare (€)" :value="k.outstanding.toFixed(2)" icon="alert" color="rose" />
    </div>

    <!-- Charts row -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
      <SectionCard title="Stato fatture">
        <InvoicesStatusRadial :loading="loading" :labels="radialLabels" :series="radialSeries" />
      </SectionCard>

      <SectionCard title="Andamento (ultimi 30 giorni)">
        <InvoicesMonthlyChart :loading="loading" :categories="areaCategories" :series="areaSeries" />
      </SectionCard>
    </div>

    <!-- Lists row -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
   <SectionCard title="Ultime fatture">
  <RecentInvoicesList :limit="5" />
</SectionCard>

   <SectionCard title="Fatture in scadenza (10 gg)">
  <UpcomingDue :limit="5" />
</SectionCard>

    </div>

    <!-- Distribuzione / Top clienti -->
  <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
      <SectionCard title="Distribuzione clienti B2B / B2C">
        <!-- 👇 passa i dati veri -->
        <ClientsDistribution :loading="loading" :counts="countsClients" />
      </SectionCard>

      <SectionCard title="Top clienti per fatturato (90 gg)">
        <TopClientsBar :loading="loading" :items="topCustomers" />
      </SectionCard>
    </div>
  </section>
</template>


<script setup>
definePageMeta({ layout: 'default' })

import StatsCard from '@/components/Dashboard/StatsCard.vue'
import SectionCard from '@/components/Dashboard/SectionCard.vue'
import InvoicesStatusRadial from '@/components/Dashboard/InvoicesStatusRadial.vue'
import InvoicesMonthlyChart from '@/components/Dashboard/InvoicesMonthlyChart.vue'
import RecentInvoicesList from '@/components/Dashboard/RecentInvoicesList.vue'
import UpcomingDue from '@/components/Dashboard/UpcomingDue.vue'
import ClientsDistribution from '@/components/Dashboard/ClientsDistribution.vue'
import TopClientsBar from '@/components/Dashboard/TopClientsBar.vue'

import { useDashboardStats } from '@/composables/useDashboardStats'

const { kpi, series, topCustomers, clientsDistribution, loading, error, refreshAll } = useDashboardStats()

const k = computed(() => {
  const c = kpi.value?.counts || {}
  const a = kpi.value?.amounts || {}
  return {
    totalInvoices: c.total || 0,
    issued: c.issued || 0,
    draft: c.draft || 0,
    cancelled: c.cancelled || 0,
    paidCount: c.paid || 0,
    revenueTotal: a.total || 0,
    revenuePaid: a.paid || 0,
    outstanding: a.outstanding || 0
  }
})

const radialLabels = ['Emesse', 'Bozze', 'Annullate']
const radialSeries = computed(() => [k.value.issued, k.value.draft, k.value.cancelled])

const areaCategories = computed(() => (series.value || []).map(d => d.date))
const areaSeries = computed(() => ([
  { name: 'Emesso', data: (series.value || []).map(d => d.total) },
  { name: 'Pagato', data: (series.value || []).map(d => d.paid) }
]))

// 👇 mappa per ClientsDistribution
const countsClients = computed(() => ({
  b2b: Number(clientsDistribution.value?.b2b || 0),
  b2c: Number(clientsDistribution.value?.b2c || 0)
}))

function doRefresh () {
  refreshAll({ kpiRange: {}, tsDays: 30, topCfg: { limit: 5, days: 90 } })
}

onMounted(doRefresh)
</script>
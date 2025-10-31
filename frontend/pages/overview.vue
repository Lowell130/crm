<template>
  <section class="p-4 space-y-6">
    <!-- Header -->
    <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-3">
      <h1 class="text-2xl font-semibold text-gray-900">Overview</h1>
      <div class="flex flex-wrap gap-2">
        <button class="px-3 py-2 text-sm rounded-lg border hover:bg-gray-50">Aggiorna</button>
        <button class="px-3 py-2 text-sm rounded-lg bg-blue-600 text-white hover:bg-blue-700">Esporta</button>
      </div>
    </div>

    <!-- KPI row -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      <StatsCard title="Totale clienti" :value="0" icon="users" color="blue" />
      <StatsCard title="Fatture totali" :value="0" icon="file" color="indigo" />
      <StatsCard title="Pagate (mese)" :value="0" icon="check" color="emerald" />
      <StatsCard title="Da incassare" :value="0" icon="alert" color="amber" />
    </div>

    <!-- Charts row -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
      <SectionCard title="Stato fatture">
        <InvoicesStatusRadial />
      </SectionCard>

      <SectionCard title="Andamento mensile fatturato">
        <InvoicesMonthlyChart />
      </SectionCard>
    </div>

    <!-- Lists row -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
      <SectionCard title="Ultime fatture">
        <RecentInvoicesList />
      </SectionCard>

      <SectionCard title="Fatture in scadenza (10 gg)">
        <UpcomingDue />
      </SectionCard>
    </div>

    <!-- Distribution / Top clients -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
      <SectionCard title="Distribuzione clienti B2B / B2C">
        <ClientsDistribution />
      </SectionCard>

      <SectionCard title="Top clienti per fatturato">
        <TopClientsBar />
      </SectionCard>
    </div>
  </section>
</template>

<script setup>
definePageMeta({ layout: 'default' })

// === Import espliciti ===
import StatsCard from '@/components/Dashboard/StatsCard.vue'
import SectionCard from '@/components/Dashboard/SectionCard.vue'
import InvoicesStatusRadial from '@/components/Dashboard/InvoicesStatusRadial.vue'
import InvoicesMonthlyChart from '@/components/Dashboard/InvoicesMonthlyChart.vue'
import RecentInvoicesList from '@/components/Dashboard/RecentInvoicesList.vue'
import UpcomingDue from '@/components/Dashboard/UpcomingDue.vue'
import ClientsDistribution from '@/components/Dashboard/ClientsDistribution.vue'
import TopClientsBar from '@/components/Dashboard/TopClientsBar.vue'
</script>

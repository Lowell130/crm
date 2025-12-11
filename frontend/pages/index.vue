<template>
  <section class="relative overflow-hidden bg-white">
    <!-- Hero -->
    <div class="mx-auto max-w-screen-xl px-4 sm:px-6 lg:px-8 pt-24 pb-20">
      <div class="grid lg:grid-cols-2 gap-10 items-center">
        <!-- Text block -->
        <div>
          <h1 class="text-4xl sm:text-5xl font-extrabold leading-tight text-gray-900">
            Il tuo CRM <span class="text-primary-600">semplice</span> per clienti e fatture
          </h1>
          <p class="mt-6 text-gray-600 text-lg">
            Gestisci clienti B2B/B2C, emetti fatture, monitora incassi e KPI con dashboard pronta all’uso.
          </p>

          <!-- CTA buttons -->
          <div class="mt-8 flex flex-wrap gap-3">
            <NuxtLink
              to="/register"
              class="inline-flex items-center justify-center px-5 py-3 text-base font-medium text-center text-white bg-primary-600 rounded-lg hover:bg-primary-700 focus:ring-4 focus:ring-primary-300"
            >
              Inizia gratis
            </NuxtLink>

            <NuxtLink
              to="/login"
              class="inline-flex items-center justify-center px-5 py-3 text-base font-medium text-gray-900 bg-white border border-gray-300 rounded-lg hover:bg-gray-100 focus:ring-4 focus:ring-gray-200"
            >
              Accedi
            </NuxtLink>
          </div>

          <p class="mt-4 text-sm text-gray-500">
            Nessuna carta richiesta. Disdici quando vuoi.
          </p>
        </div>

        <!-- Mockup Preview -->
        <div class="relative">
          <div class="rounded-2xl border border-gray-200 shadow-lg overflow-hidden">
            <div class="bg-gray-900 text-gray-50 px-4 py-2 text-xs font-mono">overview.vue — dashboard</div>
            <div class="p-6 bg-gray-50">
              <div class="grid grid-cols-2 gap-3">
                <div class="h-20 rounded-lg bg-gray-200" />
                <div class="h-20 rounded-lg bg-gray-200" />
                <div class="h-24 col-span-2 rounded-lg bg-gray-200" />
                <div class="h-24 col-span-2 rounded-lg bg-gray-200" />
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Features -->
      <div class="mt-20 grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
        <div class="p-6 bg-white border border-gray-200 rounded-xl shadow-sm hover:shadow transition-shadow">
          <h3 class="text-lg font-semibold text-gray-900">Clienti B2B/B2C</h3>
          <p class="mt-2 text-sm text-gray-600">Rubrica unica con campi dedicati, ricerca full-text e filtri.</p>
        </div>
        <div class="p-6 bg-white border border-gray-200 rounded-xl shadow-sm hover:shadow transition-shadow">
          <h3 class="text-lg font-semibold text-gray-900">Fatture & Pagamenti</h3>
          <p class="mt-2 text-sm text-gray-600">Emetti, marca come pagate, monitora scadenze in un click.</p>
        </div>
        <div class="p-6 bg-white border border-gray-200 rounded-xl shadow-sm hover:shadow transition-shadow">
          <h3 class="text-lg font-semibold text-gray-900">Dashboard KPI</h3>
          <p class="mt-2 text-sm text-gray-600">Grafici su stato fatture, incassato e outstanding.</p>
        </div>
      </div>
    </div>

    <!-- Final CTA -->
    <div class="bg-primary-50 border-t mt-16">
      <div class="mx-auto max-w-screen-xl px-4 sm:px-6 lg:px-8 py-12 flex flex-col sm:flex-row items-center justify-between gap-6">
        <p class="text-lg font-medium text-primary-900">Pronto a partire? Crea il tuo account in 30 secondi.</p>
        <NuxtLink
          to="/register"
          class="inline-flex items-center justify-center px-5 py-3 text-base font-medium text-white bg-primary-600 rounded-lg hover:bg-primary-700 focus:ring-4 focus:ring-primary-300"
        >
          Crea un account
        </NuxtLink>
      </div>
    </div>
  </section>
</template>

<script setup>
definePageMeta({ layout: 'marketing', public: true })
</script>

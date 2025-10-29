<template>
  <div class="min-h-screen bg-gray-50">
    <header class="flex items-center justify-between px-6 py-4 bg-white shadow">
      <h1 class="text-xl font-semibold">Clienti</h1>
      <NuxtLink
        to="/dashboard"
        class="px-3 py-2 rounded-xl border hover:bg-gray-100"
        >Dashboard</NuxtLink
      >
    </header>

    <main class="max-w-5xl mx-auto p-6">
      <div class="flex items-end gap-3 mb-4">
        <label class="text-sm">Filtro tipo:</label>
        <select v-model="kind" class="rounded-xl border px-3 py-2">
          <option value="">Tutti</option>
          <option value="B2B">B2B</option>
          <option value="B2C">B2C</option>
        </select>
        <button
          @click="load()"
          class="px-3 py-2 rounded-xl bg-blue-600 text-white"
        >
          Ricarica
        </button>
      </div>

      <div class="overflow-x-auto bg-white rounded-2xl shadow">
        <table class="min-w-full text-sm">
          <thead class="bg-gray-100">
            <tr>
              <th class="text-left p-3">ID</th>
              <th class="text-left p-3">Tipo</th>
              <th class="text-left p-3">Denominazione / Nome</th>
              <th class="text-left p-3">P.IVA / CF</th>
              <th class="text-left p-3">Email</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="c in customers" :key="c._id" class="border-t">
              <td class="p-3 font-mono">{{ c._id }}</td>
              <td class="p-3">{{ c.kind }}</td>
              <td class="p-3">
                <span v-if="c.kind === 'B2B'">{{ c.company_name }}</span>
                <span v-else>{{ c.first_name }} {{ c.last_name }}</span>
              </td>
              <td class="p-3">
                <span v-if="c.kind === 'B2B'">{{ c.vat_number }}</span>
                <span v-else>{{ c.codice_fiscale }}</span>
              </td>
              <td class="p-3">{{ c.email || "—" }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </main>
  </div>
</template>


<script setup>
const { apiFetch } = useApi();
const customers = ref([]);
const kind = ref("");
const loading = ref(false);
const error = ref("");

const load = async () => {
  loading.value = true;
  error.value = "";
  try {
    customers.value = await apiFetch("/customers", {
      query: {
        skip: 0,
        limit: 50,
        ...(kind.value ? { kind: kind.value } : {}),
      },
    });
  } catch (e) {
    error.value = e?.data?.detail || "Errore nel caricamento clienti";
  } finally {
    loading.value = false;
  }
};

// 👇 carica subito quando apri la pagina
onMounted(load);

// 👇 ricarica automaticamente quando cambi filtro
watch(kind, () => load());
</script>

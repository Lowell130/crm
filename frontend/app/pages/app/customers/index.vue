<template>
  <div>
    <PageHeader title="Clienti" />
    <div class="mt-4 flex flex-wrap gap-2 items-end">
      <input v-model="q" class="rounded-lg border-gray-300" placeholder="Cerca nome/email/telefono..." />
      <select v-model="customer_type" class="rounded-lg border-gray-300">
        <option value="">Tutti</option>
        <option value="B2C">B2C</option>
        <option value="B2B">B2B</option>
      </select>
      <input v-model="tag" class="rounded-lg border-gray-300" placeholder="Tag" />
      <button @click="refresh" class="px-4 py-2 rounded-lg bg-gray-100 dark:bg-gray-800">Filtra</button>
      <div class="ml-auto flex gap-2">
        <NuxtLink to="/app/exports" class="px-3 py-2 rounded bg-emerald-600 text-white">Esporta</NuxtLink>
      </div>
    </div>

    <div class="mt-4 overflow-x-auto">
      <table class="min-w-full text-sm">
        <thead class="text-left text-gray-500">
          <tr>
            <th class="py-2">Nome</th>
            <th>Email</th>
            <th>Tipo</th>
            <th>Tag</th>
            <th>Registrato</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="c in customers" :key="c._id" class="border-t">
            <td class="py-2">{{ c.name }}</td>
            <td>{{ c.email || '—' }}</td>
            <td><span class="px-2 py-0.5 rounded-full text-xs" :class="c.customer_type==='B2B'?'bg-purple-100':'bg-blue-100'">{{ c.customer_type }}</span></td>
            <td>
              <span v-for="t in c.tags" :key="t" class="mr-1 px-2 py-0.5 rounded-full bg-gray-100 text-xs">{{ t }}</span>
            </td>
            <td>{{ new Date(c.registered_at).toLocaleDateString() }}</td>
            <td class="text-right">
              <NuxtLink :to="`/app/customers/${c._id}`" class="text-blue-600">Apri</NuxtLink>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="mt-4 flex items-center gap-2">
      <button :disabled="skip===0" @click="prev" class="px-3 py-1 rounded bg-gray-100">Prev</button>
      <span>Page {{ Math.floor(skip/limit)+1 }}</span>
      <button @click="next" class="px-3 py-1 rounded bg-gray-100">Next</button>
    </div>
  </div>
</template>

<script setup>
definePageMeta({ layout: 'dashboard' })

const q = ref('')
const customer_type = ref('')
const tag = ref('')
const skip = ref(0)
const limit = ref(20)

const { list } = useCustomers()

const { data, refresh } = await useAsyncData('customers:list', () => list({
  q: q.value || undefined,
  customer_type: customer_type.value || undefined,
  tag: tag.value || undefined,
  sort: 'registered_at,desc',
  skip: skip.value,
  limit: limit.value
}), { watch: [q, customer_type, tag, skip, limit] })

const customers = computed(() => data.value || [])

function next(){ skip.value += limit.value }
function prev(){ skip.value = Math.max(0, skip.value - limit.value) }
</script>

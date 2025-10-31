<template>
  <div
    class="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-4 flex items-center gap-4"
  >
    <div :class="['w-10 h-10 rounded-full flex items-center justify-center text-white',
                  colorClass]">
      <span class="text-sm font-bold uppercase">{{ iconLetter }}</span>
    </div>
    <div class="flex-1">
      <div class="text-sm text-gray-500 dark:text-gray-400">{{ title }}</div>
      <div class="text-2xl font-semibold text-gray-900 dark:text-white">{{ value }}</div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  title: { type: String, default: '' },
  value: { type: [String, Number], default: 0 },
  icon:  { type: String, default: 'dot' },
  color: { type: String, default: 'blue' } // blue | indigo | emerald | amber ...
})

const colorClass = computed(() => ({
  blue: 'bg-blue-600',
  indigo: 'bg-indigo-600',
  emerald: 'bg-emerald-600',
  amber: 'bg-amber-600',
  rose: 'bg-rose-600'
}[props.color] || 'bg-gray-600'))

const iconLetter = computed(() => (props.icon?.[0] || '•').toUpperCase())
</script>

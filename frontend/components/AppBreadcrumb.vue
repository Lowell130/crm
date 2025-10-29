<template>
  <nav class="flex" aria-label="Breadcrumb">
    <ol class="inline-flex items-center space-x-1 md:space-x-2 rtl:space-x-reverse">
      <li
        v-for="(item, idx) in normalizedItems"
        :key="idx"
        class="inline-flex items-center"
        :aria-current="item.current ? 'page' : undefined"
      >
        <!-- Separator (skip first) -->
        <template v-if="idx !== 0">
          <svg
            class="rtl:rotate-180 w-3 h-3 text-gray-400 mx-1"
            aria-hidden="true"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 6 10"
          >
            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="m1 9 4-4-4-4"/>
          </svg>
        </template>

        <!-- Link VS testo corrente -->
        <component
          :is="item.current || !item.to ? 'span' : NuxtLink"
          v-bind="item.current || !item.to ? {} : { to: item.to }"
          class="inline-flex items-center text-sm font-medium"
          :class="item.current || !item.to
            ? 'text-gray-500'
            : 'text-gray-700 hover:text-blue-600'"
        >
          <!-- Icona opzionale (passata via item.icon = render fn o stringa 'home') -->
          <slot name="icon" :item="item">
            <svg
              v-if="item.icon === 'home'"
              class="w-3 h-3 me-2.5"
              aria-hidden="true"
              xmlns="http://www.w3.org/2000/svg"
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path
                d="m19.707 9.293-2-2-7-7a1 1 0 0 0-1.414 0l-7 7-2 2a1 1 0 0 0 1.414 1.414L2 10.414V18a2 2 0 0 0 2 2h3a1 1 0 0 0 1-1v-4a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v4a1 1 0 0 0 1 1h3a2 2 0 0 0 2-2v-7.586l.293.293a1 1 0 0 0 1.414-1.414Z"
              />
            </svg>
          </slot>

          <span class="truncate max-w-[28ch]" :title="item.label">{{ item.label }}</span>
        </component>
      </li>
    </ol>
  </nav>
</template>

<script setup>
const props = defineProps({
  /**
   * items: Array<{ label: string, to?: string|object, current?: boolean, icon?: 'home'|any }>
   * - label: testo mostrato
   * - to: route path/string o oggetto { name, params, query }
   * - current: se true, è l'ultimo elemento non cliccabile
   * - icon: opzionale ('home' per l’icona home built-in)
   */
  items: { type: Array, required: true }
})

const NuxtLink = resolveComponent('NuxtLink')

// fallback di sicurezza: rimuovi elementi vuoti, marca l'ultimo come current se nessuno lo è
const normalizedItems = computed(() => {
  const list = (props.items || []).filter(Boolean)
  if (!list.some(i => i?.current) && list.length) {
    list[list.length - 1] = { ...list[list.length - 1], current: true, to: undefined }
  }
  return list
})
</script>

<template>
  <div class="relative">
    <button
      ref="btn"
      @click="open = !open"
      class="w-full md:w-auto flex items-center justify-center py-2 px-4 text-sm font-medium text-gray-900 bg-white rounded-full border border-gray-200 hover:bg-gray-100 hover:text-primary-700"
      type="button"
    >
      Filtra
    </button>

    <div
      v-show="open"
      ref="panel"
      @click.stop
      class="absolute right-0 mt-2 z-10 w-56 p-3 bg-white rounded-lg shadow"
    >
      <h6 class="mb-3 text-sm font-medium text-gray-900">Tipo cliente</h6>
      <ul class="space-y-2 text-sm">
        <li class="flex items-center">
          <input id="flt-all" type="radio" value="" v-model="localKind" class="w-4 h-4 bg-gray-100 border-gray-300 rounded text-primary-600 focus:ring-primary-500">
          <label for="flt-all" class="ml-2 text-sm font-medium text-gray-900">Tutti</label>
        </li>
        <li class="flex items-center">
          <input id="flt-b2b" type="radio" value="B2B" v-model="localKind" class="w-4 h-4 bg-gray-100 border-gray-300 rounded text-primary-600 focus:ring-primary-500">
          <label for="flt-b2b" class="ml-2 text-sm font-medium text-gray-900">B2B</label>
        </li>
        <li class="flex items-center">
          <input id="flt-b2c" type="radio" value="B2C" v-model="localKind" class="w-4 h-4 bg-gray-100 border-gray-300 rounded text-primary-600 focus:ring-primary-500">
          <label for="flt-b2c" class="ml-2 text-sm font-medium text-gray-900">B2C</label>
        </li>
      </ul>

      <div class="flex justify-end mt-3 gap-2">
       <button
  @click="onReset"
  class="flex items-center justify-center w-10 h-10 rounded-full bg-red-700 hover:bg-red-800 focus:ring-4 focus:ring-red-300"
>
  <svg
    class="w-5 h-5 text-white"
    xmlns="http://www.w3.org/2000/svg"
    fill="none"
    viewBox="0 0 24 24"
    stroke="currentColor"
    stroke-width="2"
  >
    <path
      stroke-linecap="round"
      stroke-linejoin="round"
      d="M17.651 7.65a7.131 7.131 0 0 0-12.68 3.15M18.001 4v4h-4m-7.652 8.35a7.13 7.13 0 0 0 12.68-3.15M6 20v-4h4"
    />
  </svg>
</button>

        <button class="px-3 py-2 text-xs text-white bg-green-700 rounded-full" @click="onApply">Applica</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onClickOutside } from '@vueuse/core'

const props = defineProps({ modelValue: { type: String, default: '' } })
const emit = defineEmits(['update:modelValue','apply','reset'])

const open = ref(false)
const panel = ref(null)
const btn = ref(null)
const localKind = ref(props.modelValue)

// sincronia quando cambia dall'esterno
watch(() => props.modelValue, v => { localKind.value = v })

// chiudi se clic fuori (ma non sul bottone)
onClickOutside(panel, (e) => {
  if (btn.value && e.target instanceof Element && btn.value.contains(e.target)) return
  open.value = false
})

function onApply() {
  emit('update:modelValue', localKind.value)
  emit('apply')
  open.value = false
}
function onReset() {
  localKind.value = ''
  emit('update:modelValue', '')
  emit('reset')
}
</script>

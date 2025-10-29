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
        <button class="px-3 py-2 text-xs text-white bg-red-700 rounded-full" @click="onReset">Reset</button>
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

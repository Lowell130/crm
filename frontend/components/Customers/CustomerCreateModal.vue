<template>
  <Transition name="fade">
    <div v-if="open" class="fixed inset-0 z-50 flex items-center justify-center" role="dialog" aria-modal="true" @keydown.esc="$emit('close')">
      <!-- backdrop -->
      <div class="fixed inset-0 bg-black/40" @click="$emit('close')"></div>

      <!-- dialog -->
      <div ref="dialog" class="relative p-4 w-full max-w-2xl max-h-[90vh] overflow-y-auto overscroll-contain bg-white rounded-lg shadow sm:p-5 hide-scrollbar outline-none" tabindex="-1">
        <div class="flex justify-between items-center pb-4 mb-4">
          <h3 class="text-lg font-semibold text-gray-900">Aggiungi cliente</h3>
          <button type="button" class="text-gray-400 hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm p-1.5" @click="$emit('close')">
            <svg class="w-5 h-5" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"/>
            </svg>
          </button>
        </div>

        <CustomerForm :kindDefault="'B2C'" @created="$emit('created')" @cancel="$emit('close')" />
      </div>
    </div>
  </Transition>
</template>

<script setup>
const props = defineProps({ open: { type: Boolean, default: false } })
defineEmits(['close','created'])

const { lockScroll, unlockScroll } = useModalScrollLock()

watch(() => props.open, (v) => v ? lockScroll() : unlockScroll())
onBeforeUnmount(unlockScroll)
</script>

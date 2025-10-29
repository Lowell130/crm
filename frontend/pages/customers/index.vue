<template>
  <div class="p-4 text-sm text-gray-600">Sezione clienti</div>
</template>

<script setup>
definePageMeta({ layout: 'default' })
// Se per ora non hai una lista, puoi anche reindirizzare:
const router = useRouter()
onMounted(() => {
  // manda alla dashboard o dove preferisci
  router.replace('/dashboard')
})
</script>

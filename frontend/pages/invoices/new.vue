<template>
  <InvoiceForm mode="create" @saved="onSaved"/>
</template>

<script setup>
import InvoiceForm from '@/components/Invoices/InvoiceForm.vue'
function onSaved(){ /* opzionale */ }
</script>

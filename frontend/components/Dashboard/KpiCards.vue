<script setup>
const props = defineProps({
  loading: { type: Boolean, default: false },
  data: {
    type: Object,
    default: () => ({
      totalInvoices: 0, issued: 0, draft: 0, cancelled: 0,
      paidCount: 0, revenueTotal: 0, revenuePaid: 0, outstanding: 0
    })
  }
})
</script>

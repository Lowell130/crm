export function useStats() {
  const { $api } = useNuxtApp()

  const summary = async () => $api('/stats/summary')
  const activeByMonth = async () => $api('/stats/active-by-month')

  return { summary, activeByMonth }
}

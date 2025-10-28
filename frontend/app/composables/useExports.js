export function useExports() {
  const { $api } = useNuxtApp()

  async function download(path, filename) {
    const res = await $api.raw(path, { responseType: 'blob' })
    const blob = await res._data
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = filename
    a.click()
    URL.revokeObjectURL(url)
  }

  const downloadCsv = () => download('/exports/customers.csv', 'customers.csv')
  const downloadXlsx = () => download('/exports/customers.xlsx', 'customers.xlsx')

  return { downloadCsv, downloadXlsx }
}

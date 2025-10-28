export function useCustomers() {
  const {$api} = useNuxtApp()

  const list = async (params = {}) => $api('/customers', { query: params })
  const get = async (id) => $api(`/customers/${id}`)
  const create = async (payload) => $api('/customers', { method: 'POST', body: payload })
  const update = async (id, payload) => $api(`/customers/${id}`, { method: 'PATCH', body: payload })
  const remove = async (id) => $api(`/customers/${id}`, { method: 'DELETE' })
  const uploadFile = async (id, file) => {
    const fd = new FormData()
    fd.append('file', file)
    return $api(`/customers/${id}/files`, { method: 'POST', body: fd })
  }

  return { list, get, create, update, remove, uploadFile }
}

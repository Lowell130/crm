// Stack di toast semplice (push + auto-dismiss + dismiss)
export function useToasts() {
  const toasts = reactive([]) // { id, title?, message, onRetry? }
  let seq = 1

  function pushToast({ title, message, onRetry } = {}) {
    const id = seq++
    toasts.push({ id, title, message, onRetry })
    // autodismiss dopo 5s
    setTimeout(() => dismissToast(id), 5000)
    return id
  }

  function dismissToast(id) {
    const i = toasts.findIndex(t => t.id === id)
    if (i !== -1) toasts.splice(i, 1)
  }

  return { toasts, pushToast, dismissToast }
}

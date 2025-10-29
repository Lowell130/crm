// Lock/unlock dello scroll del body (compensa la scrollbar per evitare "salti")
export function useModalScrollLock() {
  let bodyOriginalPaddingRight = ''

  const getScrollbarWidth = () => {
    const sc = document.createElement('div')
    sc.style.visibility = 'hidden'
    sc.style.overflow = 'scroll'
    sc.style.position = 'absolute'
    sc.style.top = '-9999px'
    sc.style.width = '100px'
    document.body.appendChild(sc)
    const inner = document.createElement('div')
    inner.style.width = '100%'
    sc.appendChild(inner)
    const width = sc.offsetWidth - inner.offsetWidth
    sc.parentNode?.removeChild(sc)
    return width
  }

  const lockScroll = () => {
    const sw = getScrollbarWidth()
    bodyOriginalPaddingRight = document.body.style.paddingRight || ''
    if (sw > 0) document.body.style.paddingRight = `${sw}px`
    document.body.classList.add('body-lock')
  }

  const unlockScroll = () => {
    document.body.classList.remove('body-lock')
    document.body.style.paddingRight = bodyOriginalPaddingRight
  }

  onBeforeUnmount(unlockScroll)

  return { lockScroll, unlockScroll }
}

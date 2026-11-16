export function setPageMeta(title: string, description: string, robots = 'index, follow') {
  document.title = `${title} | Radar Cultural`
  const canonical = new URL(window.location.pathname, 'https://radarcultural.mx').href
  const values: Record<string, string> = {
    'meta[name="description"]': description,
    'meta[name="robots"]': robots,
    'meta[property="og:title"]': document.title,
    'meta[property="og:description"]': description,
    'meta[property="og:url"]': canonical,
    'meta[name="twitter:title"]': document.title,
    'meta[name="twitter:description"]': description,
  }
  for (const [selector, value] of Object.entries(values)) {
    document.querySelector(selector)?.setAttribute('content', value)
  }
  document.querySelector('link[rel="canonical"]')?.setAttribute('href', canonical)
}

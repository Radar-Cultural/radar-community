export function formatEventDate(value: string, timeZone: string | null, style: 'long' | 'full') {
  const zone = timeZone || 'UTC'
  const locale = navigator.language || 'es-MX'
  const options: Intl.DateTimeFormatOptions = {
    dateStyle: style,
    timeStyle: 'short',
    timeZone: zone,
  }
  try {
    return `${new Intl.DateTimeFormat(locale, options).format(new Date(value))} · ${zone}`
  } catch (error) {
    if (!(error instanceof RangeError)) throw error
    return `${new Intl.DateTimeFormat(locale, { ...options, timeZone: 'UTC' }).format(new Date(value))} · UTC`
  }
}

export function formatEventTeaserDate(value: string, timeZone: string | null) {
  const options: Intl.DateTimeFormatOptions = {
    day: 'numeric',
    month: 'short',
    year: 'numeric',
    timeZone: timeZone || 'UTC',
  }
  try {
    return new Intl.DateTimeFormat('es-MX', options).format(new Date(value))
  } catch (error) {
    if (!(error instanceof RangeError)) throw error
    return new Intl.DateTimeFormat('es-MX', { ...options, timeZone: 'UTC' }).format(new Date(value))
  }
}

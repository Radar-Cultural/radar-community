export interface PaginatedResponse<T> {
  count: number
  next: string | null
  previous: string | null
  results: T[]
}

export interface CulturalCategory {
  id: string
  name: string
  slug: string
  description: string
}

export interface CulturalPlace {
  id: string
  name: string
  slug: string
  kind: string
  address: string
  locality: string
  region: string
  country_code: string
  latitude: string | null
  longitude: string | null
  same_as: string | null
}

export interface CulturalOrganization {
  id: string
  name: string
  slug: string
  description: string
  website: string | null
  same_as: string[]
  verified: true
}

export interface EventScheduleItem {
  title: string
  starts_at: string
  ends_at: string | null
  position: number
}

export interface CulturalEvent {
  id: string
  slug: string
  title: string
  summary: string
  description: string
  language_code: string | null
  time_zone: string | null
  starts_at: string
  ends_at: string | null
  event_status: 'EventScheduled' | 'EventCancelled' | 'EventPostponed' | 'EventRescheduled'
  attendance_mode:
    'OfflineEventAttendanceMode' | 'OnlineEventAttendanceMode' | 'MixedEventAttendanceMode'
  admission_type: 'free' | 'paid'
  admission_options: Array<{
    name: string
    price: string | number
    price_currency: string
    url?: string
  }>
  place: CulturalPlace | null
  location_details: string
  online_url: string | null
  organizer: CulturalOrganization | { name: string }
  categories: CulturalCategory[]
  audiences: CulturalCategory[]
  schedule: EventScheduleItem[]
  links: Array<{ label: string; url: string }>
  image: {
    url: string
    license: 'CC0-1.0' | 'CC-BY-4.0' | 'CC-BY-SA-4.0'
    credit: string
    source_url: string
  } | null
  source_url: string
  description_license: 'CC0-1.0' | 'permission-recorded'
  license_url: string | null
  schema_url: string
  rdf_url: string
  calendar_url: string
  updated_at: string
}

export interface EventQuery {
  q?: string
  category?: string
  audience?: string
  place?: string
  organizer?: string
  from?: string
  not_finished_at?: string
  to?: string
  updated_since?: string
  status?: CulturalEvent['event_status']
  has_image?: boolean
  attendance_mode?: CulturalEvent['attendance_mode']
  ordering?: 'starts_at' | '-starts_at' | 'updated_at' | '-updated_at'
  page?: number
  page_size?: number
}

export class RadarApiError extends Error {
  constructor(
    message: string,
    readonly status: number,
    readonly details: unknown,
  ) {
    super(message)
    this.name = 'RadarApiError'
  }
}

const API_ROOT = '/api/v1'

async function requestJson<T>(path: string, signal?: AbortSignal): Promise<T> {
  const response = await fetch(`${API_ROOT}${path}`, {
    headers: { Accept: 'application/json' },
    signal,
  })
  const contentType = response.headers.get('content-type') ?? ''
  const body: unknown = contentType.includes('json') ? await response.json() : await response.text()
  if (!response.ok) {
    throw new RadarApiError('Radar Cultural no pudo completar la solicitud.', response.status, body)
  }
  return body as T
}

function queryString(query: EventQuery): string {
  const params = new URLSearchParams()
  for (const [key, value] of Object.entries(query)) {
    if (value !== undefined && value !== '') params.set(key, String(value))
  }
  const encoded = params.toString()
  return encoded ? `?${encoded}` : ''
}

export function listEvents(query: EventQuery = {}, signal?: AbortSignal) {
  return requestJson<PaginatedResponse<CulturalEvent>>(`/events/${queryString(query)}`, signal)
}

export function getEvent(slug: string, signal?: AbortSignal) {
  return requestJson<CulturalEvent>(`/events/${encodeURIComponent(slug)}/`, signal)
}

export function listCategories(signal?: AbortSignal) {
  return requestJson<PaginatedResponse<CulturalCategory>>('/categories/', signal)
}

export function listAudiences(signal?: AbortSignal) {
  return requestJson<PaginatedResponse<CulturalCategory>>('/audiences/', signal)
}

export function listPlaces(signal?: AbortSignal) {
  return requestJson<PaginatedResponse<CulturalPlace>>('/places/', signal)
}

export function listOrganizations(signal?: AbortSignal) {
  return requestJson<PaginatedResponse<CulturalOrganization>>('/organizations/', signal)
}

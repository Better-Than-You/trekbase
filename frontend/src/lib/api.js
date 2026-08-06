const BASE = '/api'

async function request(endpoint, options = {}) {
  const token = localStorage.getItem('trekbase_token')
  const headers = { 'Content-Type': 'application/json', ...options.headers }
  if (token) headers['Authorization'] = `Bearer ${token}`

  const res = await fetch(`${BASE}${endpoint}`, { ...options, headers })
  const data = await res.json()

  if (!res.ok) throw new Error(data.error || 'Request failed')
  return data
}

export function login(email, password) {
  return request('/auth/login', {
    method: 'POST',
    body: JSON.stringify({ email, password }),
  })
}

export function register(name, email, password) {
  return request('/auth/register', {
    method: 'POST',
    body: JSON.stringify({ name, email, password }),
  })
}

export function getProfile() {
  return request('/auth/profile')
}

export function getAdminDashboard() {
  return request('/admin/dashboard')
}

export function getAdminUsers() {
  return request('/admin/users')
}

export function addUser(name, email, password) {
  return request('/admin/users', {
    method: 'POST',
    body: JSON.stringify({ name, email, password }),
  })
}

export function getAdminStaff() {
  return request('/admin/staff')
}

export function addStaff(name, contact, email, password) {
  return request('/admin/staff', {
    method: 'POST',
    body: JSON.stringify({ name, contact, email, password }),
  })
}

export function getUserDetail(userId) {
  return request(`/admin/users/${userId}`)
}

export function updateUser(userId, payload) {
  return request(`/admin/users/${userId}`, {
    method: 'PUT',
    body: JSON.stringify(payload),
  })
}

export function deleteUser(userId) {
  return request(`/admin/users/${userId}`, { method: 'DELETE' })
}

export function getStaffDetail(staffId) {
  return request(`/admin/staff/${staffId}`)
}

export function updateStaff(staffId, payload) {
  return request(`/admin/staff/${staffId}`, {
    method: 'PUT',
    body: JSON.stringify(payload),
  })
}

export function deleteStaff(staffId) {
  return request(`/admin/staff/${staffId}`, { method: 'DELETE' })
}

export function getAdminTreks() {
  return request('/admin/treks')
}

export function addTrek(payload) {
  return request('/admin/treks', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}

export function getTrekDetail(trekId) {
  return request(`/admin/treks/${trekId}`)
}

export function updateTrek(trekId, payload) {
  return request(`/admin/treks/${trekId}`, {
    method: 'PUT',
    body: JSON.stringify(payload),
  })
}

export function deleteTrek(trekId) {
  return request(`/admin/treks/${trekId}`, { method: 'DELETE' })
}

export function getUserDashboard() {
  return request('/user/dashboard')
}

export function searchTreks(q) {
  const query = q ? `?q=${encodeURIComponent(q)}` : ''
  return request(`/user/treks${query}`)
}

export function getMyBookings() {
  return request('/user/bookings')
}

export function bookTrek(trekId) {
  return request('/user/bookings', {
    method: 'POST',
    body: JSON.stringify({ trek_id: trekId }),
  })
}

export function cancelBooking(bookingId) {
  return request(`/user/bookings/${bookingId}`, { method: 'DELETE' })
}

export function updateProfile(name) {
  return request('/user/profile', {
    method: 'PUT',
    body: JSON.stringify({ name }),
  })
}

export function getStaffDashboard() {
  return request('/staff/dashboard')
}

export function getStaffTrek(trekId) {
  return request(`/staff/treks/${trekId}`)
}

export function updateStaffTrek(trekId, payload) {
  return request(`/staff/treks/${trekId}`, {
    method: 'PUT',
    body: JSON.stringify(payload),
  })
}

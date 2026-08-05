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

export function addStaff(name, contact, password) {
  return request('/admin/staff', {
    method: 'POST',
    body: JSON.stringify({ name, contact, password }),
  })
}

export function getUserDetail(userId) {
  return request(`/admin/users/${userId}`)
}

export function deleteUser(userId) {
  return request(`/admin/users/${userId}`, { method: 'DELETE' })
}

export function getStaffDetail(staffId) {
  return request(`/admin/staff/${staffId}`)
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

export function deleteTrek(trekId) {
  return request(`/admin/treks/${trekId}`, { method: 'DELETE' })
}

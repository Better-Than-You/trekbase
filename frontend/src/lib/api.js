import axios from 'axios'

const axiosInstance = axios.create({
  baseURL: '/api',
  headers: { 'Content-Type': 'application/json' },
})

// attach access token for each request
axiosInstance.interceptors.request.use((config) => {
  const token = localStorage.getItem('trekbase_token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

// if access token is expired create a new one using refresh_token
let refreshPromise = null

axiosInstance.interceptors.response.use(
  (response) => response,
  async (error) => {
    const original = error.config
    if (error.response?.status === 401) {
      original._retry = true
      try {
        refreshPromise =
          refreshPromise ||
          axios.post('/api/auth/refresh', null, {
            headers: { Authorization: `Bearer ${localStorage.getItem('trekbase_refresh_token')}` },
          })
        const { data } = await refreshPromise
        refreshPromise = null

        localStorage.setItem('trekbase_token', data.access_token)
        original.headers.Authorization = `Bearer ${data.access_token}`
        return axiosInstance(original)
      } catch (refreshError) {
        refreshPromise = null

        localStorage.removeItem('trekbase_token')
        localStorage.removeItem('trekbase_refresh_token')
        localStorage.removeItem('trekbase_user')
        window.location.href = '/auth/login'

        return Promise.reject(refreshError)
      }
    }

    // error handling msg for frontend
    error.message = error.response?.data?.error || error.message
    return Promise.reject(error)
  }
)

export function login(email, password) {
  return axiosInstance.post('/auth/login', { email, password }).then((r) => r.data)
}

export function register(name, email, password) {
  return axiosInstance.post('/auth/register', { name, email, password }).then((r) => r.data)
}

export function getProfile() {
  return axiosInstance.get('/auth/profile').then((r) => r.data)
}

export function getAdminDashboard() {
  return axiosInstance.get('/admin/dashboard').then((r) => r.data)
}

export function triggerReminders() {
  return axiosInstance.post('/admin/jobs/reminders').then((r) => r.data)
}

export function triggerMonthlyReport() {
  return axiosInstance.post('/admin/jobs/monthly-report').then((r) => r.data)
}

export function getAdminUsers(q) {
  return axiosInstance.get('/admin/users', { params: q ? { q } : undefined }).then((r) => r.data)
}

export function addUser(payload) {
  return axiosInstance.post('/admin/users', payload).then((r) => r.data)
}

export function blacklistUser(userId, isBlacklisted) {
  return axiosInstance.put(`/admin/users/${userId}/blacklist`, { is_blacklisted: isBlacklisted }).then((r) => r.data)
}

export function getAdminStaff(q) {
  return axiosInstance.get('/admin/staff', { params: q ? { q } : undefined }).then((r) => r.data)
}

export function blacklistStaff(staffId, isBlacklisted) {
  return axiosInstance.put(`/admin/staff/${staffId}/blacklist`, { is_blacklisted: isBlacklisted }).then((r) => r.data)
}

export function addStaff(name, contact, email, password) {
  return axiosInstance.post('/admin/staff', { name, contact, email, password }).then((r) => r.data)
}

export function getUserDetail(userId) {
  return axiosInstance.get(`/admin/users/${userId}`).then((r) => r.data)
}

export function updateUser(userId, payload) {
  return axiosInstance.put(`/admin/users/${userId}`, payload).then((r) => r.data)
}

export function deleteUser(userId) {
  return axiosInstance.delete(`/admin/users/${userId}`).then((r) => r.data)
}

export function getStaffDetail(staffId) {
  return axiosInstance.get(`/admin/staff/${staffId}`).then((r) => r.data)
}

export function updateStaff(staffId, payload) {
  return axiosInstance.put(`/admin/staff/${staffId}`, payload).then((r) => r.data)
}

export function deleteStaff(staffId) {
  return axiosInstance.delete(`/admin/staff/${staffId}`).then((r) => r.data)
}

export function getAdminTreks(q) {
  return axiosInstance.get('/admin/treks', { params: q ? { q } : undefined }).then((r) => r.data)
}

export function addTrek(payload) {
  return axiosInstance.post('/admin/treks', payload).then((r) => r.data)
}

export function getTrekDetail(trekId) {
  return axiosInstance.get(`/admin/treks/${trekId}`).then((r) => r.data)
}

export function updateTrek(trekId, payload) {
  return axiosInstance.put(`/admin/treks/${trekId}`, payload).then((r) => r.data)
}

export function deleteTrek(trekId) {
  return axiosInstance.delete(`/admin/treks/${trekId}`).then((r) => r.data)
}

export function getUserDashboard() {
  return axiosInstance.get('/user/dashboard').then((r) => r.data)
}

export function searchTreks(q) {
  return axiosInstance.get('/user/treks', { params: q ? { q } : undefined }).then((r) => r.data)
}

export function getMyBookings() {
  return axiosInstance.get('/user/bookings').then((r) => r.data)
}

export function bookTrek(trekId) {
  return axiosInstance.post('/user/bookings', { trek_id: trekId }).then((r) => r.data)
}

export function cancelBooking(bookingId) {
  return axiosInstance.delete(`/user/bookings/${bookingId}`).then((r) => r.data)
}

export function updateProfile(payload) {
  return axiosInstance.put('/user/profile', payload).then((r) => r.data)
}

export function triggerExportHistory() {
  return axiosInstance.post('/user/export-history').then((r) => r.data)
}

export function getExportHistoryStatus(taskId) {
  return axiosInstance.get(`/user/export-history/${taskId}`).then((r) => r.data)
}

export function getStaffDashboard() {
  return axiosInstance.get('/staff/dashboard').then((r) => r.data)
}

export function getStaffTrek(trekId) {
  return axiosInstance.get(`/staff/treks/${trekId}`).then((r) => r.data)
}

export function updateStaffTrek(trekId, payload) {
  return axiosInstance.put(`/staff/treks/${trekId}`, payload).then((r) => r.data)
}

export default axiosInstance
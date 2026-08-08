<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getUserDashboard, searchTreks, bookTrek, cancelBooking, triggerExportHistory, getExportHistoryStatus } from '@/lib/api'
import { state } from '@/store/auth'
import { difficultyBadge, statusBadge, bookingBadge } from '@/lib/badges'
import { toast } from 'vue3-toastify'
import 'vue3-toastify/dist/index.css'

const router = useRouter()

const availableTreks = ref([])
const bookings = ref([])
const searchResults = ref(null)
const query = ref('')
const exporting = ref(false)

onMounted(async () => {
  try {
    const data = await getUserDashboard()
    availableTreks.value = data.available_treks
    bookings.value = data.bookings
  } catch {
  }
})

async function handleExport() {
  if (!confirm('Export your booking history as CSV?')) return
  exporting.value = true
  let taskId
  try {
    const res = await triggerExportHistory()
    taskId = res.task_id
    toast.success('Export started. This may take a moment...', {
      position: toast.POSITION.BOTTOM_CENTER,
      autoClose: 3000,
    })
  } catch (e) {
    toast.error(e.message, {
      position: toast.POSITION.BOTTOM_CENTER,
      autoClose: 3000,
    })
    exporting.value = false
    return
  }

  // poll until the background job finishes
  const poll = async () => {
    try {
      const res = await getExportHistoryStatus(taskId)
      if (res.status === 'ready') {
        downloadCsv(res.csv_content, res.user_name)
        toast.success(`Export complete! Downloaded ${res.record_count} record(s).`, {
          position: toast.POSITION.BOTTOM_CENTER,
          autoClose: 5000,
        })
        exporting.value = false
        return
      }
      if (res.status === 'failed') {
        toast.error(res.error || 'Export failed', {
          position: toast.POSITION.BOTTOM_CENTER,
          autoClose: 5000,
        })
        exporting.value = false
        return
      }
      setTimeout(poll, 1500)
    } catch (e) {
      toast.error(e.message, {
        position: toast.POSITION.BOTTOM_CENTER,
        autoClose: 5000,
      })
      exporting.value = false
    }
  }
  poll()
}

function downloadCsv(content, userName) {
  const blob = new Blob([content], { type: 'text/csv;charset=utf-8;' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  const safe = (userName || 'user').replace(/[^a-z0-9]+/gi, '-').toLowerCase()
  a.href = url
  a.download = `trek-${safe}-history.csv`
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
}

async function doSearch() {
  try {
    const data = await searchTreks(query.value)
    searchResults.value = data.treks
  } catch (e) {
    alert(e.message)
  }
}

function clearSearch() {
  query.value = ''
  searchResults.value = null
}

async function handleBook(trekId) {
  if (!confirm('Book this trek?')) return
  try {
    await bookTrek(trekId)
    const data = await getUserDashboard()
    availableTreks.value = data.available_treks
    bookings.value = data.bookings
    searchResults.value = null
    query.value = ''
    alert('Trek booked')
  } catch (e) {
    alert(e.message)
  }
}

async function handleCancel(bookingId) {
  if (!confirm('Cancel this booking?')) return
  try {
    await cancelBooking(bookingId)
    const data = await getUserDashboard()
    bookings.value = data.bookings
    availableTreks.value = data.available_treks
  } catch (e) {
    alert(e.message)
  }
}

// format a db datetime string to dd-mm-yyyy hh:mm AM/PM
function formatDateTime(dt) {
  const d = new Date(dt)
  const options = { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit', hour12: true }
  return d.toLocaleString('en-US', options).replace(',', '')
}

</script>

<template>
  <div class="container py-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <div>
        <h4 class="fw-bold text-uppercase mb-0" style="letter-spacing: 0.04em;">My Dashboard</h4>
        <p class="text-secondary small mb-0">Welcome back, {{ state.user?.name }}</p>
      </div>
      <button @click="router.push('/user/history')" class="btn btn-outline-primary">
        <i class="bi bi-clock-history me-1"></i>History
      </button>
      <button class="btn btn-outline-success" :disabled="exporting" @click="handleExport">
        <i class="bi bi-download me-1"></i>{{ exporting ? 'Exporting...' : 'Export CSV' }}
      </button>
    </div>

    <div class="row g-3 mb-4">
        <div class="col-6 col-lg-6">
          <div class="card shadow-sm h-100">
            <div class="card-body d-flex align-items-center gap-3">
              <div class="d-inline-flex align-items-center justify-content-center p-3 rounded-3 bg-success text-white">
                <i class="bi bi-compass"></i>
              </div>
              <div>
                <div class="text-secondary text-uppercase small fw-semibold">Available treks</div>
                <div class="h3 mb-0 fw-bold">{{ availableTreks.length }}</div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-6 col-lg-6">
          <div class="card shadow-sm h-100">
            <div class="card-body d-flex align-items-center gap-3">
              <div class="d-inline-flex align-items-center justify-content-center p-3 rounded-3 bg-primary text-white">
                <i class="bi bi-ticket-perforated"></i>
              </div>
              <div>
                <div class="text-secondary text-uppercase small fw-semibold">Active bookings</div>
                <div class="h3 mb-0 fw-bold">{{ bookings.filter(b => b.status === 'booked').length }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="card shadow-sm mb-4">
        <div class="card-header bg-white py-3">
          <h6 class="mb-0 fw-bold">Find a Trek</h6>
        </div>
        <div class="card-body">
          <div class="input-group mb-3" style="max-width: 480px;">
            <span class="input-group-text bg-white"><i class="bi bi-search"></i></span>
            <input v-model="query" type="text" class="form-control" placeholder="Search by name or location"
                   @keyup.enter="doSearch">
            <button class="btn btn-primary" type="button" @click="doSearch">Search</button>
            <button v-if="searchResults" class="btn btn-outline-secondary" type="button" @click="clearSearch">
              <i class="bi bi-x-lg"></i>
            </button>
          </div>

          <div class="table-responsive">
            <table class="table table-hover align-middle mb-0">
              <thead class="table-light">
                <tr>
                  <th class="ps-3">#</th>
                  <th>Name</th>
                  <th>Location</th>
                  <th>Difficulty</th>
                  <th>Slots</th>
                  <th>Status</th>
                  <th class="pe-3 text-end"></th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="t in (searchResults || availableTreks)" :key="t.id">
                  <td class="ps-3 text-secondary">{{ t.id }}</td>
                  <td class="fw-semibold">{{ t.name }}</td>
                  <td class="text-secondary">{{ t.location }}</td>
                  <td><span class="badge rounded-pill fw-semibold" :class="difficultyBadge(t.difficulty)">{{ t.difficulty }}</span></td>
                  <td>{{ t.available_slots }}</td>
                  <td><span class="badge rounded-pill fw-semibold" :class="statusBadge(t.status)">{{ t.status }}</span></td>
                  <td class="pe-3 text-end">
                    <button class="btn btn-sm btn-primary" :disabled="t.available_slots <= 0" @click="handleBook(t.id)">
                      <i class="bi bi-check2-square me-1"></i>Book
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <div v-if="(searchResults || availableTreks).length === 0" class="text-center text-secondary py-5">
            <i class="bi bi-signpost-split fs-3 d-block mb-2"></i>
            <p class="mb-1 fw-semibold text-dark">No treks available right now</p>
            <p class="small mb-0">Check back soon, new routes are added regularly.</p>
          </div>
        </div>
      </div>

      <div class="card shadow-sm">
        <div class="card-header bg-white py-3">
          <h6 class="mb-0 fw-bold">My Bookings</h6>
        </div>
        <div class="card-body p-0">
          <div class="table-responsive">
            <table class="table table-hover align-middle mb-0">
              <thead class="table-light">
                <tr>
                  <th class="ps-3">#</th>
                  <th>Trek</th>
                  <th>Location</th>
                  <th>Status</th>
                  <th>Booked On</th>
                  <th class="pe-3 text-end"></th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="b in bookings" :key="b.id">
                  <td class="ps-3 text-secondary">{{ b.id }}</td>
                  <td class="fw-semibold">{{ b.trek?.name || '-' }}</td>
                  <td class="text-secondary">{{ b.trek?.location || '-' }}</td>
                  <td><span class="badge rounded-pill fw-semibold" :class="bookingBadge(b.status)">{{ b.status }}</span></td>
                  <td class="text-secondary">{{ formatDateTime(b.booking_date) }}</td>
                  <td class="pe-3 text-end">
                    <button v-if="b.status === 'booked'" class="btn btn-sm btn-outline-danger" @click="handleCancel(b.id)">
                      <i class="bi bi-x-circle me-1"></i>Cancel
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <div v-if="!bookings.length" class="text-center text-secondary py-5">
            <i class="bi bi-journal-x fs-3 d-block mb-2"></i>
            <p class="mb-1 fw-semibold text-dark">You have not booked a trek yet</p>
            <p class="small mb-0">Pick one from the list above to get started.</p>
          </div>
        </div>
      </div>
    </div>
</template>
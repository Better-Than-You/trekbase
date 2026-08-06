<script setup>
import { ref, onMounted } from 'vue'
import { getStaffDashboard, getStaffTrek, updateStaffTrek } from '@/lib/api'
import { state } from '@/store/auth'

const treks = ref([])

const editing = ref(null)
const slotsInput = ref('')
const statusInput = ref('')
const participants = ref([])
const showParticipants = ref(false)
const participantTrekName = ref('')

onMounted(async () => {
  try {
    const data = await getStaffDashboard()
    treks.value = data.treks
  } catch {
    treks.value = []
  }
})

function statusBadge(s) {
  return ({
    pending: 'bg-secondary', approved: 'bg-info text-dark', open: 'bg-success',
    closed: 'bg-secondary', completed: 'bg-primary',
  })[s] || 'bg-secondary'
}

function bookingBadge(s) {
  return ({ booked: 'bg-primary', cancelled: 'bg-danger', completed: 'bg-success' })[s] || 'bg-secondary'
}

function openEdit(t) {
  editing.value = t
  slotsInput.value = t.available_slots
  statusInput.value = t.status
}

function closeEdit() {
  editing.value = null
}

async function saveEdit() {
  try {
    const data = await updateStaffTrek(editing.value.id, {
      available_slots: slotsInput.value,
      status: statusInput.value,
    })
    editing.value = { ...editing.value, ...data.trek }
    const idx = treks.value.findIndex(t => t.id === editing.value.id)
    if (idx !== -1) treks.value[idx] = { ...treks.value[idx], ...data.trek }
  } catch {
  }
}

async function viewParticipants(t) {
  try {
    const data = await getStaffTrek(t.id)
    participants.value = data.trek.participants
    participantTrekName.value = data.trek.name
    showParticipants.value = true
  } catch (e) {
    alert(e.message)
  }
}
</script>

<template>
  <div class="container py-4">
    <h4 class="fw-bold text-uppercase mb-1" style="letter-spacing: 0.04em;">Staff Dashboard</h4>
    <p class="text-secondary small mb-4">Here are the treks assigned to you, {{ state.user?.name }}</p>

    <div class="row g-3 mb-4">
        <div class="col-12 col-md-4">
          <div class="card shadow-sm h-100">
            <div class="card-body d-flex align-items-center gap-3">
              <div class="d-inline-flex align-items-center justify-content-center p-3 rounded-3 bg-primary text-white">
                <i class="bi bi-compass"></i>
              </div>
              <div>
                <div class="text-secondary text-uppercase small fw-semibold">Assigned treks</div>
                <div class="h3 mb-0 fw-bold">{{ treks.length }}</div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-6 col-md-4">
          <div class="card shadow-sm h-100">
            <div class="card-body d-flex align-items-center gap-3">
              <div class="d-inline-flex align-items-center justify-content-center p-3 rounded-3 bg-success text-white">
                <i class="bi bi-people"></i>
              </div>
              <div>
                <div class="text-secondary text-uppercase small fw-semibold">Total participants</div>
                <div class="h3 mb-0 fw-bold">{{ treks.reduce((s, t) => s + (t.participants_count || 0), 0) }}</div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-6 col-md-4">
          <div class="card shadow-sm h-100">
            <div class="card-body d-flex align-items-center gap-3">
              <div class="d-inline-flex align-items-center justify-content-center p-3 rounded-3 bg-warning text-white">
                <i class="bi bi-calendar-check"></i>
              </div>
              <div>
                <div class="text-secondary text-uppercase small fw-semibold">Open treks</div>
                <div class="h3 mb-0 fw-bold">{{ treks.filter(t => t.status === 'open').length }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-if="treks.length === 0" class="alert alert-info">
        No treks assigned to you yet.
      </div>

      <div v-for="t in treks" :key="t.id" class="card shadow-sm mb-3">
        <div class="card-body">
          <div class="d-flex justify-content-between align-items-start flex-wrap gap-2">
            <div>
              <h5 class="fw-bold mb-1">{{ t.name }}</h5>
              <span class="text-secondary small">{{ t.location }} &middot; {{ t.duration_days }} days</span>
              <div class="mt-2 d-flex gap-2 flex-wrap">
                <span class="badge rounded-pill fw-semibold" :class="statusBadge(t.status)">{{ t.status }}</span>
                <span class="badge rounded-pill bg-body-secondary">{{ t.available_slots }} slots</span>
                <span class="badge rounded-pill bg-body-secondary">{{ t.participants_count }} registered</span>
              </div>
            </div>
            <div class="d-flex gap-2">
              <button class="btn btn-sm btn-outline-primary" @click="viewParticipants(t)">
                <i class="bi bi-people me-1"></i>Participants
              </button>
              <button class="btn btn-sm btn-primary" @click="openEdit(t)">
                <i class="bi bi-sliders me-1"></i>Manage
              </button>
            </div>
          </div>

          <div v-if="editing && editing.id === t.id" class="border-top pt-3 mt-3">
            <div class="row g-3">
              <div class="col-md-4">
                <label class="form-label small fw-semibold">Available Slots</label>
                <input v-model="slotsInput" type="number" min="0" class="form-control">
              </div>
              <div class="col-md-4">
                <label class="form-label small fw-semibold">Status</label>
                <select v-model="statusInput" class="form-select">
                  <option value="open">Open (Started)</option>
                  <option value="closed">Closed</option>
                  <option value="completed">Completed</option>
                </select>
              </div>
              <div class="col-md-4 d-flex align-items-end gap-2">
                <button class="btn btn-primary" @click="saveEdit">Save</button>
                <button class="btn btn-outline-secondary" @click="closeEdit">Cancel</button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-if="showParticipants" class="card shadow-sm mb-3">
        <div class="card-header bg-white py-3 d-flex justify-content-between align-items-center">
          <h6 class="mb-0 fw-bold">Participants &mdash; {{ participantTrekName }}</h6>
          <button class="btn btn-sm btn-outline-secondary" @click="showParticipants = false">
            <i class="bi bi-x-lg"></i>
          </button>
        </div>
        <div class="card-body p-0">
          <div class="table-responsive">
            <table class="table table-hover align-middle mb-0">
              <thead class="table-light">
                <tr>
                  <th class="ps-3">#</th>
                  <th>Name</th>
                  <th>Email</th>
                  <th class="pe-3 text-end">Booking Status</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="p in participants" :key="p.id">
                  <td class="ps-3 text-secondary">{{ p.id }}</td>
                  <td class="fw-semibold">{{ p.user?.name || '-' }}</td>
                  <td class="text-secondary">{{ p.user?.email || '-' }}</td>
                  <td class="pe-3 text-end"><span class="badge rounded-pill fw-semibold" :class="bookingBadge(p.status)">{{ p.status }}</span></td>
                </tr>
              </tbody>
            </table>
          </div>
          <div v-if="!participants.length" class="text-center text-secondary py-5">
            <i class="bi bi-people fs-3 d-block mb-2"></i>
            <p class="mb-1 fw-semibold text-dark">Nobody has booked this trek yet</p>
            <p class="small mb-0">Set the status to Open so trekkers can book it.</p>
          </div>
        </div>
      </div>
  </div>
</template>
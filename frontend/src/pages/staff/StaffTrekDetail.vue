<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getStaffTrek, updateStaffTrek } from '@/lib/api'
import { statusBadge, difficultyBadge, bookingBadge } from '@/lib/badges'
import { toast } from 'vue3-toastify'
import 'vue3-toastify/dist/index.css'

const route = useRoute()
const router = useRouter()

const trek = ref(null)
const notFound = ref(false)
const participantQuery = ref('')

const filteredParticipants = computed(() => {
  const q = participantQuery.value.trim().toLowerCase()
  const list = trek.value?.participants || []
  if (!q) return list
  // filter participants by name, email or booking status
  return list.filter(p =>
    p.user?.name?.toLowerCase().includes(q) ||
    p.user?.email?.toLowerCase().includes(q) ||
    p.status?.toLowerCase().includes(q)
  )
})

// manage form
const editing = ref(false)
const slotsInput = ref('')
const statusInput = ref('')
const saving = ref(false)

onMounted(async () => {
  await load()
})

async function load() {
  try {
    const id = Number(route.params.id)
    if (!id) {
      notFound.value = true
      return
    }
    const data = await getStaffTrek(id)
    if (!data.trek) {
      notFound.value = true
      return
    }
    trek.value = data.trek
  } catch {
    notFound.value = true
  }
}

function openEdit() {
  editing.value = true
  slotsInput.value = trek.value.available_slots
  statusInput.value = trek.value.status
}

function closeEdit() {
  editing.value = false
}

async function saveEdit() {
  if (saving.value) return
  saving.value = true
  try {
    const data = await updateStaffTrek(trek.value.id, {
      available_slots: slotsInput.value,
      status: statusInput.value,
    })
    trek.value = data.trek
    editing.value = false
    toast.success('Trek updated successfully', {
      position: toast.POSITION.BOTTOM_CENTER,
      autoClose: 3000,
    })
  } catch (e) {
    toast.error(e?.message || 'Failed to update trek', {
      position: toast.POSITION.BOTTOM_CENTER,
      autoClose: 3000,
    })
  } finally {
    saving.value = false
  }
}
</script>

<template>
  <div class="container py-4">
    <button type="button" class="btn btn-link btn-sm px-0 mb-3 text-secondary" @click="router.push('/staff/dashboard')">
      <i class="bi bi-arrow-left me-1"></i>Back to dashboard
    </button>

    <div v-if="notFound" class="alert alert-danger">Trek not found or you don't have access.</div>

    <template v-else-if="trek">
      <div class="mb-4">
        <h4 class="fw-bold text-uppercase mb-1" style="letter-spacing: 0.04em;">{{ trek.name }}</h4>
        <p class="text-secondary small mb-0">
          {{ trek.location }} &middot; {{ trek.duration_days }} days &middot; {{ trek.difficulty }}
        </p>
        <div class="mt-2 d-flex gap-2 flex-wrap">
          <span class="badge rounded-pill fw-semibold" :class="statusBadge(trek.status)">{{ trek.status }}</span>
          <span class="badge rounded-pill" :class="difficultyBadge(trek.difficulty)">{{ trek.difficulty }}</span>
          <span class="badge rounded-pill bg-secondary text-white">{{ trek.available_slots }} open slots</span>
          <span class="badge rounded-pill bg-secondary text-white">{{ trek.participants?.length || 0 }} registered</span>
        </div>
      </div>

      <!-- manage slots / status -->
      <div class="card shadow-sm mb-4">
        <div class="card-header bg-white py-3 d-flex justify-content-between align-items-center">
          <h6 class="mb-0 fw-bold">Manage trek</h6>
          <button v-if="!editing" type="button" class="btn btn-sm btn-outline-primary" @click="openEdit">
            <i class="bi bi-sliders me-1"></i>Edit
          </button>
        </div>
        <div class="card-body">
          <div v-if="!editing" class="row g-3">
            <div class="col-md-4">
              <div class="text-secondary text-uppercase small fw-semibold">Available slots</div>
              <div class="fs-5 fw-bold">{{ trek.available_slots }}</div>
            </div>
            <div class="col-md-4">
              <div class="text-secondary text-uppercase small fw-semibold">Status</div>
              <div class="fs-5 fw-bold">{{ trek.status }}</div>
            </div>
          </div>
          <div v-else class="row g-3">
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

      <!-- participants -->
      <div class="card shadow-sm">
        <div class="card-header bg-white py-3 d-flex align-items-center justify-content-between">
          <h6 class="mb-0 fw-bold"><i class="bi bi-people me-1"></i>Participants</h6>
          <div class="input-group input-group-sm" style="max-width: 320px;">
            <span class="input-group-text bg-white"><i class="bi bi-search"></i></span>
            <input v-model="participantQuery" type="text" class="form-control"
                   placeholder="Search by name, email or status">
          </div>
        </div>
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
              <tr v-for="p in filteredParticipants" :key="p.id">
                <td class="ps-3 text-secondary">{{ p.id }}</td>
                <td class="fw-semibold">{{ p.user?.name || '-' }}</td>
                <td class="text-secondary">{{ p.user?.email || '-' }}</td>
                <td class="pe-3 text-end">
                  <span class="badge rounded-pill fw-semibold" :class="bookingBadge(p.status)">{{ p.status }}</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <div v-if="!filteredParticipants.length" class="text-center text-secondary py-5">
          <i class="bi bi-people fs-3 d-block mb-2"></i>
          <p class="mb-1 fw-semibold text-dark">{{ filteredParticipants.length !== (trek.participants || []).length ? 'No participants match your search' : 'Nobody has booked this trek yet' }}</p>
          <p class="small mb-0">{{ filteredParticipants.length !== (trek.participants || []).length ? 'Try a different search term.' : 'Set the status to Open so trekkers can book it.' }}</p>
        </div>
      </div>
    </template>
  </div>
</template>
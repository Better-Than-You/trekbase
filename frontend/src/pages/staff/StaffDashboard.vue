<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getStaffDashboard } from '@/lib/api'
import { state } from '@/store/auth'
import { statusBadge } from '@/lib/badges'

const router = useRouter()
const treks = ref([])
const trekQuery = ref('')

const filteredTreks = computed(() => {
  const q = trekQuery.value.trim().toLowerCase()
  if (!q) return treks.value
  // filter assigned treks by name, location or status
  return treks.value.filter(t =>
    t.name?.toLowerCase().includes(q) ||
    t.location?.toLowerCase().includes(q) ||
    t.status?.toLowerCase().includes(q)
  )
})

onMounted(async () => {
  try {
    const data = await getStaffDashboard()
    treks.value = data.treks
  } catch {
    treks.value = []
  }
})
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

      <div v-else class="input-group mb-3" style="max-width: 400px;">
        <span class="input-group-text bg-white"><i class="bi bi-search"></i></span>
        <input v-model="trekQuery" type="text" class="form-control"
               placeholder="Search treks by name, location or status">
      </div>

      <div v-for="t in filteredTreks" :key="t.id" class="card shadow-sm mb-3">
        <div class="card-body">
          <div class="d-flex justify-content-between align-items-start flex-wrap gap-2">
            <div>
              <h5 class="fw-bold mb-1">{{ t.name }}</h5>
              <span class="text-secondary small">{{ t.location }} &middot; {{ t.duration_days }} days</span>
              <div class="mt-2 d-flex gap-2 flex-wrap">
                <span class="badge rounded-pill fw-semibold" :class="statusBadge(t.status)">{{ t.status }}</span>
                <span class="badge rounded-pill bg-secondary text-white">{{ t.available_slots }} slots</span>
                <span class="badge rounded-pill bg-secondary text-white">{{ t.participants_count }} registered</span>
              </div>
            </div>
            <button type="button" class="btn btn-sm btn-outline-primary" @click="router.push(`/staff/treks/${t.id}`)">
              <i class="bi bi-arrow-right me-1"></i>View
            </button>
          </div>
        </div>
      </div>
  </div>
</template>
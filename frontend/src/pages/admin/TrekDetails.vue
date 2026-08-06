<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getTrekDetail } from '@/lib/api'

const route = useRoute()
const router = useRouter()

const trek = ref(null)

onMounted(async () => {
  try {
    const data = await getTrekDetail(route.params.id)
    trek.value = data.trek
  } catch {
    trek.value = null
  }
})

function difficultyBadge(d) {
  return ({ easy: 'bg-success', moderate: 'bg-warning text-dark', hard: 'bg-danger' })[d] || 'bg-secondary'
}

function statusBadge(s) {
  return ({
    pending: 'bg-secondary', approved: 'bg-info text-dark', open: 'bg-success',
    closed: 'bg-secondary', completed: 'bg-primary',
  })[s] || 'bg-secondary'
}

function bookingBadge(s) {
  return ({ booked: 'bg-primary', cancelled: 'bg-danger', completed: 'bg-success' })[s] || 'bg-secondary'
}
</script>

<template>
  <div class="container py-4">
    <button @click="router.push('/admin/treks')" class="btn btn-link px-0 mb-3 text-decoration-none">
      <i class="bi bi-arrow-left me-1"></i>Back to trek list
    </button>

    <h4 class="fw-bold text-uppercase mb-4" style="letter-spacing: 0.04em;">Trek Details</h4>

    <template v-if="trek">
      <div class="card shadow-sm mb-4">
        <div class="card-body">
          <div class="row g-3">
            <div class="col-md-6">
              <small class="text-secondary text-uppercase small">Name</small>
              <p class="fw-bold mb-0">{{ trek.name }}</p>
            </div>
            <div class="col-md-6">
              <small class="text-secondary text-uppercase small">Location</small>
              <p class="mb-0">{{ trek.location }}</p>
            </div>
            <div class="col-md-6">
              <small class="text-secondary text-uppercase small">Difficulty</small>
              <p class="mb-0"><span class="badge rounded-pill fw-semibold" :class="difficultyBadge(trek.difficulty)">{{ trek.difficulty }}</span></p>
            </div>
            <div class="col-md-6">
              <small class="text-secondary text-uppercase small">Status</small>
              <p class="mb-0"><span class="badge rounded-pill fw-semibold" :class="statusBadge(trek.status)">{{ trek.status }}</span></p>
            </div>
            <div class="col-md-6">
              <small class="text-secondary text-uppercase small">Duration</small>
              <p class="mb-0">{{ trek.duration_days }} days</p>
            </div>
            <div class="col-md-6">
              <small class="text-secondary text-uppercase small">Available Slots</small>
              <p class="mb-0">{{ trek.available_slots }}</p>
            </div>
            <div class="col-md-6">
              <small class="text-secondary text-uppercase small">Dates</small>
              <p class="mb-0">{{ trek.start_date }} to {{ trek.end_date }}</p>
            </div>
            <div class="col-md-6">
              <small class="text-secondary text-uppercase small">Assigned Staff</small>
              <p class="mb-0">{{ trek.assigned_staff ? trek.assigned_staff.name : '-' }}</p>
            </div>
          </div>
        </div>
      </div>

      <div class="card shadow-sm">
        <div class="card-header bg-white py-3">
          <h6 class="mb-0 fw-bold">Bookings</h6>
        </div>
        <div class="card-body p-0">
          <div class="table-responsive">
            <table class="table table-hover align-middle mb-0">
              <thead class="table-light">
                <tr>
                  <th class="ps-3">#</th>
                  <th>Trekker</th>
                  <th>Status</th>
                  <th class="pe-3">Booked On</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="b in trek.bookings" :key="b.id">
                  <td class="ps-3 text-secondary">{{ b.id }}</td>
                  <td class="fw-semibold">{{ b.user ? b.user.name : '-' }}</td>
                  <td><span class="badge rounded-pill fw-semibold" :class="bookingBadge(b.status)">{{ b.status }}</span></td>
                  <td class="pe-3 text-secondary">{{ b.booking_date }}</td>
                </tr>
              </tbody>
            </table>
          </div>
          <div v-if="!trek.bookings.length" class="text-center text-secondary py-5">
            <p class="mb-1 fw-semibold text-dark">No bookings yet</p>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>
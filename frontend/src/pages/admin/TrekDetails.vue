<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getTrekDetail } from '@/lib/api'

const route = useRoute()
const router = useRouter()

const trek = ref(null)
const loading = ref(true)
const error = ref('')

onMounted(async () => {
  try {
    const data = await getTrekDetail(route.params.id)
    trek.value = data.trek
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
})

function difficultyBadge(d) {
  return {
    easy: 'bg-success',
    moderate: 'bg-warning text-dark',
    hard: 'bg-danger',
  }[d] || 'bg-secondary'
}

function statusBadge(s) {
  return {
    pending: 'bg-secondary',
    approved: 'bg-info text-dark',
    open: 'bg-success',
    closed: 'bg-dark',
    completed: 'bg-primary',
  }[s] || 'bg-secondary'
}

function bookingBadge(status) {
  return {
    booked: 'bg-primary',
    cancelled: 'bg-danger',
    completed: 'bg-success',
  }[status] || 'bg-secondary'
}
</script>

<template>
  <section class="min-vh-100" style="padding-top: 56px; background: var(--deep-space-blue);">
    <div class="container py-4" style="max-width: 860px;">
      <button @click="router.push('/admin/treks')" class="btn btn-link text-light px-0 mb-3">
        <i class="bi bi-arrow-left me-1"></i>Back to trek list
      </button>

      <h1 class="text-light fw-bold mb-4" style="letter-spacing: 3px;">TREK DETAILS</h1>

      <div v-if="error" class="alert alert-danger">{{ error }}</div>
      <div v-else-if="loading" class="text-light">Loading...</div>

      <template v-else>
        <div class="card border-0 shadow-sm mb-4">
          <div class="card-body">
            <div class="row">
              <div class="col-md-6 mb-2">
                <small class="text-muted text-uppercase">Name</small>
                <p class="fw-bold mb-0">{{ trek.name }}</p>
              </div>
              <div class="col-md-6 mb-2">
                <small class="text-muted text-uppercase">Location</small>
                <p class="mb-0">{{ trek.location }}</p>
              </div>
              <div class="col-md-6 mb-2">
                <small class="text-muted text-uppercase">Difficulty</small>
                <p class="mb-0"><span class="badge" :class="difficultyBadge(trek.difficulty)">{{ trek.difficulty }}</span></p>
              </div>
              <div class="col-md-6 mb-2">
                <small class="text-muted text-uppercase">Status</small>
                <p class="mb-0"><span class="badge" :class="statusBadge(trek.status)">{{ trek.status }}</span></p>
              </div>
              <div class="col-md-6 mb-2">
                <small class="text-muted text-uppercase">Duration</small>
                <p class="mb-0">{{ trek.duration_days }} days</p>
              </div>
              <div class="col-md-6 mb-2">
                <small class="text-muted text-uppercase">Available Slots</small>
                <p class="mb-0">{{ trek.available_slots }}</p>
              </div>
              <div class="col-md-6 mb-2">
                <small class="text-muted text-uppercase">Dates</small>
                <p class="mb-0">{{ trek.start_date }} to {{ trek.end_date }}</p>
              </div>
              <div class="col-md-6 mb-2">
                <small class="text-muted text-uppercase">Assigned Staff</small>
                <p class="mb-0">{{ trek.assigned_staff ? trek.assigned_staff.name : '-' }}</p>
              </div>
            </div>
          </div>
        </div>

        <div class="card border-0 shadow-sm">
          <div class="card-header bg-white border-bottom">
            <h6 class="mb-0 fw-bold text-uppercase">Bookings</h6>
          </div>
          <div class="table-responsive">
            <table class="table table-hover align-middle mb-0">
              <thead class="table-light">
                <tr>
                  <th>#</th>
                  <th>Trekker</th>
                  <th>Status</th>
                  <th>Booked On</th>
                </tr>
              </thead>
              <tbody>
                <tr v-if="trek.bookings.length === 0">
                  <td colspan="4" class="text-center text-muted py-4">No bookings yet</td>
                </tr>
                <tr v-for="b in trek.bookings" :key="b.id">
                  <td>{{ b.id }}</td>
                  <td>{{ b.user ? b.user.name : '-' }}</td>
                  <td><span class="badge" :class="bookingBadge(b.status)">{{ b.status }}</span></td>
                  <td>{{ b.booking_date }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </template>
    </div>
  </section>
</template>
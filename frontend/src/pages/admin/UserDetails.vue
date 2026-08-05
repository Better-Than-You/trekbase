<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getUserDetail } from '@/lib/api'

const route = useRoute()
const router = useRouter()

const user = ref(null)
const loading = ref(true)
const error = ref('')

onMounted(async () => {
  try {
    const data = await getUserDetail(route.params.id)
    user.value = data.user
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
})

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
      <button @click="router.push('/admin/users')" class="btn btn-link text-light px-0 mb-3">
        <i class="bi bi-arrow-left me-1"></i>Back to user list
      </button>

      <h1 class="text-light fw-bold mb-4" style="letter-spacing: 3px;">USER DETAILS</h1>

      <div v-if="error" class="alert alert-danger">{{ error }}</div>
      <div v-else-if="loading" class="text-light">Loading...</div>

      <template v-else>
        <div class="card border-0 shadow-sm mb-4">
          <div class="card-body">
            <div class="row">
              <div class="col-md-6 mb-2">
                <small class="text-muted text-uppercase">Name</small>
                <p class="fw-bold mb-0">{{ user.name }}</p>
              </div>
              <div class="col-md-6 mb-2">
                <small class="text-muted text-uppercase">Email</small>
                <p class="mb-0">{{ user.email }}</p>
              </div>
              <div class="col-md-6 mb-2">
                <small class="text-muted text-uppercase">Joined</small>
                <p class="mb-0">{{ user.created_at || '-' }}</p>
              </div>
              <div class="col-md-6 mb-2">
                <small class="text-muted text-uppercase">Total Bookings</small>
                <p class="mb-0">{{ user.bookings.length }}</p>
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
                  <th>Trek</th>
                  <th>Status</th>
                  <th>Booked On</th>
                </tr>
              </thead>
              <tbody>
                <tr v-if="user.bookings.length === 0">
                  <td colspan="4" class="text-center text-muted py-4">No bookings yet</td>
                </tr>
                <tr v-for="b in user.bookings" :key="b.id">
                  <td>{{ b.id }}</td>
                  <td>{{ b.trek ? b.trek.name : '-' }}</td>
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
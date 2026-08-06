<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getUserDetail } from '@/lib/api'

const route = useRoute()
const router = useRouter()

const user = ref(null)

onMounted(async () => {
  try {
    const data = await getUserDetail(route.params.id)
    user.value = data.user
  } catch {
    user.value = null
  }
})

function bookingBadge(s) {
  return ({ booked: 'bg-primary', cancelled: 'bg-danger', completed: 'bg-success' })[s] || 'bg-secondary'
}
</script>

<template>
  <div class="container py-4">
    <button @click="router.push('/admin/users')" class="btn btn-link px-0 mb-3 text-decoration-none">
      <i class="bi bi-arrow-left me-1"></i>Back to user list
    </button>

    <h4 class="fw-bold text-uppercase mb-4" style="letter-spacing: 0.04em;">User Details</h4>

    <template v-if="user">
      <div class="card shadow-sm mb-4">
        <div class="card-body">
          <div class="row g-3">
            <div class="col-md-6">
              <small class="text-secondary text-uppercase small">Name</small>
              <p class="fw-bold mb-0">{{ user.name }}</p>
            </div>
            <div class="col-md-6">
              <small class="text-secondary text-uppercase small">Email</small>
              <p class="mb-0">{{ user.email }}</p>
            </div>
            <div class="col-md-6">
              <small class="text-secondary text-uppercase small">Joined</small>
              <p class="mb-0">{{ user.created_at || '-' }}</p>
            </div>
            <div class="col-md-6">
              <small class="text-secondary text-uppercase small">Total Bookings</small>
              <p class="mb-0"><span class="badge rounded-pill bg-body-secondary">{{ user.bookings.length }}</span></p>
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
                  <th>Trek</th>
                  <th>Status</th>
                  <th class="pe-3">Booked On</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="b in user.bookings" :key="b.id">
                  <td class="ps-3 text-secondary">{{ b.id }}</td>
                  <td class="fw-semibold">{{ b.trek ? b.trek.name : '-' }}</td>
                  <td><span class="badge rounded-pill fw-semibold" :class="bookingBadge(b.status)">{{ b.status }}</span></td>
                  <td class="pe-3 text-secondary">{{ b.booking_date }}</td>
                </tr>
              </tbody>
            </table>
          </div>
          <div v-if="!user.bookings.length" class="text-center text-secondary py-5">
            <p class="mb-1 fw-semibold text-dark">No bookings yet</p>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>
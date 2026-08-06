<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getMyBookings } from '@/lib/api'
import { difficultyBadge, bookingBadge } from '@/lib/badges'

const router = useRouter()

const bookings = ref([])

onMounted(async () => {
  try {
    const data = await getMyBookings()
    bookings.value = data.bookings
  } catch {
    bookings.value = []
  }
})

</script>

<template>
  <div class="container py-4">
    <button @click="router.push('/user/dashboard')" class="btn btn-link px-0 mb-3 text-decoration-none">
      <i class="bi bi-arrow-left me-1"></i>Back to dashboard
    </button>

    <h4 class="fw-bold text-uppercase mb-4" style="letter-spacing: 0.04em;">My Bookings</h4>

    <div class="card shadow-sm">
      <div class="card-body p-0">
        <div class="table-responsive">
          <table class="table table-hover align-middle mb-0">
            <thead class="table-light">
              <tr>
                <th class="ps-3">#</th>
                <th>Trek</th>
                <th>Location</th>
                <th>Difficulty</th>
                <th>Status</th>
                <th class="pe-3">Booked On</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="b in bookings" :key="b.id">
                <td class="ps-3 text-secondary">{{ b.id }}</td>
                <td class="fw-semibold">{{ b.trek?.name || '-' }}</td>
                <td class="text-secondary">{{ b.trek?.location || '-' }}</td>
                <td><span class="badge rounded-pill fw-semibold" :class="difficultyBadge(b.trek?.difficulty)">{{ b.trek?.difficulty || '-' }}</span></td>
                <td><span class="badge rounded-pill fw-semibold" :class="bookingBadge(b.status)">{{ b.status }}</span></td>
                <td class="pe-3 text-secondary">{{ b.booking_date }}</td>
              </tr>
            </tbody>
          </table>
        </div>
        <div v-if="!bookings.length" class="text-center text-secondary py-5">
          <i class="bi bi-journal-x fs-3 d-block mb-2"></i>
          <p class="mb-1 fw-semibold text-dark">You have no bookings yet</p>
          <p class="small mb-0">Browse treks from your dashboard to get started.</p>
        </div>
      </div>
    </div>
  </div>
</template>
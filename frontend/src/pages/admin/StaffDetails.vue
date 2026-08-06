<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getStaffDetail } from '@/lib/api'

const route = useRoute()
const router = useRouter()

const staff = ref(null)

onMounted(async () => {
  try {
    const data = await getStaffDetail(route.params.id)
    staff.value = data.staff
  } catch {
    staff.value = null
  }
})

function staffBadge(s) {
  return ({ available: 'bg-success', assigned: 'bg-primary', not_working: 'bg-secondary' })[s] || 'bg-secondary'
}
</script>

<template>
  <div class="container py-4">
    <button @click="router.push('/admin/staff')" class="btn btn-link px-0 mb-3 text-decoration-none">
      <i class="bi bi-arrow-left me-1"></i>Back to staff list
    </button>

    <h4 class="fw-bold text-uppercase mb-4" style="letter-spacing: 0.04em;">Staff Details</h4>

    <template v-if="staff">
      <div class="card shadow-sm mb-4">
        <div class="card-body">
          <div class="row g-3">
            <div class="col-md-6">
              <small class="text-secondary text-uppercase small">Name</small>
              <p class="fw-bold mb-0">{{ staff.name }}</p>
            </div>
            <div class="col-md-6">
              <small class="text-secondary text-uppercase small">Contact</small>
              <p class="mb-0">{{ staff.contact }}</p>
            </div>
            <div class="col-md-6">
              <small class="text-secondary text-uppercase small">Status</small>
              <p class="mb-0"><span class="badge rounded-pill fw-semibold" :class="staffBadge(staff.status)">{{ staff.status }}</span></p>
            </div>
            <div class="col-md-6">
              <small class="text-secondary text-uppercase small">Assigned Treks</small>
              <p class="mb-0"><span class="badge rounded-pill bg-body-secondary">{{ staff.assigned_treks.length }}</span></p>
            </div>
          </div>
        </div>
      </div>

      <div class="card shadow-sm">
        <div class="card-header bg-white py-3">
          <h6 class="mb-0 fw-bold">Assigned Treks</h6>
        </div>
        <div class="card-body p-0">
          <div class="table-responsive">
            <table class="table table-hover align-middle mb-0">
              <thead class="table-light">
                <tr>
                  <th class="ps-3">#</th>
                  <th>Name</th>
                  <th>Location</th>
                  <th class="pe-3">Status</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="t in staff.assigned_treks" :key="t.id">
                  <td class="ps-3 text-secondary">{{ t.id }}</td>
                  <td class="fw-semibold">{{ t.name }}</td>
                  <td class="text-secondary">{{ t.location }}</td>
                  <td class="pe-3"><span class="badge rounded-pill fw-semibold" :class="staffBadge(t.status)">{{ t.status }}</span></td>
                </tr>
              </tbody>
            </table>
          </div>
          <div v-if="!staff.assigned_treks.length" class="text-center text-secondary py-5">
            <p class="mb-1 fw-semibold text-dark">No treks assigned</p>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>
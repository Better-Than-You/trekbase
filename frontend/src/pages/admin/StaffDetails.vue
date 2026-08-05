<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getStaffDetail } from '@/lib/api'

const route = useRoute()
const router = useRouter()

const staff = ref(null)
const loading = ref(true)
const error = ref('')

onMounted(async () => {
  try {
    const data = await getStaffDetail(route.params.id)
    staff.value = data.staff
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
})

function staffBadge(status) {
  return {
    available: 'bg-success',
    assigned: 'bg-primary',
    not_working: 'bg-secondary',
  }[status] || 'bg-secondary'
}
</script>

<template>
  <section class="min-vh-100" style="padding-top: 56px; background: var(--deep-space-blue);">
    <div class="container py-4" style="max-width: 860px;">
      <button @click="router.push('/admin/staff')" class="btn btn-link text-light px-0 mb-3">
        <i class="bi bi-arrow-left me-1"></i>Back to staff list
      </button>

      <h1 class="text-light fw-bold mb-4" style="letter-spacing: 3px;">STAFF DETAILS</h1>

      <div v-if="error" class="alert alert-danger">{{ error }}</div>
      <div v-else-if="loading" class="text-light">Loading...</div>

      <template v-else>
        <div class="card border-0 shadow-sm mb-4">
          <div class="card-body">
            <div class="row">
              <div class="col-md-6 mb-2">
                <small class="text-muted text-uppercase">Name</small>
                <p class="fw-bold mb-0">{{ staff.name }}</p>
              </div>
              <div class="col-md-6 mb-2">
                <small class="text-muted text-uppercase">Contact</small>
                <p class="mb-0">{{ staff.contact }}</p>
              </div>
              <div class="col-md-6 mb-2">
                <small class="text-muted text-uppercase">Status</small>
                <p class="mb-0"><span class="badge" :class="staffBadge(staff.status)">{{ staff.status }}</span></p>
              </div>
              <div class="col-md-6 mb-2">
                <small class="text-muted text-uppercase">Assigned Treks</small>
                <p class="mb-0">{{ staff.assigned_treks.length }}</p>
              </div>
            </div>
          </div>
        </div>

        <div class="card border-0 shadow-sm">
          <div class="card-header bg-white border-bottom">
            <h6 class="mb-0 fw-bold text-uppercase">Assigned Treks</h6>
          </div>
          <div class="table-responsive">
            <table class="table table-hover align-middle mb-0">
              <thead class="table-light">
                <tr>
                  <th>#</th>
                  <th>Name</th>
                  <th>Location</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                <tr v-if="staff.assigned_treks.length === 0">
                  <td colspan="4" class="text-center text-muted py-4">No treks assigned</td>
                </tr>
                <tr v-for="t in staff.assigned_treks" :key="t.id">
                  <td>{{ t.id }}</td>
                  <td>{{ t.name }}</td>
                  <td>{{ t.location }}</td>
                  <td>{{ t.status }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </template>
    </div>
  </section>
</template>
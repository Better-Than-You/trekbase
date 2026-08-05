<script setup>
import { ref, onMounted } from 'vue'
import { getAdminStaff, deleteStaff } from '@/lib/api'

const staff = ref([])
const loading = ref(true)
const error = ref('')

onMounted(async () => {
  try {
    const data = await getAdminStaff()
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

async function handleDelete(s) {
  if (!confirm(`Delete staff ${s.name}?`)) return
  try {
    await deleteStaff(s.id)
    staff.value = staff.value.filter(x => x.id !== s.id)
  } catch (e) {
    alert(e.message)
  }
}
</script>

<template>
  <section class="min-vh-100" style="padding-top: 56px; background: var(--deep-space-blue);">
    <div class="container py-4">
      <h1 class="text-light fw-bold mb-4" style="letter-spacing: 3px;">STAFF LIST</h1>

      <div v-if="error" class="alert alert-danger">{{ error }}</div>
      <div v-else-if="loading" class="text-light">Loading...</div>

      <div v-else class="card border-0 shadow-sm">
        <div class="table-responsive">
          <table class="table table-hover align-middle mb-0">
            <thead class="table-light">
              <tr>
                <th>#</th>
                <th>Name</th>
                <th>Contact</th>
                <th>Status</th>
                <th>Assigned Treks</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="staff.length === 0">
                <td colspan="6" class="text-center text-muted py-4">No staff added yet</td>
              </tr>
              <tr v-for="s in staff" :key="s.id">
                <td>{{ s.id }}</td>
                <td>{{ s.name }}</td>
                <td>{{ s.contact }}</td>
                <td>
                  <span class="badge" :class="staffBadge(s.status)">{{ s.status }}</span>
                </td>
                <td>
                  <span class="text-muted small">{{ s.assigned_treks.length }}</span>
                </td>
                <td>
                  <router-link :to="`/admin/staff/${s.id}`" class="btn btn-sm btn-outline-primary me-1"
                               title="View details">
                    <i class="bi bi-eye"></i>
                  </router-link>
                  <button type="button" class="btn btn-sm btn-outline-danger" title="Delete" @click="handleDelete(s)">
                    <i class="bi bi-trash"></i>
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </section>
</template>
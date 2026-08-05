<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getAdminTreks, deleteTrek } from '@/lib/api'

const router = useRouter()

const treks = ref([])
const loading = ref(true)
const error = ref('')

onMounted(async () => {
  try {
    const data = await getAdminTreks()
    treks.value = data.treks
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

async function handleDelete(t) {
  if (!confirm(`Delete trek ${t.name}?`)) return
  try {
    await deleteTrek(t.id)
    treks.value = treks.value.filter(x => x.id !== t.id)
  } catch (e) {
    alert(e.message)
  }
}
</script>

<template>
  <section class="min-vh-100" style="padding-top: 56px; background: var(--deep-space-blue);">
    <div class="container py-4">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h1 class="text-light fw-bold mb-0" style="letter-spacing: 3px;">TREK LIST</h1>
        <button @click="router.push('/admin/treks/add')" class="btn btn-primary">
          <i class="bi bi-plus-lg me-1"></i>Add Trek
        </button>
      </div>

      <div v-if="error" class="alert alert-danger">{{ error }}</div>
      <div v-else-if="loading" class="text-light">Loading...</div>

      <div v-else class="card border-0 shadow-sm">
        <div class="table-responsive">
          <table class="table table-hover align-middle mb-0">
            <thead class="table-light">
              <tr>
                <th>#</th>
                <th>Name</th>
                <th>Location</th>
                <th>Difficulty</th>
                <th>Slots</th>
                <th>Assigned Staff</th>
                <th>Bookings</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="treks.length === 0">
                <td colspan="9" class="text-center text-muted py-4">No treks yet</td>
              </tr>
              <tr v-for="t in treks" :key="t.id">
                <td>{{ t.id }}</td>
                <td>{{ t.name }}</td>
                <td>{{ t.location }}</td>
                <td><span class="badge" :class="difficultyBadge(t.difficulty)">{{ t.difficulty }}</span></td>
                <td>{{ t.available_slots }}</td>
                <td>{{ t.assigned_staff ? t.assigned_staff.name : '-' }}</td>
                <td><span class="badge bg-secondary">{{ t.bookings_count }}</span></td>
                <td><span class="badge" :class="statusBadge(t.status)">{{ t.status }}</span></td>
                <td>
                  <router-link :to="`/admin/treks/${t.id}`" class="btn btn-sm btn-outline-primary me-1"
                               title="View details">
                    <i class="bi bi-eye"></i>
                  </router-link>
                  <button type="button" class="btn btn-sm btn-outline-danger" title="Delete" @click="handleDelete(t)">
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
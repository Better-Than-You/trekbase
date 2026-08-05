<script setup>
import { ref, onMounted } from 'vue'
import { getAdminUsers, deleteUser } from '@/lib/api'

const users = ref([])
const loading = ref(true)
const error = ref('')

onMounted(async () => {
  try {
    const data = await getAdminUsers()
    users.value = data.users
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
})

async function handleDelete(u) {
  if (!confirm(`Delete user ${u.name}?`)) return
  try {
    await deleteUser(u.id)
    users.value = users.value.filter(x => x.id !== u.id)
  } catch (e) {
    alert(e.message)
  }
}
</script>

<template>
  <section class="min-vh-100" style="padding-top: 56px; background: var(--deep-space-blue);">
    <div class="container py-4">
      <h1 class="text-light fw-bold mb-4" style="letter-spacing: 3px;">USER LIST</h1>

      <div v-if="error" class="alert alert-danger">{{ error }}</div>
      <div v-else-if="loading" class="text-light">Loading...</div>

      <div v-else class="card border-0 shadow-sm">
        <div class="table-responsive">
          <table class="table table-hover align-middle mb-0">
            <thead class="table-light">
              <tr>
                <th>#</th>
                <th>Name</th>
                <th>Email</th>
                <th>Bookings</th>
                <th>Joined</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="users.length === 0">
                <td colspan="6" class="text-center text-muted py-4">No users yet</td>
              </tr>
              <tr v-for="u in users" :key="u.id">
                <td>{{ u.id }}</td>
                <td>{{ u.name }}</td>
                <td>{{ u.email }}</td>
                <td><span class="badge bg-secondary">{{ u.bookings_count }}</span></td>
                <td>{{ u.created_at || '-' }}</td>
                <td>
                  <router-link :to="`/admin/users/${u.id}`" class="btn btn-sm btn-outline-primary me-1"
                               title="View details">
                    <i class="bi bi-eye"></i>
                  </router-link>
                  <button type="button" class="btn btn-sm btn-outline-danger" title="Delete" @click="handleDelete(u)">
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
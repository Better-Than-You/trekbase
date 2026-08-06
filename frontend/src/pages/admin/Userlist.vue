<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getAdminUsers, deleteUser } from '@/lib/api'

const router = useRouter()

const users = ref([])

onMounted(async () => {
  try {
    const data = await getAdminUsers()
    users.value = data.users
  } catch {
    users.value = []
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
  <div class="container py-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <div>
        <h4 class="fw-bold text-uppercase mb-0" style="letter-spacing: 0.04em;">Users</h4>
        <p class="text-secondary small mb-0">Everyone who has registered to book treks</p>
      </div>
      <button @click="router.push('/admin/user/add')" class="btn btn-primary">
        <i class="bi bi-person-plus me-1"></i>Add User
      </button>
    </div>

    <div class="card shadow-sm">
      <div class="card-body p-0">
        <div class="table-responsive">
          <table class="table table-hover align-middle mb-0">
            <thead class="table-light">
              <tr>
                <th class="ps-3">#</th>
                <th>Name</th>
                <th>Email</th>
                <th>Bookings</th>
                <th>Joined</th>
                <th class="pe-3 text-end">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="u in users" :key="u.id">
                <td class="ps-3 text-secondary">{{ u.id }}</td>
                <td class="fw-semibold">{{ u.name }}</td>
                <td class="text-secondary">{{ u.email }}</td>
                <td><span class="badge rounded-pill bg-secondary text-white">{{ u.bookings_count }}</span></td>
                <td class="text-secondary">{{ u.created_at || '-' }}</td>
                <td class="pe-3 text-end text-nowrap">
                  <router-link :to="`/admin/users/${u.id}`" class="btn btn-sm btn-outline-primary me-1" title="View details">
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
        <div v-if="!users.length" class="text-center text-secondary py-5">
          <i class="bi bi-person-x fs-3 d-block mb-2"></i>
          <p class="mb-1 fw-semibold text-dark">No users found</p>
          <p class="small mb-0">Trekkers appear here once they register.</p>
        </div>
      </div>
    </div>
  </div>
</template>
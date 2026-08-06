<script setup>
// vue basics
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getAdminUsers, deleteUser, blacklistUser } from '@/lib/api'

const router = useRouter()

const users = ref([])
const query = ref('')
let searchTimer = null

async function load(q) {
  try {
    const data = await getAdminUsers(q)
    users.value = data.users
  } catch {
    users.value = []
  }
}

onMounted(() => load())

async function handleDelete(u) {
  if (!confirm(`Delete user ${u.name}?`)) return
  try {
    await deleteUser(u.id)
    users.value = users.value.filter(x => x.id !== u.id)
  } catch (e) {
    alert(e.message)
  }
}

async function toggleBlacklist(u) {
  if (!confirm(`${u.is_blacklisted ? 'Unban' : 'Ban'} user ${u.name}?`)) return
  try {
    const data = await blacklistUser(u.id, !u.is_blacklisted)
    u.is_blacklisted = data.user.is_blacklisted
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
      <div class="card-body">
        <div class="input-group mb-3" style="max-width: 400px;">
          <span class="input-group-text bg-white"><i class="bi bi-search"></i></span>
          <input v-model="query" type="text" class="form-control" placeholder="Search by name or email"
                 @input="onSearchInput">
        </div>
      </div>
      <div class="card-body p-0">
        <div class="table-responsive">
          <table class="table table-hover align-middle mb-0">
            <thead class="table-light">
              <tr>
                <th class="ps-3">#</th>
                <th>Name</th>
                <th>Email</th>
                <th>Bookings</th>
                <th class="pe-3 text-end">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="u in users" :key="u.id" :class="u.is_blacklisted ? 'table-danger' : ''">
                <td class="ps-3 text-secondary">{{ u.id }}</td>
                <td class="fw-semibold">
                  {{ u.name }}
                  <span v-if="u.is_blacklisted" class="badge rounded-pill bg-dark ms-1">Banned</span>
                </td>
                <td class="text-secondary">{{ u.email }}</td>
                <td><span class="badge rounded-pill bg-secondary text-white">{{ u.bookings_count }}</span></td>
                <td class="pe-3 text-end text-nowrap">
                  <router-link :to="`/admin/users/${u.id}`" class="btn btn-sm btn-outline-primary me-1" title="View details">
                    <i class="bi bi-eye"></i>
                  </router-link>
                  <button type="button" class="btn btn-sm btn-outline-warning me-1"
                          :title="u.is_blacklisted ? 'Unban' : 'Ban'"
                          @click="toggleBlacklist(u)">
                    <i :class="u.is_blacklisted ? 'bi bi-person-check' : 'bi bi-person-slash'"></i>
                  </button>
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
          <p class="small mb-0">Try a different search, or wait for trekkers to register.</p>
        </div>
      </div>
    </div>
  </div>
</template>
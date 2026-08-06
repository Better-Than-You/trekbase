<script setup>
// vue basics
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getAdminStaff, deleteStaff, blacklistStaff } from '@/lib/api'
import { staffBadge } from '@/lib/badges'

const router = useRouter()

const staff = ref([])
const query = ref('')
let searchTimer = null

async function load(q) {
  try {
    const data = await getAdminStaff(q)
    staff.value = data.staff
  } catch {
    staff.value = []
  }
}

onMounted(() => load())

async function handleDelete(s) {
  if (!confirm(`Delete staff ${s.name}?`)) return
  try {
    await deleteStaff(s.id)
    staff.value = staff.value.filter(x => x.id !== s.id)
  } catch (e) {
    alert(e.message)
  }
}

async function toggleBlacklist(s) {
  if (!confirm(`${s.is_blacklisted ? 'Unban' : 'Ban'} staff ${s.name}?`)) return
  try {
    const data = await blacklistStaff(s.id, !s.is_blacklisted)
    s.is_blacklisted = data.staff.is_blacklisted
  } catch (e) {
    alert(e.message)
  }
}
</script>

<template>
  <div class="container py-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <div>
        <h4 class="fw-bold text-uppercase mb-0" style="letter-spacing: 0.04em;">Trekking Staff</h4>
        <p class="text-secondary small mb-0">Staff accounts are created here, they cannot register themselves</p>
      </div>
      <button @click="router.push('/admin/staff/add')" class="btn btn-primary">
        <i class="bi bi-person-plus me-1"></i>Add Staff
      </button>
    </div>

    <div class="card shadow-sm">
      <div class="card-body">
        <div class="input-group mb-3" style="max-width: 400px;">
          <span class="input-group-text bg-white"><i class="bi bi-search"></i></span>
          <input v-model="query" type="text" class="form-control" placeholder="Search by name, email or contact"
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
                <th>Contact</th>
                <th>Status</th>
                <th>Assigned Treks</th>
                <th class="pe-3 text-end">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="s in staff" :key="s.id" :class="s.is_blacklisted ? 'table-danger' : ''">
                <td class="ps-3 text-secondary">{{ s.id }}</td>
                <td class="fw-semibold">
                  {{ s.name }}
                  <span v-if="s.is_blacklisted" class="badge rounded-pill bg-dark ms-1">Banned</span>
                </td>
                <td class="text-secondary">{{ s.contact }}</td>
                <td><span class="badge rounded-pill fw-semibold" :class="staffBadge(s.status)">{{ s.status }}</span></td>
                <td><span class="badge rounded-pill bg-secondary text-white">{{ s.assigned_treks.length }}</span></td>
                <td class="pe-3 text-end text-nowrap">
                  <router-link :to="`/admin/staff/${s.id}`" class="btn btn-sm btn-outline-primary me-1" title="View details">
                    <i class="bi bi-eye"></i>
                  </router-link>
                  <button type="button" class="btn btn-sm btn-outline-warning me-1"
                          :title="s.is_blacklisted ? 'Unban' : 'Ban'"
                          @click="toggleBlacklist(s)">
                    <i :class="s.is_blacklisted ? 'bi bi-person-check' : 'bi bi-person-slash'"></i>
                  </button>
                  <button type="button" class="btn btn-sm btn-outline-danger" title="Delete" @click="handleDelete(s)">
                    <i class="bi bi-trash"></i>
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <div v-if="!staff.length" class="text-center text-secondary py-5">
          <i class="bi bi-person-x fs-3 d-block mb-2"></i>
          <p class="mb-1 fw-semibold text-dark">No staff found</p>
          <p class="small mb-0">Try a different search, or create a staff account to start assigning treks.</p>
        </div>
      </div>
    </div>
  </div>
</template>
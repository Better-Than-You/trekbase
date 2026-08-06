<script setup>
// vue basics
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getAdminTreks, deleteTrek } from '@/lib/api'
import { difficultyBadge, statusBadge } from '@/lib/badges'

const router = useRouter()

const treks = ref([])
const query = ref('')
let searchTimer = null

async function load(q) {
  try {
    const data = await getAdminTreks(q)
    treks.value = data.treks
  } catch {
    treks.value = []
  }
}

onMounted(() => load())

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
  <div class="container py-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <div>
        <h4 class="fw-bold text-uppercase mb-0" style="letter-spacing: 0.04em;">Treks</h4>
        <p class="text-secondary small mb-0">Create trek routes, assign staff and control booking status</p>
      </div>
      <button @click="router.push('/admin/treks/add')" class="btn btn-primary">
        <i class="bi bi-plus-lg me-1"></i>Add Trek
      </button>
    </div>

    <div class="card shadow-sm">
      <div class="card-body">
        <div class="input-group mb-3" style="max-width: 400px;">
          <span class="input-group-text bg-white"><i class="bi bi-search"></i></span>
          <input v-model="query" type="text" class="form-control" placeholder="Search by name or location"
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
                <th>Location</th>
                <th>Difficulty</th>
                <th>Slots</th>
                <th>Assigned Staff</th>
                <th>Bookings</th>
                <th>Status</th>
                <th class="pe-3 text-end">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="t in treks" :key="t.id">
                <td class="ps-3 text-secondary">{{ t.id }}</td>
                <td class="fw-semibold">{{ t.name }}</td>
                <td class="text-secondary">{{ t.location }}</td>
                <td><span class="badge rounded-pill fw-semibold" :class="difficultyBadge(t.difficulty)">{{ t.difficulty }}</span></td>
                <td>{{ t.available_slots }}</td>
                <td>{{ t.assigned_staff ? t.assigned_staff.name : 'Not assigned' }}</td>
                <td><span class="badge rounded-pill bg-secondary text-white">{{ t.bookings_count }}</span></td>
                <td><span class="badge rounded-pill fw-semibold" :class="statusBadge(t.status)">{{ t.status }}</span></td>
                <td class="pe-3 text-end text-nowrap">
                  <router-link :to="`/admin/treks/${t.id}`" class="btn btn-sm btn-outline-primary me-1" title="View details">
                    <i class="bi bi-eye"></i>
                  </router-link>
                  <router-link :to="`/admin/treks/${t.id}/edit`" class="btn btn-sm btn-outline-secondary me-1" title="Edit">
                    <i class="bi bi-pencil-square"></i>
                  </router-link>
                  <button type="button" class="btn btn-sm btn-outline-danger" title="Delete" @click="handleDelete(t)">
                    <i class="bi bi-trash"></i>
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <div v-if="!treks.length" class="text-center text-secondary py-5">
          <i class="bi bi-signpost-split fs-3 d-block mb-2"></i>
          <p class="mb-1 fw-semibold text-dark">No treks found</p>
          <p class="small mb-0">Add your first trek route with the button above.</p>
        </div>
      </div>
    </div>
  </div>
</template>
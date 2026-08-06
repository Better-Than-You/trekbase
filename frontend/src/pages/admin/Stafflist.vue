<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getAdminStaff, deleteStaff } from '@/lib/api'

const router = useRouter()

const staff = ref([])

onMounted(async () => {
  try {
    const data = await getAdminStaff()
    staff.value = data.staff
  } catch {
    staff.value = []
  }
})

function staffBadge(s) {
  return ({ available: 'bg-success', assigned: 'bg-primary', not_working: 'bg-secondary' })[s] || 'bg-secondary'
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
              <tr v-for="s in staff" :key="s.id">
                <td class="ps-3 text-secondary">{{ s.id }}</td>
                <td class="fw-semibold">{{ s.name }}</td>
                <td class="text-secondary">{{ s.contact }}</td>
                <td><span class="badge rounded-pill fw-semibold" :class="staffBadge(s.status)">{{ s.status }}</span></td>
                <td><span class="badge rounded-pill bg-body-secondary">{{ s.assigned_treks.length }}</span></td>
                <td class="pe-3 text-end text-nowrap">
                  <router-link :to="`/admin/staff/${s.id}`" class="btn btn-sm btn-outline-primary me-1" title="View details">
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
        <div v-if="!staff.length" class="text-center text-secondary py-5">
          <i class="bi bi-person-x fs-3 d-block mb-2"></i>
          <p class="mb-1 fw-semibold text-dark">No staff found</p>
          <p class="small mb-0">Create a staff account to start assigning treks.</p>
        </div>
      </div>
    </div>
  </div>
</template>
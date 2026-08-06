<script setup>
import { ref, onMounted } from 'vue'
import { getAdminDashboard, deleteUser, deleteStaff, deleteTrek } from '@/lib/api'
import { difficultyBadge, statusBadge, bookingBadge, staffBadge } from '@/lib/badges'

const data = ref({
  counts: { bookings: 0, treks: 0, staff: 0, users: 0 },
  treks: [],
  bookings: [],
  staff: [],
  users: [],
})

onMounted(async () => {
  try {
    data.value = await getAdminDashboard()
  } catch {
  }
})

async function handleDeleteTrek(t) {
  if (!confirm(`Delete trek ${t.name}?`)) return
  try {
    await deleteTrek(t.id)
    data.value.treks = data.value.treks.filter(x => x.id !== t.id)
    data.value.counts.treks -= 1
  } catch (e) {
    alert(e.message)
  }
}

async function handleDeleteUser(u) {
  if (!confirm(`Delete user ${u.name}?`)) return
  try {
    await deleteUser(u.id)
    data.value.users = data.value.users.filter(x => x.id !== u.id)
    data.value.counts.users -= 1
  } catch (e) {
    alert(e.message)
  }
}

async function handleDeleteStaff(s) {
  if (!confirm(`Delete staff ${s.name}?`)) return
  try {
    await deleteStaff(s.id)
    data.value.staff = data.value.staff.filter(x => x.id !== s.id)
    data.value.counts.staff -= 1
  } catch (e) {
    alert(e.message)
  }
}
</script>

<template>
  <div class="container py-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <div>
        <h4 class="fw-bold text-uppercase mb-0" style="letter-spacing: 0.04em;">Admin Dashboard</h4>
        <p class="text-secondary small mb-0">An overview of everything happening in the system</p>
      </div>
    </div>

    <div class="row g-3 mb-4">
        <div class="col-6 col-xl-3">
          <div class="card shadow-sm h-100">
            <div class="card-body d-flex align-items-center gap-3">
              <div class="d-inline-flex align-items-center justify-content-center p-3 rounded-3 bg-primary text-white">
                <i class="bi bi-ticket-perforated"></i>
              </div>
              <div>
                <div class="text-secondary text-uppercase small fw-semibold">Reservations</div>
                <div class="h3 mb-0 fw-bold">{{ data.counts.bookings }}</div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-6 col-xl-3">
          <div class="card shadow-sm h-100">
            <div class="card-body d-flex align-items-center gap-3">
              <div class="d-inline-flex align-items-center justify-content-center p-3 rounded-3 bg-success text-white">
                <i class="bi bi-compass"></i>
              </div>
              <div>
                <div class="text-secondary text-uppercase small fw-semibold">Treks</div>
                <div class="h3 mb-0 fw-bold">{{ data.counts.treks }}</div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-6 col-xl-3">
          <div class="card shadow-sm h-100">
            <div class="card-body d-flex align-items-center gap-3">
              <div class="d-inline-flex align-items-center justify-content-center p-3 rounded-3 bg-warning text-white">
                <i class="bi bi-person-gear"></i>
              </div>
              <div>
                <div class="text-secondary text-uppercase small fw-semibold">Trekking staff</div>
                <div class="h3 mb-0 fw-bold">{{ data.counts.staff }}</div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-6 col-xl-3">
          <div class="card shadow-sm h-100">
            <div class="card-body d-flex align-items-center gap-3">
              <div class="d-inline-flex align-items-center justify-content-center p-3 rounded-3 bg-info text-white">
                <i class="bi bi-people"></i>
              </div>
              <div>
                <div class="text-secondary text-uppercase small fw-semibold">Trekkers</div>
                <div class="h3 mb-0 fw-bold">{{ data.counts.users }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="card shadow-sm mb-4">
        <div class="card-header bg-white d-flex align-items-center justify-content-between py-3">
          <h6 class="mb-0 fw-bold">Treks</h6>
          <router-link to="/admin/treks/add" class="btn btn-sm btn-primary">
            <i class="bi bi-plus-lg me-1"></i>Add Trek
          </router-link>
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
                  <th>Status</th>
                  <th class="pe-3 text-end">Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="t in data.treks" :key="t.id">
                  <td class="ps-3 text-secondary">{{ t.id }}</td>
                  <td class="fw-semibold">{{ t.name }}</td>
                  <td class="text-secondary">{{ t.location }}</td>
                  <td><span class="badge rounded-pill fw-semibold" :class="difficultyBadge(t.difficulty)">{{ t.difficulty }}</span></td>
                  <td>{{ t.available_slots }}</td>
                  <td><span class="badge rounded-pill fw-semibold" :class="statusBadge(t.status)">{{ t.status }}</span></td>
                  <td class="pe-3 text-end text-nowrap">
                    <router-link :to="`/admin/treks/${t.id}`" class="btn btn-sm btn-outline-primary me-1" title="View details">
                      <i class="bi bi-eye"></i>
                    </router-link>
                        <router-link :to="`/admin/treks/${t.id}/edit`" class="btn btn-sm btn-outline-secondary me-1" title="Edit">
                          <i class="bi bi-pencil-square"></i>
                        </router-link>
                    <button type="button" class="btn btn-sm btn-outline-danger" title="Delete" @click="handleDeleteTrek(t)">
                      <i class="bi bi-trash"></i>
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <div v-if="!data.treks.length" class="text-center text-secondary py-5">
            <i class="bi bi-signpost-split fs-3 d-block mb-2"></i>
            <p class="mb-1 fw-semibold text-dark">No treks yet</p>
            <p class="small mb-0">Add your first trek with the button above.</p>
          </div>
        </div>
      </div>

      <div class="card shadow-sm mb-4">
        <div class="card-header bg-white d-flex align-items-center justify-content-between py-3">
          <h6 class="mb-0 fw-bold">Reservations</h6>
          <span class="badge rounded-pill bg-primary">{{ data.bookings.length }}</span>
        </div>
        <div class="card-body p-0">
          <div class="table-responsive">
            <table class="table table-hover align-middle mb-0">
              <thead class="table-light">
                <tr>
                  <th class="ps-3">#</th>
                  <th>Trek</th>
                  <th>Trekker</th>
                  <th>Status</th>
                  <th class="pe-3">Booked On</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="b in data.bookings" :key="b.id">
                  <td class="ps-3 text-secondary">{{ b.id }}</td>
                  <td class="fw-semibold">{{ b.trek ? b.trek.name : '-' }}</td>
                  <td>{{ b.user ? b.user.name : '-' }}</td>
                  <td><span class="badge rounded-pill fw-semibold" :class="bookingBadge(b.status)">{{ b.status }}</span></td>
                  <td class="pe-3 text-secondary">{{ b.booking_date }}</td>
                </tr>
              </tbody>
            </table>
          </div>
          <div v-if="!data.bookings.length" class="text-center text-secondary py-5">
            <i class="bi bi-signpost-split fs-3 d-block mb-2"></i>
            <p class="mb-1 fw-semibold text-dark">No reservations yet</p>
            <p class="small mb-0">Bookings will appear here as soon as trekkers sign up.</p>
          </div>
        </div>
      </div>

      <div class="row g-4">
        <div class="col-lg-6">
          <div class="card shadow-sm h-100">
            <div class="card-header bg-white d-flex align-items-center justify-content-between py-3">
              <h6 class="mb-0 fw-bold">Trekking staff</h6>
              <router-link to="/admin/staff/add" class="btn btn-sm btn-primary">
                <i class="bi bi-plus-lg me-1"></i>Add Staff
              </router-link>
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
                      <th class="pe-3 text-end">Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="s in data.staff" :key="s.id">
                      <td class="ps-3 text-secondary">{{ s.id }}</td>
                      <td class="fw-semibold">{{ s.name }}</td>
                      <td class="text-secondary">{{ s.contact }}</td>
                      <td><span class="badge rounded-pill fw-semibold" :class="staffBadge(s.status)">{{ s.status }}</span></td>
                      <td class="pe-3 text-end text-nowrap">
                        <router-link :to="`/admin/staff/${s.id}`" class="btn btn-sm btn-outline-primary me-1" title="View details">
                          <i class="bi bi-eye"></i>
                        </router-link>
                        <router-link :to="`/admin/staff/${s.id}/edit`" class="btn btn-sm btn-outline-secondary me-1" title="Edit">
                          <i class="bi bi-pencil-square"></i>
                        </router-link>
                        <button type="button" class="btn btn-sm btn-outline-danger" title="Delete" @click="handleDeleteStaff(s)">
                          <i class="bi bi-trash"></i>
                        </button>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <div v-if="!data.staff.length" class="text-center text-secondary py-5">
                <p class="mb-1 fw-semibold text-dark">No staff added yet</p>
              </div>
            </div>
          </div>
        </div>

        <div class="col-lg-6">
          <div class="card shadow-sm h-100">
            <div class="card-header bg-white d-flex align-items-center justify-content-between py-3">
              <h6 class="mb-0 fw-bold">Users</h6>
              <router-link to="/admin/user/add" class="btn btn-sm btn-primary">
                <i class="bi bi-plus-lg me-1"></i>Add User
              </router-link>
            </div>
            <div class="card-body p-0">
              <div class="table-responsive">
                <table class="table table-hover align-middle mb-0">
                  <thead class="table-light">
                    <tr>
                      <th class="ps-3">#</th>
                      <th>Name</th>
                      <th>Email</th>
                      <th class="pe-3 text-end">Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="u in data.users" :key="u.id">
                      <td class="ps-3 text-secondary">{{ u.id }}</td>
                      <td class="fw-semibold">{{ u.name }}</td>
                      <td class="text-secondary">{{ u.email }}</td>
                      <td class="pe-3 text-end text-nowrap">
                        <router-link :to="`/admin/users/${u.id}`" class="btn btn-sm btn-outline-primary me-1" title="View details">
                          <i class="bi bi-eye"></i>
                        </router-link>
                        <router-link :to="`/admin/users/${u.id}/edit`" class="btn btn-sm btn-outline-secondary me-1" title="Edit">
                          <i class="bi bi-pencil-square"></i>
                        </router-link>
                        <button type="button" class="btn btn-sm btn-outline-danger" title="Delete" @click="handleDeleteUser(u)">
                          <i class="bi bi-trash"></i>
                        </button>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <div v-if="!data.users.length" class="text-center text-secondary py-5">
                <p class="mb-1 fw-semibold text-dark">No users yet</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
</template>
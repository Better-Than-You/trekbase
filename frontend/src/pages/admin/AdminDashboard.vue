<script setup>
import { ref, onMounted } from 'vue'
import { getAdminDashboard, deleteUser, deleteStaff, deleteTrek } from '@/lib/api'

const data = ref(null)
const loading = ref(true)
const error = ref('')

onMounted(async () => {
  try {
    data.value = await getAdminDashboard()
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
})

function bookingBadge(status) {
  return {
    booked: 'bg-primary',
    cancelled: 'bg-danger',
    completed: 'bg-success',
  }[status] || 'bg-secondary'
}

function staffBadge(status) {
  return {
    available: 'bg-success',
    assigned: 'bg-primary',
    not_working: 'bg-secondary',
  }[status] || 'bg-secondary'
}

function trekDifficultyBadge(d) {
  return {
    easy: 'bg-success',
    moderate: 'bg-warning text-dark',
    hard: 'bg-danger',
  }[d] || 'bg-secondary'
}

function trekStatusBadge(s) {
  return {
    pending: 'bg-secondary',
    approved: 'bg-info text-dark',
    open: 'bg-success',
    closed: 'bg-dark',
    completed: 'bg-primary',
  }[s] || 'bg-secondary'
}

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
  <section class="admin-page">
    <div class="container pt-5 pb-5">
      <h1 class="text-light fw-bold mb-1" style="letter-spacing: 4px;">ADMIN DASHBOARD</h1>
      <p class="text-secondary mb-4" style="letter-spacing: 1px;">Overview of reservations, staff and trekkers</p>

      <div v-if="error" class="alert alert-danger">{{ error }}</div>
      <div v-else-if="loading" class="text-light">Loading...</div>

      <template v-else>
        <div class="row g-3 mb-4">
          <div class="col-md-3 col-6">
            <div class="card stat-card border-0">
              <div class="card-body">
                <h5 class="stat-label">Reservations</h5>
                <p class="stat-value mb-0">{{ data.counts.bookings }}</p>
              </div>
            </div>
          </div>
          <div class="col-md-3 col-6">
            <div class="card stat-card border-0">
              <div class="card-body">
                <h5 class="stat-label">Treks</h5>
                <p class="stat-value mb-0">{{ data.counts.treks }}</p>
              </div>
            </div>
          </div>
          <div class="col-md-3 col-6">
            <div class="card stat-card border-0">
              <div class="card-body">
                <h5 class="stat-label">Staff</h5>
                <p class="stat-value mb-0">{{ data.counts.staff }}</p>
              </div>
            </div>
          </div>
          <div class="col-md-3 col-6">
            <div class="card stat-card border-0">
              <div class="card-body">
                <h5 class="stat-label">Trekkers</h5>
                <p class="stat-value mb-0">{{ data.counts.users }}</p>
              </div>
            </div>
          </div>
        </div>

        <div class="card border-0 section-card mb-4">
          <div class="card-header section-header">
            Treks
            <router-link to="/admin/treks/add" class="btn btn-sm bg-white text-dark" style="float: right;">Add Trek</router-link>
          </div>
          <div class="table-responsive">
            <table class="table table-hover align-middle mb-0">
              <thead>
                <tr>
                  <th>#</th>
                  <th>Name</th>
                  <th>Location</th>
                  <th>Difficulty</th>
                  <th>Slots</th>
                  <th>Status</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-if="data.treks.length === 0">
                  <td colspan="7" class="text-muted text-center py-4">No treks added yet</td>
                </tr>
                <tr v-for="t in data.treks" :key="t.id">
                  <td>{{ t.id }}</td>
                  <td>{{ t.name }}</td>
                  <td>{{ t.location }}</td>
                  <td><span class="badge" :class="trekDifficultyBadge(t.difficulty)">{{ t.difficulty }}</span></td>
                  <td>{{ t.available_slots }}</td>
                  <td><span class="badge" :class="trekStatusBadge(t.status)">{{ t.status }}</span></td>
                  <td>
                    <router-link :to="`/admin/treks/${t.id}`" class="btn btn-sm btn-outline-primary me-1"
                                 title="View details">
                      <i class="bi bi-eye"></i>
                    </router-link>
                    <button type="button" class="btn btn-sm btn-outline-danger" title="Delete"
                            @click="handleDeleteTrek(t)">
                      <i class="bi bi-trash"></i>
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <div class="card border-0 section-card mb-4">
          <div class="card-header section-header">Reservations</div>
          <div class="table-responsive">
            <table class="table table-hover align-middle mb-0">
              <thead>
                <tr>
                  <th>#</th>
                  <th>Trek</th>
                  <th>Trekker</th>
                  <th>Status</th>
                  <th>Booked On</th>
                </tr>
              </thead>
              <tbody>
                <tr v-if="data.bookings.length === 0">
                  <td colspan="5" class="text-muted text-center py-4">No reservations yet</td>
                </tr>
                <tr v-for="b in data.bookings" :key="b.id">
                  <td>{{ b.id }}</td>
                  <td>{{ b.trek ? b.trek.name : '-' }}</td>
                  <td>{{ b.user ? b.user.name : '-' }}</td>
                  <td>
                    <span class="badge" :class="bookingBadge(b.status)">{{ b.status }}</span>
                  </td>
                  <td>{{ b.booking_date }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <div class="row g-4">
          <div class="col-lg-6">
            <div class="card border-0 section-card">
              <div class="card-header section-header">
                Staff
                <router-link to="/admin/staff/add" class="btn btn-sm bg-white text-dark" style="float: right;">Add
                  Staff</router-link>
              </div>

              <div class="table-responsive">
                <table class="table table-hover align-middle mb-0">
                  <thead>
                    <tr>
                      <th>#</th>
                      <th>Name</th>
                      <th>Contact</th>
                      <th>Status</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-if="data.staff.length === 0">
                      <td colspan="5" class="text-muted text-center py-4">No staff added yet</td>
                    </tr>
                    <tr v-for="s in data.staff" :key="s.id">
                      <td>{{ s.id }}</td>
                      <td>{{ s.name }}</td>
                      <td>{{ s.contact }}</td>
                      <td>
                        <span class="badge" :class="staffBadge(s.status)">{{ s.status }}</span>
                      </td>
                      <td>
                        <router-link :to="`/admin/staff/${s.id}`" class="btn btn-sm btn-outline-primary me-1"
                                     title="View details">
                          <i class="bi bi-eye"></i>
                        </router-link>
                        <button type="button" class="btn btn-sm btn-outline-danger" title="Delete"
                                @click="handleDeleteStaff(s)">
                          <i class="bi bi-trash"></i>
                        </button>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>

          <div class="col-lg-6">
            <div class="card border-0 section-card">
              <div class="card-header section-header">
                User
                <router-link to="/admin/user/add" class="btn btn-sm bg-white text-dark" style="float: right;">Add
                  User</router-link>
              </div>
              <div class="table-responsive">
                <table class="table table-hover align-middle mb-0">
                  <thead>
                    <tr>
                      <th>#</th>
                      <th>Name</th>
                      <th>Email</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-if="data.users.length === 0">
                      <td colspan="4" class="text-muted text-center py-4">No users yet</td>
                    </tr>
                    <tr v-for="u in data.users" :key="u.id">
                      <td>{{ u.id }}</td>
                      <td>{{ u.name }}</td>
                      <td>{{ u.email }}</td>
                      <td>
                        <router-link :to="`/admin/users/${u.id}`" class="btn btn-sm btn-outline-primary me-1"
                                     title="View details">
                          <i class="bi bi-eye"></i>
                        </router-link>
                        <button type="button" class="btn btn-sm btn-outline-danger" title="Delete"
                                @click="handleDeleteUser(u)">
                          <i class="bi bi-trash"></i>
                        </button>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </template>
    </div>
  </section>
</template>

<style scoped>
.admin-page {
  min-height: 100vh;
  background: var(--deep-space-blue);
  padding-top: 56px;
}

.stat-card {
  background: var(--parchment);
}

.stat-label {
  font-size: 0.75rem;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: var(--rich-cerulean);
  margin-bottom: 0.25rem;
}

.stat-value {
  font-size: 2rem;
  font-weight: 800;
  color: var(--deep-space-blue);
}

.section-card {
  background: var(--parchment);
}

.section-header {
  background: var(--yale-blue);
  color: #fff;
  font-weight: 600;
  letter-spacing: 2px;
  border-bottom: 0;
}
</style>

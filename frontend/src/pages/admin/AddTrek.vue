<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { addTrek, getAdminStaff } from '@/lib/api'

const router = useRouter()

const name = ref('')
const location = ref('')
const difficulty = ref('moderate')
const durationDays = ref('')
const availableSlots = ref('')
const status = ref('pending')
const startDate = ref('')
const endDate = ref('')
const assignedStaffId = ref('')
const staffOptions = ref([])
const error = ref('')
const success = ref('')
const loading = ref(false)

onMounted(async () => {
  try {
    const data = await getAdminStaff()
    staffOptions.value = data.staff
  } catch (e) {
    error.value = e.message
  }
})

async function handleSubmit() {
  error.value = ''
  success.value = ''
  loading.value = true
  try {
    await addTrek({
      name: name.value,
      location: location.value,
      difficulty: difficulty.value,
      duration_days: durationDays.value,
      available_slots: availableSlots.value,
      status: status.value,
      start_date: startDate.value,
      end_date: endDate.value,
      assigned_staff_id: assignedStaffId.value || null,
    })
    success.value = 'Trek added successfully'
    name.value = ''
    location.value = ''
    durationDays.value = ''
    availableSlots.value = ''
    startDate.value = ''
    endDate.value = ''
    assignedStaffId.value = ''
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <section class="min-vh-100" style="padding-top: 56px; background: var(--deep-space-blue);">
    <div class="container py-4" style="max-width: 720px;">
      <h1 class="text-light fw-bold mb-4" style="letter-spacing: 3px;">ADD TREK</h1>

      <div class="card border-0 shadow-sm">
        <div class="card-body p-4">
          <div v-if="error" class="alert alert-danger py-2 small">{{ error }}</div>
          <div v-if="success" class="alert alert-success py-2 small">{{ success }}</div>

          <form @submit.prevent="handleSubmit">
            <div class="row">
              <div class="col-md-6 mb-3">
                <label class="form-label">Name</label>
                <input v-model="name" type="text" class="form-control" required placeholder="e.g. Everest Base Camp">
              </div>
              <div class="col-md-6 mb-3">
                <label class="form-label">Location</label>
                <input v-model="location" type="text" class="form-control" required placeholder="e.g. Solukhumbu">
              </div>
              <div class="col-md-6 mb-3">
                <label class="form-label">Difficulty</label>
                <select v-model="difficulty" class="form-select">
                  <option value="easy">Easy</option>
                  <option value="moderate">Moderate</option>
                  <option value="hard">Hard</option>
                </select>
              </div>
              <div class="col-md-6 mb-3">
                <label class="form-label">Status</label>
                <select v-model="status" class="form-select">
                  <option value="pending">Pending</option>
                  <option value="approved">Approved</option>
                  <option value="open">Open</option>
                  <option value="closed">Closed</option>
                  <option value="completed">Completed</option>
                </select>
              </div>
              <div class="col-md-6 mb-3">
                <label class="form-label">Duration (days)</label>
                <input v-model="durationDays" type="number" min="1" class="form-control" required>
              </div>
              <div class="col-md-6 mb-3">
                <label class="form-label">Available Slots</label>
                <input v-model="availableSlots" type="number" min="0" class="form-control" required>
              </div>
              <div class="col-md-6 mb-3">
                <label class="form-label">Start Date</label>
                <input v-model="startDate" type="date" class="form-control">
              </div>
              <div class="col-md-6 mb-3">
                <label class="form-label">End Date</label>
                <input v-model="endDate" type="date" class="form-control">
              </div>
              <div class="col-md-6 mb-4">
                <label class="form-label">Assigned Staff</label>
                <select v-model="assignedStaffId" class="form-select">
                  <option value="">None</option>
                  <option v-for="s in staffOptions" :key="s.id" :value="s.id">{{ s.name }}</option>
                </select>
              </div>
            </div>

            <button type="submit" class="btn btn-primary w-100 py-2" :disabled="loading">
              {{ loading ? 'Adding...' : 'Add Trek' }}
            </button>
          </form>
        </div>
      </div>

      <div class="text-center mt-3">
        <button @click="router.push('/admin/treks')" class="btn btn-link text-light">View trek list</button>
      </div>
    </div>
  </section>
</template>
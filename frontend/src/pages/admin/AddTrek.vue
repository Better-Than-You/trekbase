<script setup>
// vue basics: reactive state, lifecycle hook and watchers
import { ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { addTrek, getAdminStaff } from '@/lib/api'

// toast notifications
import { toast } from 'vue3-toastify';
import 'vue3-toastify/dist/index.css';

const router = useRouter()

// form fields
const name = ref('')
const location = ref('')
const difficulty = ref('moderate')
const durationDays = ref('')
const availableSlots = ref('')
const status = ref('pending')
const startDate = ref('')
const endDate = ref('')
const assignedStaffId = ref('')
// staff dropdown options
const staffOptions = ref([])

// load the list of staff for the "assigned staff" dropdown
onMounted(async () => {
  try {
    const data = await getAdminStaff()
    staffOptions.value = data.staff
  } catch {
    staffOptions.value = []
  }
})

// auto-fill end date = start date + duration (days) whenever either changes
function autoFillEndDate() {
  if (startDate.value && durationDays.value) {
    const end = new Date(startDate.value)
    end.setDate(end.getDate() + Number(durationDays.value))
    endDate.value = end.toISOString().slice(0, 10)
  }
}
// watch hook from react
watch([startDate, durationDays], autoFillEndDate)

// send the new trek to the backend
async function handleSubmit() {
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
    toast.success('Trek added successfully', {
      position: toast.POSITION.BOTTOM_CENTER,
      autoClose: 3000,
    })
    router.push('/admin/dashboard')
  } catch (e) {
    toast.error(e, {
      position: toast.POSITION.BOTTOM_CENTER,
      autoClose: 3000,
    })
  }
}
</script>

<template>
  <div class="container pt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <div>
        <h4 class="fw-bold text-uppercase mb-0" style="letter-spacing: 0.04em;">Add Trek</h4>
        <p class="text-secondary small mb-0">Create a new trek route</p>
      </div>
      <button @click="router.push('/admin/treks')" class="btn btn-outline-secondary">
        <i class="bi bi-arrow-left me-1"></i>Back
      </button>
    </div>
    </div>
    
    <div class="container pb-4 d-flex justify-content-center pt-2">
    <div class="card shadow-sm d-flex justify-content-center w-50" >
      <div class="card-body p-4">
        <form @submit.prevent="handleSubmit">
          <div class="row">
            <div class="col-md-6 mb-3">
              <label class="form-label small fw-semibold">Name</label>
              <input v-model="name" type="text" class="form-control" required placeholder="e.g. Everest Base Camp">
            </div>
            <div class="col-md-6 mb-3">
              <label class="form-label small fw-semibold">Location</label>
              <input v-model="location" type="text" class="form-control" required placeholder="e.g. Solukhumbu">
            </div>
            <div class="col-md-6 mb-3">
              <label class="form-label small fw-semibold">Difficulty</label>
              <select v-model="difficulty" class="form-select">
                <option value="easy">Easy</option>
                <option value="moderate">Moderate</option>
                <option value="hard">Hard</option>
              </select>
            </div>
            <div class="col-md-6 mb-3">
              <label class="form-label small fw-semibold">Status</label>
              <select v-model="status" class="form-select">
                <option value="open">Open</option>
                <option value="closed">Closed</option>
                <option value="completed">Completed</option>
              </select>
            </div>
            <div class="col-md-6 mb-3">
              <label class="form-label small fw-semibold">Duration (days)</label>
              <input v-model="durationDays" type="number" min="1" class="form-control" required>
            </div>
            <div class="col-md-6 mb-3">
              <label class="form-label small fw-semibold">Available Slots</label>
              <input v-model="availableSlots" type="number" min="0" class="form-control" required>
            </div>
            <div class="col-md-6 mb-3">
              <label class="form-label small fw-semibold">Start Date</label>
              <input v-model="startDate" type="date" class="form-control">
            </div>
            <div class="col-md-6 mb-3">
              <label class="form-label small fw-semibold">End Date</label>
              <input v-model="endDate" type="date" class="form-control">
            </div>
            <div class="col-md-6 mb-4">
              <label class="form-label small fw-semibold">Assigned Staff</label>
              <select v-model="assignedStaffId" class="form-select">
                <option value="">Not assigned</option>
                <option v-for="s in staffOptions" :key="s.id" :value="s.id">{{ s.name }}</option>
              </select>
            </div>
          </div>

          <div class="d-flex gap-2">
            <button type="submit" class="btn btn-primary">
              <i class="bi bi-plus-lg me-1"></i>Add Trek
            </button>
            <button type="button" class="btn btn-outline-secondary" @click="router.push('/admin/treks')">Cancel</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>
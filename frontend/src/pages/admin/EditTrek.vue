<script setup>
// vue basics: reactive state, lifecycle hook and watchers
import { ref, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getTrekDetail, updateTrek, getAdminStaff } from '@/lib/api'

// toast notifications
import { toast } from 'vue3-toastify';
import 'vue3-toastify/dist/index.css';

const route = useRoute()
const router = useRouter()

// id of the trek being edited, from the url (/admin/treks/:id/edit)
const trekId = route.params.id

// form fields, prefilled when the page loads
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

// load the current trek data and fill the form
onMounted(async () => {
  try {
    // load the list of staff for the "assigned staff" dropdown
    const staffData = await getAdminStaff()
    staffOptions.value = staffData.staff

    // load the trek's current values
    const data = await getTrekDetail(trekId)
    const t = data.trek
    name.value = t.name
    location.value = t.location
    difficulty.value = t.difficulty
    durationDays.value = t.duration_days
    availableSlots.value = t.available_slots
    status.value = t.status
    startDate.value = t.start_date || ''
    endDate.value = t.end_date || ''
    assignedStaffId.value = t.assigned_staff_id || ''
  } catch (e) {
    toast.error(e, {
      position: toast.POSITION.BOTTOM_CENTER,
      autoClose: 3000,
    })
    router.push('/admin/treks')
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
watch([startDate, durationDays], autoFillEndDate)

// send the edited values back to the backend
async function handleSubmit() {
  try {
    await updateTrek(trekId, {
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
    toast.success('Trek updated successfully', {
      position: toast.POSITION.BOTTOM_CENTER,
      autoClose: 3000,
    })
    router.push(`/admin/treks/${trekId}`)
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
        <h4 class="fw-bold text-uppercase mb-0" style="letter-spacing: 0.04em;">Edit Trek</h4>
        <p class="text-secondary small mb-0">Update trek route details</p>
      </div>
      <button @click="router.push('/admin/treks')" class="btn btn-outline-secondary">
        <i class="bi bi-arrow-left me-1"></i>Back
      </button>
    </div>

    <div class="container pb-4 d-flex justify-content-center pt-2">
      <div class="card shadow-sm d-flex justify-content-center w-50">
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
                  <option value="pending">Pending</option>
                  <option value="approved">Approved</option>
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
                <i class="bi bi-check-lg me-1"></i>Save Changes
              </button>
              <button type="button" class="btn btn-outline-secondary" @click="router.push('/admin/treks')">Cancel</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
// vue basics: reactive state and lifecycle hook
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getStaffDetail, updateStaff } from '@/lib/api'

// toast notifications
import { toast } from 'vue3-toastify';
import 'vue3-toastify/dist/index.css';

const route = useRoute()
const router = useRouter()

// id of the staff being edited, from the url (/admin/staff/:id/edit)
const staffId = route.params.id

// form fields, prefilled when the page loads
const name = ref('')
const contact = ref('')
const email = ref('')
const password = ref('')
const status = ref('available')

// load the current staff data and fill the form
onMounted(async () => {
  try {
    const data = await getStaffDetail(staffId)
    name.value = data.staff.name
    contact.value = data.staff.contact || ''
    email.value = data.staff.email || ''
    status.value = data.staff.status || 'available'
  } catch (e) {
    toast.error(e, {
      position: toast.POSITION.BOTTOM_CENTER,
      autoClose: 3000,
    })
    router.push('/admin/staff')
  }
})

// send the edited values back to the backend
async function handleSubmit() {
  try {
    // only send the password if a new one was typed in
    const payload = { name: name.value, contact: contact.value, email: email.value, status: status.value }
    if (password.value) payload.password = password.value

    await updateStaff(staffId, payload)
    toast.success('Staff updated successfully', {
      position: toast.POSITION.BOTTOM_CENTER,
      autoClose: 3000,
    })
    router.push(`/admin/staff/${staffId}`)
  } catch (e) {
    toast.error(e, {
      position: toast.POSITION.BOTTOM_CENTER,
      autoClose: 3000,
    })
  }
}
</script>

<template>
  <div class="container py-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <div>
        <h4 class="fw-bold text-uppercase mb-0" style="letter-spacing: 0.04em;">Edit Staff</h4>
        <p class="text-secondary small mb-0">Update trekking staff account</p>
      </div>
      <button @click="router.push('/admin/staff')" class="btn btn-outline-secondary">
        <i class="bi bi-arrow-left me-1"></i>Back
      </button>
    </div>

    <div class="container py-4 d-flex justify-content-center">
      <div class="card shadow-sm w-50">
        <div class="card-body p-4">
          <form @submit.prevent="handleSubmit">
            <div class="mb-3">
              <label class="form-label small fw-semibold">Name</label>
              <input v-model="name" type="text" class="form-control" required placeholder="Full name">
            </div>

            <div class="mb-3">
              <label class="form-label small fw-semibold">Contact</label>
              <input v-model="contact" type="text" class="form-control" placeholder="Phone or email">
            </div>

            <div class="mb-3">
              <label class="form-label small fw-semibold">Email</label>
              <input v-model="email" type="email" class="form-control" placeholder="Used to log in">
            </div>

            <div class="mb-3">
              <label class="form-label small fw-semibold">Status</label>
              <select v-model="status" class="form-select">
                <option value="available">Available</option>
                <option value="assigned">Assigned</option>
                <option value="not_available">Not Working</option>
              </select>
            </div>

            <div class="mb-4">
              <label class="form-label small fw-semibold">New Password</label>
              <input v-model="password" type="password" class="form-control" minlength="6" placeholder="Leave blank to keep current password">
            </div>

            <div class="d-flex gap-2">
              <button type="submit" class="btn btn-primary">
                <i class="bi bi-check-lg me-1"></i>Save Changes
              </button>
              <button type="button" class="btn btn-outline-secondary" @click="router.push('/admin/staff')">Cancel</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
// vue basics: reactive state and lifecycle hook
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getUserDetail, updateUser } from '@/lib/api'

// toast notifications
import { toast } from 'vue3-toastify';
import 'vue3-toastify/dist/index.css';

const route = useRoute()
const router = useRouter()

// id of the user being edited, from the url (/admin/users/:id/edit)
const userId = route.params.id

// form fields, prefilled when the page loads
const name = ref('')
const email = ref('')
const password = ref('')
const address = ref('')
const pin = ref('')
const phone = ref('')

// load the current user data and fill the form
onMounted(async () => {
  try {
    const data = await getUserDetail(userId)
    const u = data.user
    name.value = u.name
    email.value = u.email
    address.value = u.address || ''
    pin.value = u.pin || ''
    phone.value = u.phone || ''
  } catch (e) {
    toast.error(e, {
      position: toast.POSITION.BOTTOM_CENTER,
      autoClose: 3000,
    })
    router.push('/admin/users')
  }
})

// send the edited values back to the backend
async function handleSubmit() {
  try {
    // only send the password if a new one was typed in
    const payload = {
      name: name.value,
      email: email.value,
      address: address.value,
      pin: pin.value,
      phone: phone.value,
    }
    if (password.value) payload.password = password.value

    await updateUser(userId, payload)
    toast.success('User updated successfully', {
      position: toast.POSITION.BOTTOM_CENTER,
      autoClose: 3000,
    })
    router.push(`/admin/users/${userId}`)
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
        <h4 class="fw-bold text-uppercase mb-0" style="letter-spacing: 0.04em;">Edit User</h4>
        <p class="text-secondary small mb-0">Update trekker account details</p>
      </div>
      <button @click="router.push('/admin/users')" class="btn btn-outline-secondary">
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
              <label class="form-label small fw-semibold">Email</label>
              <input v-model="email" type="email" class="form-control" required placeholder="you@example.com">
            </div>

            <div class="mb-3">
              <label class="form-label small fw-semibold">New Password</label>
              <input v-model="password" type="password" class="form-control" minlength="6" placeholder="Leave blank to keep current password">
            </div>

            <div class="row">
              <div class="col-md-6 mb-3">
                <label class="form-label small fw-semibold">Phone</label>
                <input v-model="phone" type="text" class="form-control" placeholder="Optional, unique">
              </div>
              <div class="col-md-6 mb-3">
                <label class="form-label small fw-semibold">PIN / Pincode</label>
                <input v-model="pin" type="text" class="form-control" placeholder="Optional">
              </div>
              <div class="col-12 mb-4">
                <label class="form-label small fw-semibold">Address</label>
                <input v-model="address" type="text" class="form-control" placeholder="Optional">
              </div>
            </div>

            <div class="d-flex gap-2">
              <button type="submit" class="btn btn-primary">
                <i class="bi bi-check-lg me-1"></i>Save Changes
              </button>
              <button type="button" class="btn btn-outline-secondary" @click="router.push('/admin/users')">Cancel</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

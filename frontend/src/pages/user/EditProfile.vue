<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { updateProfile } from '@/lib/api'
import { state, setAuth } from '@/store/auth'

import { toast } from 'vue3-toastify';
import 'vue3-toastify/dist/index.css';

const router = useRouter()

const name = ref(state.user?.name || '')
const address = ref(state.user?.address || '')
const pin = ref(state.user?.pin || '')
const phone = ref(state.user?.phone || '')

async function handleSubmit() {
  try {
    const data = await updateProfile({
      name: name.value,
      address: address.value,
      pin: pin.value,
      phone: phone.value,
    })
    setAuth({ ...state.user, ...data.user }, state.token)
    toast.success('Profile updated successfully', {
      position: toast.POSITION.BOTTOM_CENTER,
      autoClose: 3000,
    })
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
    <h4 class="fw-bold text-uppercase mb-4" style="letter-spacing: 0.04em;">My Profile</h4>

    <!-- left hand side -->
    <div class="row g-4">
      <div class="col-lg-4">
        <div class="card shadow-sm text-center">
          <div class="card-body py-4">
            <span class="bg-primary-subtle text-primary d-inline-flex align-items-center justify-content-center rounded-circle p-3 mb-3 fs-4 fw-bold"><i class="bi bi-person p-2"></i></span>
            <h6 class="fw-bold mb-1">{{ name || state.user?.name }}</h6>
            <p class="text-secondary small mb-2">{{ state.user?.email }}</p>
            <p class="text-secondary small mb-0">
              <i class="bi bi-telephone me-1"></i>{{ phone || 'No phone' }}
              <br><i class="bi bi-geo-alt me-1"></i>{{ address || 'No address' }}
            </p>
          </div>
        </div>
      </div>

      <!-- right hand side -->
      <div class="col-lg-6">
        <div class="card shadow-sm">
          <div class="card-header bg-white py-3 fw-bold">Account details</div>
          <div class="card-body">
            <div class="mb-3">
              <label class="form-label small fw-semibold">Email address</label>
              <input :value="state.user?.email" type="email" class="form-control" disabled>
              <div class="form-text">Your email cannot be changed.</div>
            </div>
            <div class="mb-3">
              <label class="form-label small fw-semibold">Full name</label>
              <input v-model="name" type="text" class="form-control" required>
            </div>
            <div class="mb-3">
              <label class="form-label small fw-semibold">Phone</label>
              <input v-model="phone" type="text" class="form-control" placeholder="Optional, unique">
            </div>
            <div class="mb-3">
              <label class="form-label small fw-semibold">PIN / Pincode</label>
              <input v-model="pin" type="text" class="form-control" placeholder="Optional">
            </div>
            <div class="mb-4">
              <label class="form-label small fw-semibold">Address</label>
              <input v-model="address" type="text" class="form-control" placeholder="Optional">
            </div>

            <div class="d-flex gap-2">
              <button class="btn btn-primary" @click="handleSubmit">
                <i class="bi bi-check2-circle me-1"></i>Save changes
              </button>
              <button class="btn btn-outline-secondary" @click="router.push('/user/dashboard')">Cancel</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
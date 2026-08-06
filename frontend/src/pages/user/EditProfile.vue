<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { updateProfile } from '@/lib/api'
import { state, setAuth } from '@/store/auth'

import { toast } from 'vue3-toastify';
import 'vue3-toastify/dist/index.css';


const router = useRouter()

const name = ref(state.user?.name || '')

async function handleSubmit() {
  try {
    const data = await updateProfile(name.value) // more fields if needed
    setAuth({ ...state.user, ...data.user }, state.token)

    // show a success toast notification
    toast.success('Profile updated successfully', {
      position: toast.POSITION.BOTTOM_CENTER,
      autoClose: 3000,
    });
  } catch (e) {
    // handle errors like, showing a toast notification for invalid credentials, etc.
    // console.log(e);
    toast.error(e, {
      position: toast.POSITION.BOTTOM_CENTER,
      autoClose: 3000,
    });
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

            <!-- more details in future -->
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
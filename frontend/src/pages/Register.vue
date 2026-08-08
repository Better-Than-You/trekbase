<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { register } from '@/lib/api'
import { setAuth } from '@/store/auth'

import { toast } from 'vue3-toastify';
import 'vue3-toastify/dist/index.css';


const router = useRouter()

const name = ref('')
const email = ref('')
const password = ref('')

async function handleSubmit() {
  try {    const data = await register(name.value, email.value, password.value)
    setAuth(data.user, data.access_token, data.refresh_token)
    router.push('/user/dashboard')
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
  <div class="container py-5">
    <div class="row justify-content-center">
      <div class="col-md-7 col-lg-5">

        <div class="text-center mb-4">
          <span class="text-white d-inline-flex align-items-center justify-content-center rounded-3 p-2 mb-2">
            <!-- <i class="bi bi-mountain"></i> -->
            <img src="/trekbase_logo.png" alt="TrekBase" class="d-block" style="width: 50px; height: 50px;" />

          </span>
          <h5 class="fw-semibold mb-1">Create your trekker account</h5>
          <p class="text-secondary small mb-0">Register to browse and book treks</p>
        </div>

        <div class="card shadow-sm">
          <div class="card-body p-4">
            <div class="mb-3">
              <label class="form-label small fw-semibold">Full name</label>
              <input v-model="name" type="text" class="form-control" required placeholder="Your full name">
            </div>

            <div class="mb-3">
              <label class="form-label small fw-semibold">Email address</label>
              <input v-model="email" type="email" class="form-control" required placeholder="you@example.com">
            </div>

            <div class="row g-3 mb-4">
              <div class="col-sm-12">
                <label class="form-label small fw-semibold">Password</label>
                <input v-model="password" type="password" class="form-control" required minlength="6">
              </div>
            </div>

            <button class="btn btn-primary w-100 py-2" @click="handleSubmit">Register</button>

            <p class="text-center mt-3 mb-0 small">
              Already have an account?
              <router-link to="/auth/login" class="fw-semibold text-decoration-none">Sign in</router-link>
            </p>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>
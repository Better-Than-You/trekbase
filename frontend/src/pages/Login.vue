<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { login } from '@/lib/api'
import { setAuth } from '@/store/auth'

const router = useRouter()

const email = ref('')
const password = ref('')

async function handleSubmit() {
  try {
    const data = await login(email.value, password.value)
    setAuth(data.user, data.access_token)
    if (data.user.role === 'admin') router.push('/admin/dashboard')
    else if (data.user.role === 'staff') router.push('/staff/dashboard')
    else router.push('/user/dashboard')
  } catch {
  }
}
</script>

<template>
  <div class="container py-5">
    <div class="row justify-content-center">
      <div class="col-md-7 col-lg-5">

        <div class="text-center mb-4">
          <span class="bg-primary text-white d-inline-flex align-items-center justify-content-center rounded-3 p-2 mb-2">
            <i class="bi bi-mountain"></i>
          </span>
          <h4 class="fw-bold mb-1">TrekBase</h4>
          <p class="text-secondary small mb-0">Sign in to continue</p>
        </div>

        <div class="card shadow-sm">
          <div class="card-body p-4">
            <div class="mb-3">
              <label class="form-label small fw-semibold">Email address</label>
              <input v-model="email" type="email" class="form-control" required placeholder="you@example.com"
                     @keyup.enter="handleSubmit">
            </div>

            <div class="mb-4">
              <label class="form-label small fw-semibold">Password</label>
              <input v-model="password" type="password" class="form-control" required placeholder="Your password"
                     @keyup.enter="handleSubmit">
            </div>

            <button class="btn btn-primary w-100 py-2" @click="handleSubmit">Login</button>

            <p class="text-center mt-3 mb-0 small">
              No account?
              <router-link to="/auth/register" class="fw-semibold text-decoration-none">Register as User (Trekker)</router-link>
            </p>

          </div>
        </div>

      </div>
    </div>
  </div>
</template>
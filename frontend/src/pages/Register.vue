<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { register } from '@/lib/api'
import { setAuth } from '@/store/auth'

const router = useRouter()

const name = ref('')
const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const error = ref('')
const loading = ref(false)

async function handleSubmit() {
  error.value = ''

  if (password.value !== confirmPassword.value) {
    error.value = 'Passwords do not match'
    return
  }

  loading.value = true
  try {
    const data = await register(name.value, email.value, password.value)
    setAuth(data.user, data.access_token)
    router.push('/')
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <section class="auth-page">
    <div class="auth-card">
      <div class="text-center mb-4">
        <h1 class="auth-brand">TREKBASE</h1>
        <p class="auth-subtitle">Create your account</p>
      </div>

      <form @submit.prevent="handleSubmit">
        <div v-if="error" class="alert alert-danger py-2 small">{{ error }}</div>

        <div class="mb-3">
          <label class="form-label small text-uppercase" style="letter-spacing: 1px;">Name</label>
          <input v-model="name" type="text" class="form-control" required placeholder="Your full name">
        </div>

        <div class="mb-3">
          <label class="form-label small text-uppercase" style="letter-spacing: 1px;">Email</label>
          <input v-model="email" type="email" class="form-control" required placeholder="you@example.com">
        </div>

        <div class="mb-3">
          <label class="form-label small text-uppercase" style="letter-spacing: 1px;">Password</label>
          <input v-model="password" type="password" class="form-control" required minlength="6">
        </div>

        <div class="mb-4">
          <label class="form-label small text-uppercase" style="letter-spacing: 1px;">Confirm Password</label>
          <input v-model="confirmPassword" type="password" class="form-control" required minlength="6">
        </div>

        <button type="submit" class="btn btn-primary w-100 py-2" :disabled="loading" style="letter-spacing: 1px;">
          {{ loading ? 'Creating account...' : 'Create Account' }}
        </button>
      </form>

      <p class="text-center mt-4 mb-0 small text-muted">
        Already have an account?
        <router-link to="/auth/login" class="auth-link">Sign in</router-link>
      </p>
    </div>
  </section>
</template>

<style scoped>
.auth-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--deep-space-blue);
  position: relative;
}

.auth-card {
  position: relative;
  width: 100%;
  max-width: 400px;
  padding: 2.5rem;
  background: var(--parchment);
}

.auth-brand {
  font-size: 1.75rem;
  font-weight: 800;
  letter-spacing: 4px;
  color: var(--deep-space-blue);
  margin-bottom: 0.25rem;
}

.auth-subtitle {
  color: var(--rich-cerulean);
  font-size: 0.875rem;
  letter-spacing: 1px;
}

.auth-link {
  color: var(--yale-blue);
  font-weight: 600;
  text-decoration: none;
}

.auth-link:hover {
  text-decoration: underline;
}
</style>

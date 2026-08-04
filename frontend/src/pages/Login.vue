<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { login } from '@/lib/api'
import { setAuth } from '@/store/auth'

const router = useRouter()

const email = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

async function handleSubmit() {
  error.value = ''
  loading.value = true
  try {
    const data = await login(email.value, password.value)
    setAuth(data.user, data.access_token)
    
    // redirect to dashboard
    // router.push('/')

    // if admin
    if (data.user.role === 'admin') {
      router.push('/admin/dashboard')
    } else if (data.user.role === 'staff') {
      router.push('/staff/dashboard')
    } else if (data.user.role === 'user') {
      router.push('/dashboard') // plain dashboard for normal users
    }
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
        <p class="auth-subtitle">Sign in to continue</p>
      </div>

      <form @submit.prevent="handleSubmit">
        <div v-if="error" class="alert alert-danger py-2 small">{{ error }}</div>

        <div class="mb-3">
          <label class="form-label small text-uppercase" style="letter-spacing: 1px;">Email</label>
          <input v-model="email" type="email" class="form-control" required placeholder="you@example.com">
        </div>

        <div class="mb-4">
          <label class="form-label small text-uppercase" style="letter-spacing: 1px;">Password</label>
          <input v-model="password" type="password" class="form-control" required>
        </div>

        <button type="submit" class="btn btn-primary w-100 py-2" :disabled="loading" style="letter-spacing: 1px;">
          {{ loading ? 'Signing in...' : 'Sign In' }}
        </button>
      </form>

      <p class="text-center mt-4 mb-0 small text-muted">
        No account?
        <router-link to="/auth/register" class="auth-link">Register here</router-link>
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

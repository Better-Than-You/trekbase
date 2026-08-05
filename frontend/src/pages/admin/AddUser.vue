<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { addUser } from '@/lib/api'

const router = useRouter()

const name = ref('')
const email = ref('')
const password = ref('')
const error = ref('')
const success = ref('')
const loading = ref(false)

async function handleSubmit() {
  error.value = ''
  success.value = ''
  loading.value = true
  try {
    await addUser(name.value, email.value, password.value)
    success.value = 'User added successfully'
    name.value = ''
    email.value = ''
    password.value = ''
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <section class="min-vh-100" style="padding-top: 56px; background: var(--deep-space-blue);">
    <div class="container py-4" style="max-width: 720px;">
      <h1 class="text-light fw-bold mb-4" style="letter-spacing: 3px;">ADD USER</h1>

      <div class="card border-0 shadow-sm">
        <div class="card-body p-4">
          <div v-if="error" class="alert alert-danger py-2 small">{{ error }}</div>
          <div v-if="success" class="alert alert-success py-2 small">{{ success }}</div>

          <form @submit.prevent="handleSubmit">
            <div class="mb-3">
              <label class="form-label">Name</label>
              <input v-model="name" type="text" class="form-control" required placeholder="Full name">
            </div>

            <div class="mb-3">
              <label class="form-label">Email</label>
              <input v-model="email" type="email" class="form-control" required placeholder="you@example.com">
            </div>

            <div class="mb-4">
              <label class="form-label">Password</label>
              <input v-model="password" type="password" class="form-control" required minlength="6">
            </div>

            <button type="submit" class="btn btn-primary w-100 py-2" :disabled="loading">
              {{ loading ? 'Adding...' : 'Add User' }}
            </button>
          </form>
        </div>
      </div>

      <div class="text-center mt-3">
        <button @click="router.push('/admin/users')" class="btn btn-link text-light">View user list</button>
      </div>
    </div>
  </section>
</template>
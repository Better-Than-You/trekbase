<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { addStaff } from '@/lib/api'

const router = useRouter()

const name = ref('')
const contact = ref('')
const password = ref('')
const error = ref('')
const success = ref('')
const loading = ref(false)

async function handleSubmit() {
  error.value = ''
  success.value = ''
  loading.value = true
  try {
    await addStaff(name.value, contact.value, password.value)
    success.value = 'Staff added successfully'
    name.value = ''
    contact.value = ''
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
      <h1 class="text-light fw-bold mb-4" style="letter-spacing: 3px;">ADD STAFF</h1>

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
              <label class="form-label">Contact</label>
              <input v-model="contact" type="text" class="form-control" placeholder="Phone or email">
            </div>

            <div class="mb-4">
              <label class="form-label">Password</label>
              <input v-model="password" type="password" class="form-control" placeholder="Login password">
            </div>

            <button type="submit" class="btn btn-primary w-100 py-2" :disabled="loading">
              {{ loading ? 'Adding...' : 'Add Staff' }}
            </button>
          </form>
        </div>
      </div>

      <div class="text-center mt-3">
        <button @click="router.push('/admin/staff')" class="btn btn-link text-light">View staff list</button>
      </div>
    </div>
  </section>
</template>
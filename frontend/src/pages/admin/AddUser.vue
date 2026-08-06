<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { addUser } from '@/lib/api'

import { toast } from 'vue3-toastify';
import 'vue3-toastify/dist/index.css';

const router = useRouter()

const name = ref('')
const email = ref('')
const password = ref('')

async function handleSubmit() {
  try {
    await addUser(name.value, email.value, password.value)
    name.value = ''
    email.value = ''
    password.value = ''
  toast.success('Staff account created successfully', {
      position: toast.POSITION.BOTTOM_CENTER,
      autoClose: 3000,
    });
    router.push('/admin/dashboard');
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
    <div class="d-flex justify-content-between align-items-center mb-4">
      <div>
        <h4 class="fw-bold text-uppercase mb-0" style="letter-spacing: 0.04em;">Add User</h4>
        <p class="text-secondary small mb-0">Create a new trekker account</p>
      </div>
      <button @click="router.push('/admin/users')" class="btn btn-outline-secondary">
        <i class="bi bi-arrow-left me-1"></i>Back
      </button>
    </div>
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

          <div class="mb-4">
            <label class="form-label small fw-semibold">Password</label>
            <input v-model="password" type="password" class="form-control" required minlength="6">
          </div>

          <div class="d-flex gap-2">
            <button type="submit" class="btn btn-primary">
              <i class="bi bi-person-plus me-1"></i>Add User
            </button>
            <button type="button" class="btn btn-outline-secondary" @click="router.push('/admin/users')">Cancel</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>
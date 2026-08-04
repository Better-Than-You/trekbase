import { createRouter, createWebHistory } from 'vue-router'
import { Home, Login, Register } from '@/pages/auth'
import NotFound from '@/pages/NotFound.vue'
import { AdminDashboard } from '@/pages/admin'

const routes = [
  { path: '/', component: Home, name: 'home' },
  { path: '/auth/login', component: Login, name: 'login' },
  { path: '/auth/register', component: Register, name: 'register' },

  // admin routes
  { path: '/admin/dashboard', component: AdminDashboard, name: 'admin_dashboard' },

  { path: '/:pathMatch(.*)*', component: NotFound, name: 'not_found' },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router

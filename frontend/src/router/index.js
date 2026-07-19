import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/pages/Home.vue'
import Login from '@/pages/Login.vue'
import Register from '@/pages/Register.vue'
import NotFound from '@/pages/NotFound.vue'

const routes = [
  { path: '/', component: Home, name: 'home' },
  { path: '/auth/login', component: Login, name: 'login' },
  { path: '/auth/register', component: Register, name: 'register' },
  { path: '/:pathMatch(.*)*', component: NotFound, name: 'not_found' },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router

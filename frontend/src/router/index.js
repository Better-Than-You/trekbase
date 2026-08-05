import { createRouter, createWebHistory } from 'vue-router'
import { Home, Login, Register } from '@/pages/auth'
import NotFound from '@/pages/NotFound.vue'
import { AdminDashboard, AddUser, AddStaff, AddTrek, Userlist, Stafflist, Treklist, UserDetails, StaffDetails, TrekDetails } from '@/pages/admin'

const routes = [
  { path: '/', component: Home, name: 'home' },
  { path: '/auth/login', component: Login, name: 'login' },
  { path: '/auth/register', component: Register, name: 'register' },

  // admin routes
  { path: '/admin/dashboard', component: AdminDashboard, name: 'admin_dashboard' },
  { path: '/admin/users', component: Userlist, name: 'userlist' },
  { path: '/admin/users/:id', component: UserDetails, name: 'admin_user_details' },
  { path: '/admin/user/add', component: AddUser, name: 'admin_add_user' },
  { path: '/admin/staff', component: Stafflist, name: 'stafflist' },
  { path: '/admin/staff/:id', component: StaffDetails, name: 'admin_staff_details' },
  { path: '/admin/staff/add', component: AddStaff, name: 'admin_add_staff' },
  { path: '/admin/treks', component: Treklist, name: 'treklist' },
  { path: '/admin/treks/add', component: AddTrek, name: 'admin_add_trek' },
  { path: '/admin/treks/:id', component: TrekDetails, name: 'admin_trek_details' },

  { path: '/:pathMatch(.*)*', component: NotFound, name: 'not_found' },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router

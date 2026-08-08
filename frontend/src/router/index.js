import { createRouter, createWebHistory } from 'vue-router'
import { Home, Login, Register } from '@/pages/auth'
import NotFound from '@/pages/NotFound.vue'
import { AdminDashboard, AddUser, AddStaff, AddTrek, Userlist, Stafflist, Treklist, UserDetails, StaffDetails, TrekDetails, EditUser, EditStaff, EditTrek } from '@/pages/admin'
import { UserDashboard, BookingHistory, EditProfile } from '@/pages/user'
import { StaffDashboard, StaffTrekDetail } from '@/pages/staff'
import { state } from '@/store/auth'

const routes = [
  { path: '/', component: Home, name: 'home' },
  { path: '/auth/login', component: Login, name: 'login' },
  { path: '/auth/register', component: Register, name: 'register' },

  // user routes
  { path: '/user/dashboard', component: UserDashboard, name: 'user_dashboard', meta: { requiresRole: 'user' } },
  { path: '/user/history', component: BookingHistory, name: 'user_history', meta: { requiresRole: 'user' } },
  { path: '/user/profile', component: EditProfile, name: 'user_profile', meta: { requiresRole: 'user' } },

  // staff routes
  { path: '/staff/dashboard', component: StaffDashboard, name: 'staff_dashboard', meta: { requiresRole: 'staff' } },
  { path: '/staff/treks/:id', component: StaffTrekDetail, name: 'staff_trek_detail', meta: { requiresRole: 'staff' } },

  // admin routes
  { path: '/admin/dashboard', component: AdminDashboard, name: 'admin_dashboard', meta: { requiresRole: 'admin' } },
  { path: '/admin/users', component: Userlist, name: 'userlist', meta: { requiresRole: 'admin' } },
  { path: '/admin/users/:id', component: UserDetails, name: 'admin_user_details', meta: { requiresRole: 'admin' } },
  { path: '/admin/users/:id/edit', component: EditUser, name: 'admin_edit_user', meta: { requiresRole: 'admin' } },
  { path: '/admin/user/add', component: AddUser, name: 'admin_add_user', meta: { requiresRole: 'admin' } },
  { path: '/admin/staff', component: Stafflist, name: 'stafflist', meta: { requiresRole: 'admin' } },
  { path: '/admin/staff/:id', component: StaffDetails, name: 'admin_staff_details', meta: { requiresRole: 'admin' } },
  { path: '/admin/staff/:id/edit', component: EditStaff, name: 'admin_edit_staff', meta: { requiresRole: 'admin' } },
  { path: '/admin/staff/add', component: AddStaff, name: 'admin_add_staff', meta: { requiresRole: 'admin' } },
  { path: '/admin/treks', component: Treklist, name: 'treklist', meta: { requiresRole: 'admin' } },
  { path: '/admin/treks/add', component: AddTrek, name: 'admin_add_trek', meta: { requiresRole: 'admin' } },
  { path: '/admin/treks/:id', component: TrekDetails, name: 'admin_trek_details', meta: { requiresRole: 'admin' } },
  { path: '/admin/treks/:id/edit', component: EditTrek, name: 'admin_edit_trek', meta: { requiresRole: 'admin' } },

  { path: '/:pathMatch(.*)*', component: NotFound, name: 'not_found' },
]

const dashboards = {
  admin: '/admin/dashboard',
  staff: '/staff/dashboard',
  user: '/user/dashboard',
}

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to) => {
  const role = state.role
  const token = state.token
  const needsRole = to.meta.requiresRole

  // logged in
  if (token) {
    // trying to go in a protected route
    if (needsRole && role !== needsRole) {
      return { path: dashboards[role] || '/' } // go  to either dashboard or landing page
    }
    // redirect to dashboard if logged in
    if (!needsRole && (to.name === 'home' || to.name === 'login' || to.name === 'register')) {
      return { path: dashboards[role] || '/' }
    }
    return true
  }

  // not logged in
  if (needsRole) {
    return { path: '/auth/login' }
  }
  return true
})

export default router
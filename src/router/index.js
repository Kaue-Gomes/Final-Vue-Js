import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/store/auth'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home.vue')
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: { requiresGuest: true }
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('@/views/Dashboard.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/produtos',
    name: 'Produtos',
    component: () => import('@/views/Produtos.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/produtos/novo',
    name: 'ProdutoNovo',
    component: () => import('@/views/ProdutoNovo.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/produtos/:id',
    name: 'ProdutoDetalhes',
    component: () => import('@/views/ProdutoDetalhes.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/produtos/:id/editar',
    name: 'ProdutoEdit',
    component: () => import('@/views/ProdutoEdit.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/perfil',
    name: 'Perfil',
    component: () => import('@/views/Perfil.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/sobre',
    name: 'Sobre',
    component: () => import('@/views/Sobre.vue')
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/'
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  }
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  // Verificar autenticação
  authStore.verificarAutenticacao()
  
  const isAuthenticated = authStore.isAuthenticated
  
  if (to.meta.requiresAuth && !isAuthenticated) {
    next({ name: 'Login', query: { redirect: to.fullPath } })
  } else if (to.meta.requiresGuest && isAuthenticated) {
    next({ name: 'Produtos' })
  } else {
    next()
  }
})

export default router


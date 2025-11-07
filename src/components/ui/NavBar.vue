<template>
  <nav class="navbar">
    <div class="navbar-container">
      <div class="navbar-left">
        <button class="sidebar-toggle" @click="toggleSidebar" v-if="!hideMenu">
          <i class="bi bi-list"></i>
        </button>
        <router-link to="/" class="navbar-brand">
          <i class="bi bi-box-seam"></i>
          <span>Sistema de Produtos</span>
        </router-link>
      </div>
      
      <div class="navbar-right">
        <ThemeToggle />
        
        <div v-if="isAuthenticated" class="navbar-user">
          <div class="user-info">
            <span class="user-nome">{{ nomeUsuario }}</span>
            <span class="user-email">{{ emailUsuario }}</span>
          </div>
          <div class="user-avatar">
            {{ nomeUsuario.charAt(0).toUpperCase() }}
          </div>
          <div class="user-menu">
            <router-link to="/dashboard" class="menu-item">
              <i class="bi bi-speedometer2"></i> Dashboard
            </router-link>
            <router-link to="/perfil" class="menu-item">
              <i class="bi bi-person"></i> Perfil
            </router-link>
            <button class="menu-item" @click="logout">
              <i class="bi bi-box-arrow-right"></i> Sair
            </button>
          </div>
        </div>
        
        <router-link v-else to="/login" class="btn btn-primary">
          Entrar
        </router-link>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/store/auth'
import { useUIStore } from '@/store/ui'
import ThemeToggle from './ThemeToggle.vue'

defineProps({
  hideMenu: {
    type: Boolean,
    default: false
  }
})

const router = useRouter()
const authStore = useAuthStore()
const uiStore = useUIStore()

const isAuthenticated = computed(() => authStore.isAuthenticated)
const nomeUsuario = computed(() => authStore.nomeUsuario)
const emailUsuario = computed(() => authStore.emailUsuario)

const toggleSidebar = () => {
  uiStore.toggleSidebar()
}

const logout = () => {
  authStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.navbar {
  background: var(--bg-primary);
  border-bottom: 1px solid var(--border-color);
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: var(--shadow-sm);
}

.navbar-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 1.5rem;
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.navbar-left {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.sidebar-toggle {
  background: none;
  border: none;
  color: var(--text-primary);
  font-size: 1.5rem;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 6px;
  transition: background 0.2s ease;
  display: none;
}

.sidebar-toggle:hover {
  background: var(--bg-secondary);
}

@media (max-width: 768px) {
  .sidebar-toggle {
    display: block;
  }
}

.navbar-brand {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  text-decoration: none;
  color: var(--text-primary);
  font-size: 1.25rem;
  font-weight: 600;
}

.navbar-brand i {
  font-size: 1.5rem;
  color: var(--color-primary);
}

.navbar-right {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.navbar-user {
  position: relative;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.user-info {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  display: none;
}

@media (min-width: 768px) {
  .user-info {
    display: flex;
  }
}

.user-nome {
  font-weight: 500;
  color: var(--text-primary);
  font-size: 0.9rem;
}

.user-email {
  font-size: 0.75rem;
  color: var(--text-tertiary);
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: var(--color-primary);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s ease;
}

.user-avatar:hover {
  transform: scale(1.05);
}

.user-menu {
  position: absolute;
  top: calc(100% + 0.5rem);
  right: 0;
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  box-shadow: var(--shadow-lg);
  padding: 0.5rem;
  min-width: 180px;
  opacity: 0;
  visibility: hidden;
  transform: translateY(-10px);
  transition: all 0.2s ease;
}

.user-avatar:hover + .user-menu,
.user-menu:hover {
  opacity: 1;
  visibility: visible;
  transform: translateY(0);
}

.menu-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  width: 100%;
  padding: 0.75rem;
  background: none;
  border: none;
  color: var(--text-primary);
  text-decoration: none;
  cursor: pointer;
  border-radius: 6px;
  transition: background 0.2s ease;
  font-size: 0.9rem;
}

.menu-item:hover {
  background: var(--bg-secondary);
}
</style>

